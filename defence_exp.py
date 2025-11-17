import pandas as pd

# 1. Load the CSV with encoding fix
df = pd.read_csv(
    r"C:\Users\naman\OneDrive\Desktop\Naman Data Analytics\defence_per.csv",
    encoding='latin1'
)

# 2. Reshape into long format
df_long = df.melt(
    id_vars=["Country"],        # keep country as is
    var_name="Year",            # new column for year
    value_name="Percentage"     # rename to match the new dataset
)

# 3. Clean the Year column (remove "e" from 2024e, convert to int)
df_long["Year"] = df_long["Year"].str.replace("e", "", regex=False).astype(int)

# 4. Sort for readability
df_long = df_long.sort_values(by=["Country", "Year"])

# 5. Save reshaped file for later use
df_long.to_csv(
    r"C:\Users\naman\OneDrive\Desktop\Naman Data Analytics\defence_per_long.csv",
    index=False
)

print(df_long.head(20))
