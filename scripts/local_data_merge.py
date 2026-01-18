import pandas as pd

# 1. Load both datasets for each category

# BIOMETRIC
# FILE_PATH = "data/processed/api_data_aadhar_biometric/"
bio_p1 = pd.read_csv('api_data_aadhar_biometric_0_500000_cleaned.csv')
bio_p2 = pd.read_csv('api_data_aadhar_biometric_500000_1000000_cleaned.csv')
df_biometric = pd.concat([bio_p1, bio_p2], axis=0, ignore_index=True)

# DEMOGRAPHIC
# FILE_PATH = "data/processed/api_data_aadhar_demographic/"
demo_p1 = pd.read_csv('api_data_aadhar_demographic_0_500000_cleaned.csv')
demo_p2 = pd.read_csv('api_data_aadhar_demographic_500000_1000000_cleaned.csv')
df_demographic = pd.concat([demo_p1, demo_p2], axis=0, ignore_index=True)

# ENROLMENT
# FILE_PATH = "data/processed/api_data_aadhar_enrolment/"
enrol_p1 = pd.read_csv('api_data_aadhar_enrolment_0_500000_cleaned.csv')
enrol_p2 = pd.read_csv('api_data_aadhar_enrolment_500000_1000000_cleaned.csv')
df_enrolment = pd.concat([enrol_p1, enrol_p2], axis=0, ignore_index=True)


# 2. Remove duplicates by key-based aggregation
group_cols = ['date', 'state', 'district', 'pincode']

df_biometric = df_biometric.groupby(group_cols).sum().reset_index()
df_demographic = df_demographic.groupby(group_cols).sum().reset_index()
df_enrolment = df_enrolment.groupby(group_cols).sum().reset_index()

print("Vertical Stacking Complete")

# 3. Standardize column names
df_biometric = df_biometric.rename(columns={'bio_age_5_17': 'bio_child', 'bio_age_17_': 'bio_adult'})
df_demographic = df_demographic.rename(columns={'demo_age_5_17': 'demo_child', 'demo_age_17_': 'demo_adult'})
df_enrolment = df_enrolment.rename(columns={'age_0_5': 'enrol_infant', 'age_5_17': 'enrol_child', 'age_18_greater': 'enrol_adult'})


# 4. Standardize date format
for df in [df_biometric, df_demographic, df_enrolment]:
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)


# 5. Horizontal Merge (Combine all three datasets)
df_master = pd.merge(df_biometric, df_demographic, on=['date', 'state', 'district', 'pincode', 'valid_flag', 'pin_prefix'], how='outer')
df_master = pd.merge(df_master, df_enrolment, on=['date', 'state', 'district', 'pincode', 'valid_flag', 'pin_prefix'], how='outer')


# =====================
# FEATURE ENGINEERING
# =====================

# Remove "Not Valid" entries
df_master = df_master[df_master['valid_flag'] != 'Not Valid']

# Remove the 'valid_flag' column
df_master = df_master.drop(columns=['valid_flag'])

# Replace NaN with 0
df_master = df_master.fillna(0)

# Saving master dataset (with compression)
df_master.to_parquet("master_dataset.parquet", index=False)         # smaller file size
# df_master.to_csv("master_dataset.csv.gz", index=False, compression='gzip')

# Load master dataset
# df = pd.read_parquet("master_dataset.parquet")