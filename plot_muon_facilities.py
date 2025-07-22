import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

# Read CSV 
df = pd.read_csv("muon_facilities.csv")
df.columns = df.columns.str.strip().str.lower()

x_material, y_material, types_material = [], [], []
x_particle, y_particle, labels_particle, types_particle = [], [], [], []
x_jlab, y_jlab, types_jlab = [], [], []

current_group = ""

for _, row in df.iterrows():
    group = row.get("category", current_group)
    lab = row.get("laboratory", "")
    mom_gev = row.get("momentum", np.nan)
    rate = row.get("intensity", np.nan)
    muon_type = row.get("muon type", "")  # Added: extract muon type

    if pd.isna(mom_gev) or pd.isna(rate):
        continue

    current_group = group

    if group == "Material Science":
        x_material.append(mom_gev)
        y_material.append(rate)
        types_material.append(muon_type)  # Added
    elif group == "Particle Physics":
        x_particle.append(mom_gev)
        y_particle.append(rate)
        labels_particle.append(lab)
        types_particle.append(muon_type)  # Added
    elif group == "BDX @ Jefferson Lab":
        x_jlab.append(mom_gev)
        y_jlab.append(rate)
        types_jlab.append(muon_type)  # Added
# Begin plotting
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xscale("log")
ax.set_yscale("log")

# Plot points
ax.scatter(x_material, y_material, label="Material Science", color="gray", s=60, marker="^")
ax.scatter(x_particle, y_particle, label="Particle Physics", color="darkblue", s=80, marker="s")
ax.scatter(x_jlab, y_jlab, label="BDX @ Jefferson Lab", color="black", s=40, marker="D")

# Label particle physics points
for x, y, label in zip(x_particle, y_particle, labels_particle):
    ax.text(x * 0.8, y * 1.3, label, fontsize=13)

# Label JLab
if len(x_jlab) > 0:
    idx = min(50, len(x_jlab)-1)
    x = x_jlab[idx]
    y = y_jlab[idx]
    ax.text(x * 0.4, y * 0.5, "JLab", fontsize=15)
    
# Label Muon Types 

# Material Science
for x, y, mtype in zip(x_material, y_material, types_material):
    if isinstance(mtype, str) and mtype.strip():
        ax.text(x * 1.13, y * 0.90, mtype, fontsize=9, color="black", alpha=0.7)

# Particle Physics
for x, y, mtype in zip(x_particle, y_particle, types_particle):
    if isinstance(mtype, str) and mtype.strip():
        ax.text(x * 1.1, y * 0.90, mtype, fontsize=9, color="blue", alpha=0.7)

# Jefferson Lab
for x, y, mtype in zip(x_jlab, y_jlab, types_jlab):
    if isinstance(mtype, str) and mtype.strip():
        ax.text(x * 1.1, y * 0.93, mtype, fontsize=9, color="black", alpha=0.7)

# Axis configuration
ax.set_xlim(0.005, 300)
ax.set_ylim(1e4, 1e9)
ax.set_xlabel("Momentum [GeV/c]", fontsize=14)
ax.set_ylabel("Intensity [1/s]", fontsize=14)
ax.grid(True, which="major", linestyle="--", linewidth=0.7)
ax.tick_params(axis='x', which='major', labelsize=10)
ax.tick_params(axis='y', which='major', labelsize=10)

# Title
plt.title("Muon Beam Facilities", fontsize=20, pad=35)

# Legend
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.1), ncol=3, fontsize=10, frameon=False)

plt.tight_layout()
plt.savefig("muon_facilities_plot.jpeg", dpi=300)
plt.show()