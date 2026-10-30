# Audio Signal and Frequency Analyzer – Software

## Overview

This folder contains the complete Python source code for the  
**Audio Signal and Frequency Analyzer** ECE mini-project.

The application is a **pure software** desktop tool built with:
- **Python 3** – core language
- **Tkinter** – graphical user interface
- **NumPy** – numerical signal processing
- **SciPy** – WAV file I/O
- **Matplotlib** – signal visualization

---

## Folder Contents

| File | Purpose |
|---|---|
| `main.py` | Entry point – builds and runs the GUI |
| `audio_loader.py` | Load WAV files / generate test sine waves |
| `signal_processor.py` | Time-domain analysis (amplitude, duration) |
| `frequency_analyzer.py` | FFT-based frequency-domain analysis |
| `visualization.py` | Matplotlib graphs embedded in Tkinter |
| `requirements.txt` | Python package dependencies |
| `samples/` | Folder to store sample WAV files |
| `screenshots/` | Application screenshots |

---

## Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Operating System: Windows / macOS / Linux

---

## Python Installation

Download and install Python from [python.org](https://www.python.org/downloads/).

> Make sure to tick **"Add Python to PATH"** during installation on Windows.

Verify installation:

```bash
python --version
pip --version
```

---

## Dependency Installation

Open a terminal in the `software/` folder and run:

```bash
pip install -r requirements.txt
```

This installs numpy, scipy, and matplotlib.

---

## How to Run

```bash
cd software
python main.py
```

The application window will open immediately.

---

## How to Upload an Audio File

1. Click **📂 Upload Audio** in the left panel.
2. Select a `.wav` file from your computer.
3. A confirmation message will appear showing file details.
4. Click **🔬 Analyze Signal** to process and display the graphs.

> **Note:** Only WAV format is supported. Other formats will show an error.

---

## How to Analyze a Signal

1. Load an audio file **or** generate a test signal.
2. Click **🔬 Analyze Signal**.
3. The application will:
   - Display the **time-domain waveform** (left graph)
   - Display the **frequency spectrum** (right graph)
   - Update all info fields (duration, sample rate, dominant frequency, etc.)

---

## How to Generate a Test Signal

1. Click **🎛️ Generate Test Signal**.
2. A dialog box will appear. Enter:
   - **Frequency (Hz)**: e.g., 440 for musical note A4
   - **Duration (s)**: e.g., 2.0 seconds
   - **Sample Rate (Hz)**: e.g., 44100
   - **Noise Level**: 0.0 to 1.0 (0 = pure sine, 0.05 = slight noise)
3. Click **Generate Signal**.
4. Click **🔬 Analyze Signal** to view the graphs.

---

## How to Export a Report

1. Analyze a signal first.
2. Click **📄 Export Report**.
3. Choose a save location.
4. A `.txt` report file is saved containing:
   - File name
   - Duration, sample rate, number of samples
   - Max/min/RMS amplitude
   - Dominant frequency
   - Analysis timestamp

---

## Frequency Display Limit

Use the **slider** in the left panel to limit the frequency axis of the spectrum graph (e.g., 0–8000 Hz). This is useful for zooming into the region of interest.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `No module named tkinter` | On Linux: `sudo apt install python3-tk` |
| Graph area is blank | Click **Analyze Signal** after loading a file |
| File not loading | Ensure the file is a valid `.wav` file |
| App is slow on large files | Waveform is automatically downsampled for display |
| `Permission denied` when saving report | Choose a different folder (e.g., Desktop) |

---

## Tips

- Use **440 Hz** as a test frequency – it is the standard musical tuning note A4.
- Use **Reset** to clear everything and start a fresh analysis.
- The **dominant frequency** is the frequency with the highest FFT magnitude.
