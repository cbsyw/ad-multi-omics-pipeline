

import logging



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
                        "expected": expected
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
        elif expected == "string" or expected == "categorical"
            return pd.api.types.is_string_dtype(actual) or pd.api.types.is_categorical_dtype(actual)
        else:
            return str(actual) == expected
        
    # value range validation
        
    def validate_value_ranges(self,range_rules=None):
        """
            Validate values fall within expected ranges
            
            Args:
                range_rules dictionary maping columns to min/max rules

            Returns:
                dictionary of columns with range violations
        """

        if range_rules is None:
            range_rules = {}

        range_violations = {}

        for column, rules in range_rules.items():
            if column in self.date.columns:
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

    
    

    
            
