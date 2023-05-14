# Load necessary libraries
import os
import pandas as pd

# Get the absolute path of the directory containing the script file
script_dir = os.path.abspath(os.getcwd())

# File paths (relative to the script directory)
data_filepath = os.path.join(
    script_dir, 'datasets/2008_BSA_Inpatient_Claims_PUF.csv')
base_drg_filepath = os.path.join(
    script_dir, 'datasets/Base_DRG_Descriptors.csv')
icd9_filepath = os.path.join(script_dir, 'datasets/ICD9_Descriptors.csv')

# Load CSV files
data = pd.read_csv(data_filepath)
base_drg_df = pd.read_csv(base_drg_filepath)
icd9_df = pd.read_csv(icd9_filepath)

# Join the datasets and rename columns
data = pd.merge(data, base_drg_df[['Base DRG', 'Descriptor']],
                left_on='IP_CLM_BASE_DRG_CD', right_on='Base DRG',
                how='left', suffixes=('_base', '_drg'))
data = data.drop(['Base DRG'], axis=1)
data = data.rename(columns={'Descriptor': 'descriptor_drg'})

data = pd.merge(data, icd9_df[['ICD-9 Procedure Code', 'Descriptor']],
                left_on='IP_CLM_ICD9_PRCDR_CD', right_on='ICD-9 Procedure Code',
                how='left', suffixes=('_icd9', '_proc'))
data = data.drop(['ICD-9 Procedure Code'], axis=1)
data = data.rename(columns={'Descriptor': 'descriptor_icd'})

# Replace missing values'descriptor_icd'
data['descriptor_icd'] = data['descriptor_icd'].fillna(
    'No primary procedure on patient')

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
data = data.rename(columns=new_columns)

# Transform gender categories
gender_dict = {1: 'Male', 2: 'Female'}
data['gender'] = data['gender'].replace(gender_dict)

# Transform age categories
age_dict = {
    1: 'Under 65',
    2: '65-69',
    3: '70-74',
    4: '75-79',
    5: '80-84',
    6: '85 and above'
}
data['age'] = data['age'].replace(age_dict)
data['age'] = pd.Categorical(
    data['age'], ['Under 65', '65-69', '70-74', '75-79', '80-84',
                  '85 and above'])

# Transform length categories
length_dict = {1: '1 day',
               2: '2-4 days',
               3: '5-7 days',
               4: '8 or more days'}
data['length'] = data['length'].replace(length_dict)
data['length'] = pd.Categorical(
    data['length'], ['1 day', '2-4 days', '5-7 days', '8 or more days'])

# Drop DRGs with less than 2000 claims
drg_counts = data['base_drg'].value_counts()
drg_filter = drg_counts[drg_counts >= 2000].index
data = data[data['base_drg'].isin(drg_filter)]

# Export to csv
data.to_csv('data_cleaned.csv', index=False)
