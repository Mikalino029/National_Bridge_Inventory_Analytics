import pandas as pd

# 1. Ingest the raw massive dataset
raw_path = r'C:/Users/hp/OneDrive/Desktop/Const_data/bridge_const_analytics/database/Last_Year_All_Field_Bridges.csv'
df = pd.read_csv(raw_path, low_memory=False)
print(f"📥 Initial Ingestion: Loaded {df.shape} bridge inspection records.")

# 2. Precision Deduplication (Sort by Year Built, keep the newest structural logs)
df = df.sort_values(by=['27 - Year Built'], ascending=True)
df = df.drop_duplicates(subset=['8 - Structure Number'], keep='last')
print(f"🧹 Deduplication Complete: {df.shape} unique structural rows remain.")

# 3. Clean and isolate critical columns (Including our brand new 43A and 43B fields!)
target_columns = {
    '8 - Structure Number': 'Bridge_ID',
    '1 - State Code': 'State_Code',
    '27 - Year Built': 'Year_Built',
    '29 - Average Daily Traffic': 'Daily_Traffic_Count',
    '43A - Main Span Material': 'Material_Type',
    '43B - Main Span Design': 'Design_Code',
    '58 - Deck Condition Rating': 'Deck_Condition',
    '59 - Superstructure Condition Rating': 'Superstructure_Condition',
    '60 - Substructure Condition Rating': 'Substructure_Condition'
}
df = df[list(target_columns.keys())].rename(columns=target_columns)

# 4. Standardize text entries and convert structural scores to numeric floats
for col in ['Deck_Condition', 'Superstructure_Condition', 'Substructure_Condition']:
    df[col] = df[col].astype(str).str.strip()
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 5. Smart Group Imputation (Fill missing scores with average of bridges built in the same decade)
df['Decade_Built'] = (df['Year_Built'] // 10) * 10
for col in ['Deck_Condition', 'Superstructure_Condition', 'Substructure_Condition']:
    df[col] = df.groupby('Decade_Built')[col].transform(lambda x: x.fillna(round(x.mean(), 0)))

# 6. FEATURE ENGINEERING: Calculate the Master Health Rating
df['Average_Condition_Score'] = round((df['Deck_Condition'] + df['Superstructure_Condition'] + df['Substructure_Condition']) / 3, 2)

# 7. FEATURE ENGINEERING: Create Maintenance Urgency Tiers (For Pie & Donut Charts)
def assign_urgency(score):
    if score <= 4.0:
        return "Critical Action Required"
    elif score <= 6.0:
        return "Routine Monitoring"
    else:
        return "Stable / Acceptable Health"

df['Maintenance_Urgency'] = df['Average_Condition_Score'].apply(assign_urgency)

# 8. FEATURE ENGINEERING: Clean and Standardize Material Descriptions
# Strip out dangerous inner commas that break CSV column alignments
df['Material_Type'] = df['Material_Type'].astype(str).str.replace(',', '', regex=False).str.strip()
df['Material_Type'] = df['Material_Type'].replace(['nan', 'None', ''], 'Other / Unknown')

# 9. FEATURE ENGINEERING: Group Bridges into Infrastructure Generations
def assign_generation(year):
    if year < 1960:
        return "1. Pre-1960 Historic"
    elif year < 1980:
        return "2. 1960 - 1970s Era"
    elif year < 1990:
        return "3. 1980s Era"
    elif year < 2000:
        return "4. 1990s Era"
    elif year < 2010:
        return "5. 2000s Era"
    else:
        return "6. 2010s Modern"

df['Infrastructure_Generation'] = df['Year_Built'].apply(assign_generation)

# 10. Export the newly enriched analytical file back to your database directory
output_path = r'C:/Users/hp/OneDrive/Desktop/Const_data/bridge_const_analytics/database/updated_bridge_logs.csv'
df.to_csv(output_path, index=False)
print("💾 Success! Your newly enriched pipeline dataset has been compiled and saved.")