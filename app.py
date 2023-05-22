# Import packages
from dash import Dash
import pandas as pd
import glob
import os

folder_path = "/Users/onkar/Desktop/Quantium Virtual Program/quantium-virtual-program/data"  # Replace with the actual folder path where the CSV files are located
file_pattern = "*.csv"

# Construct the full file paths by joining the folder path with the file pattern
file_paths = glob.glob(os.path.join(folder_path, file_pattern))
data_frames = []

for file_path in file_paths:
    df = pd.read_csv(file_path)
    data_frames.append(df)

combined_df = pd.concat(data_frames, ignore_index=True)

combined_df = combined_df[combined_df['product'] == 'pink morsel']

combined_df['sales'] = combined_df['price'].str.replace('$', '').astype(float) * combined_df['quantity']
combined_df = combined_df.drop(['product','price', 'quantity'], axis=1)

print(combined_df)

# Save the merged data frame to a new CSV file
output_file = "/Users/onkar/Desktop/Quantium Virtual Program/quantium-virtual-program/output.csv"  # Replace with the desired output file path
combined_df.to_csv(output_file, index=False)