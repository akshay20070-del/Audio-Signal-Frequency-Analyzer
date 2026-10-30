"""Quick functional test for all modules."""
import audio_loader
import signal_processor
import frequency_analyzer

# Test 1: Generate test signal
print("Test 1: Generating 440 Hz test signal...")
data = audio_loader.generate_test_signal(440, 2.0)
assert data["sample_rate"] == 44100
assert abs(data["duration"] - 2.0) < 0.01
print(f"  OK: Duration={data['duration']:.2f}s, Samples={data['num_samples']}")

# Test 2: Time-domain analysis
print("Test 2: Time-domain analysis...")
t = signal_processor.analyze_time_domain(data)
assert len(t["time_axis"]) == data["num_samples"]
assert t["max_amplitude"] > 0.9
assert t["min_amplitude"] < -0.9
print(f"  OK: Max={t['max_amplitude']:.4f}, Min={t['min_amplitude']:.4f}, RMS={t['rms_amplitude']:.4f}")

# Test 3: FFT frequency analysis
print("Test 3: FFT frequency analysis...")
f = frequency_analyzer.analyze_frequency_domain(data)
dom = f["dominant_frequency"]
assert 430 < dom < 450, f"Expected ~440 Hz, got {dom:.2f} Hz"
print(f"  OK: Dominant frequency = {dom:.2f} Hz (expected ~440 Hz)")

# Test 4: 1000 Hz signal
print("Test 4: Generating 1000 Hz test signal...")
data2 = audio_loader.generate_test_signal(1000, 1.0, 44100, 0.0)
f2 = frequency_analyzer.analyze_frequency_domain(data2)
dom2 = f2["dominant_frequency"]
assert 995 < dom2 < 1005, f"Expected ~1000 Hz, got {dom2:.2f} Hz"
print(f"  OK: Dominant frequency = {dom2:.2f} Hz (expected ~1000 Hz)")

print("\nAll tests passed!")
