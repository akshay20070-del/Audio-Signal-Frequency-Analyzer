"""
main.py
-------
Entry point for the Audio Signal and Frequency Analyzer application.

Builds the Tkinter GUI and wires together all modules:
    audio_loader      → load / generate audio
    signal_processor  → time-domain analysis
    frequency_analyzer→ FFT frequency analysis
    visualization     → Matplotlib graphs

Run:
    python main.py
"""

import os
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ── Project modules ─────────────────────────────────────────────────────
import audio_loader
import signal_processor
import frequency_analyzer
import visualization

# ── Colour palette ──────────────────────────────────────────────────────
C_BG        = "#0A1628"   # Darkest navy – main background
C_PANEL     = "#0D1F3C"   # Slightly lighter – side-panel
C_CARD      = "#112240"   # Card / info-box background
C_BORDER    = "#1E3A5F"   # Border / separator colour
C_ACCENT    = "#00C8FF"   # Cyan accent – buttons, highlights
C_ACCENT2   = "#FF6B35"   # Orange accent – secondary buttons
C_TEXT      = "#E8F0FE"   # Light text
C_SUBTEXT   = "#7BA3CC"   # Dimmed text
C_BTN_FG    = "#0A1628"   # Button foreground (dark on bright)
C_SUCCESS   = "#00E676"   # Green – success states
C_WARNING   = "#FFD700"   # Yellow – warning states
C_ERROR     = "#FF5252"   # Red – error states

FONT_TITLE   = ("Segoe UI", 18, "bold")
FONT_HEADING = ("Segoe UI", 10, "bold")
FONT_NORMAL  = ("Segoe UI", 9)
FONT_MONO    = ("Consolas",  9)
FONT_SMALL   = ("Segoe UI",  8)


