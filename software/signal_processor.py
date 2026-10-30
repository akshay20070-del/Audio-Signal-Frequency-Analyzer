"""
signal_processor.py
--------------------
Performs time-domain signal analysis.

Extracts information like:
- Signal duration
- Number of samples
- Maximum and minimum amplitude
- Root Mean Square (RMS) amplitude
- Time axis for plotting
"""

import numpy as np


def analyze_time_domain(audio_data):
    """
    Perform time-domain analysis on the loaded audio signal.

    Parameters:
        audio_data (dict): Output from audio_loader.load_audio_file() or
                           audio_loader.generate_test_signal()

    Returns:
        dict: {
            'time_axis':    numpy array (time values in seconds),
            'signal':       numpy array (amplitude values),
            'duration':     float (total duration in seconds),
            'sample_rate':  int,
            'num_samples':  int,
            'max_amplitude': float,
            'min_amplitude': float,
            'rms_amplitude': float,
            'filename':     str
        }
    """
    signal      = audio_data["signal"]
    sample_rate = audio_data["sample_rate"]
    num_samples = audio_data["num_samples"]
    duration    = audio_data["duration"]

    # Build time axis: one time-stamp per sample
    # t[n] = n / sample_rate   (seconds)
    time_axis = np.linspace(0, duration, num_samples, endpoint=False)

    # Basic amplitude statistics
    max_amplitude = float(np.max(signal))
    min_amplitude = float(np.min(signal))

    # RMS = sqrt( mean( x^2 ) )  — measures average signal energy
    rms_amplitude = float(np.sqrt(np.mean(signal ** 2)))

    return {
        "time_axis":     time_axis,
        "signal":        signal,
        "duration":      duration,
        "sample_rate":   sample_rate,
        "num_samples":   num_samples,
        "max_amplitude": max_amplitude,
        "min_amplitude": min_amplitude,
        "rms_amplitude": rms_amplitude,
        "filename":      audio_data["filename"],
    }
