import pandas as pd

def save_to_arff(df, file_path, relation_name="data"):
    """
    Save a pandas DataFrame to an ARFF file.

    Parameters:
    - df: pandas DataFrame
    - file_path: Path to save the ARFF file
    - relation_name: Name of the ARFF relation
    """
    with open(file_path, "w") as f:
        # Write the relation name
        f.write(f"@RELATION {relation_name}\n\n")
        """
        # Write attribute information (generate generic attribute names)
        for i in range(len(df.columns)):
            f.write(f"@ATTRIBUTE attr{i} NUMERIC\n")
        """
        f.write("\n@DATA\n")
        
        # Write data
        for _, row in df.iterrows():
            f.write(",".join(map(str, row.values)) + "\n")

# Load the data (pure data, no headers)
input_file = "E:\Thesis\data\outfit.csv"  # Replace with the actual file path
df = pd.read_csv(input_file, header=None)  # Use `header=None` to avoid misinterpreting any row as headers

# Extract the first 500 rows
df_100 = df.head(500)

# Save to ARFF
output_file = "E:\\Thesis\\data\\outfit_sample.arff"  # Make sure the output file has the .arff extension
save_to_arff(df_100, output_file)
print(f"Saved the first 500 rows to {output_file}")
