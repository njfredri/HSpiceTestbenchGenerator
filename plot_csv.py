import pandas as pd
import matplotlib.pyplot as plt
import sys

def plot_csv(file_path):
    """Reads a CSV file and plots each column as a separate line."""
    try:
        # Load CSV
        df = pd.read_csv(file_path)

        # Plot each column
        plt.figure(figsize=(10, 6))
        for column in df.columns:
            plt.plot(df.index, df[column], label=column)  # x-axis = row number

        # Labels and title
        plt.xlabel("Time (Row Number)")
        plt.ylabel("Values")
        plt.title("CSV Data Plot")
        plt.legend()
        plt.grid(True)

        # Show plot
        plt.show()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python plot_csv.py data.csv")
        sys.exit(1)

    csv_file = sys.argv[1]
    plot_csv(csv_file)
