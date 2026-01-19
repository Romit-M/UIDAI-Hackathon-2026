import pandas as pd

# Load files
df_master = pd.read_csv("master_dataset.csv")
df_census = pd.read_csv("census_data.csv")

# NORMALIZE DISTRICTS

# # 1. Get unique districts from both
# master_districts = set(df_master['district'].astype(str).unique())
# census_districts = set(df_census['name'].astype(str).unique())

# # 2. Districts in Master but MISSING in Census
# missing_in_census = master_districts - census_districts

# # 3. Districts in Census but NOT in Master
# missing_in_master = census_districts - master_districts

# # 4. Print Results
# print(f"Count in Master: {len(master_districts)}")
# print(f"Count in Census: {len(census_districts)}")
# print("-" * 30)


# NORMALIZE STATES  

# 1. Get unique districts from both
# master_districts = set(df_master['district'].astype(str).unique())
# census_districts = set(df_census['name'].astype(str).unique())

# # 2. Districts in Master but MISSING in Census
# missing_in_census = master_districts - census_districts

# # 3. Districts in Census but NOT in Master
# missing_in_master = census_districts - master_districts

# # 4. Print Results
# print(f"Count in Master: {len(master_districts)}")
# print(f"Count in Census: {len(census_districts)}")
# print("-" * 30)

# print(f"Districts in Master NOT found in Census ({len(missing_in_census)}):")
# print(sorted(list(missing_in_census)))

# print(f"\nDistricts in Census NOT found in Master ({len(missing_in_master)}):")
# print(sorted(list(missing_in_master)))