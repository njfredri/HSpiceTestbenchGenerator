import pandas as pd
import re
import sys

def convert_tr0_to_csv(input_file, output_file):
    """Converts an HSPICE .tr0 plaintext file to CSV format."""
    with open(input_file, "r") as f:
        lines = f.readlines()

    data = []
    headers = []
    collecting_data = False

    # Improved regex for numbers, including scientific notation
    number_pattern = re.compile(r"[-+]?\d*\.\d+(?:[Ee][-+]?\d+)?|\b\d+\b")

    for line in lines:
        line = line.strip()

        # Skip metadata and locate the header
        if not collecting_data:
            if "TIME" in line:  # Detect header row (modify if needed)
                headers = re.split(r'\s+', line.strip())  # Extract headers
                collecting_data = True  # Start collecting numerical data after this
            continue  # Skip other metadata

        # Extract valid numerical values
        values = number_pattern.findall(line)
        if values:
            try:
                data.append([float(v) for v in values])
            except ValueError:
                print(f"Skipping invalid data line: {line}")

    if not headers or not data:
        print("Error: No valid data found in the .tr0 file.")
        return

    # Ensure correct number of columns
    if len(headers) != len(data[0]):
        print("Warning: Number of headers and data columns do not match. Adjusting...")
        headers = ["Column_" + str(i) for i in range(len(data[0]))]  # Generic column names

    # Convert to Pandas DataFrame and save as CSV
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(output_file, index=False)
    print(f"Converted and saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python tr0_to_csv.py input.tr0 output.csv")
        sys.exit(1)

    input_tr0 = sys.argv[1]
    output_csv = sys.argv[2]

    convert_tr0_to_csv(input_tr0, output_csv)
