


import pandas as pd
import numpy as np
import logging
from datetime import datetime


class DataStandardizer:
    """
        Base class for standardizing clinical and omics data
    """

    def __init__(self,data, logger=None):
        self.data = data
        self.logger = logger or logging.getLogger(__name__)
        self.standardization_info = {
            "transformations_applied": [],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


        # date standardization 

    def standardize_dates(self, date_columns, target_format="%Y-%m-%d"):
        """
            Standardize date columns to consistent format 
            
            Args:
                date_columns: list of columns with dates
                target_format: desired date format for string
        """


        if not date_columns:
            return False

        transformed_columns = {}

        for column in date_columns:
            if column in self.data.columns:
                try:
                    # convert to date time
                    self.data[column] = self.data[column].dt.strftime(target_format)

                    # convert to new string format if requested

                    if target_format:
                        self.data[column] = self.data[column].dt.strftime(target_format)

                    transformed_columns.append(column)
                        
                
                except Exception as e:
                    self.logger.error(f"Error standardizing date column {column}: {str(e)}")


        if transformed_columns:
            self.standardization_info["transformations_applied"].append(
                    {
                        "type": "date_standardization",
                        "columns": transformed_columns,
                        "target_format": target_format,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                )
            return True

        return False

     
    # unit standardization

    def standardize_units(self, column_unit_map):
        """
            convert to standard units

            Args:
                column unit map: dictionary mapping columns to source and target units

            Returns:
                list of columns successfully standardized
        """

        standardized_columns = []

        for column, unit_info in column_unit_map.items():
            if column in self.data.columns:
                source_unit = unit_info.get("source_unit")
                target_unit = unit_info.get("target_unit")
                factor = unit_info.get("factor")
                
                if factor is None:
                    self.logger.error(f"Missing conversion factor for {column} from {source_unit} to {target_unit")
                    continue

                try:
                    # create new column with standardized unit
                    new_column = f"{column}_{target_unit}"
                    self.data[new_column] = self.data[column] * factor

                    # record the transformation
                    
                    standardized_columns.append({
                                      "original_column":column,
                                      "new_column":new_column,
                                      "source_unit":source_unit,
                                      "target_unit":target_unit,
                                      })

                    self.logger.info(f"standardized {column} from {source_unit} to {target_unit}")

                except Exception as e:
                    self.logger.error(f"error standardizing units for {column}: {str(e)}")
        
            if standardized_columns:
                self.standardization_info["transformation_applied"].append({
                    "type":"unit_standardization",
                    "columns":"standardized_columns",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            
            return standardized_columns
        
        def standardize_terminology(self, column, mapping_dict, new_column=None):
            """
            Map values in a column to standard terminology
            Args:
                column: column containing values to standardize
                mapping_dict: dictionary mapping values to standard terms
                new_column: if given, new column made instead of modifying existing

            Returns:
                Boolean indicating success 
            """

            if column not in self.data.columns
                 self.loggier.error(f"column {column} not found in the dataset")
                 return False
            
            target_column = new_column or column


            # create copy of original data in a new column..

            if new_column:
                self.data[target_column] = self.data[column].copy()

            # apply mapping

            unmapped_values = set()

            def map_value(val):
                if pd.isna(val):
                    return val

                str_val = str(val).lower().strip()
                if str_val in mapping_dict:
                        return mapping_dict[str_val]
                else:
                    unmapped_values.add(str_val)
                    return val

            self.data[target_column] = self.data[column].apply(map_value)

            # log unmapped values

            if unmapped_values:
                self.logger.warning(f"Found{len(unmapped_values)} unmapped values in {column}: {unmapped_values}")
            
            self.standardization_info["transformations_applied"].append({
                "type": "terminology_standardization",
                "column": column,
                "target_column": target_column,
                "unmapped_values_count": len(unmapped_values),
            })

            return True
        

        # harmonize ids across data sets

        def harmonize_ids(self, id_column, id_format = None, prefix = None):
            """
            Standardize patient and subject ids to a consistent format

            Args:
                id_column: column containing IDs to harmonize
                id_format: format string for id standardization
                prefix: prefix to add to ids (ex. 'PATIENT-')
            
            Returns:
                series with harmonized IDs
            """

            if id_column not in self.data.columns:
                self.logger.error(f"ID column {id_column} not found in dataset")
                return None
            
            # create harmonized id column

            harmonized_column = f"harmonized{id_column}"

            # start with og IDs

            self.data[harmonized_column] = self.data[id_column].astype(str)


            # remove non alphanumeric chars if needed

            if id_format == "alphanumeric":
                self.data[harmonized_column] = self.data[harmonized_column].str.replace(r'[^a-zA-Z0-9]', '', regex=True)
            
            # apply prefix if given

            if prefix:
                self.data[harmonized_column] = prefix + self.data[harmonized_column]
            
                self.standardization_info["transformations_applied"].append({
                    "type": "id_harmonization",
                    "source_column": id_column,
                    "result_column": harmonized_column,
                    "format": id_format,
                    "prefix": prefix,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            return self.data[harmonized_column]

        def standardize_demographics(self, name_columns=None, address_columns=None):
            """
            Standardize demographic information like names and addresses
            
            Args:
                name_columns: Dictionary mapping name fields to standard columns
                    {'name_first': 'given_name', 'name_last': 'family_name'}
                address_columns: Dictionary mapping address fields to standard columns
                    {'addr1': 'address_line', 'zip': 'postal_code'}
            
            Returns:
                Dictionary of standardized columns
            """
            standardized = {}
            
            # standardize name fields
            if name_columns:
                for source, target in name_columns.items():
                    if source in self.data.columns:
                        # Convert to proper case and remove extra spaces
                        self.data[target] = self.data[source].str.title().str.strip()
                        standardized[source] = target
            
            # Standardize address fields
            if address_columns:
                for source, target in address_columns.items():
                    if source in self.data.columns:
                        # Basic cleaning
                        self.data[target] = self.data[source].str.strip()
                        standardized[source] = target
            
            if standardized:
                self.standardization_info["transformations_applied"].append({
                    "type": "demographic_standardization",
                    "standardized_fields": standardized,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            
            return standardized

                        
        def run_standardization_pipeline(self, config):
            """
            Run a complete standardization pipeline based on configuration
            
            Args:
                config: Dictionary with standardization configuration
                    {
                    "dates": {"columns": [...], "format": "..."},
                    "units": {column_unit_mappings},
                    "terminology": {column_mapping_pairs},
                    "ids": {"column": "...", "format": "...", "prefix": "..."},
                    "demographics": {"name_columns": {...}, "address_columns": {...}}
                    }
            
            Returns:
                Standardization info dictionary
            """
            # Date standardization
            if "dates" in config:
                self.standardize_dates(
                    config["dates"].get("columns", []),
                    config["dates"].get("format")
                )
            
            # Unit standardization
            if "units" in config:
                self.standardize_units(config["units"])
            
            # Terminology mapping
            if "terminology" in config:
                for column, mapping in config["terminology"].items():
                    self.standardize_terminology(column, mapping)
            
            # ID harmonization
            if "ids" in config:
                self.harmonize_ids(
                    config["ids"].get("column"),
                    config["ids"].get("format"),
                    config["ids"].get("prefix")
                )
            
            # Demographics standardization
            if "demographics" in config:
                self.standardize_demographics(
                    config["demographics"].get("name_columns"),
                    config["demographics"].get("address_columns")
                )
            
            return self.standardization_info


                                


