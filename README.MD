

# AD Data Integration Pipeline Documentation

## Project Overview
The AD Multi-Omics Data Integration Pipeline is a framework demo for integrating, validating, standardizing, and visualizing data types in research. The pipeline is designed to handle clinical data types with a focus on data quality and reproducibility.

## System Architecture

The pipeline consists of the following core components:

1. **Data Ingestion Layer**: Handles loading data from various file formats
2. **Data Validation Module**: Performs quality checks and identifies issues
3. **Data Standardization Engine**: Normalizes data formats and terminology
4. **Visualization Dashboard**: Provides interactive data exploration
5. **CSV Schema Validator**: Check CSV upload vs. Schema 
6. **Synapse Integration**: Simple integration with synapseclient 

### Directory Structure
```
ad-multi-omics-pipeline/
├── src/
│   ├── data_ingestion/
│   │   ├── __init__.py
│   │   ├── base_ingestion.py
│   │   └── clinical_ingestor.py
│   ├── data_validation/
│   │   ├── __init__.py
│   │   └── validator.py
│   ├── data_standardization/
│   │   ├── __init__.py
│   │   └── standardizer.py
│   ├── data_checker/
│   │   ├── __init__.py
│   │   └── checker.py
│   ├── synapse/
│   │   ├── __init__.py
│   │   └── synapse.py
│   └── visualization/
│       └── dashboard.py
├── data/
│   ├── raw/
│   └── processed/
├── tests/
│   ├── test_clinical_ingestor.py
│   ├── test_validator.py
│   └── test_standardizer.py
└── README.md
```

## Component Documentation

### Data Ingestion

#### Base Ingestion Class
The `DataIngestionBase` class provides a common interface for all data ingestion modules:

- Path validation
- Logging configuration
- Methods for data loading and metadata extraction

#### Clinical Data Ingestor
The `ClinicalDataIngestor` class handles tabular clinical data:

```python
from src.data_ingestion.clinical_ingestor import ClinicalDataIngestor

# Initialize with a data path
ingestor = ClinicalDataIngestor("data/raw/patient.csv")

# Load the data
clinical_data = ingestor.load_data()

# Get metadata about the dataset
metadata = ingestor.get_metadata()
```

**Features:**
- Automatic format detection (CSV, Excel, TSV)
- Metadata extraction
- Age calculation from birth dates
- Error handling and logging

### Data Validation

The `DataValidator` class performs quality checks on loaded data:

```python
from src.data_validation.validator import DataValidator

# Initialize with a DataFrame
validator = DataValidator(clinical_data)

# Define validation rules
expected_types = {
    "patient_id": "string",
    "age": "numeric",
    "diagnosis_date": "datetime"
}

range_rules = {
    "age": {"min": 0, "max": 120},
    "bmi": {"min": 10, "max": 50}
}

# Run all validations
results = validator.run_all_validations(
    expected_types=expected_types,
    range_rules=range_rules
)
```

**Validation Checks:**
- Missing data identification
- Data type verification
- Value range validation
- Statistical outlier detection

### Data Standardization

The `DataStandardizer` class normalizes data formats and terminology:

```python
from src.data_standardization.standardizer import DataStandardizer

# Initialize with a DataFrame
standardizer = DataStandardizer(clinical_data)

# Standardize dates
standardizer.standardize_dates(["birth_date", "diagnosis_date"])

# Harmonize IDs
standardizer.harmonize_ids("patient_id", prefix="PATIENT-")

# Standardize terminology
gender_mapping = {"m": "male", "f": "female", "male": "male", "female": "female"}
standardizer.standardize_terminology("gender", gender_mapping)
```

**Standardization Features:**
- Date format normalization
- Unit conversion for measurements
- Terminology mapping to standard ontologies
- ID harmonization across datasets
- Demographic information standardization

### Visualization Dashboard

The Streamlit-based dashboard provides interactive exploration of the processed data:

```bash
# Run the dashboard
streamlit run src/visualization/dashboard.py --server.address=0.0.0.0 --server.port=8501
```

**Dashboard Features:**
- Data overview and summary statistics
- Validation results visualization
- Standardized data exploration
- Interactive filtering and visualization

## Getting Started

### Prerequisites
- Python 3.9+
- Conda environment

### Installation

1. Clone the repository:
```bash
git clone https://github.com/username/ad-multi-omics-pipeline.git
cd ad-multi-omics-pipeline
```

2. Create and activate conda environment:
```bash
conda create -n ad-data-demo python=3.9
conda activate ad-data-demo
```

3. Install required packages:
```bash
pip install pandas numpy streamlit matplotlib seaborn
```

### Running the Pipeline

1. **Data Ingestion:**
```python
from src.data_ingestion.clinical_ingestor import ClinicalDataIngestor

ingestor = ClinicalDataIngestor("path/to/your/data.csv")
data = ingestor.load_data()
```

2. **Data Validation:**
```python
from src.data_validation.validator import DataValidator

validator = DataValidator(data)
validation_results = validator.run_all_validations()
```

3. **Data Standardization:**
```python
from src.data_standardization.standardizer import DataStandardizer

standardizer = DataStandardizer(data)
standardized_data = standardizer.standardize_dates(["birth_date"])
```

4. **Launch Dashboard:**
```bash
streamlit run src/visualization/dashboard.py --server.address=0.0.0.0 --server.port=8501
```

## Accessing the Dashboard

The dashboard is available at:
```
http://150.136.70.185:8501
```

## Next Steps and Roadmap

1. **Planned Enhancements**
   - Additional data type ingestors (genomic, imaging)
   - Integration layer for cross-modality analysis
   - Advanced analytics and machine learning capabilities

2. **Ongoing Development**
   - Feature engineering for AD-specific analyses
   - Advanced visualization options
   - Export capabilities for processed data

## Troubleshooting

### Common Issues
- **Import Errors**: Ensure Python path includes the project root directory
- **File Loading Errors**: Verify file paths and permissions
- **Dashboard Access Issues**: Check firewall settings and security rules
