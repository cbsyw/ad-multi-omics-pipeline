# src/data_ingestion/clinical_ingestor.py


import pandas as pd
import numpy as np
from datetime import datetime
from .base_ingestion import DataIngestionBase

# pandas for tabular, numpy for operations, datetime for timestamp
# base class!

# inherits from abstract base class

class ClinicalDataIngestor(DataIngestionBase):
    """
    Clinical data ingestion class for tabular clinical data.
    This class handles clinical data formats (csv,excel,tsv)
    """

    # call class constructor to handle file path validation
    # set file format (input or infer)
    # init self.data as None (lazy loading)
    # logs the format being used

    def __init__(self, data_path, file_format=None):
        super().__init__(data_path)
        self.file_format = file_format or self._infer_format(data_path)
        self.data = None
        self.logger.info(f"Initialized clinical data ingestor with format: {self.flie_format}")

    def _infer_format(self,data_path):

        
    
