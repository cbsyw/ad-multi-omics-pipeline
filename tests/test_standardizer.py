
# test_standardizer.py
import logging
import pandas as pd
import os
from src.data_ingestion.clinical_ingestor import ClinicalDataIngestor
from src.data_standardization.standardizer import DataStandardizer

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_data_standardization():
    """Test the data standardization pipeline on clinical data"""
    
    # 1. Load clinical data
    logger.info("Loading clinical data...")
    data_path = 'data/raw/patient.csv'
    
    if not os.path.exists(data_path):
        logger.error(f"File not found: {data_path}")
        return
    
    # Using ClinicalDataIngestor with specific parameters for this complex CSV
    ingestor = ClinicalDataIngestor(data_path)
    clinical_data = ingestor.load_data(skiprows=2, header=0)
    
    # Cleanup column names (remove asterisks and curly brace notations)
    clinical_data.columns = [col.replace('*', '').split(' {')[0].strip() for col in clinical_data.columns]
    
    logger.info(f"Loaded clinical data with shape: {clinical_data.shape}")
    logger.info(f"Columns: {clinical_data.columns.tolist()}")
    
    # 2. Create standardization configuration
    standardization_config = {
        "dates": {
            "columns": ["birthDate"],
            "format": "%Y-%m-%d"
        },
        "ids": {
            "column": "Id",
            "format": "alphanumeric",
            "prefix": "PATIENT-"
        },
        "demographics": {
            "name_columns": {
                "Family Name": "family_name",
                "Given Name": "given_name"
            },
            "address_columns": {
                "line": "address_line",
                "city": "city",
                "state": "state",
                "postalCode": "postal_code"
            }
        }
    }
    
    # 3. Run standardization
    logger.info("Running data standardization...")
    standardizer = DataStandardizer(clinical_data, logger=logger)
    results = standardizer.run_standardization_pipeline(standardization_config)
    
    # 4. Display results
    logger.info("=== STANDARDIZATION RESULTS ===")
    
    for transformation in results["transformations_applied"]:
        logger.info(f"Applied {transformation['type']} at {transformation.get('timestamp')}")
        
        if transformation["type"] == "date_standardization":
            logger.info(f"  Standardized date columns: {transformation['columns']} to format {transformation['target_format']}")
        
        elif transformation["type"] == "id_harmonization":
            logger.info(f"  Harmonized ID column: {transformation['source_column']} → {transformation['result_column']}")
            logger.info(f"  Format: {transformation.get('format')}, Prefix: {transformation.get('prefix')}")
        
        elif transformation["type"] == "demographic_standardization":
            logger.info(f"  Standardized demographic fields: {transformation['standardized_fields']}")
    
    # 5. Show sample of standardized data
    logger.info("\n=== SAMPLE OF STANDARDIZED DATA ===")
    display_columns = []
    
    # Find created columns to display
    if "harmonized_Id" in clinical_data.columns:
        display_columns.append("harmonized_Id")
    
    if "family_name" in clinical_data.columns and "given_name" in clinical_data.columns:
        display_columns.extend(["family_name", "given_name"])
    
    if "address_line" in clinical_data.columns:
        display_columns.extend(["address_line", "city", "state", "postal_code"])
    
    # If we found columns to display
    if display_columns:
        logger.info(clinical_data[display_columns].head().to_string())
    else:
        logger.info(clinical_data.head().to_string())
    
    return clinical_data, results

if __name__ == "__main__":
    test_data_standardization()
