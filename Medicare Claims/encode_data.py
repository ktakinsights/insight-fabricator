# Load necessary libraries
import os
import pandas as pd

# Get the absolute path of the directory containing the script file
script_dir = os.path.abspath(os.getcwd())

# File paths (relative to the script directory)
data_filepath = os.path.join(
    script_dir, 'datasets/2008_BSA_Inpatient_Claims_PUF.csv')

# Load CSV files
pr_data = pd.read_csv(data_filepath)

# Define the new column names
new_columns = {
    'IP_CLM_ID': 'id',
    'BENE_SEX_IDENT_CD': 'gender',
    'BENE_AGE_CAT_CD': 'age',
    'IP_CLM_BASE_DRG_CD': 'base_drg',
    'IP_CLM_ICD9_PRCDR_CD': 'icd9',
    'IP_CLM_DAYS_CD': 'length',
    'IP_DRG_QUINT_PMT_AVG': 'payment',
    'IP_DRG_QUINT_PMT_CD': 'quintile'
}

# Rename the columns
pr_data = pr_data.rename(columns=new_columns)

# Drop DRGs with less than 2000 claims
drg_counts = pr_data['base_drg'].value_counts()
drg_filter = drg_counts[drg_counts >= 2000].index
pr_data = pr_data[pr_data['base_drg'].isin(drg_filter)]

# Change icd9 missing values to code 100
pr_data['icd9'] = pr_data['icd9'].fillna(100)

# Export to csv
pr_data.to_csv('data_encoded.csv', index=False)
