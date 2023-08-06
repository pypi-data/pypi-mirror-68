import json
from servicemapper.ioc import Core, Mapper
from servicemapper.types import Constants, DataDialect, EventSources, Operations, _operation_dialect_factory, _queue_arn_to_url

class MapperWorker():

    def __init__(self):
        self.logger = Core.logger()
        self.service_connector = Mapper.service_connector()
        self.sqs_client = Mapper.sqs_client()

        self.EVENT_SOURCE_OPERATION = {
            EventSources.QUEUE: _operation_dialect_factory(Operations.PUSH_TO_SERVICE, DataDialect.DATA_STEWARD),
            EventSources.TIMER: _operation_dialect_factory(Operations.PULL_FROM_SERVICE, DataDialect.CONNECTED_SERVICE),
            EventSources.WEBHOOK: _operation_dialect_factory(Operations.RECEIVE_FROM_SERVICE, DataDialect.CONNECTED_SERVICE),
            EventSources.OTHER: _operation_dialect_factory(Operations.NOOP, DataDialect.NONE)
        }      

    def _cleanup_input_event(self, record) -> None:
        """Do any cleanup work needed for the input event (i.e. delete from queue)
        
        Arguments:
            record {[type]} -- [description]
        """
        self.logger.debug('BEGIN: _cleanup_input_event')
        source = self._get_event_source(record=record)
        self.logger.debug(f'Source: {source}')

        if source == EventSources.QUEUE:
            self.logger.info('Deleting message from queue')
            url = _queue_arn_to_url(queue_arn=record['eventSourceARN'])
            receipt_handle = record['receiptHandle']
            self.sqs_client.delete_message(QueueUrl=url, ReceiptHandle=receipt_handle)
            
    def _get_event_source(self, record) -> EventSources:
        """Get the event source based on the input record
        
        Arguments:
            record {Input record} -- An SQS, SNS, or CloudWatch record
        
        Returns:
            EventSources -- The event source
        """
        if ('eventSource' in record and record['eventSource'] == 'aws:sqs'):
            event_source = EventSources.QUEUE
        elif ('EventSource' in record and record['EventSource'] == 'aws:sns'):
            event_source = EventSources.WEBHOOK
        elif ('source' in record and record['source'] == 'aws.events'):
            event_source = EventSources.TIMER
        else:
            raise ValueError('Unsupported event source')

        return event_source

    def _get_input_data(self, record: dict) -> (dict, DataDialect):
        """Get the input data.  The input location is dependant on the operation
           we are performing.  It may come from the connected service, the webhook
           data, or the output data queue
        
        Arguments:
            record {Input record} -- An SQS, SNS, or CloudWatch record
        
        Returns:
            (input_data, data_dialect, operation) -- Tuple consisting of the data, the dialect, and the operation
        """
        self.logger.debug(f"BEGIN: _get_input_data({record})")
        
        # Get the event source for this record
        source = self._get_event_source(record)

        # Get the data based on the event source
        data = {}
        self.logger.error("_get_input_data: Not implemented")

        ret_val = (
            data,
            self.EVENT_SOURCE_OPERATION[source][Constants.KEY_DIALECT],
            self.EVENT_SOURCE_OPERATION[source][Constants.KEY_OPERATION]
        )
        self.logger.debug(f"END: _get_input_data returning {ret_val}")
        return ret_val

    def _get_input_records(self, input_event) -> []:
        """Convert the input_event to an iterable list
        
        Arguments:
            input_event {Lambda Input Event} -- The event data that triggered the function\
      
        Returns:
            [records] -- List of records to process
        """
        # We can be triggered by SNS and SQS, which have a 'Records' list, or by a periodic 
        # CloudWatch event, which does not have a 'Records' list
        records = input_event['Records'] if 'Records' in input_event else [ input_event ]
        return records

    @staticmethod
    def _run_output_builder(input_dialect: DataDialect, output_dialect: DataDialect, operation: Operations):
        return {
            Constants.KEY_INPUT: {
                Constants.KEY_DIALECT: input_dialect
            },
            Constants.KEY_OUTPUT: {
                Constants.KEY_DIALECT: output_dialect
            },
            Constants.KEY_OPERATION: operation
        }

    def run(self, input_event: dict, context: dict) -> dict:
        self.logger.info("BEGIN: MapperWorker.run")
        self.logger.debug(f"input_event: {json.dumps(input_event, indent=2)}")
        self.logger.debug(f"context: {json.dumps(context, indent=2)}")

        # Get the input data
        records = self._get_input_records(input_event=input_event)
        self.logger.debug(f"{len(records)} records in the input event")

        retval = {
            Constants.KEY_RECORDS: []
        }
        for r in records:
            self.logger.debug(f"Processing record: {r}")

            # Get the input data
            input_data, dialect, operation = self._get_input_data(record=r)

            # Translate the data to the correct dialect
            output_data, output_dialect = self.service_connector.translate_data(input_data=input_data, input_dialect=dialect)
            self.logger.info(f"Translated data from {dialect} to {output_dialect}")

            # Write the data to the destination
            self.service_connector.write_output_data(output_data=output_data, operation=operation)

            # Finish processing the input event
            self._cleanup_input_event(record=r)

            record_retval = self._run_output_builder(input_dialect=dialect, output_dialect=output_dialect, operation=operation)
            retval[Constants.KEY_RECORDS].append(record_retval)
    
        return retval
            