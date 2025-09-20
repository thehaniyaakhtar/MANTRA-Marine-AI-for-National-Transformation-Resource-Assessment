import pandas as pd

# Load your raw SAU data
sau_raw = pd.read_csv('data/sau.csv')  # Your actual file path

print(f"Raw SAU shape: {sau_raw.shape}")
print(f"Years: {sau_raw['year'].min()} - {sau_raw['year'].max()}")
print(f"Unique scientific names: {sau_raw['scientific_name'].nunique()}")

# Filter to India EEZ only
sau_india = sau_raw[sau_raw['area_name'] == 'India (mainland)'].copy()
print(f"India EEZ only: {sau_india.shape}")

# Create CMLRE category mapping (scientific name → your categories)
cmlre_mapping = {
    # Oil Sardine
    'Sardinella longiceps': 'Oil sardine',
    'Sardinella gibbosa': 'Oil sardine',
    'Sardinella fimbriata': 'Oil sardine',
    
    # Hilsa Shad
    'Tenualosa ilisha': 'Hilsa shad',
    'Hilsa kelee': 'Hilsa shad',
    
    # Penaeid Prawns
    'Penaeus monodon': 'Penaeid prawns',
    'Penaeus indicus': 'Penaeid prawns',
    'Penaeus semisulcatus': 'Penaeid prawns',
    'Metapenaeus affinis': 'Penaeid prawns',
    
    # Non-penaeid Prawns
    'Metapenaeus dobsoni': 'Non-penaeid prawns',
    'Exopalaemon styliferus': 'Non-penaeid prawns',
    
    # Catfishes
    'Arius thalassinus': 'Catfishes',
    'Tachysurus dussumieri': 'Catfishes',
    
    # Eels
    'Muraenesox cinereus': 'Eels',
    
    # Sharks
    'Carcharhinus sorrah': 'Sharks',
    'Rhizoprionodon acutus': 'Sharks',
    
    # Rays
    'Rhinobatos schlegelii': 'Rays',
    'Glaucostegus granulatus': 'Rays',
    
    # Squids
    'Loligo duvaucelii': 'Squids',
    'Sepia pharaonis': 'Squids',
    
    # Other categories (add more as needed)
    'Polydactylus indicus': 'Threadfin breams',
    'Nemipterus japonicus': 'Threadfin breams',
    'Chanos chanos': 'Wolf herring',
    'Stolephorus indicus': 'Stolephorus',
    'Setipinna taty': 'Setipinna',
    'Coilia dussumieri': 'Coilia',
}

# Map scientific names to CMLRE categories
sau_india['cmlre_category'] = sau_india['scientific_name'].map(cmlre_mapping).fillna('Other')

# Aggregate by year and CMLRE category
print("\n🔄 Aggregating by year and species category...")
agg_data = sau_india.groupby(['year', 'cmlre_category'])['tonnes'].sum().reset_index()

# Pivot to match your original dataset structure
pivot_data = agg_data.pivot(index='year', columns='cmlre_category', values='tonnes').fillna(0)

# Define your original dataset's fish columns
target_columns = [
    'Catfishes', 'Coilia', 'Eels', 'Hilsa shad', 'Non-penaeid prawns',
    'Oil sardine', 'Other sardines', 'Penaeid prawns', 'Rays', 'Setipinna',
    'Sharks', 'Skates', 'Squids', 'Stolephorus', 'Threadfin breams', 'Wolf herring'
]

# Keep only the columns that match your original dataset
available_cols = [col for col in target_columns if col in pivot_data.columns]
print(f"Matched categories: {len(available_cols)}/{len(target_columns)}")

# Add missing columns as zeros
for col in target_columns:
    if col not in pivot_data.columns:
        pivot_data[col] = 0

# Reorder columns to match your original dataset
pivot_data = pivot_data[target_columns + [col for col in pivot_data.columns if col not in target_columns]]

# Add total catch
pivot_data['total_catch'] = pivot_data[target_columns].sum(axis=1)

# Reset index and rename
sau_processed = pivot_data.reset_index()
sau_processed = sau_processed.rename(columns={'year': 'Year'})

print(f"\n✅ Processed SAU Dataset:")
print(f"Shape: {sau_processed.shape}")
print(f"Years: {sau_processed['Year'].min()} - {sau_processed['Year'].max()}")

# Show sample
print("\n📊 Sample (2010):")
print(sau_processed[sau_processed['Year'] == 2010][target_columns[:5] + ['total_catch']].round(0))

# Save processed SAU data
sau_processed.to_csv('final.csv', index=False)
print(f"\n💾 Saved: final.csv")