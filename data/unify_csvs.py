import pandas as pd

# Load files (replace with your paths)
import os
base_dir = r"C:/Users/theha/OneDrive/Desktop/mantra"

incois_df = pd.read_csv(os.path.join(base_dir, "data/incois_cleaned.csv"))
cmfri_df = pd.read_csv(os.path.join(base_dir, "data/cmfri_landings.csv"))
occurrence_df = pd.read_csv(
    os.path.join(base_dir, "data/cmlre-platform/occurrence.txt"),
    sep="\t",   # tab-separated
    low_memory=False
)



# Parse year from occurrence.eventDate (handles ISO, YYYY, etc.)
def parse_year(date_str):
    if pd.isna(date_str) or not str(date_str).strip():
        return None
    date_str = str(date_str).strip()
    try:
        if 'T' in date_str:
            return int(date_str.split('-')[0])
        elif len(date_str) == 4 and date_str.isdigit():
            return int(date_str)
        elif '-' in date_str and len(date_str.split('-')) >= 2:
            return int(date_str.split('-')[0])
        elif '/' in date_str and len(date_str.split('/')) >= 2:
            return int(date_str.split('/')[-1])
        else:
            return None
    except:
        return None

occurrence_df['year'] = occurrence_df['eventDate'].apply(parse_year)
occurrence_df = occurrence_df[occurrence_df['year'].between(1996, 2011)]  # Filter common dates

# Group occurrence by year for count and species list
occurrence_grouped = occurrence_df.groupby('year').agg(
    occurrence_count=('id', 'count'),
    occurrence_species_list=('scientificName', lambda x: ', '.join(x.unique()[:5]))  # Limit to 5 for brevity
).reset_index()

# Pivot cmfri landings to wide format (years x resources)
cmfri_pivot = cmfri_df.pivot(index='Year', columns='Resource', values='Quantity_tonnes').fillna(0).reset_index()

# Merge cmfri and occurrence on year
unified_df = pd.merge(cmfri_pivot, occurrence_grouped, left_on='Year', right_on='year', how='left').drop('year', axis=1)
unified_df['occurrence_count'] = unified_df['occurrence_count'].fillna(0)
unified_df['occurrence_species_list'] = unified_df['occurrence_species_list'].fillna('No data')

# Parse start/end year from incois.Availability
def parse_start_year(avail_str):
    if pd.isna(avail_str) or not avail_str:
        return None
    avail_str = str(avail_str).strip()
    try:
        if ' - ' in avail_str:
            start = avail_str.split(' - ')[0].strip()
            if start.isdigit() and len(start) == 4:
                return int(start)
            elif '-' in start:
                return int(start.split('-')[-1])
        return None
    except:
        return None

def parse_end_year(avail_str):
    if pd.isna(avail_str) or not avail_str:
        return None
    avail_str = str(avail_str).strip()
    try:
        if 'till date' in avail_str:
            return 2025
        if ' - ' in avail_str:
            end = avail_str.split(' - ')[1].strip()
            if end.isdigit() and len(end) == 4:
                return int(end)
            elif '-' in end:
                return int(end.split('-')[-1])
        return None
    except:
        return None

incois_df['start_year'] = incois_df['Availability'].apply(parse_start_year)
incois_df['end_year'] = incois_df['Availability'].apply(parse_end_year)

# Add ocean_params to unified_df based on year range
def get_ocean_params(y):
    matching = incois_df[(incois_df['start_year'] <= y) & ((incois_df['end_year'] >= y) | incois_df['end_year'].isna())]
    return ', '.join(matching['Parameters'].dropna().unique()[:3])  # Limit to 3 for brevity

unified_df['ocean_params'] = unified_df['Year'].apply(get_ocean_params)

# Save to unified CSV
unified_df.to_csv('unified_marine_data.csv', index=False)
print("Unified CSV saved as 'unified_marine_data.csv'. Head:")
print(unified_df.head(10))