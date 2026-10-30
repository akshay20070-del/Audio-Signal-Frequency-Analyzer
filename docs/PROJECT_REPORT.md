# Project Report

## Audio Signal and Frequency Analyzer Using Python

**Department of Electronics and Communication Engineering**  
**ECE Mini-Project – Software-Based Signal Analysis**  
**October 2024**

---

## Table of Contents

1. [Abstract](#abstract)
2. [Introduction](#introduction)
3. [Problem Statement](#problem-statement)
4. [Objectives](#objectives)
5. [Existing System](#existing-system)
6. [Proposed System](#proposed-system)
7. [System Architecture](#system-architecture)
8. [Software Requirements](#software-requirements)
9. [Methodology](#methodology)
10. [Time-Domain Analysis](#time-domain-analysis)
11. [Frequency-Domain Analysis](#frequency-domain-analysis)
12. [FFT Explanation](#fft-explanation)
13. [Implementation](#implementation)
14. [Testing](#testing)
15. [Results](#results)
16. [Applications](#applications)
17. [Limitations](#limitations)
18. [Future Scope](#future-scope)
19. [Conclusion](#conclusion)

---

## Abstract

This report describes the design and development of a **Python-based Audio Signal
and Frequency Analyzer** — a software-only ECE mini-project that enables students
to analyze audio signals without the need for physical laboratory equipment.

The system accepts WAV audio files or synthetically generated sine wave signals,
performs **time-domain** and **frequency-domain** analysis using **Fast Fourier
Transform (FFT)**, and displays interactive waveform and spectrum graphs.
Key signal parameters such as duration, sampling frequency, dominant frequency,
and amplitude statistics are computed and displayed in a clean graphical user interface.

The project is implemented in Python 3 using NumPy, SciPy, Matplotlib, and Tkinter,
and is fully executable on Windows, macOS, and Linux without any additional hardware.

---

## Introduction

Audio signals are **continuous-time, analog signals** in the real world. When recorded
digitally, they become **discrete-time sequences** represented as arrays of numerical
samples. Each sample captures the signal's amplitude at a specific point in time.

A digital audio signal is characterized by:

| Parameter | Description |
|---|---|
| **Sample Rate (fs)** | Number of samples recorded per second (e.g., 44100 Hz) |
| **Bit Depth** | Precision of each sample (e.g., 16-bit = 65536 levels) |
| **Duration** | Total length = Number of samples / Sample rate |
| **Channels** | Mono (1 channel) or Stereo (2 channels) |

Understanding what frequencies are present in an audio signal is crucial in
**signal processing**, **telecommunications**, **audio engineering**, and **speech analysis**.
The mathematical tool used to extract frequency information from a time-domain signal
is the **Fourier Transform** and its efficient implementation: the **FFT**.

---

## Problem Statement

Engineering students learning signal processing face several challenges:

1. **Access to equipment:** Spectrum analyzers and oscilloscopes are expensive.
2. **Abstraction gap:** FFT formulas in textbooks are difficult to connect to real signals.
3. **Lack of interactive tools:** Static textbook examples do not allow experimentation.

This project addresses all three challenges by providing a **free, interactive,
desktop software tool** that performs real signal analysis using Python.

---

## Objectives

The project has the following specific objectives:

1. Accept WAV audio files as input and validate them.
2. Generate synthetic sine wave test signals for testing without audio files.
3. Perform time-domain analysis: compute duration, max/min amplitude, and RMS value.
4. Apply FFT to compute the frequency-domain representation.
5. Identify the dominant (strongest) frequency component.
6. Display both waveform and frequency spectrum as interactive Matplotlib graphs.
7. Provide a user-friendly GUI using Tkinter.
8. Export signal analysis reports to text files.

---

## Existing System

Traditional audio signal analysis tools include:

| Tool | Type | Cost | Limitations |
|---|---|---|---|
| Oscilloscope | Hardware | High | Lab access required |
| Spectrum Analyzer | Hardware | Very High | Expensive, complex |
| MATLAB Signal Toolbox | Software | High | Paid license |
| Audacity | Software | Free | Limited analysis data |
| LabVIEW | Software | High | Paid, complex |

**Limitations of existing systems:**
- Most hardware tools are inaccessible outside laboratory environments
- MATLAB is expensive for individual students
- Simple audio editors (e.g., Audacity) lack detailed numerical analysis
- None provide a beginner-friendly educational FFT visualization tool

---

## Proposed System

The proposed system is a **Python-based desktop application** that:

- Runs on any computer without special hardware
- Is completely **free and open-source**
- Provides **real-time visual feedback** through interactive graphs
- Is **beginner-friendly** with a clean GUI and helpful error messages
- Demonstrates actual ECE concepts: sampling theorem, FFT, frequency spectrum

**System Highlights:**

```
Input:   WAV file  OR  Synthetic sine wave
Process: Time-domain analysis + FFT frequency analysis
Output:  Waveform graph + Spectrum graph + Exported report
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     main.py (GUI Controller)                 │
│                  Tkinter Application Window                  │
└──────┬──────────────┬───────────────┬───────────────────────┘
       │              │               │
       ▼              ▼               ▼
┌─────────────┐ ┌──────────────┐ ┌──────────────────────────┐
│audio_loader │ │signal_       │ │frequency_analyzer.py     │
│.py          │ │processor.py  │ │                          │
│─────────────│ │──────────────│ │ FFT using numpy.fft.fft  │
│ Load WAV    │ │ Time axis    │ │ Magnitude spectrum        │
│ Generate    │ │ Duration     │ │ Frequency axis            │
│ test signal │ │ Max/Min/RMS  │ │ Dominant frequency        │
└──────┬──────┘ └──────┬───────┘ └────────────┬─────────────┘
       │               │                        │
       └───────────────┴────────────┬───────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  visualization.py   │
                         │  Matplotlib Graphs  │
                         │  embedded in TkAgg  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Report Export     │
                         │   (.txt file)       │
                         └─────────────────────┘
```

---

## Software Requirements

| Component | Specification |
|---|---|
| Programming Language | Python 3.8 or higher |
| GUI Framework | Tkinter (built into Python) |
| Numerical Library | NumPy ≥ 1.24.0 |
| Scientific Library | SciPy ≥ 1.10.0 |
| Visualization | Matplotlib ≥ 3.7.0 |
| Operating System | Windows 10/11, macOS 11+, Ubuntu 20.04+ |
| Minimum RAM | 512 MB |
| Disk Space | ~200 MB (including Python installation) |

---

## Methodology

The project follows a structured signal processing pipeline:

```
Step 1: INPUT
   ├── Load WAV file (scipy.io.wavfile.read)
   └── Generate synthetic signal (numpy.sin)

Step 2: PRE-PROCESSING
   ├── Convert stereo to mono (average channels)
   ├── Normalize amplitude to [-1.0, 1.0]
   └── Validate file format and data integrity

Step 3: TIME-DOMAIN ANALYSIS
   ├── Build time axis: t[n] = n / sample_rate
   ├── Compute max amplitude = max(x)
   ├── Compute min amplitude = min(x)
   └── Compute RMS = sqrt(mean(x²))

Step 4: FREQUENCY-DOMAIN ANALYSIS
   ├── Apply FFT: X = numpy.fft.fft(x)
   ├── Compute magnitude: |X(k)| = abs(X) * 2/N
   ├── Build one-sided spectrum (0 to Nyquist)
   └── Find dominant frequency (argmax of |X|, excluding DC)

Step 5: VISUALIZATION
   ├── Plot time-domain waveform (amplitude vs. time)
   └── Plot frequency spectrum (magnitude vs. frequency)

Step 6: REPORT (optional)
   └── Export analysis results to .txt file
```

---

## Time-Domain Analysis

Time-domain analysis examines how the signal amplitude varies with time.

### Key Formulas

| Measurement | Formula | Description |
|---|---|---|
| Time axis | `t[n] = n / fs` | Converts sample index to seconds |
| Duration | `T = N / fs` | Total signal length in seconds |
| Max amplitude | `A_max = max(x[n])` | Peak positive value |
| Min amplitude | `A_min = min(x[n])` | Peak negative value |
| RMS amplitude | `A_rms = √(Σx²/N)` | Effective signal level |

Where:
- `n` = sample index
- `fs` = sampling frequency (Hz)
- `N` = total number of samples
- `x[n]` = signal amplitude at sample `n`

### Implementation

```python
# From signal_processor.py

# Build time axis
time_axis = np.linspace(0, duration, num_samples, endpoint=False)

# Amplitude statistics
max_amplitude = float(np.max(signal))
min_amplitude = float(np.min(signal))
rms_amplitude = float(np.sqrt(np.mean(signal ** 2)))
```

---

## Frequency-Domain Analysis

Frequency-domain analysis shows which frequencies are present in the signal
and their relative strengths (magnitudes).

### What is the Frequency Domain?

- In the **time domain:** We see how amplitude changes over time.
- In the **frequency domain:** We see how much energy exists at each frequency.

For example, a pure 440 Hz sine wave has:
- Time domain: A smooth sinusoidal curve
- Frequency domain: A single sharp peak at 440 Hz

A musical chord (multiple notes) would have:
- Time domain: A complex irregular waveform
- Frequency domain: Multiple peaks — one at each note's frequency

---

## FFT Explanation

### What is FFT?

The **Fast Fourier Transform (FFT)** is an efficient algorithm to compute the
**Discrete Fourier Transform (DFT)**.

### Mathematical Formula

$$X(k) = \sum_{n=0}^{N-1} x(n) \cdot e^{-j \cdot 2\pi k n / N}$$

### Term-by-Term Explanation

| Symbol | Meaning |
|---|---|
| `x(n)` | Signal amplitude at time step `n` (input) |
| `X(k)` | Complex frequency component at bin `k` (output) |
| `N` | Total number of samples |
| `k` | Frequency bin index (0 to N-1) |
| `n` | Time sample index (0 to N-1) |
| `j` | Imaginary unit: `j = √(-1)` |
| `e^(-j·2π·k·n/N)` | Complex sinusoid at frequency `k/N` |

### In Simple Language

The FFT:
1. **Takes** the audio signal (an array of numbers) as input.
2. **Computes** how much of each possible frequency is present.
3. **Outputs** an array of complex numbers — one per frequency bin.
4. The **magnitude** (absolute value) of each output tells the **strength** of that frequency.

### One-Sided Spectrum

For real-valued signals (all audio signals), the FFT output is symmetric.
Only the **first half** (0 Hz to Nyquist frequency) carries unique information.

```
Nyquist Frequency = Sample Rate / 2
Example: 44100 Hz sample rate → Nyquist = 22050 Hz
```

### Implementation

```python
# From frequency_analyzer.py

# Step 1: Apply FFT
fft_result = np.fft.fft(signal)

# Step 2: Compute normalized magnitude
magnitude = (2.0 / num_samples) * np.abs(fft_result)

# Step 3: Take one-sided spectrum
half_n = num_samples // 2
magnitude = magnitude[:half_n]

# Step 4: Build frequency axis
frequencies = np.fft.fftfreq(num_samples, d=1.0/sample_rate)[:half_n]

# Step 5: Find dominant frequency (skip DC at index 0)
dominant_index = np.argmax(magnitude[1:]) + 1
dominant_frequency = frequencies[dominant_index]
```

---

## Implementation

### Module Breakdown

#### `audio_loader.py`
- `load_audio_file(path)` — Reads WAV files using `scipy.io.wavfile`
- `generate_test_signal(frequency, duration, sample_rate, noise_level)` — Creates synthetic sine waves

#### `signal_processor.py`
- `analyze_time_domain(audio_data)` — Computes duration, amplitude statistics, time axis

#### `frequency_analyzer.py`
- `analyze_frequency_domain(audio_data)` — Applies FFT, computes spectrum, finds dominant frequency

#### `visualization.py`
- `create_figure(parent_frame)` — Creates Matplotlib figure embedded in Tkinter
- `plot_time_domain(ax, time_result)` — Draws waveform graph
- `plot_frequency_domain(ax, freq_result, max_freq_hz)` — Draws spectrum graph
- `refresh_canvas(canvas, fig)` — Updates the display

#### `main.py`
- `AudioAnalyzerApp` class — Main Tkinter application
- Buttons: Upload Audio, Analyze Signal, Generate Test Signal, Export Report, Reset
- Info panel with all signal parameters
- Frequency limit slider for spectrum zoom

---

## Testing

### Test Cases

| Test Case | Input | Expected Result | Status |
|---|---|---|---|
| TC-01 | 440 Hz sine wave, 2 s, 44100 Hz | Dominant freq ≈ 440 Hz | ✅ Pass |
| TC-02 | 1000 Hz sine wave, 1 s, 44100 Hz | Dominant freq ≈ 1000 Hz | ✅ Pass |
| TC-03 | Valid WAV file | File loads, info displayed | ✅ Pass |
| TC-04 | Invalid file (e.g., .mp3) | Error message displayed | ✅ Pass |
| TC-05 | Non-existent file | FileNotFoundError shown | ✅ Pass |
| TC-06 | Stereo WAV file | Converted to mono | ✅ Pass |
| TC-07 | Export report after analysis | .txt file saved | ✅ Pass |
| TC-08 | Reset button | All fields cleared, graphs reset | ✅ Pass |
| TC-09 | Frequency slider at 2000 Hz | Spectrum zoomed to 0–2000 Hz | ✅ Pass |
| TC-10 | Analyze without loading | Warning message shown | ✅ Pass |

---

## Results

### Test Signal – 440 Hz Sine Wave (2 seconds, 44100 Hz)

| Parameter | Value |
|---|---|
| Duration | 2.0000 seconds |
| Sample Rate | 44,100 Hz |
| Number of Samples | 88,200 |
| Max Amplitude | ~1.0000 |
| Min Amplitude | ~-1.0000 |
| RMS Amplitude | ~0.7071 |
| Dominant Frequency | ~440.00 Hz |

**Observation:**  
The FFT correctly identifies 440 Hz as the dominant frequency.  
The RMS value of ≈ 0.707 matches the theoretical value for a sine wave (1/√2 ≈ 0.7071).

### Time-Domain Result
- A clean sinusoidal curve is visible in the waveform graph.

### Frequency-Domain Result
- A single sharp peak appears at 440 Hz in the spectrum graph.
- All other frequencies have near-zero magnitude.

---

## Applications

| Domain | Application |
|---|---|
| **Education** | Teaching FFT and signal analysis to ECE students |
| **Audio Engineering** | Identifying frequency components in music/speech |
| **Noise Analysis** | Finding dominant noise frequencies in industrial signals |
| **Music Technology** | Detecting pitch, note frequency, and tuning |
| **Speech Processing** | Analysing voice frequency characteristics |
| **Biomedical** | Audio-based health signal monitoring (e.g., heart sounds) |
| **Telecommunications** | Understanding signal bandwidth and frequency allocation |

---

## Limitations

1. **File Format:** Only WAV (PCM) format is supported. MP3, FLAC, OGG, etc. require additional libraries.
2. **Mono Conversion:** Stereo audio is averaged to mono; stereo channel separation is not displayed.
3. **No Live Input:** The microphone cannot be used in real-time (requires additional library such as PyAudio).
4. **FFT Resolution:** Frequency resolution = Sample Rate / N. Short signals have coarser resolution.
5. **Large Files:** Audio files longer than a few minutes may be slow to process.
6. **No Filtering:** The application does not implement digital filters (low-pass, high-pass, band-pass).
7. **No Spectrogram:** Time-varying frequency content (spectrogram) is not currently visualized.

---

## Future Scope

1. **MP3/FLAC Support** — Add `pydub` or `librosa` for multi-format audio loading.
2. **Live Microphone Input** — Real-time FFT using `PyAudio` and `sounddevice`.
3. **Spectrogram Display** — Time-frequency heatmap using `librosa.display.specshow`.
4. **Digital Filters** — Implement FIR/IIR filters using `scipy.signal`.
5. **Musical Note Detection** — Map dominant frequency to musical note names.
6. **Graph Export** — Save waveform and spectrum as PNG images.
7. **Batch Processing** — Analyze multiple WAV files at once.
8. **THD Analysis** — Calculate Total Harmonic Distortion for audio quality testing.
9. **Phase Spectrum** — Display phase angle vs. frequency in addition to magnitude.
10. **Cross-Platform Mobile App** — Port to Android using Kivy.

---

## Conclusion

The **Audio Signal and Frequency Analyzer** successfully achieves all its stated objectives.
The application provides a functional, beginner-friendly, software-based tool for
performing audio signal analysis — a fundamental topic in Electronics and Communication
Engineering.

Key achievements:
- A working Python GUI application with WAV file loading and test signal generation
- Correct implementation of FFT-based frequency analysis
- Clear visualization of both time-domain and frequency-domain representations
- Identification of dominant frequency with high accuracy for pure sine waves
- A clean, professional dark-mode interface using Tkinter and Matplotlib
- Export functionality for analysis reports

The project demonstrates that powerful signal processing can be performed with
**zero hardware cost** using free Python libraries, making ECE concepts more
accessible to students worldwide.

The modular code design (separate files for loading, processing, analysis, and
visualization) makes the project easy to understand, maintain, and extend in the future.

---

*End of Report*

---

**Project:** Audio Signal and Frequency Analyzer Using Python  
**Type:** ECE Software Mini-Project  
**Tools:** Python 3, NumPy, SciPy, Matplotlib, Tkinter  
**License:** MIT
