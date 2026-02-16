import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# -----------------------------
# Load Data
# -----------------------------
lamp = pd.read_csv("iv_in_lamp.csv")
sun  = pd.read_csv("iv_in_sunlight.csv")

# Remove first row (units row)
lamp = lamp.iloc[1:].reset_index(drop=True)
sun  = sun.iloc[1:].reset_index(drop=True)

lamp.columns = lamp.columns.str.strip()
sun.columns  = sun.columns.str.strip()

filters = [
    "No Filter",
    "Yellow Filter",
    "Green Filter",
    "Pink Filter",
    "Blue Filter"
]

# -----------------------------
# Analysis Function
# -----------------------------
def analyze(df, title):

    print(f"\n========== {title} ==========")

    for filt in filters:

        I_col = f"{filt} (I)"
        V_col = f"{filt} (V)"

        # Convert data
        I = pd.to_numeric(df[I_col], errors='coerce') / 1000  # mA → A
        V = pd.to_numeric(df[V_col], errors='coerce')

        mask = ~(I.isna() | V.isna())
        I = I[mask].values
        V = V[mask].values

        # Power
        P = V * I

        # Isc (Voltage ≈ 0)
        Isc = I[np.argmin(np.abs(V))]

        # Voc (Current ≈ 0)
        Voc = V[np.argmin(np.abs(I))]

        # Maximum Power Point
        idx = np.argmax(P)
        Pmax = P[idx]
        Vmp = V[idx]
        Imp = I[idx]

        # Fill Factor
        FF = Pmax / (Voc * Isc)

        print(f"\n--- {filt} ---")
        print(f"Isc  = {Isc:.6f} A")
        print(f"Voc  = {Voc:.6f} V")
        print(f"Pmax = {Pmax:.6f} W")
        print(f"Vmp  = {Vmp:.6f} V")
        print(f"Imp  = {Imp:.6f} A")
        print(f"Fill Factor = {FF:.4f}")

        # -----------------------------
        # I-V Plot (Separate)
        # -----------------------------
        plt.figure()
        plt.plot(V, I, marker='o')
        plt.xlabel("Voltage (V)")
        plt.ylabel("Current (A)")
        plt.title(f"I-V Curve ({filt}) - {title}")
        plt.grid(True)
        plt.savefig(f"Images/{title}/I-V Curve ({filt}) - {title}.png")
        plt.close()

        # -----------------------------
        # P-V Plot (Separate)
        # -----------------------------
        plt.figure()
        plt.plot(V, P, marker='o')
        plt.xlabel("Voltage (V)")
        plt.ylabel("Power (W)")
        plt.title(f"P-V Curve ({filt}) - {title}")
        plt.grid(True)
        plt.savefig(f"Images/{title}/P-V Curve ({filt}) - {title}.png")
        plt.close()


# -----------------------------
# Run for Lamp and Sun
# -----------------------------
analyze(lamp, "Lamp Illumination")
analyze(sun, "Sunlight Illumination")
