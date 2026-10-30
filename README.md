# 🎵 Audio Signal and Frequency Analyzer Using Python

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-013243?style=for-the-badge&logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-11557c?style=for-the-badge)
![SciPy](https://img.shields.io/badge/SciPy-1.10%2B-8CAAE6?style=for-the-badge&logo=scipy)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A software-based ECE mini-project that analyzes audio signals,  
displays waveforms, and performs FFT frequency analysis.**

</div>

---

## 📋 Abstract

This project presents a **Python-based desktop application** for analyzing audio signals
in both the **time domain** and **frequency domain**. The application uses the
**Fast Fourier Transform (FFT)** algorithm to decompose audio signals into their
constituent frequency components. It provides an intuitive graphical user interface
built with **Tkinter** and displays professional visualizations using **Matplotlib**.

This is a **software-only** ECE mini-project. No hardware, Arduino, or physical
circuits are involved.

---

## 📖 Introduction

Audio signals are fundamental to Electronics and Communication Engineering.
Every sound we hear — speech, music, noise — is a **mixture of multiple frequency
components**. Analyzing these components allows engineers to understand, process,
and improve audio signals.

Traditionally, signal analysis requires expensive laboratory equipment such as
oscilloscopes and spectrum analyzers. This project demonstrates that the same
analysis can be performed using **free, open-source Python libraries** on any
modern computer.

The application allows engineering students to:
- Visualize audio signals as **waveforms** (amplitude vs. time)
- Analyze the **frequency content** of any audio signal (amplitude vs. frequency)
- Identify the **dominant frequency** component
- Apply and understand the **FFT algorithm** in practice

---

## ❓ Problem Statement

Analyzing audio signals requires:
1. Understanding both time-domain and frequency-domain representations
2. Applying mathematical transforms (FFT) to extract frequency information
3. Visualizing the results in a readable, interactive format

Existing laboratory tools are expensive and not always accessible to students.
This project provides a **free, beginner-friendly software alternative**.

---

## 🎯 Objectives

- [x] Build a graphical desktop application for audio signal analysis
- [x] Support WAV audio file upload and validation
- [x] Generate synthetic test signals (sine waves) for quick testing
- [x] Perform time-domain analysis (duration, amplitude statistics)
- [x] Apply Fast Fourier Transform (FFT) for frequency-domain analysis
- [x] Identify and display the dominant frequency
- [x] Visualize waveform and frequency spectrum using Matplotlib
- [x] Export signal analysis reports as text files

---

## ✨ Features

| Feature | Description |
|---|---|
| 📂 **WAV File Upload** | Load and validate WAV audio files |
| 🎛️ **Test Signal Generator** | Create sine waves with configurable frequency, duration, and noise |
| 📊 **Time-Domain Graph** | View amplitude vs. time waveform |
| 📈 **Frequency Spectrum** | View magnitude vs. frequency (FFT output) |
| 🔍 **Dominant Frequency** | Automatically identifies the strongest frequency |
| 📋 **Signal Info Panel** | Duration, sample rate, samples, max/min/RMS amplitude |
| 🎚️ **Frequency Limit Slider** | Zoom into any frequency range of the spectrum |
| 📄 **Report Export** | Save a complete analysis report as a `.txt` file |
| 🔄 **Reset** | Clear everything and start a new analysis |
| 🌙 **Dark Blue Theme** | Professional dark-mode GUI |

---

## 🛠️ Technologies Used

| Technology | Version | Purpose |
|---|---|---|
| **Python** | 3.8+ | Core programming language |
| **Tkinter** | Built-in | GUI framework |
| **NumPy** | ≥1.24 | Array operations, FFT computation |
| **SciPy** | ≥1.10 | WAV file reading (`scipy.io.wavfile`) |
| **Matplotlib** | ≥3.7 | Signal visualization (embedded in Tkinter) |

---

## 📐 Signal Processing Concepts

### 1. Time-Domain Analysis

The signal is represented as **amplitude (voltage) vs. time**.  
Key measurements:
- **Duration** = Number of samples ÷ Sampling rate
- **Max Amplitude** = Peak positive value
- **Min Amplitude** = Peak negative value  
- **RMS** = √(mean(x²)) — represents average signal power

### 2. Fast Fourier Transform (FFT)

The FFT converts a time-domain signal into its frequency components.

**Formula:**

$$X(k) = \sum_{n=0}^{N-1} x(n) \cdot e^{-j \cdot 2\pi \cdot k \cdot n / N}$$

**In simple terms:**
- `x(n)` = audio sample at time index `n`
- `X(k)` = how much of frequency `f = k × (sample_rate / N)` is in the signal
- `N` = total number of samples
- The output magnitude `|X(k)|` tells us the strength of each frequency

### 3. Dominant Frequency

The frequency with the **highest FFT magnitude** (excluding DC at 0 Hz).

### 4. Nyquist Theorem

The maximum detectable frequency = **Sample Rate / 2**.  
At 44100 Hz sampling rate → maximum detectable frequency = 22050 Hz.

---

## 🔄 System Workflow

```
User Action
    │
    ▼
┌─────────────────┐    ┌──────────────────┐
│  Upload WAV     │ or │  Generate Test   │
│  audio_loader   │    │  Sine Wave       │
└────────┬────────┘    └────────┬─────────┘
         │                      │
         └──────────┬───────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │  signal_processor.py │
         │  Time-Domain Analysis│
         │  (duration, amplitude│
         │   max, min, RMS)     │
         └──────────┬───────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │ frequency_analyzer.py│
         │ FFT Analysis         │
         │ (spectrum, dominant  │
         │  frequency)          │
         └──────────┬───────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │  visualization.py    │
         │  Matplotlib Graphs   │
         │  Time + Frequency    │
         └──────────┬───────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │  Report Export       │
         │  (optional .txt)     │
         └──────────────────────┘
```

---

## 💻 Software Requirements

| Component | Requirement |
|---|---|
| Operating System | Windows 10/11, macOS 11+, Ubuntu 20.04+ |
| Python | 3.8 or higher |
| RAM | 512 MB minimum (1 GB recommended) |
| Disk Space | ~100 MB (including Python + packages) |
| Display | 1280×720 minimum resolution |

---

## 📦 Installation

### Step 1 – Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Audio-Signal-Frequency-Analyzer.git
cd Audio-Signal-Frequency-Analyzer
```

### Step 2 – Install Dependencies

```bash
cd software
pip install -r requirements.txt
```

### Step 3 – Run the Application

```bash
python main.py
```

---

## ▶️ Execution

```bash
# Navigate to software folder
cd Audio-Signal-Frequency-Analyzer/software

# Run the application
python main.py
```

The application window will open. Then:
1. Click **Upload Audio** to load a WAV file, **or**
2. Click **Generate Test Signal** to create a sine wave
3. Click **Analyze Signal** to process and view graphs
4. Optionally click **Export Report** to save results

---

## 📸 Screenshots

> *Add screenshots to `software/screenshots/` and update these paths.*

| Main Window | Signal Analysis |
|---|---|
| *(Add screenshot here)* | *(Add screenshot here)* |

---

## 📊 Expected Results

| Test | Expected Output |
|---|---|
| 440 Hz sine wave | Dominant frequency ≈ 440 Hz |
| 1000 Hz sine wave | Dominant frequency ≈ 1000 Hz |
| 2-second signal @ 44100 Hz | Duration = 2.0 s, Samples = 88200 |
| Pure sine wave | Clean single peak in frequency spectrum |

---

## 🌍 Applications

- **ECE Education:** Teaching Fourier transforms and signal analysis
- **Audio Engineering:** Identifying frequency components in recordings
- **Noise Analysis:** Detecting dominant noise frequencies
- **Music Technology:** Analyzing pitch and tone content
- **Speech Processing:** Understanding frequency structure of voice
- **Quality Control:** Detecting abnormal frequencies in machinery audio

---

## ⚠️ Limitations

- Only **WAV format** is supported (no MP3, FLAC, OGG, etc.)
- **Multi-channel audio** is automatically converted to mono (averaging)
- FFT accuracy depends on **signal length** (longer = more accurate)
- The application does **not record live audio** from microphone
- Large audio files (>10 MB) may be slow to load

---

## 🚀 Future Enhancements

- [ ] Add MP3 / FLAC file support via `pydub` or `librosa`
- [ ] Live microphone recording and real-time FFT
- [ ] Spectrogram display (frequency vs. time heatmap)
- [ ] Band-pass / low-pass / high-pass filter implementation
- [ ] Musical note detection from frequency values
- [ ] Save graphs as PNG images
- [ ] Multi-channel (stereo) waveform display
- [ ] Batch analysis of multiple audio files

---

## 📝 Conclusion

The **Audio Signal and Frequency Analyzer** successfully demonstrates core ECE signal
processing concepts using free, open-source Python tools. By combining NumPy's FFT
implementation with Matplotlib visualizations in a Tkinter GUI, the project provides
an accessible educational tool for understanding audio signal analysis.

This project reinforces concepts such as the Fourier Transform, Nyquist theorem,
sampling rate, and frequency spectrum — all fundamental topics in Electronics and
Communication Engineering.

---

## 📁 Project Structure

```
Audio-Signal-Frequency-Analyzer/
├── README.md                    ← This file
├── LICENSE                      ← MIT License
├── .gitignore                   ← Git exclusions
│
├── software/
│   ├── README.md                ← Software usage guide
│   ├── requirements.txt         ← Python dependencies
│   ├── main.py                  ← Main application (GUI entry point)
│   ├── audio_loader.py          ← WAV loading + test signal generation
│   ├── signal_processor.py      ← Time-domain analysis
│   ├── frequency_analyzer.py    ← FFT frequency-domain analysis
│   ├── visualization.py         ← Matplotlib graphs
│   │
│   ├── samples/
│   │   └── README.md            ← Where to place WAV test files
│   │
│   └── screenshots/
│       └── README.md            ← Where to place app screenshots
│
└── docs/
    └── PROJECT_REPORT.md        ← Full academic project report
```

---

## 👩‍💻 Author

**ECE Mini-Project – 3rd Project**  
Department of Electronics and Communication Engineering  
Python 3 | NumPy | Matplotlib | SciPy | Tkinter

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
