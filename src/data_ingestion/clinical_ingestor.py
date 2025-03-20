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
        self.logger.info(f"Initialized clinical data ingestor with format: {self.file_format}")

    def _infer_format(self,data_path):
        extension = data_path.split('.')[-1].lower()
        format_map ={
                'csv': 'csv',
                'xlsx': 'excel',
                'xls': 'excel',
                'tsv': 'tsv',
                'txt': 'tsv'
                }
        
        file_format = format_map.get(extension)
        if not file_format:
            self.logger.warning(f"unknown file extension: {extension}. default to csv.")
            file_format = 'csv'

        return file_format
        

    def load_data(self):
        self.logger.info(f"Loading clinical data from {self.data_path}")

        try:
            if self.file_format == 'csv':
                self.data = pd.read_csv(self.data_path)
            elif self.file_format == 'excel':
                self.data = pd.read_excel(self.data_path)
            elif self.file_format == 'tsv':
                self.data = pd.read_csv(self.data_path)
            else:
                raise ValueError(f"unsupported file format: {self.file_format}")

            self.logger.info(f"succesfully loaded data with shape: self.data.shape")
            return self.data

        except Exception as e:
            self.logger.error(f"error loading clinical data: {str(e)}")
            raise

    def get_metadata(self):
        if self.data is None:
            self.load_data()


        metadata = {
                "data_type": "clinical",
                "file_format": self.file_format,
                "num_subjects": self.data.shape[0],
                "num_features": self.data.shape[1],
                "column_names": self.data.columns.tolist(),
                "data_types": {col: str(dtype) for col, dtype in self.data.dtypes.items()},
                "missing_values": {col:int(self.data[col].isna().sum()) for col in self.data.columns},
                "processing_date": datetime.now().strftime("%Y-%m_5d %H:%M:%S")
            }

        # check for id columns

        possible_id_cols = [col for col in self.data.columns if 'id' in col.lower() or 'subject' in col.lower()]
        if possible_id_cols:
            metadata["possible_id_columns"] = possible_id_cols

        return metadata

    # data transformation example (birthdate to age)

    def calculate_age(self, birth_date_col, reference_date=None):
        
        """

        calc age based on birth date

        args:
            birth_date_col (str): name of column containing birth dates
            reference_date (datetime, optional): ref date for age calc
            if none, use current date..

        returns:
            pandas.Series: ages calc from birth dates


        """

        if self.data is None:
            self.load_data()

        if reference_date is None:
            reference_date = datetime.now()

        # birthdate to datetime if not already

        birth_dates = pd.to_datetime(self.data[birth_date_col])

        # calc age

        ages = (reference_date - birth_dates).astype('<m8[Y]').astype(int)

        return ages


        
                    





