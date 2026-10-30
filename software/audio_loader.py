"""
audio_loader.py
---------------
Handles loading audio files and generating test signals.
Supports WAV format using scipy.io.wavfile.
"""

import numpy as np
from scipy.io import wavfile
import os


def load_audio_file(file_path):
    """
    Load an audio file and return signal data.

    Parameters:
        file_path (str): Path to the audio file (.wav)

    Returns:
        dict: {
            'signal': numpy array of audio samples,
            'sample_rate': int (samples per second),
            'duration': float (duration in seconds),
            'filename': str (base name of file),
            'num_samples': int,
            'channels': int (1=mono, 2=stereo)
        }

    Raises:
        ValueError: If the file is unsupported or invalid.
        FileNotFoundError: If the file does not exist.
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Check file extension
    _, ext = os.path.splitext(file_path)
    if ext.lower() != ".wav":
        raise ValueError(
            f"Unsupported file format: '{ext}'. Only WAV files are supported."
        )

    try:
        # Read WAV file using scipy
        sample_rate, data = wavfile.read(file_path)
    except Exception as e:
        raise ValueError(f"Could not read audio file: {e}")

    # Convert stereo to mono by averaging channels
    if data.ndim == 2:
        # Stereo: average left and right channels
        signal = data.mean(axis=1)
        channels = 2
    else:
        # Already mono
        signal = data.astype(np.float64)
        channels = 1

    # Normalize signal to float in range [-1.0, 1.0]
    max_val = np.iinfo(data.dtype).max if np.issubdtype(data.dtype, np.integer) else 1.0
    signal = signal.astype(np.float64) / max_val

    num_samples = len(signal)
    duration = num_samples / sample_rate

    return {
        "signal": signal,
        "sample_rate": sample_rate,
        "duration": duration,
        "filename": os.path.basename(file_path),
        "num_samples": num_samples,
        "channels": channels,
    }


def generate_test_signal(frequency=440.0, duration=2.0, sample_rate=44100, noise_level=0.05):
    """
    Generate a synthetic sine-wave test signal.

    Parameters:
        frequency (float): Frequency of the sine wave in Hz (default: 440 Hz = musical note A4)
        duration (float): Duration of the signal in seconds (default: 2.0 s)
        sample_rate (int): Sampling rate in Hz (default: 44100)
        noise_level (float): Amount of Gaussian noise to add (default: 0.05)

    Returns:
        dict: Same structure as load_audio_file()
    """
    # Total number of samples
    num_samples = int(sample_rate * duration)

    # Create a time array: 0, 1/sr, 2/sr, ..., (N-1)/sr
    t = np.linspace(0, duration, num_samples, endpoint=False)

    # Generate sine wave: A * sin(2 * pi * f * t)
    signal = np.sin(2 * np.pi * frequency * t)

    # Add small amount of random noise to make it realistic
    if noise_level > 0:
        noise = noise_level * np.random.randn(num_samples)
        signal = signal + noise

    # Clip to valid range [-1, 1]
    signal = np.clip(signal, -1.0, 1.0)

    return {
        "signal": signal,
        "sample_rate": sample_rate,
        "duration": duration,
        "filename": f"test_signal_{int(frequency)}Hz.wav",
        "num_samples": num_samples,
        "channels": 1,
    }
