# src/visualization/dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_ingestion.clinical_ingestor import ClinicalDataIngestor
from src.data_validation.validator import DataValidator
from src.data_standardization.standardizer import DataStandardizer

def main():
    st.title("AD Multi-Omics Data Integration Pipeline")
    st.sidebar.title("Controls")
    
    # File Upload Section
    st.sidebar.header("Data Input")
    uploaded_file = st.sidebar.file_uploader("Upload clinical data file", type=["csv", "xlsx", "tsv", "txt"])
    
    demo_files = st.sidebar.checkbox("Use demo data instead")
    
    # Pipeline control
    st.sidebar.header("Pipeline Steps")
    run_validation = st.sidebar.checkbox("Run Data Validation", value=True)
    run_standardization = st.sidebar.checkbox("Run Data Standardization", value=True)
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["Data Overview", "Validation Results", "Standardized Data"])
    
    # Process data
    df = None
    validation_results = None
    standardized_data = None
    
    # Load data
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with open("temp_upload.csv", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        df = process_data("temp_upload.csv")
    elif demo_files:
        df = process_data("/home/ubuntu/sage-bio/ad-multi-omics-pipeline/data/raw/GSE289715_counts.csv")
    
    # Display data overview
    if df is not None:
        with tab1:
            display_data_overview(df)
        
        # Run validation if selected
        if run_validation:
            validation_results = run_data_validation(df)
            with tab2:
                display_validation_results(validation_results, df)
        
        # Run standardization if selected
        if run_standardization:
            standardized_data = run_data_standardization(df)
            with tab3:
                display_standardized_data(standardized_data)

def process_data(file_path):
    """Load and process data from file"""
    try:
        # Determine if we need to skip rows based on file structure
        ingestor = ClinicalDataIngestor(file_path)
        
        # For FHIR formatted data, skip the first 2 rows
        if "patient.csv" in file_path:
            df = ingestor.load_data(skiprows=2, header=0)
            # Clean column names
            df.columns = [col.replace('*', '').split(' {')[0].strip() for col in df.columns]
        else:
            df = ingestor.load_data()
        
        st.success(f"Data loaded successfully with {df.shape[0]} rows and {df.shape[1]} columns")
        return df
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def display_data_overview(df):
    """Display basic data overview"""
    st.header("Data Overview")
    
    # Display basic info
    st.subheader("Data Sample")
    st.dataframe(df.head())
    
    # Data summary
    st.subheader("Data Summary")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", df.shape[0])
    with col2:
        st.metric("Columns", df.shape[1])
    with col3:
        missing_percentage = (df.isna().sum().sum() / (df.shape[0] * df.shape[1])) * 100
        st.metric("Missing Data", f"{missing_percentage:.1f}%")
    
    # Data types
    st.subheader("Column Data Types")
    dtypes_df = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes.astype(str),
        'Missing Values': df.isna().sum(),
        'Missing %': (df.isna().sum() / len(df) * 100).round(1)
    })
    st.dataframe(dtypes_df)

def run_data_validation(df):
    """Run validation on the data"""
    validator = DataValidator(df)
    
    # Create validation rules based on data
    expected_types = {}
    range_rules = {}
    
    # Detect ID columns
    id_cols = [col for col in df.columns if 'id' in col.lower()]
    for col in id_cols:
        expected_types[col] = "string"
    
    # Detect date columns
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    for col in date_cols:
        expected_types[col] = "datetime"
    
    # Run validation
    results = validator.run_all_validations(
        expected_types=expected_types,
        range_rules=range_rules
    )
    
    return results

