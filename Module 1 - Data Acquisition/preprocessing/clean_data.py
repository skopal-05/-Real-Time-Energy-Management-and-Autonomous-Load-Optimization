import pandas as pd
from pathlib import Path

INPUT_FILE = Path("outputs/air_compressor.csv")
OUTPUT_FILE = Path("outputs/cleaned_data/air_compressor_cleaned.csv")

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully!\n")

print("First 5 rows:")
print(df.head())

print("\nShape of dataset:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nNumber of duplicate rows:")
print(df.duplicated().sum())

df = df.drop_duplicates()

print("\nShape after removing duplicates:")
print(df.shape)

# Standardize column names
df.columns = (
    df.columns
    .str.strip()        # Remove extra spaces
    .str.lower()        # Convert to lowercase
    .str.replace(" ", "_")  # Replace spaces with underscores
)

print("\nStandardized Column Names:")
print(df.columns.tolist())

# Convert timestamp column to datetime format
df["timestamp"] = pd.to_datetime(df["timestamp"])

print("\nTimestamp datatype:")
print(df["timestamp"].dtype)

# Display data types of all columns
print("\nData Types:")
print(df.dtypes)

# Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\nCleaned dataset saved successfully!")
print(f"Saved to: {OUTPUT_FILE}")