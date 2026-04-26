import pandas as pd
import json
import os

# Create directory if it doesn't exist
os.makedirs('static/data', exist_ok=True)

# Read Excel
df = pd.read_excel('assets/mata kuliah.xlsx')

# Clean columns (strip whitespace)
df.columns = [col.strip() for col in df.columns]

# Print columns for debugging
print('Columns found:', df.columns.tolist())

# Convert to dictionary
data = df.to_dict(orient='records')

# Save to JSON
with open('static/data/mata_kuliah.json', 'w') as f:
    json.dump(data, f, indent=4)

print('Successfully saved data to static/data/mata_kuliah.json')
