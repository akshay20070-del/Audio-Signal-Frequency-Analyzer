# Samples

This folder is intended to store sample WAV audio files for testing  
the **Audio Signal and Frequency Analyzer** application.

## Supported Format

| Format | Extension | Notes |
|---|---|---|
| WAV (PCM) | `.wav` | Recommended — fully supported |

## How to Obtain Sample Files

1. **Generate using the application:** Click "Generate Test Signal" to create a sine wave without any external file.
2. **Record your own:** Use any audio recorder that can save in WAV format.
3. **Download free samples:** Websites like [freesound.org](https://freesound.org) offer free WAV files.
4. **Convert existing audio:** Use [Audacity](https://www.audacityteam.org/) (free) to convert MP3/other formats to WAV.

## Recommended Test Files

| Type | Frequency | Use Case |
|---|---|---|
| Pure Sine Wave | 440 Hz | Verify FFT accuracy |
| Piano Note | ~261 Hz (C4) | Real-world test |
| Speech Recording | Variable | Multi-frequency test |

## Notes

- Place `.wav` files directly in this folder.
- Use short files (2–10 seconds) for quick testing.
- Stereo WAV files are supported — they are automatically converted to mono.
