

## Base Data Ingestion Class

### Why?
* Consistent Interface - all data ingestors have same basic methods
* Error Handling - validation and logging are handled in one place
* Flexy - different data types can be handled in a unique specialized way
* Extensibility - new data types can be added by creating new subclasses


### Next???

* ClinicalDataIngestor - for tabular patient data (csv,excel)
* GenomicDataIngestor - for genetic data formats (VCF, FASTA, expression data)
* ImagingDataIngestor - for brain imaging only (DICOM, NIFTI)
* ProteinDataIngestor - For proteomics data analysis
* MetabolomicsDataIngestor - For metabolite profiling data





