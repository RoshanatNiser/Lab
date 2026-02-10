import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------
# Enter your experimental data
# ---------------------------------
Thickness_cm = np.array([0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0])

Gross_counts=np.array([28587,26077,23702,21255,19630,18028,16242,14828,13310,12752,11616,10715,9730])
Counts = Gross_counts - 1555

# ---------------------------------
# Constants
# ---------------------------------
rho = 2.7   # g/cm^3 (Aluminium)

# ---------------------------------
# Initial and Half Counts
# ---------------------------------
I0 = Counts[0]
I_half = I0 / 2

# ---------------------------------
# Find HVL by linear interpolation
# ---------------------------------
# Find interval where counts cross I_half
for i in range(len(Counts)-1):
    if Counts[i] >= I_half and Counts[i+1] <= I_half:
        # linear interpolation
        x1 = Thickness_cm[i]
        x2 = Thickness_cm[i+1]
        y1 = Counts[i]
        y2 = Counts[i+1]
        
        HVL_cm = x1 + (I_half - y1) * (x2 - x1) / (y2 - y1)
        break



# ---------------------------------
# Calculate coefficients
# ---------------------------------
mu = np.log(2) / HVL_cm          # cm^-1
mu_mass = mu / rho               # cm^2/g

# ---------------------------------
# Print results
# ---------------------------------
print("Initial Counts I0 =", I0)
print("Half Counts =", I_half)
print("HVL =", HVL_cm, "mm")
print("Linear attenuation coefficient mu =", mu, "cm^-1")
print("Mass attenuation coefficient =", mu_mass, "cm^2/g")

# ---------------------------------
# Plot (Graphical method)
# ---------------------------------
plt.figure(figsize=(6,5))
plt.plot(Thickness_cm, Counts, 'o--', label='Data')

# Horizontal half-count line
plt.axhline(I_half, color='r', linestyle='--', label='Half Count')

# Vertical HVL line
plt.axvline(HVL_cm, color='g', linestyle='--', label='HVL')

plt.xlabel("Thickness (cm)")
plt.ylabel("Counts")
plt.title("Counts vs Thickness (Aluminium)")
plt.legend()
plt.savefig("HVL_Aluminium.png")
plt.close()

"""

Initial Counts I0 = 27032
Half Counts = 13516.0
HVL = 3.414073550212164 mm
Linear attenuation coefficient mu = 0.20302643465805545 cm^-1
Mass attenuation coefficient = 0.07519497579927979 cm^2/g
Literature value of Mass attenuation coefficient=0.07 to 0.08 cm²/g. 
Literature value of Linear attenuation coefficient mu= around 0.2024 cm^-1

"""
