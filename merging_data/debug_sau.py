import pandas as pd

# Load your SAU file and check structure
sau_df = pd.read_csv('data/sau.csv')  # Your actual SAU file

print("🔍 SAU Dataset Debug:")
print(f"Shape: {sau_df.shape}")
print(f"\n📋 First 3 rows:")
print(sau_df.head(3))
print(f"\n📋 Column names:")
print(list(sau_df.columns))
print(f"\n🔢 Data types:")
print(sau_df.dtypes)
print(f"\n📊 Sample values for potential year columns:")
for col in sau_df.columns:
    if sau_df[col].dtype in ['int64', 'float64'] and sau_df[col].min() < 2100 and sau_df[col].max() > 1900:
        print(f"  {col}: {sau_df[col].min()} - {sau_df[col].max()} (possible year)")