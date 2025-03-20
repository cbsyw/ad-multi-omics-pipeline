

# test_validator.py
import logging
import pandas as pd
from src.data_ingestion.clinical_ingestor import ClinicalDataIngestor
from src.data_validation.validator import DataValidator
import os

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_clinical_data_validation():
    """Test the data validation on clinical data"""
    
    # 1. Load clinical data
    logger.info("Loading clinical data...")
    data_path = 'data/raw/patient.csv'
    
    if not os.path.exists(data_path):
        logger.error(f"File not found: {data_path}")
        return
    
    # Using ClinicalDataIngestor with specific parameters for this complex CSV
    ingestor = ClinicalDataIngestor(data_path)
    
    # Since this CSV has multiple header rows, we need special handling
    # Let's specify we want to skip the first 2 rows and use the 3rd row as header
    clinical_data = ingestor.load_data(skiprows=2, header=0)
    
    # Cleanup column names (remove asterisks and curly brace notations)
    clinical_data.columns = [col.replace('*', '').split(' {')[0].strip() for col in clinical_data.columns]
    
    logger.info(f"Loaded clinical data with shape: {clinical_data.shape}")
    logger.info(f"Columns: {clinical_data.columns.tolist()}")
    
    # 2. Define validation rules based on the FHIR patient data structure
    
    # Expected data types for key columns
    expected_types = {
        "Id": "string",
        "gender": "categorical",
        "birthDate": "string",  # Initially as string, can be converted to datetime
        "postalCode": "string"
    }
    
    # Expected value ranges - for demonstration
    range_rules = {
        # We can extract birth year and validate it
        # This requires preprocessing the birthDate column
        "birth_year": {"min": 1900, "max": 2025}
    }
    
    # Preprocess data - extract birth year for validation
    if "birthDate" in clinical_data.columns:
        try:
            clinical_data["birth_year"] = pd.to_datetime(clinical_data["birthDate"]).dt.year
        except:
            logger.warning("Could not convert birthDate to datetime for year extraction")
    
    # 3. Run validation
    logger.info("Running data validation...")
    validator = DataValidator(clinical_data, logger=logger)
    results = validator.run_all_validations(
        expected_types=expected_types,
        range_rules=range_rules
    )
    
    # 4. Display validation results
    logger.info("=== VALIDATION RESULTS ===")
    
    # Completeness
    logger.info(f"Overall data completeness: {results['missing_data']['overall_completeness']:.2%}")
    if results['missing_data']['columns_above_threshold']:
        logger.warning("Columns with excessive missing values:")
        for col, pct in results['missing_data']['columns_above_threshold'].items():
            logger.warning(f"  - {col}: {pct:.2%} missing")
    
    # Type issues
    if results['type_mismatches']:
        logger.warning("Data type mismatches:")
        for col, details in results['type_mismatches'].items():
            logger.warning(f"  - {col}: expected {details['expected']}, got {details['actual']}")
    
    # Range violations
    if results['range_violations']:
        logger.warning("Value range violations:")
        for col, details in results['range_violations'].items():
            rules = details['rules']
            logger.warning(f"  - {col}: {details['violation_count']} values ({details['violation_percentage']:.2%}) "
                          f"outside range [min={rules.get('min', 'None')}, max={rules.get('max', 'None')}]")
    
    # Outliers
    if results['outliers']:
        logger.warning("Columns with statistical outliers:")
        for col, details in results['outliers'].items():
            logger.warning(f"  - {col}: {details['outlier_count']} outliers ({details['outlier_percentage']:.2%}) "
                          f"using {details['method']} method")
    
    return results

if __name__ == "__main__":
    test_clinical_data_validation()