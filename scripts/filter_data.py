import pandas as pd

# ====================================
# NORMALIZE EXCEL COLUMNS
# ====================================

# # 1. Load your file
# df = pd.read_excel("2011-IndiaStateDist-0000.xlsx")

# # 2. Define the two columns you want to clean
# target_columns = ['Level', 'Name', 'TRU']

# # 3. Apply the transformation
# for col in target_columns:
#     df[col] = (
#         df[col]
#         .astype(str)             # Ensure it's a string
#         .str.lower()            # Convert to lowercase
#         .str.replace(r'[^a-z0-9]', '', regex=True) # Remove everything EXCEPT letters and numbers
#     )

# # 4. Save the result
# df.to_excel("census_data.xlsx", index=False)


# ====================================
# FILTER CENSUS DATA BASED ON STATE
# ====================================

# df_census = pd.read_csv("data/external/census_data.csv")

# # Filter for both "state" and "total" simultaneously
# df_census_states = df_census[(df_census['level'].str.lower() == 'state') & 
#                  (df_census['type'].str.lower() == 'total')]

# df_census_states.to_csv("data/external/census_data_states_updated.csv", index=False)


# ====================================
# IDENTIFY UNIQUE STATES
# ====================================

df_master = pd.read_parquet("data/processed/master_dataset.parquet")
df_census = pd.read_csv("data/external/census_data_states_updated.csv")

# 1. Unique states in census dataset
print("Unique states in Census states-only dataset:")
print(df_census[df_census['level'] == 'state']['name'].nunique())
print(sorted(df_census[df_census['level'] == 'state']['name'].unique()))
print()

# 2. Unique states in master dataset
print("Unique states in Master dataset:")
print(df_master['state'].nunique())
print(df_master['state'].unique())
print()


# ====================================
# EXTRACT STATE DATA FROM CENSUS DATA
# ====================================

# df_census = pd.read_csv("data/external/census_data.csv")
# df_census_state = df_census[df_census['level'] == 'state']
# # df_state = df[df['level'].str.lower() == 'state']

# # df_state.to_csv("census_data_state_scope.csv", index=False)