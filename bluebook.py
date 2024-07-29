import pandas as pd

# Load the Excel file
file_path = 'tax.xlsx'
excel_data = pd.ExcelFile(file_path)

# Function to extract and structure data from a sheet
def extract_data(sheet_name):
    data = excel_data.parse(sheet_name)
    
    # Get column names dynamically
    columns = data.columns.tolist()
    
    structured_data = []
    
    # Iterate through the rows and extract relevant data
    for index, row in data.iterrows():
        row_data = {}
        for col in columns:
            row_data[col] = row[col] if not pd.isna(row[col]) else None
        structured_data.append(row_data)
    
    return structured_data

# Extract data from each sheet
insurance_data_structured = extract_data('Insurance')
koshi_data_structured = extract_data('Koshi')
madhesh_data_structured = extract_data('Madhesh')
lumbini_data_structured = extract_data('Lumbini')
bagmati_data_structured = extract_data('Bagmati')

# Combine all structured data
all_provinces_data = {
    "insurance": insurance_data_structured,
    "koshi": koshi_data_structured,
    "madhesh": madhesh_data_structured,
    "lumbini": lumbini_data_structured,
    "bagmati": bagmati_data_structured
}

# Convert the structured data to JSON
import json
json_data = json.dumps(all_provinces_data, indent=4)

# Save JSON data to a file
json_file_path = 'vehicle_tax_insurance_2081.json'
with open(json_file_path, 'w') as json_file:
    json_file.write(json_data)

# Print JSON data
print(json_data)
