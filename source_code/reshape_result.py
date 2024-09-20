import pandas as pd

# Load the Excel file
file_path = 'source_code/company_event_results.xlsx'
df = pd.read_excel(file_path)

# Pivot the data so that each unique 'Event Type' becomes a column
reshaped_df = df.pivot_table(index='Company Name', columns='Event Type', values='Result', aggfunc='first').reset_index()

# Save the reshaped data to a new Excel file
output_file = 'source_code/reshaped_company_event_results.xlsx'
reshaped_df.to_excel(output_file, index=False)
