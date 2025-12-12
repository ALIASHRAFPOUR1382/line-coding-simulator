# Line Coding Techniques Simulator

A comprehensive Python tool for simulating and visualizing various line coding techniques used in digital communications. This project demonstrates how different binary data sequences are encoded into electrical signals for transmission over communication channels.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Supported Line Coding Techniques](#supported-line-coding-techniques)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Line Coding Techniques Explained](#line-coding-techniques-explained)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

Line coding is a fundamental concept in digital communications that converts binary data into electrical signals suitable for transmission. This simulator provides an educational tool to understand and compare different line coding schemes, each with its own advantages and use cases.

## ✨ Features

- **6 Different Line Coding Techniques**: Implementations of the most common line coding methods
- **Visual Comparison**: Side-by-side visualization of all techniques for easy comparison
- **Educational Tool**: Perfect for learning digital communications and signal encoding
- **Customizable Parameters**: Adjustable bit rate and sample rate for different scenarios
- **Clean Visualization**: Professional plots with clear labels and grid lines

## 🔧 Supported Line Coding Techniques

1. **NRZ (Non-Return-to-Zero)**: Simple binary encoding where 1 = high voltage, 0 = low voltage
2. **NRZI (Non-Return-to-Zero Inverted)**: Transition-based encoding where 1 = change level, 0 = maintain level
3. **RZ (Return-to-Zero)**: Each bit returns to zero level, providing clock recovery capability
4. **Manchester**: Self-clocking encoding with transition in the middle of each bit period
5. **Differential Manchester**: Similar to Manchester but with differential encoding
6. **AMI (Alternate Mark Inversion)**: Bipolar encoding where 1s alternate between positive and negative

## 📦 Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install numpy matplotlib
```

Or using requirements.txt:

```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Basic Usage

Run the script with default settings:

```bash
python Simulate_and_demonstrate_Line_Coding_techniques.py
```

### Custom Input Bits

Modify the `bits` array in the `__main__` section to test different binary sequences:

```python
if __name__ == "__main__":
    bits = [0, 1, 0, 0, 1, 1, 0, 1]  # Change this to your desired sequence
    print(f"Input bits: {bits}")
    plot_all_signals(bits)
```

### Custom Parameters

You can also adjust the bit rate and sample rate:

```python
plot_all_signals(bits, bit_rate=2, sample_rate=200)
```

- `bit_rate`: Number of bits per second (default: 1)
- `sample_rate`: Number of samples per bit period (default: 100)

## 📊 Examples

### Example 1: Default Binary Sequence

```python
bits = [0, 1, 0, 0, 1, 1, 0, 1]
plot_all_signals(bits)
```

This will generate a plot showing all 6 line coding techniques for the given binary sequence.

### Example 2: Using Individual Functions

You can also use individual encoding functions:

```python
bits = [1, 0, 1, 1, 0]
nrz_signal = nrz(bits)
manchester_signal = manchester(bits)
# Use the signals as needed
```

## 📚 Line Coding Techniques Explained

### NRZ (Non-Return-to-Zero)
- **Encoding**: 1 → +1V, 0 → -1V
- **Advantages**: Simple, bandwidth efficient
- **Disadvantages**: No clock recovery, DC component
- **Use Cases**: Short-distance communications

### NRZI (Non-Return-to-Zero Inverted)
- **Encoding**: 1 → transition, 0 → no transition
- **Advantages**: Better than NRZ for long sequences of zeros
- **Disadvantages**: Still has DC component issues
- **Use Cases**: USB, some network protocols

### RZ (Return-to-Zero)
- **Encoding**: Each bit returns to zero in the middle
- **Advantages**: Clock recovery possible, no DC component
- **Disadvantages**: Requires more bandwidth
- **Use Cases**: Optical communications

### Manchester
- **Encoding**: 0 → low-to-high transition, 1 → high-to-low transition (in middle of bit)
- **Advantages**: Self-clocking, no DC component
- **Disadvantages**: Requires twice the bandwidth
- **Use Cases**: Ethernet (10BASE-T), RFID

### Differential Manchester
- **Encoding**: Transition at start of bit period, 0 → additional transition in middle
- **Advantages**: Self-clocking, no DC component, better noise immunity
- **Disadvantages**: Complex encoding/decoding
- **Use Cases**: Token Ring networks

### AMI (Alternate Mark Inversion)
- **Encoding**: 0 → 0V, 1 → alternates between +1V and -1V
- **Advantages**: No DC component, error detection
- **Disadvantages**: Long sequences of zeros can cause clock recovery issues
- **Use Cases**: T1/E1 lines, ISDN

## 📋 Requirements

- `numpy` >= 1.19.0
- `matplotlib` >= 3.3.0

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Some ideas for improvements:

- Add more line coding techniques (e.g., 4B/5B, 8B/10B)
- Add decoding functions
- Add error analysis and comparison
- Improve visualization options
- Add unit tests

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

This project is designed for educational purposes to help students and engineers understand line coding techniques in digital communications.

---

**Note**: This simulator is intended for educational and demonstration purposes. For production use, consider using established communication libraries and protocols.

