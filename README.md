## 1. Correlation Analysis

Performing a correlation analysis between DMI (Dipole Mode Index) and drought indices (e.g., SPI – Standardized Precipitation Index, SPEI – Standardized Precipitation Evapotranspiration Index) is a common approach in climate and environmental studies to understand how large-scale climate patterns like the Indian Ocean Dipole influence regional drought conditions.

🧪 1. Understand Your Data
You’ll need:
- DMI dataset: Monthly or seasonal DMI values (usually from agencies like JMA or NOAA)
- Drought index dataset: e.g., SPI/SPEI at a specific time scale (e.g., SPI-3, SPI-6, SPI-12)

*Ensure both datasets are aligned in time (same start/end dates, same temporal resolution — monthly is ideal)*

```python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr

# -----------------------------
# 1. Load Your Data
# -----------------------------
# Replace these with your actual file paths
dmi_file = 'dmi_monthly.csv'     # e.g., columns: date, DMI
drought_file = 'spi_monthly.csv' # e.g., columns: date, SPI/SPEI

# Load data
dmi_df = pd.read_csv(dmi_file, parse_dates=['date'], index_col='date')
drought_df = pd.read_csv(drought_file, parse_dates=['date'], index_col='date')

# Rename column for clarity (optional)
dmi_df.columns = ['DMI']
drought_df.columns = ['Drought_Index']

# -----------------------------
# 2. Align Time Series
# -----------------------------
# Merge datasets on date
combined = pd.merge(dmi_df, drought_df, left_index=True, right_index=True, how='inner')

# Optional: Resample if needed (e.g., to monthly or seasonal)
# combined = combined.resample('M').mean()

print("Data successfully loaded and aligned.")
print(f"Time range: {combined.index.min()} to {combined.index.max()}")
print(f"Total overlapping months: {len(combined)}\n")

# -----------------------------
# 3. Basic Correlation Analysis
# -----------------------------
pear_corr, pear_p = pearsonr(combined['DMI'], combined['Drought_Index'])
spear_corr, spear_p = spearmanr(combined['DMI'], combined['Drought_Index'])

print(f"Pearson Correlation: {pear_corr:.3f}, p-value: {pear_p:.4f}")
print(f"Spearman Correlation: {spear_corr:.3f}, p-value: {spear_p:.4f}\n")

# -----------------------------
# 4. Lagged Correlation Analysis
# -----------------------------
max_lag = 6  # test up to 6 months lag
lag_results = []

for lag in range(0, max_lag + 1):
    lagged = combined.copy()
    lagged['DMI'] = lagged['DMI'].shift(lag)
    lagged.dropna(inplace=True)

    if len(lagged) == 0:
        continue

    corr, p = pearsonr(lagged['DMI'], lagged['Drought_Index'])
    lag_results.append({'lag': lag, 'correlation': corr, 'p_value': p})

lag_df = pd.DataFrame(lag_results)
print("Lagged Pearson Correlation Results:")
print(lag_df.to_string(index=False))

# -----------------------------
# 5. Visualization
# -----------------------------

# A. Scatter Plot
plt.figure(figsize=(8, 6))
sns.scatterplot(x='DMI', y='Drought_Index', data=combined)
plt.title(f"DMI vs Drought Index\nPearson r = {pear_corr:.2f}")
plt.xlabel("DMI")
plt.ylabel("Drought Index")
plt.grid(True)
plt.tight_layout()
plt.show()

# B. Time Series Plot
fig, ax1 = plt.subplots(figsize=(12, 6))
color = 'tab:blue'
ax1.set_xlabel('Date')
ax1.set_ylabel('DMI', color=color)
ax1.plot(combined.index, combined['DMI'], label='DMI', color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Drought Index', color=color)
ax2.plot(combined.index, combined['Drought_Index'], label='Drought Index', color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title("DMI and Drought Index Over Time")
plt.grid(True)
plt.show()

# C. Lagged Correlation Plot
plt.figure(figsize=(10, 5))
sns.barplot(x='lag', y='correlation', data=lag_df, palette='viridis')
plt.axhline(0, color='black', linewidth=0.8)
plt.title("Lagged Pearson Correlation Between DMI and Drought Index")
plt.xlabel("Lag (months)")
plt.ylabel("Correlation Coefficient")
plt.grid(True, axis='y', linestyle='--')
plt.tight_layout()
plt.show()
```
