import numpy as np
import matplotlib.pyplot as plt

# =========================
# USER INPUT SECTION
# =========================

Vref = 5.0  # Reference voltage in volts

# ---------- 3-bit DAC ----------
digital_3bit = np.arange(0, 8)

# ENTER YOUR NEGATIVE MEASURED VALUES
observed_3bit = -1*np.array([
    -0.002,1.312,2.583,3.898,5.140,6.450,7.72,9.04 ])

print("Observed_3bit=",observed_3bit)

# ---------- 4-bit DAC ----------
digital_4bit = np.arange(0, 16)

# ENTER YOUR NEGATIVE MEASURED VALUES
observed_4bit = -1*np.array([
    -0.002,0.347,1.304,1.954,
    2.572,3.224,3.884,4.530,
    5.14,5.80,6.45,7.11,
    7.72,8.37,9.03,9.69])

print("Observed_4bit=",observed_4bit)

# =========================
# EXPECTED (THEORETICAL) OUTPUT
# =========================

def expected_output(digital, n_bits, Vref):
    return -Vref * 2*digital / (2**n_bits)

expected_3bit = expected_output(digital_3bit, 3, Vref)
expected_4bit = expected_output(digital_4bit, 4, Vref)

print("Expected_3bit=",expected_3bit)
print("Expected_4bit=",expected_4bit)
# =========================
# ANALYSIS FUNCTION
# =========================

def analyze_dac(digital, observed, expected, n_bits, title):
    error = observed - expected
    rms_error = np.sqrt(np.mean(error**2))
    lsb = Vref / (2**n_bits)

    # Linearity fit
    coeffs = np.polyfit(digital, observed, 1)
    fit = np.polyval(coeffs, digital)

    print(f"\n===== {title} =====")
    print(f"Resolution (LSB): {lsb:.4f} V")
    print(f"RMS Error: {rms_error:.4f} V")
    print(f"Slope (V/code): {coeffs[0]:.4f}")
    print(f"Intercept (V): {coeffs[1]:.4f}")

    # Monotonicity check
    monotonic = np.all(np.diff(observed) < 0)
    print(f"Monotonic: {'YES' if monotonic else 'NO'}")

    return fit, error

fit3, err3 = analyze_dac(
    digital_3bit, observed_3bit, expected_3bit, 3, "3-bit DAC"
)

fit4, err4 = analyze_dac(
    digital_4bit, observed_4bit, expected_4bit, 4, "4-bit DAC"
)

# =========================
# PLOTTING
# =========================

plt.figure()
plt.plot(digital_3bit, expected_3bit, 'o-', label="Expected")
plt.plot(digital_3bit, observed_3bit, 's', label="Observed")
plt.plot(digital_3bit, fit3, '--', label="Best Fit")
plt.xlabel("Digital Input (Decimal)")
plt.ylabel("Output Voltage (V)")
plt.title("3-bit Inverting DAC Transfer Characteristic")
plt.legend()
plt.grid()
plt.savefig("3-bit.jpeg")
plt.close()

plt.figure()
plt.plot(digital_4bit, expected_4bit, 'o-', label="Expected")
plt.plot(digital_4bit, observed_4bit, 's', label="Observed")
plt.plot(digital_4bit, fit4, '--', label="Best Fit")
plt.xlabel("Digital Input (Decimal)")
plt.ylabel("Output Voltage (V)")
plt.title("4-bit Inverting DAC Transfer Characteristic")
plt.legend()
plt.grid()
plt.savefig("4-bit.jpeg")


"""
Observed_3bit= [ 2.000e-03 -1.312e+00 -2.583e+00 -3.898e+00 -5.140e+00 -6.450e+00
 -7.720e+00 -9.040e+00]
Observed_4bit= [ 2.000e-03 -3.470e-01 -1.304e+00 -1.954e+00 -2.572e+00 -3.224e+00
 -3.884e+00 -4.530e+00 -5.140e+00 -5.800e+00 -6.450e+00 -7.110e+00
 -7.720e+00 -8.370e+00 -9.030e+00 -9.690e+00]
Expected_3bit= [-0.   -1.25 -2.5  -3.75 -5.   -6.25 -7.5  -8.75]
Expected_4bit= [-0.    -0.625 -1.25  -1.875 -2.5   -3.125 -3.75  -4.375 -5.    -5.625
 -6.25  -6.875 -7.5   -8.125 -8.75  -9.375]

===== 3-bit DAC =====
Resolution (LSB): 0.6250 V
RMS Error: 0.1676 V
Slope (V/code): -1.2878
Intercept (V): -0.0102
Monotonic: YES

===== 4-bit DAC =====
Resolution (LSB): 0.3125 V
RMS Error: 0.1896 V
Slope (V/code): -0.6502
Intercept (V): 0.0563
Monotonic: YES


"""