# ═══════════════════════════════════════════════════════════════════════════
class AudioAnalyzerApp:
    """Main application class."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self._setup_window()

        # State
        self.audio_data      = None   # raw loaded/generated data
        self.time_result     = None   # signal_processor output
        self.freq_result     = None   # frequency_analyzer output
        self.current_file    = None   # file path (None for test signals)
        self.fig             = None
        self.ax_time         = None
        self.ax_freq         = None
        self.canvas          = None

        # Build UI
        self._build_header()
        self._build_body()
        self._build_status_bar()

    # ── Window ──────────────────────────────────────────────────────────
    def _setup_window(self):
        self.root.title("Audio Signal and Frequency Analyzer")
        self.root.configure(bg=C_BG)
        self.root.geometry("1200x780")
        self.root.minsize(900, 650)
        self.root.resizable(True, True)
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 1200) // 2
        y = (self.root.winfo_screenheight() - 780)  // 2
        self.root.geometry(f"1200x780+{x}+{y}")

    # ── Header ──────────────────────────────────────────────────────────
    def _build_header(self):
        header = tk.Frame(self.root, bg=C_PANEL, pady=14)
        header.pack(fill=tk.X, side=tk.TOP)

        # Decorative left bar
        tk.Frame(header, bg=C_ACCENT, width=5).pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

        tk.Label(
            header,
            text="🎵  Audio Signal and Frequency Analyzer",
            font=FONT_TITLE, fg=C_ACCENT, bg=C_PANEL
        ).pack(side=tk.LEFT, padx=16)

        tk.Label(
            header,
            text="ECE Mini-Project  |  FFT Signal Analysis Tool",
            font=FONT_SMALL, fg=C_SUBTEXT, bg=C_PANEL
        ).pack(side=tk.RIGHT, padx=20)

    # ── Body (left panel + graph area) ──────────────────────────────────
    def _build_body(self):
        body = tk.Frame(self.root, bg=C_BG)
        body.pack(fill=tk.BOTH, expand=True)

        self._build_left_panel(body)
        self._build_graph_area(body)

    # ── Left control / info panel ────────────────────────────────────────
    def _build_left_panel(self, parent):
        panel = tk.Frame(parent, bg=C_PANEL, width=270)
        panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 1))
        panel.pack_propagate(False)

        # ── Action buttons ────────────────────────────────────────────
        btn_frame = tk.Frame(panel, bg=C_PANEL)
        btn_frame.pack(fill=tk.X, padx=14, pady=(16, 6))

        self._btn(btn_frame, "📂  Upload Audio",    self._upload_audio,    C_ACCENT,  C_BTN_FG).pack(fill=tk.X, pady=3)
        self._btn(btn_frame, "🔬  Analyze Signal",  self._analyze_signal,  C_SUCCESS, C_BTN_FG).pack(fill=tk.X, pady=3)
        self._btn(btn_frame, "🎛️  Generate Test Signal", self._open_test_dialog, "#9B59B6", C_TEXT).pack(fill=tk.X, pady=3)
        self._btn(btn_frame, "📄  Export Report",   self._export_report,   C_ACCENT2, C_BTN_FG).pack(fill=tk.X, pady=3)
        self._btn(btn_frame, "🔄  Reset",           self._reset,           C_BORDER,  C_TEXT).pack(fill=tk.X, pady=3)

        tk.Frame(panel, bg=C_BORDER, height=1).pack(fill=tk.X, padx=10, pady=10)

        # ── Info cards ────────────────────────────────────────────────
        tk.Label(panel, text="SIGNAL INFORMATION", font=FONT_SMALL, fg=C_SUBTEXT, bg=C_PANEL).pack(anchor="w", padx=14)

        info_frame = tk.Frame(panel, bg=C_PANEL)
        info_frame.pack(fill=tk.X, padx=10, pady=(4, 0))

        # Build info rows and store StringVar references
        self.sv_filename   = self._info_row(info_frame, "File Name",         "—")
        self.sv_duration   = self._info_row(info_frame, "Duration",          "—")
        self.sv_samplerate = self._info_row(info_frame, "Sample Rate",       "—")
        self.sv_numsamples = self._info_row(info_frame, "No. of Samples",    "—")
        self.sv_maxamp     = self._info_row(info_frame, "Max Amplitude",     "—")
        self.sv_minamp     = self._info_row(info_frame, "Min Amplitude",     "—")
        self.sv_rms        = self._info_row(info_frame, "RMS Amplitude",     "—")
        self.sv_dominant   = self._info_row(info_frame, "Dominant Frequency","—")

        tk.Frame(panel, bg=C_BORDER, height=1).pack(fill=tk.X, padx=10, pady=10)

        # ── Frequency limit slider ─────────────────────────────────────
        tk.Label(panel, text="DISPLAY FREQ LIMIT", font=FONT_SMALL, fg=C_SUBTEXT, bg=C_PANEL).pack(anchor="w", padx=14)

        self.freq_limit_var = tk.IntVar(value=8000)
        slider_frame = tk.Frame(panel, bg=C_PANEL)
        slider_frame.pack(fill=tk.X, padx=14, pady=(4, 0))

        self.freq_slider = tk.Scale(
            slider_frame,
            from_=500, to=22050, resolution=500,
            orient=tk.HORIZONTAL,
            variable=self.freq_limit_var,
            bg=C_PANEL, fg=C_TEXT,
            troughcolor=C_BORDER, highlightthickness=0,
            font=FONT_SMALL, label=""
        )
        self.freq_slider.pack(fill=tk.X)

        self.lbl_freq_limit = tk.Label(
            panel,
            text="Limit: 8000 Hz",
            font=FONT_SMALL, fg=C_SUBTEXT, bg=C_PANEL
        )
        self.lbl_freq_limit.pack(anchor="w", padx=14)
        self.freq_limit_var.trace_add("write", self._on_freq_limit_change)

    def _btn(self, parent, text, command, bg, fg):
        """Helper to create a styled button."""
        return tk.Button(
            parent, text=text, command=command,
            bg=bg, fg=fg, relief=tk.FLAT,
            font=FONT_HEADING, cursor="hand2",
            activebackground=C_BORDER, activeforeground=C_TEXT,
            padx=8, pady=8
        )

    def _info_row(self, parent, label, default):
        """Create a label-value card row; returns StringVar for the value."""
        card = tk.Frame(parent, bg=C_CARD, padx=8, pady=5)
        card.pack(fill=tk.X, pady=2)

        tk.Label(card, text=label, font=FONT_SMALL, fg=C_SUBTEXT, bg=C_CARD).pack(anchor="w")
        sv = tk.StringVar(value=default)
        tk.Label(card, textvariable=sv, font=FONT_MONO, fg=C_TEXT, bg=C_CARD).pack(anchor="w")
        return sv

    # ── Graph area (right side) ──────────────────────────────────────────
    def _build_graph_area(self, parent):
        graph_frame = tk.Frame(parent, bg=C_BG)
        graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Graph title strip
        tk.Label(
            graph_frame,
            text="Signal Visualization",
            font=FONT_HEADING, fg=C_SUBTEXT, bg=C_BG
        ).pack(anchor="w", pady=(0, 4))

        # Matplotlib canvas
        canvas_frame = tk.Frame(graph_frame, bg=C_BG)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.fig, self.ax_time, self.ax_freq, self.canvas = \
            visualization.create_figure(canvas_frame)

        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ── Status bar ──────────────────────────────────────────────────────
    def _build_status_bar(self):
        bar = tk.Frame(self.root, bg=C_PANEL, height=26)
        bar.pack(side=tk.BOTTOM, fill=tk.X)
        bar.pack_propagate(False)

        self.sv_status = tk.StringVar(value="Ready. Upload a WAV file or generate a test signal.")
        tk.Label(
            bar, textvariable=self.sv_status,
            font=FONT_SMALL, fg=C_SUBTEXT, bg=C_PANEL, anchor="w"
        ).pack(side=tk.LEFT, padx=12, fill=tk.Y)

        self.sv_time = tk.StringVar()
        tk.Label(
            bar, textvariable=self.sv_time,
            font=FONT_SMALL, fg=C_SUBTEXT, bg=C_PANEL
        ).pack(side=tk.RIGHT, padx=12)
        self._update_clock()

    def _update_clock(self):
        now = datetime.datetime.now().strftime("%d %b %Y  %H:%M:%S")
        self.sv_time.set(now)
        self.root.after(1000, self._update_clock)

    # ── Button actions ───────────────────────────────────────────────────

    def _upload_audio(self):
        """Open a file dialog to select a WAV file."""
        path = filedialog.askopenfilename(
            title="Select an Audio File",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if not path:
            return

        self._set_status("Loading audio file…", C_WARNING)
        try:
            self.audio_data   = audio_loader.load_audio_file(path)
            self.current_file = path
            self._set_status(f"Loaded: {os.path.basename(path)}", C_SUCCESS)
            self.sv_filename.set(os.path.basename(path))
            messagebox.showinfo("File Loaded",
                f"File loaded successfully!\n\n"
                f"File: {os.path.basename(path)}\n"
                f"Duration: {self.audio_data['duration']:.2f} s\n"
                f"Sample Rate: {self.audio_data['sample_rate']} Hz\n\n"
                f"Click 'Analyze Signal' to process.")
        except (FileNotFoundError, ValueError) as e:
            messagebox.showerror("Error Loading File", str(e))
            self._set_status("Error loading file.", C_ERROR)

    def _open_test_dialog(self):
        """Open a small dialog to configure and generate a test sine wave."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Generate Test Signal")
        dialog.configure(bg=C_BG)
        dialog.geometry("360x280")
        dialog.resizable(False, False)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width()  - 360) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 280) // 2
        dialog.geometry(f"360x280+{x}+{y}")

        tk.Label(dialog, text="Generate Sine Wave Test Signal",
                 font=FONT_HEADING, fg=C_ACCENT, bg=C_BG).pack(pady=(16, 4))

        fields_frame = tk.Frame(dialog, bg=C_BG)
        fields_frame.pack(fill=tk.X, padx=24, pady=8)

        def labeled_entry(parent, label, default):
            row = tk.Frame(parent, bg=C_BG)
            row.pack(fill=tk.X, pady=4)
            tk.Label(row, text=label, font=FONT_NORMAL, fg=C_TEXT, bg=C_BG, width=20, anchor="w").pack(side=tk.LEFT)
            var = tk.StringVar(value=str(default))
            tk.Entry(row, textvariable=var, bg=C_CARD, fg=C_TEXT, font=FONT_MONO,
                     insertbackground=C_TEXT, relief=tk.FLAT, width=10).pack(side=tk.LEFT)
            return var

        var_freq  = labeled_entry(fields_frame, "Frequency (Hz):",   440)
        var_dur   = labeled_entry(fields_frame, "Duration (s):",      2.0)
        var_sr    = labeled_entry(fields_frame, "Sample Rate (Hz):", 44100)
        var_noise = labeled_entry(fields_frame, "Noise Level (0-1):", 0.05)

        def do_generate():
            try:
                freq  = float(var_freq.get())
                dur   = float(var_dur.get())
                sr    = int(var_sr.get())
                noise = float(var_noise.get())
                if freq <= 0 or dur <= 0 or sr <= 0:
                    raise ValueError("Frequency, duration, and sample rate must be positive.")
                if not 0 <= noise <= 1:
                    raise ValueError("Noise level must be between 0 and 1.")
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e), parent=dialog)
                return

            self.audio_data   = audio_loader.generate_test_signal(freq, dur, sr, noise)
            self.current_file = None
            self.sv_filename.set(self.audio_data["filename"])
            dialog.destroy()
            self._set_status(f"Test signal generated: {freq:.0f} Hz sine wave", C_SUCCESS)
            messagebox.showinfo("Test Signal Generated",
                f"Sine wave generated!\n\nFrequency: {freq} Hz\n"
                f"Duration: {dur} s\nSample Rate: {sr} Hz\n\n"
                f"Click 'Analyze Signal' to process.")

        tk.Button(
            dialog, text="Generate Signal", command=do_generate,
            bg=C_ACCENT, fg=C_BTN_FG, font=FONT_HEADING,
            relief=tk.FLAT, cursor="hand2", padx=12, pady=8
        ).pack(pady=10)

    def _analyze_signal(self):
        """Run time-domain and frequency-domain analysis on loaded data."""
        if self.audio_data is None:
            messagebox.showwarning("No Signal", "Please upload an audio file or generate a test signal first.")
            return

        self._set_status("Analyzing signal…", C_WARNING)

        try:
            # Time-domain
            self.time_result = signal_processor.analyze_time_domain(self.audio_data)
            # Frequency-domain (FFT)
            self.freq_result = frequency_analyzer.analyze_frequency_domain(self.audio_data)

            # Update info panel
            self.sv_duration.set(f"{self.time_result['duration']:.4f} s")
            self.sv_samplerate.set(f"{self.time_result['sample_rate']:,} Hz")
            self.sv_numsamples.set(f"{self.time_result['num_samples']:,}")
            self.sv_maxamp.set(f"{self.time_result['max_amplitude']:.4f}")
            self.sv_minamp.set(f"{self.time_result['min_amplitude']:.4f}")
            self.sv_rms.set(f"{self.time_result['rms_amplitude']:.4f}")
            self.sv_dominant.set(f"{self.freq_result['dominant_frequency']:.2f} Hz")

            # Plot graphs
            max_f = self.freq_limit_var.get()
            visualization.plot_time_domain(self.ax_time, self.time_result)
            visualization.plot_frequency_domain(self.ax_freq, self.freq_result, max_freq_hz=max_f)
            visualization.refresh_canvas(self.canvas, self.fig)

            self._set_status(
                f"Analysis complete. Dominant frequency: {self.freq_result['dominant_frequency']:.2f} Hz",
                C_SUCCESS
            )

        except Exception as e:
            messagebox.showerror("Analysis Error", f"An error occurred during analysis:\n\n{e}")
            self._set_status("Analysis failed.", C_ERROR)

    def _on_freq_limit_change(self, *_):
        """Redraw frequency spectrum when the slider changes."""
        limit = self.freq_limit_var.get()
        self.lbl_freq_limit.config(text=f"Limit: {limit} Hz")
        if self.freq_result:
            visualization.plot_frequency_domain(self.ax_freq, self.freq_result, max_freq_hz=limit)
            visualization.refresh_canvas(self.canvas, self.fig)

    def _export_report(self):
        """Save a text analysis report to a file chosen by the user."""
        if self.time_result is None or self.freq_result is None:
            messagebox.showwarning("No Analysis", "Please analyze a signal before exporting.")
            return

        save_path = filedialog.asksaveasfilename(
            title="Save Analysis Report",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"analysis_report_{datetime.datetime.now():%Y%m%d_%H%M%S}.txt"
        )
        if not save_path:
            return

        try:
            report = self._build_report_text()
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(report)
            self._set_status(f"Report exported: {os.path.basename(save_path)}", C_SUCCESS)
            messagebox.showinfo("Report Exported",
                f"Report saved successfully!\n\n{save_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not save report:\n{e}")

    def _build_report_text(self):
        tr = self.time_result
        fr = self.freq_result
        now = datetime.datetime.now().strftime("%d %B %Y, %H:%M:%S")

        lines = [
            "=" * 60,
            "   AUDIO SIGNAL AND FREQUENCY ANALYZER",
            "   Signal Analysis Report",
            "=" * 60,
            "",
            f"  Analysis Date & Time : {now}",
            "",
            "─" * 60,
            "  FILE INFORMATION",
            "─" * 60,
            f"  File Name            : {tr['filename']}",
            f"  Duration             : {tr['duration']:.4f} seconds",
            f"  Sampling Frequency   : {tr['sample_rate']:,} Hz",
            f"  Number of Samples    : {tr['num_samples']:,}",
            "",
            "─" * 60,
            "  TIME-DOMAIN ANALYSIS",
            "─" * 60,
            f"  Maximum Amplitude    : {tr['max_amplitude']:.6f}",
            f"  Minimum Amplitude    : {tr['min_amplitude']:.6f}",
            f"  RMS Amplitude        : {tr['rms_amplitude']:.6f}",
            "",
            "─" * 60,
            "  FREQUENCY-DOMAIN ANALYSIS (FFT)",
            "─" * 60,
            f"  Dominant Frequency   : {fr['dominant_frequency']:.2f} Hz",
            f"  FFT Points           : {fr['num_samples']:,}",
            "",
            "─" * 60,
            "  NOTES",
            "─" * 60,
            "  - FFT computed using numpy.fft.fft (Cooley-Tukey algorithm)",
            "  - One-sided magnitude spectrum displayed (0 to Nyquist)",
            "  - Dominant frequency excludes DC component (0 Hz)",
            "",
            "=" * 60,
            "  Generated by Audio Signal and Frequency Analyzer v1.0",
            "  ECE Mini-Project | Python + NumPy + Matplotlib",
            "=" * 60,
        ]
        return "\n".join(lines)

    def _reset(self):
        """Clear all data and reset the UI to its initial state."""
        self.audio_data   = None
        self.time_result  = None
        self.freq_result  = None
        self.current_file = None

        self.sv_filename.set("—")
        self.sv_duration.set("—")
        self.sv_samplerate.set("—")
        self.sv_numsamples.set("—")
        self.sv_maxamp.set("—")
        self.sv_minamp.set("—")
        self.sv_rms.set("—")
        self.sv_dominant.set("—")

        # Clear and re-placeholder the graphs
        from visualization import _style_axes, _placeholder
        for ax, msg in [
            (self.ax_time, "Time-Domain Waveform\n\nUpload or generate a signal"),
            (self.ax_freq, "Frequency Spectrum\n\nUpload or generate a signal"),
        ]:
            ax.clear()
            _style_axes(ax)
            _placeholder(ax, msg)

        visualization.refresh_canvas(self.canvas, self.fig)
        self._set_status("Reset complete. Ready for a new signal.", C_SUBTEXT)

    def _set_status(self, message, color=None):
        self.sv_status.set(message)
        if color:
            # Find the status label widget and update its fg colour
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame) and widget.cget("bg") == C_PANEL:
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label) and child.cget("textvariable") == str(self.sv_status):
                            child.config(fg=color)
                            break


# ═══════════════════════════════════════════════════════════════════════════
def main():
    root = tk.Tk()
    app  = AudioAnalyzerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
