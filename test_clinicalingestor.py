
import sys
import os
import json
import pandas as pd
from datetime import datetime 

# Add the src directory to the Python path
sys.path.append(os.path.abspath('src'))

from src.data_ingestion.base_ingestion import DataIngestionBase
from src.data_ingestion.clinical_ingestor import ClinicalDataIngestor

def main():
    """Test the clinical data ingestor with a sample file."""
    # Path to the sample clinical data
    data_path = 'data/raw/patient.csv'

    print(f"Testing clinical data ingestor with file: {data_path}")

    # Create an ingestor instance
    ingestor = ClinicalDataIngestor(data_path)

    # Load the data
    data = ingestor.load_data()

    # Get metadata
    metadata = ingestor.get_metadata()

    # Print data shape and first few rows
    print("\n----- Data Preview -----")
    print(f"Shape: {data.shape}")
    print("\nFirst 3 rows:")
    print(data.head(3).to_string())

    # Print metadata in a readable format
    print("\n----- Metadata -----")
    print(json.dumps(metadata, indent=2, default=str))

    print("\n----- Basic Statistics -----")

    # transform date to age

    if 'age' in data.columns:
        print("Age statistics:")
        print(f"  Mean age: {data['age'].mean():.1f}")
        print(f"  Age range: {data['age'].min()} - {data['age'].max()}")
         

    elif 'birthDate' in data.columns:
        print("age statistics (calculated from birthDate):")
        # convert
        birth_dates = pd.to_datetime(data['birthDate'], errors='coerce')
        #filter out NaT values
        valid_dates = birth_dates.dropna()

        if not valid_dates.empty:
            #calc age
            today = datetime.now()
            ages = ((today - valid_dates).dt.days/365.25).round().astype(int)

            print(f" Mean age: {ages.mean():.1f}")
            print(f" age range: {ages.min()} - {ages.max()}")
        else:
            print(" no valid birth dates found")
    else:
        print ("no age or birthDate columns found in data")


    if 'diagnosis' in data.columns:
        print("\nDiagnosis distribution:")
        for diagnosis, count in data['diagnosis'].value_counts().items():
            print(f"  {diagnosis}: {count} patients")
    else:
        print("\nNo diagnosis column found in the dataset")



if __name__ == "__main__":
    main()
