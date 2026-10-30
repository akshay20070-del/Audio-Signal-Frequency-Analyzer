"""
visualization.py
----------------
Handles all Matplotlib graph plotting.

Provides two plots:
  1. Time-Domain Waveform  – Amplitude vs. Time
  2. Frequency-Domain Spectrum – Magnitude vs. Frequency (FFT)
"""

import numpy as np
import matplotlib
matplotlib.use("TkAgg")          # Use TkAgg backend so plots embed in Tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# -----------------------------------------------------------------------
# Color palette matching the dark-blue / white application theme
# -----------------------------------------------------------------------
BG_COLOR        = "#0A1628"      # Very dark navy – figure background
AXES_COLOR      = "#0D1F3C"      # Slightly lighter – axes background
GRID_COLOR      = "#1E3A5F"      # Muted blue – grid lines
WAVEFORM_COLOR  = "#00C8FF"      # Cyan-blue – waveform line
SPECTRUM_COLOR  = "#FF6B35"      # Warm orange – spectrum line
FILL_COLOR_W    = "#00C8FF"      # Waveform fill (alpha applied later)
FILL_COLOR_S    = "#FF6B35"      # Spectrum fill (alpha applied later)
TEXT_COLOR      = "#FFFFFF"      # White – labels and titles


def create_figure(parent_frame):
    """
    Create a Matplotlib Figure with two subplots and embed it in the Tkinter frame.

    Parameters:
        parent_frame: A Tkinter Frame widget to embed the canvas in.

    Returns:
        (fig, ax_time, ax_freq, canvas)
            fig       – Matplotlib Figure
            ax_time   – Axes for time-domain plot
            ax_freq   – Axes for frequency-domain plot
            canvas    – FigureCanvasTkAgg widget
    """
    fig = Figure(figsize=(11, 5), dpi=96)
    fig.patch.set_facecolor(BG_COLOR)

    # Two subplots side by side
    ax_time = fig.add_subplot(1, 2, 1)
    ax_freq = fig.add_subplot(1, 2, 2)

    _style_axes(ax_time)
    _style_axes(ax_freq)

    # Placeholder text before any signal is loaded
    _placeholder(ax_time, "Time-Domain Waveform\n\nUpload or generate a signal")
    _placeholder(ax_freq, "Frequency Spectrum\n\nUpload or generate a signal")

    fig.tight_layout(pad=2.5)

    # Embed the figure into the Tkinter parent frame
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()

    return fig, ax_time, ax_freq, canvas


def _style_axes(ax):
    """Apply dark theme styling to a single Axes object."""
    ax.set_facecolor(AXES_COLOR)
    ax.tick_params(colors=TEXT_COLOR, labelsize=8)
    ax.spines["bottom"].set_color(GRID_COLOR)
    ax.spines["top"].set_color(GRID_COLOR)
    ax.spines["left"].set_color(GRID_COLOR)
    ax.spines["right"].set_color(GRID_COLOR)
    ax.title.set_color(TEXT_COLOR)
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.grid(True, color=GRID_COLOR, linestyle="--", linewidth=0.5, alpha=0.7)


def _placeholder(ax, message):
    """Display centered placeholder text on an empty axes."""
    ax.text(
        0.5, 0.5, message,
        transform=ax.transAxes,
        ha="center", va="center",
        color="#4A7AB5", fontsize=10, style="italic"
    )


def plot_time_domain(ax, time_result):
    """
    Plot the time-domain waveform.

    Parameters:
        ax          – Matplotlib Axes (ax_time)
        time_result – dict from signal_processor.analyze_time_domain()
    """
    ax.clear()
    _style_axes(ax)

    t      = time_result["time_axis"]
    signal = time_result["signal"]

    # Downsample for display if the signal is very large (>200k points)
    max_points = 200_000
    if len(t) > max_points:
        step   = len(t) // max_points
        t      = t[::step]
        signal = signal[::step]

    ax.plot(t, signal, color=WAVEFORM_COLOR, linewidth=0.8, label="Amplitude")
    ax.fill_between(t, signal, alpha=0.18, color=FILL_COLOR_W)

    ax.set_title("Time-Domain Waveform", fontsize=11, fontweight="bold", pad=8)
    ax.set_xlabel("Time (seconds)", fontsize=9)
    ax.set_ylabel("Amplitude", fontsize=9)
    ax.set_xlim(left=0, right=t[-1] if len(t) > 0 else 1)

    # Mark max and min amplitude
    max_idx = np.argmax(signal)
    min_idx = np.argmin(signal)
    ax.axhline(y=signal[max_idx], color="#FFD700", linewidth=0.7, linestyle=":", alpha=0.6)
    ax.axhline(y=signal[min_idx], color="#FF4444", linewidth=0.7, linestyle=":", alpha=0.6)

    ax.legend(
        loc="upper right", fontsize=8,
        facecolor=AXES_COLOR, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR
    )


def plot_frequency_domain(ax, freq_result, max_freq_hz=None):
    """
    Plot the frequency-domain spectrum.

    Parameters:
        ax           – Matplotlib Axes (ax_freq)
        freq_result  – dict from frequency_analyzer.analyze_frequency_domain()
        max_freq_hz  – optional upper frequency limit for x-axis (Hz)
    """
    ax.clear()
    _style_axes(ax)

    freqs = freq_result["frequencies"]
    mags  = freq_result["magnitude_spectrum"]
    dom_f = freq_result["dominant_frequency"]

    # Optionally limit the displayed frequency range (e.g. first 8 kHz)
    if max_freq_hz is not None:
        mask  = freqs <= max_freq_hz
        freqs = freqs[mask]
        mags  = mags[mask]

    ax.plot(freqs, mags, color=SPECTRUM_COLOR, linewidth=0.9, label="Magnitude")
    ax.fill_between(freqs, mags, alpha=0.2, color=FILL_COLOR_S)

    # Mark dominant frequency with a vertical dashed line
    ax.axvline(
        x=dom_f,
        color="#FFD700", linewidth=1.2, linestyle="--",
        label=f"Dominant: {dom_f:.1f} Hz"
    )

    ax.set_title("Frequency Spectrum (FFT)", fontsize=11, fontweight="bold", pad=8)
    ax.set_xlabel("Frequency (Hz)", fontsize=9)
    ax.set_ylabel("Magnitude", fontsize=9)
    ax.set_xlim(left=0)

    ax.legend(
        loc="upper right", fontsize=8,
        facecolor=AXES_COLOR, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR
    )


def refresh_canvas(canvas, fig):
    """Redraw the Matplotlib canvas after updating plots."""
    fig.tight_layout(pad=2.5)
    canvas.draw()
