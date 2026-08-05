## Key Features
- **Garmin Connect Analytics Pipeline:** Lightweight pipeline designed to ingest, clean, and visualize running logs, bypassing standard spreadsheet row and time-format limitations (`Run2025.py`).
- **Multi-Dimensional Pivoting:** Cross-tabulating monthly volume and average pace by day of the week and time of day (**Morning/Afternoon/Night**).
- **Time Normalization:** Converting text-based durations (`m:ss` / `h:mm:ss`) into linear seconds for accurate statistical aggregations (mean, median, sum).
- **Data Binned Segmentation (`pd.cut`):** Grouping continuous metrics into logical training intervals based on **distance** and **elevation gain** to map workout distribution.
- **Book Database & SQL Operations:** Computational pipelines for structured data management, combining CSV storage with relational database queries for personal book logging (`Run_SQL.py`, `Knihy.py`).

## Tech Stack
- **Pandas & NumPy** – Data wrangling, categorical sorting, and string parsing.
- **SQLite3 / SQL** – Relational database management and structured query executions.
- **Seaborn & Matplotlib** – Heatmaps (`magma_r`) and distribution plots.
