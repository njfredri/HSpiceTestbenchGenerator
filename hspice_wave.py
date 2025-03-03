import numpy as np
import matplotlib.pyplot as plt

def read_hspice_tr0(filename):
    """
    Reads an HSPICE ASCII .tr0 file and extracts time and voltage data.
    """
    time = []
    signals = {}
    with open(filename, "r") as f:
        lines = f.readlines()
        
        for line in lines:
            data = line.strip().split()
            if len(data) < 2:
                continue

            try:
                t = float(data[0])  # First column is time
                values = list(map(float, data[1:]))  # Remaining columns are signal values
                
                time.append(t)
                
                # Store signal values
                for i, val in enumerate(values):
                    signal_name = f"Signal_{i+1}"
                    if signal_name not in signals:
                        signals[signal_name] = []
                    signals[signal_name].append(val)

            except ValueError:
                continue  # Skip lines that don't contain numerical data

    return np.array(time), signals

def plot_hspice_waveform(filename):
    """
    Plots the extracted waveform from the HSPICE .tr0 file.
    """
    time, signals = read_hspice_tr0(filename)

    plt.figure(figsize=(10, 5))
    
    for signal_name, values in signals.items():
        plt.plot(time * 1e9, values, label=signal_name)  # Convert time to ns
    
    plt.xlabel("Time (ns)")
    plt.ylabel("Voltage (V)")
    plt.title("HSPICE Simulation Waveform")
    plt.legend()
    plt.grid()
    plt.show()


# Run the script with your HSPICE output file
plot_hspice_waveform("tb.tr0")
