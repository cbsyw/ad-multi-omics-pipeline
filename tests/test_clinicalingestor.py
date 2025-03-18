

import sys
import os
import join

# add src directory to python path

sys.path.append(os.path.abspath('src'))

from data_ingestion.clinical_ingestor import ClinicalDataIngestor

def main():
    """ Test cdi with a sample file"""

    # path to sample data 
    data_path = "data/raw/sample_clinical.csv"

    print(f"test data ingestor with file: {data_path}")

    # create instance of cdi

    ingestor = ClinicalDataIngestor(data_path)

    # load data

    data = ingestor.load_data()

    # get meta

    metadata = ingestor.get_metadata()

    # print data shape and first rows

    print("\n ---- data preview -----")
    print(f"Shape: {data.shape}")
    print("\nFirst 3 rows:")
    print(data.head(3).to_string())

    # print metadata in a readable format

    print("\n ---- metadata preview -----")
    print(json.dumps(metadata, indent=2, default=str))


    print("\n ---- basic statistics -----")
    print("age statistics:")
    print(f" Mean age: {data['age'].mean():1f}")
    print(f" Age range: {data['age'].min()} - {data['age'].max()}")


    print("\n diagnosis distribution:")
    for diagnosis, count in data ['diagnosis'].value_counts().items():
        print(f" {diagnosis}: {count} patients")


if __name__ == "__main__":
    main()
            
    