def display_validation_results(results, df):
    """Display validation results"""
    st.header("Data Validation Results")
    
    # Display completeness
    st.subheader("Data Completeness")
    completeness = results['missing_data']['overall_completeness'] * 100
    st.progress(completeness/100)
    st.write(f"Overall completeness: {completeness:.1f}%")
    
    # Columns with missing data
    if results['missing_data']['columns_above_threshold']:
        st.subheader("Columns with Excessive Missing Values")
        missing_df = pd.DataFrame({
            'Column': results['missing_data']['columns_above_threshold'].keys(),
            'Missing %': [v*100 for v in results['missing_data']['columns_above_threshold'].values()]
        })
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x='Missing %', y='Column', data=missing_df.sort_values('Missing %'), ax=ax)
        ax.set_title('Columns with Missing Values')
        ax.set_xlim(0, 100)
        st.pyplot(fig)
    
    # Type mismatches
    if results['type_mismatches']:
        st.subheader("Data Type Mismatches")
        type_df = pd.DataFrame([
            {
                'Column': col,
                'Expected Type': details['expected'],
                'Actual Type': details['actual']
            }
            for col, details in results['type_mismatches'].items()
        ])
        st.dataframe(type_df)
    
    # Display outliers if any
    if results['outliers']:
        st.subheader("Statistical Outliers")
        outlier_df = pd.DataFrame([
            {
                'Column': col,
                'Outlier Count': details['outlier_count'],
                'Outlier %': details['outlier_percentage'] * 100
            }
            for col, details in results['outliers'].items()
        ])
        st.dataframe(outlier_df)
        
        # Visualize one of the columns with outliers
        if outlier_df.shape[0] > 0:
            col_to_plot = outlier_df.iloc[0]['Column']
            if col_to_plot in df.columns and df[col_to_plot].dtype.kind in 'ifc':
                st.subheader(f"Distribution of {col_to_plot} (with outliers)")
                
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.histplot(df[col_to_plot].dropna(), kde=True, ax=ax)
                ax.set_title(f'Distribution of {col_to_plot}')
                st.pyplot(fig)

def run_data_standardization(df):
    """Run data standardization"""
    standardizer = DataStandardizer(df.copy())
    
    # Create a simple standardization function 
    # (since the run_standardization_pipeline method seems to be missing)
    
    standardized_df = df.copy()
    
    # 1. Standardize dates
    date_columns = [col for col in df.columns if 'date' in col.lower()]
    for col in date_columns:
        try:
            standardized_df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')
        except:
            pass
    
    # 2. Standardize IDs
    id_columns = [col for col in df.columns if 'id' in col.lower()]
    for col in id_columns:
        try:
            standardized_df[f"harmonized_{col}"] = "PATIENT-" + df[col].astype(str)
        except:
            pass
    
    # 3. Standardize names
    name_columns = [col for col in df.columns if 'name' in col.lower()]
    for col in name_columns:
        try:
            standardized_df[col] = df[col].str.title()
        except:
            pass
    
    return standardized_df

def display_standardized_data(df):
    """Display standardized data"""
    st.header("Standardized Data")
    
    if df is None:
        st.warning("No standardized data available")
        return
    
    st.subheader("Sample of Standardized Data")
    st.dataframe(df.head())
    
    # Show distribution of key variables if present
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        st.subheader("Distributions of Key Variables")
        
        # Select column to visualize
        selected_col = st.selectbox("Select variable to visualize:", numeric_cols)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df[selected_col].dropna(), kde=True, ax=ax)
        ax.set_title(f'Distribution of {selected_col}')
        st.pyplot(fig)
    
    # Show gender distribution if present
    gender_cols = [col for col in df.columns if 'gender' in col.lower() or 'sex' in col.lower()]
    if gender_cols:
        st.subheader("Gender Distribution")
        gender_col = gender_cols[0]
        
        # Count
        gender_counts = df[gender_col].value_counts()
        
        fig, ax = plt.subplots(figsize=(7, 7))
        gender_counts.plot.pie(autopct='%1.1f%%', ax=ax)
        ax.set_title('Gender Distribution')
        ax.set_ylabel('')  # Hide "None" ylabel
        st.pyplot(fig)

if __name__ == "__main__":
    main()
