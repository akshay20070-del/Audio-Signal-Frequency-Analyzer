"""
frequency_analyzer.py
----------------------
Performs frequency-domain analysis using Fast Fourier Transform (FFT).

FFT Formula:
    X(k) = Σ  x(n) * e^(-j * 2π * k * n / N)
            n=0 to N-1

  Where:
    x(n)  = input signal sample at index n
    X(k)  = complex frequency component at bin k
    N     = total number of samples
    j     = imaginary unit (sqrt(-1))
    k     = frequency bin index (0, 1, 2, ..., N-1)

In simple terms:
    FFT converts a time-domain signal (amplitude vs. time)
    into a frequency-domain representation (magnitude vs. frequency).
    Each output bin X(k) tells us how much of frequency f = k * (sample_rate / N)
    is present in the signal.
"""

import numpy as np


def analyze_frequency_domain(audio_data):
    """
    Apply FFT to the audio signal and extract frequency information.

    Parameters:
        audio_data (dict): Output from audio_loader module.

    Returns:
        dict: {
            'frequencies':        numpy array of frequency values (Hz),
            'magnitude_spectrum': numpy array of FFT magnitudes,
            'dominant_frequency': float (Hz),
            'sample_rate':        int,
            'num_samples':        int,
            'filename':           str
        }
    """
    signal      = audio_data["signal"]
    sample_rate = audio_data["sample_rate"]
    num_samples = len(signal)

    # -----------------------------------------------------------
    # Step 1: Apply FFT
    # np.fft.fft returns complex numbers X(k) for k = 0..N-1
    # -----------------------------------------------------------
    fft_result = np.fft.fft(signal)

    # -----------------------------------------------------------
    # Step 2: Compute magnitude spectrum
    # |X(k)| = sqrt( Re(X(k))^2 + Im(X(k))^2 )
    # Normalize by N so amplitude is independent of signal length.
    # Multiply by 2 to account for the mirrored negative frequencies
    # (only valid for the one-sided spectrum).
    # -----------------------------------------------------------
    magnitude = (2.0 / num_samples) * np.abs(fft_result)

    # -----------------------------------------------------------
    # Step 3: One-sided spectrum
    # Real signals have symmetric FFT; keep only first half (0 to Nyquist).
    # Nyquist frequency = sample_rate / 2
    # -----------------------------------------------------------
    half_n      = num_samples // 2
    magnitude   = magnitude[:half_n]

    # Build the corresponding frequency axis
    # freq[k] = k * (sample_rate / N)   for k = 0 .. N/2 - 1
    frequencies = np.fft.fftfreq(num_samples, d=1.0 / sample_rate)[:half_n]

    # -----------------------------------------------------------
    # Step 4: Find the dominant frequency
    # Ignore DC component at index 0 (frequency = 0 Hz)
    # -----------------------------------------------------------
    if len(magnitude) > 1:
        dominant_index = np.argmax(magnitude[1:]) + 1   # skip DC
    else:
        dominant_index = 0

    dominant_frequency = float(frequencies[dominant_index])

    return {
        "frequencies":        frequencies,
        "magnitude_spectrum": magnitude,
        "dominant_frequency": dominant_frequency,
        "sample_rate":        sample_rate,
        "num_samples":        num_samples,
        "filename":           audio_data["filename"],
    }
