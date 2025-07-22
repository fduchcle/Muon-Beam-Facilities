import os
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.lines as mlines

# Change to your working directory
os.chdir("/home/fduchcle/root/muon_beam_intensities/muon_facilities/range_facilities")

# Load CSV
df = pd.read_csv("facilities_range.csv")

# === DEBUG: Check that CERN exists ===
if "CERN" not in df["facility"].values:
    raise ValueError("CERN not found in CSV — check for spelling/case issues")

# Handle CERN skip: split into two ranges
cern_rows = df[df["facility"] == "CERN"]
if cern_rows.empty:
    raise ValueError("CERN row is empty despite match")

cern_low = cern_rows.copy()
cern_low["min"] = 0.20
cern_low["max"] = 12.0

cern_high = cern_rows.copy()
cern_high["min"] = 60.0
cern_high["max"] = 190.0

# Drop original CERN row and append two split rows
df = df[df["facility"] != "CERN"]
df = pd.concat([df, cern_low, cern_high], ignore_index=True)

# Style map
category_styles = {
    "Material Science": {'color': 'black', 'linestyle': ':'},
    "Particle Physics": {'color': 'black', 'linestyle': '-'},
    "Jefferson Lab": {'color': 'black', 'linestyle': '--'}
}

lab_order = ["TRIUMF", "J-PARC", "ISIS RIKEN", "MuSIC", "CERN", "PSI", "FERMILAB", "JLAB/BDX"]
spacing = 0.2
y_positions = {lab: i * spacing for i, lab in enumerate(reversed(lab_order))}

# Create plot
fig, ax = plt.subplots(figsize=(6, 4))

# Plot each line
for _, row in df.iterrows():
    facility = row["facility"]
    y = y_positions.get(facility)
    if y is None:
        continue

    style = category_styles.get(row["category"], {'color': 'black', 'linestyle': '-'})
    p_min, p_max = row["min"], row["max"]

    if p_min == p_max:
        ax.plot(p_min, y, 'o', color=style['color'], markersize=8)
    else:
        ax.hlines(y, p_min, p_max, color=style['color'], linestyle=style['linestyle'], linewidth=4)

# Y labels
ax.set_yticks(list(y_positions.values()))
ax.set_yticklabels([])
for lab, y in y_positions.items():
    ax.text(0.0018, y, lab, ha='right', va='center', fontsize=10)

# Axes
ax.set_xlabel("Momentum [GeV/c]", fontsize=12)
ax.set_xlim(0.002, 200)
ax.set_xscale('log')
ax.tick_params(axis='y', which='both', left=False)
ax.grid(which='major', axis='both', linestyle='--', linewidth=0.7, alpha=0.7)

# Title & legend
plt.title("Momentum Range of Muon Beam Facilities", fontsize=14)
handles = [
    mlines.Line2D([], [], color=style['color'], linestyle=style['linestyle'], lw=2, label=cat)
    for cat, style in category_styles.items()
]
plt.legend(handles=handles, loc='upper right')

plt.tight_layout()
plt.savefig("facilities_range_bw.jpeg", dpi=300)
plt.show()
