import os
os.chdir("/home/fduchcle/root/muon_beam_intensities/root_muon/range_facilities")
print("Now in:", os.getcwd())
print("Files in directory:", os.listdir())

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.lines as mlines

# Load CSV file
df = pd.read_csv("facilities_range.csv")

# Define line styles for categories
category_styles = {
    "Material Science": {'color': 'black', 'linestyle': ':'},      # Dotted
    "Particle Physics": {'color': 'black', 'linestyle': '-'},     # Solid
    "Jefferson Lab": {'color': 'black', 'linestyle': '--'}          # Dashed
}

# Define facility order 
lab_order = ["TRIUMF", "PSI", "J-PARC", "ISIS RIKEN", "MuSIC", "CERN", "FERMILAB", "JLAB/BDX"]
spacing = 0.2
y_positions = {lab: i * spacing for i, lab in enumerate(reversed(lab_order))}

# Create plot
fig, ax = plt.subplots(figsize=(6, 4))

# Plot horizontal bars
for _, row in df.iterrows():
    y = y_positions[row["facility"]]
    style = category_styles.get(row["category"], {'color': 'black', 'linestyle': '-'})
    p_min, p_max = row["min"], row["max"]

    if p_max == p_min:
        # Single point
        ax.plot(p_min, y, 'o', color=style['color'], markersize=8)
    else:
        # Horizontal line
        ax.hlines(y, p_min, p_max, color=style['color'],
                  linestyle=style['linestyle'], linewidth=4)

# Y-axis labeling
ax.set_yticks(list(y_positions.values()))
ax.set_yticklabels([])  # Hide default ticks
for lab, y in y_positions.items():
    ax.text(0.0018, y, lab, ha='right', va='center', fontsize=10)

# Axis formatting
ax.set_xlabel("Momentum [GeV/c]", fontsize=12)
ax.set_xlim(0.002, 200)
ax.set_xscale('log')
ax.tick_params(axis='y', which='both', left=False)
ax.grid(which='major', axis='both', linestyle='--', linewidth=0.7, alpha=0.7)

# Title
plt.title("Momentum Range of Muon Beam Facilities", fontsize=14)

# Legend
handles = [
    mlines.Line2D([], [], color=style['color'], linestyle=style['linestyle'], lw=2, label=cat)
    for cat, style in category_styles.items()
]
plt.legend(handles=handles, loc='upper right')

plt.tight_layout()
plt.savefig("facilities_range_bw.png", dpi=300)
plt.show()
