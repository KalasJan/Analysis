# Garmin Connect Analytics Pipeline (Running 2025)

A lightweight Python pipeline designed to ingest, clean, and visualize exactly running logs from Garmin Connect, bypassing standard spreadsheet row and time-format limitations.

## Key Features
- **Multi-Dimensional Pivoting:** Cross-tabulating monthly volume and average pace by day of the week and time of day (**Morning/Afternoon/Night**).
- **Time Normalization:** Converting text-based durations (`m:ss` / `h:mm:ss`) into linear seconds for accurate statistical aggregations (mean, median, sum).
- **Data Binned Segmentation (`pd.cut`):** Grouping continuous metrics into logical training intervals based on **distance** and **elevation gain** to map workout distribution.
- **Correlation Mapping:** Analyzing the relationship between distance and average heart rate (BPM) via scatterplots.

## Tech Stack
- **Pandas & NumPy** – Data wrangling, categorical sorting, and string parsing.
- **Seaborn & Matplotlib** – Heatmaps (`magma_r`) and distribution plots.

*Note: The script contains inline documentation and comments in Czech for reference.*
