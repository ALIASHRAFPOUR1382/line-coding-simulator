import numpy as np
import matplotlib.pyplot as plt

def nrz(bits):
    """Non-Return-to-Zero (NRZ) line coding."""
    signal = [1 if bit == 1 else -1 for bit in bits]
    return signal

def nrzi(bits):
    """Non-Return-to-Zero Inverted (NRZI) line coding."""
    signal = []
    current_level = -1
    for bit in bits:
        if bit == 1:
            current_level *= -1
        signal.append(current_level)
    return signal

def rz(bits):
    """Return-to-Zero (RZ) line coding."""
    signal = []
    for bit in bits:
        signal.extend([1, 0] if bit == 1 else [-1, 0])
    return signal

def manchester(bits):
    """Manchester line coding."""
    signal = []
    for bit in bits:
        signal.extend([1, -1] if bit == 0 else [-1, 1])
    return signal

def differential_manchester(bits):
    """Differential Manchester line coding."""
    signal = []
    current_level = 1
    for bit in bits:
        if bit == 0:
            current_level *= -1
            signal.extend([current_level, -current_level])
        else:
            signal.extend([current_level, -current_level])
    return signal

def ami(bits):
    """Alternate Mark Inversion (AMI) line coding."""
    signal = []
    last_positive = False
    for bit in bits:
        if bit == 1:
            level = 1 if not last_positive else -1
            signal.append(level)
            last_positive = not last_positive
        else:
            signal.append(0)
    return signal

def plot_all_signals(bits, bit_rate=1, sample_rate=100):
    """Plots all line coding signals together."""
    time_per_bit = 1 / bit_rate
    num_bits = len(bits)
    time = np.linspace(0, num_bits * time_per_bit, num_bits * sample_rate, endpoint=False)

    fig, axs = plt.subplots(6, 1, figsize=(14, 10), sharex=True)
    fig.suptitle('Line Coding Techniques', fontsize=18)

    # Plot NRZ
    signal_nrz = nrz(bits)
    time_nrz = np.linspace(0, num_bits * time_per_bit, num_bits * sample_rate, endpoint=False)
    axs[0].plot(time_nrz, np.repeat(signal_nrz, sample_rate), linewidth=2)
    axs[0].set_title('Non-Return-to-Zero (NRZ)', fontsize=14)
    axs[0].set_ylabel('Voltage', fontsize=12)
    axs[0].set_yticks([-1, 1])
    axs[0].grid(True)

    # Plot NRZI
    signal_nrzi = nrzi(bits)
    time_nrzi = np.linspace(0, num_bits * time_per_bit, num_bits * sample_rate, endpoint=False)
    axs[1].plot(time_nrzi, np.repeat(signal_nrzi, sample_rate), linewidth=2)
    axs[1].set_title('Non-Return-to-Zero Inverted (NRZI)', fontsize=14)
    axs[1].set_ylabel('Voltage', fontsize=12)
    axs[1].set_yticks([-1, 1])
    axs[1].grid(True)

    # Plot RZ
    signal_rz = rz(bits)
    time_rz = np.linspace(0, num_bits * time_per_bit, len(signal_rz) * (sample_rate // 2), endpoint=False)
    axs[2].plot(time_rz, np.repeat(signal_rz, sample_rate // 2), linewidth=2)
    axs[2].set_title('Return-to-Zero (RZ)', fontsize=14)
    axs[2].set_ylabel('Voltage', fontsize=12)
    axs[2].set_yticks([-1, 0, 1])
    axs[2].grid(True)

    # Plot Manchester
    signal_manchester = manchester(bits)
    time_manchester = np.linspace(0, num_bits * time_per_bit, len(signal_manchester) * (sample_rate // 2), endpoint=False)
    axs[3].plot(time_manchester, np.repeat(signal_manchester, sample_rate // 2), linewidth=2)
    axs[3].set_title('Manchester', fontsize=14)
    axs[3].set_ylabel('Voltage', fontsize=12)
    axs[3].set_yticks([-1, 1])
    axs[3].grid(True)

    # Plot Differential Manchester
    signal_diff_manchester = differential_manchester(bits)
    time_diff_manchester = np.linspace(0, num_bits * time_per_bit, len(signal_diff_manchester) * (sample_rate // 2), endpoint=False)
    axs[4].plot(time_diff_manchester, np.repeat(signal_diff_manchester, sample_rate // 2), linewidth=2)
    axs[4].set_title('Differential Manchester', fontsize=14)
    axs[4].set_ylabel('Voltage', fontsize=12)
    axs[4].set_yticks([-1, 1])
    axs[4].grid(True)

    # Plot AMI
    signal_ami = ami(bits)
    time_ami = np.linspace(0, num_bits * time_per_bit, num_bits * sample_rate, endpoint=False)
    axs[5].plot(time_ami, np.repeat(signal_ami, sample_rate), linewidth=2)
    axs[5].set_title('Alternate Mark Inversion (AMI)', fontsize=14)
    axs[5].set_ylabel('Voltage', fontsize=12)
    axs[5].set_yticks([-1, 0, 1])
    axs[5].set_xlabel('Time (seconds)', fontsize=14)
    axs[5].grid(True)

    plt.xticks(np.arange(0, num_bits + 1, 1))
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    bits = [0, 1, 0, 0, 1, 1, 0, 1]
    print(f"Input bits: {bits}")
    plot_all_signals(bits)