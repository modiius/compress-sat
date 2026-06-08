
import matplotlib.pyplot as plt

def plot(float_data, int_data, labels):
    _, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    for i, series in enumerate(float_data):
        ax1.plot(series, label=labels[i])
    ax1.set_title("DW Probabilities: Original")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Probability (0-1)")
    ax1.legend()
    ax1.grid(True)

    for i, series in enumerate(int_data):
        ax2.plot(series, label=labels[i])
    ax2.set_title("DW Probabilities: Decompressed")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Probability (0-100)")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()