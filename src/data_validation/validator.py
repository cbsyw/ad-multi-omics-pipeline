

import logging
import pandas as pd 
import numpy as np
from datetime import datetime


class DataValidator:
    """
    Base validator for data quality checks and validation
    """

    def __init__(self, data, logger = None):
        self.data = data
        self.logger = logger or logging.getLogger(__name__)
        self.validation_results = {}


    def validate_missing_data(self, threshold = 0.2):
        """
            check for columns with missing data above threshold

            args: 
                threshold: max acceptable proportion of missing values (0.2 = 20%)
        """


        # calc percentage of missing values in each columns
        
        missing_percentages = self.data.isna().mean()

        # find columns above thershold

        problematic_columns = missing_percentages[missing_percentages > threshold]

        # store in results
        
        self.validation_results["missing_data"] = {
            "columns_above_threshold": problematic_columns.to_dict(),
            "overall_completeness": 1 - self.data.isna().mean().mean()

        }

        return problematic_columns


    def validate_data_types(self, expected_types = None):
        """
        Validate that data types match expected types

        args:
            expected_types: dictionary mapping column names to expected types

        returns:
            dictionary of columns with type mismatches

        """

        if expected_types is None:
            expected_types = {}

        type_mismatches = {}
        
        for column in self.data.columns:
            if column in expected_types:
                expected = expected_types[column]
                actual = self.data[column].dtype

                # check if types are compatible
                
                if not self._is_compatible_type(actual, expected):
                    type_mismatches[column] = {
                        "expected": expected,
                        "actual": str(actual)
                    }


        self.validation_results["type_mismatches"] = type_mismatches
        return type_mismatches

    # helper function to check type compatibility

    def _is_compatible_type(self, actual, expected):
        """
            Helper method to check type compatible
        """
        # handle numpy and pands type compatibility

        if expected == "numeric":
            return pd.api.types.is_numeric_dtype(actual)
        elif expected == "datetime":
            return pd.api.types.is_datetime64_dtype(actual)
        elif expected == "string" or expected == "categorical":
            return pd.api.types.is_string_dtype(actual) or pd.api.types.is_categorical_dtype(actual)
        else:
            return str(actual) == expected
        
    # value range validation
        
    def validate_value_ranges(self,range_rules=None):
        """
            Validate values fall within expected ranges
            
            Args:
                range_rules dictionary mapping columns to min/max rules

            Returns:
                dictionary of columns with range violations
        """

        if range_rules is None:
            range_rules = {}

        range_violations = {}

        for column, rules in range_rules.items():
            if column in self.data.columns:
                min_val = rules.get("min")
                max_val = rules.get("max")

                violations = pd.Series(False, index = self.data.index)

                if min_val is not None:
                    violations = violations | (self.data[column] < min_val)
    
        
                if max_val is not None:
                    violations = violations | (self.data[column] > max_val)

                if violations.any():
                    range_violations[column] = {
                        "rules": rules,
                        "violation_count": violations.sum(),
                        "violation_percentage": violations.mean(),
                    }

        self.validation_results["range_violations"] = range_violations
        return range_violations

    # ex. dictionary of rules, checks columns against rules, records violations for minmax constraints

    # outlier detection (detect statistical outliers)

    def detect_outliers(self, columns = None, method = "zscore", threshold=3):
        
        """
        Detect statistical outlier in numeric columns
        
        Args:
            columns: list of columns to check (defaults to all numeric)
            method: (zscore or iqr) 
            threshold: for outlier classification
        
        """

        if columns is None:
            columns = self.data.select_dtypes(include=np.number).columns

        outliers = {}

        for column in columns:
            if column in self.data.columns:
                if method == "zscore":
                    # how many std devs from mean

                    z_scores = np.abs((self.data[column] - self.data[column].mean()) / self.data[column].std())
                    is_outlier = z_scores > threshold
                elif method == "iqr":
                    # values outside of 1.5 * iqr from q1/q3
                    Q1 = self.data[column].quantile(0.25)
                    Q3 = self.data[column].quantile(0.75)
                    IQR = Q3 - Q1
                    is_outlier = (self.data[column] < (Q1 - 1.5 * IQR)) | (self.data[column] > (Q3 + 1.5 * IQR))
                else: 
                    raise ValueError (f"Unsupported outlier detection method: {method}")
                
                if is_outlier.any():
                    outliers[column] = {
                        "method": method,
                        "threshold": threshold,
                        "outlier_count": is_outlier.sum(),
                        "outlier_percentage": is_outlier.mean(),
                    }
        self.validation_results["outliers"] = outliers
        return outliers

    
    # run all validations 

    def run_all_validations(self, expected_types = None, range_rules = None, outlier_columns = None):

        self.validate_missing_data()
        self.validate_data_types(expected_types)
        self.validate_value_ranges(range_rules)
        self.detect_outliers(outlier_columns) 

        # time stamp

        self.validation_results["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return self.validation_results



    
    

    
            
