## ClinicalDataIngestor

- header detection algo
  - metadata rows at top
  - multi header rows
  - non standard header format
  - empty rows
- detection Score-Based
  - eval each row based on characteristics typical of headers vs. data rows
  - multiple heuristics to create combined score
  - configure thersholds for detection sensitivity

## Data Validation

## Data Standardization

## Visualization & Dashboard

## TODO 

* CSV Validation Script
	* vaildate csv files vs schema (metadata)
	* sample JSON schema file 

* Simple Synapse Integration
	* use synapseclient 
	* maybe just an upload and validate file vs metadata template?
	* is api open


