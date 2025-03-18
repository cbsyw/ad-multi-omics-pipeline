

from abc import ABC, abstractmethod
import os
import logging

# configure logging (time, log name, log level, message)

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# define class and inherit form ABC
# template for other ingestion classes to follow

class DataIngestionBase(ABC):
    """
    Abstract base class for all data ingestion classes.

    This class defines the interface that all data ingestion classes must implement,
    ensuring consistency across different data types.
    """

# constructor, accepts data_path, creates loggger, calls to validate path

    def __init__(self, data_path):
        """
        Initialize data ingestion class:

        Args:
            data_path(str): Path to the data file or directory
        """
        self.data_path = data_path
        self.logger = logging.getLogger(self.__class__.__name__)
        self.validate_path()


    # check if path exists, if not raise error

    def validate_path(self):
        """Validate that the data path exists"""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data Path does not exist: {self.data_path}")
        self.logger.info(f"Data path validated: {self.data_path}")

    # load data, subclass must implement this method, reads data from files to memory
    @abstractmethod
    def load_data(self):
        """
        Load data from the source.

        This method must be implemented by all subclasses.

        Returns:
            Data object (type depends on the specific data being loaded)
        """
        pass

    # extract and return info about data (size, dim, types)
    @abstractmethod
    def get_metadata(self):
        """
        Extract metadata from the data:

        This method must be implemeneted by all subclasses.

        Returns:
            dict: Metadata dictionary
        """
        pass










        
