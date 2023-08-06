import abc
from servicemapper.types import DataDialect, Operations

class ServiceConnector(abc.ABC):
    TRANSLATION_MAP = {
        DataDialect.DATA_STEWARD: DataDialect.CONNECTED_SERVICE,
        DataDialect.CONNECTED_SERVICE: DataDialect.DATA_STEWARD,
        DataDialect.NONE: DataDialect.NONE
    }

    @abc.abstractmethod
    def __init__(self, config): # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def about(self):            # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def connect(self):          # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def translate_data(self, input_data: dict, input_dialect: DataDialect) -> (dict, DataDialect): # pragma: no cover
        """Translate the data from the input dialect to the output dialect
        
        Arguments:
            input_data {dict} -- Data from the input source
            input_dialect {DataDialect} -- Dialect of the input data
        
        Returns:
            (output_data, output_dialect) -- Tuple consisting of the output data and its dialect
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def write_output_data(self, output_data: dict, operation: Operations) -> dict: # pragma: no cover
        """Write the output data to the correct destination, depending on the operation
        
        Arguments:
            output_data {dict} -- Data, in the correct format for the output destination
            operation {Operation} -- Operation to perform
        
        Returns:
            dict -- Dictionary indicating results of the operation
        """
        raise NotImplementedError()