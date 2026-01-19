import pandas as pd

# 1. Load your file
df = pd.read_excel("2011-IndiaStateDist-0000.xlsx")

# 2. Define the two columns you want to clean
target_columns = ['Level', 'Name', 'TRU']

# 3. Apply the transformation
for col in target_columns:
    df[col] = (
        df[col]
        .astype(str)             # Ensure it's a string
        .str.lower()            # Convert to lowercase
        .str.replace(r'[^a-z0-9]', '', regex=True) # Remove everything EXCEPT letters and numbers
    )

# 4. Save the result
df.to_excel("census_data.xlsx", index=False)