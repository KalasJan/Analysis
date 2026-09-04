# Udelej predikci vahy metodou Monte Carlo

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

# 1) otevreni souboru a vykresleni tabulky
df = pd.read_csv(r"MC_vyvoj_vahy.csv",
                      sep = ';', # oddelovac
                      encoding = 'utf-8',  
                      decimal = '.',
                      dtype={'mesic': int,
                          'vaha':  float},
                      )

# print(df.head())
# print(df.dtypes)  # kontrola CSV

# Monte Carlo (se smazanými hodnotami)
# smazani NaN hodnot
df_clean = df.dropna(subset=['vaha']).copy()

# mezimesicni zmeny
df_clean['diff'] = df_clean['vaha'].diff()
diffs = df_clean['diff'].dropna()

mean_change = diffs.mean() # prumerna mesicni zmena
std_change = diffs.std() # smerodatna odchylka

print(f"Celkem je {len(df_clean)} platných měsíců s průměrnou změnou {mean_change:.2f} kg/měs a směrodatnou odchylkou {std_change:.2f} kg\n ")

# samotne Monte Carlo
def run_monte_carlo(mean, std, start_val, n_sims=5000, n_months=6):
    paths = np.zeros((n_sims, n_months + 1))
    paths[:, 0] = start_val
    
    for m in range(1, n_months + 1):
        random_changes = np.random.normal(loc=mean, scale=std, size=n_sims)
        paths[:, m] = paths[:, m - 1] + random_changes
        
    return paths

np.random.seed(42) # random, nahoda
last_weight = df_clean['vaha'].iloc[-1]  # Poslední známá váha
n_months_ahead = 6 # pristich n mesicu

sims = run_monte_carlo(mean_change, std_change, last_weight, n_sims=5000, n_months=n_months_ahead)

# percentil a odhady
p5 = np.percentile(sims[:, -1], 5)
p50 = np.median(sims[:, -1])
p95 = np.percentile(sims[:, -1], 95)

print(f"Medián za posledních 6 měsíců je {p50:.2f} kg v intervalu ({p5:.2f}, {p95:.2f}) kg")

# ===============================================================

# linearni interpolace (zprumerovani okoli)
df['vaha_interpolated'] = df['vaha'].interpolate(method='linear')

df['diff_lin'] = df['vaha_interpolated'].diff()
diffs2 = df['diff_lin'].dropna()

mean_change_lin = diffs2.mean()
std_change_lin = diffs2.std()

print(f"Průměrováním je průměr {mean_change_lin:.2f} kg/měs a směrodatnou odchylkou {std_change_lin:.2f} kg")

# samotne Monte Carlo
def run_monte_carlo_lin(mean_lin, std_lin, start_val_lin, n_sims_lin=5000, n_months_lin=12):
    paths_lin = np.zeros((n_sims_lin, n_months_lin + 1))
    paths_lin[:, 0] = start_val_lin
    
    for m in range(1, n_months_lin + 1):
        random_changes_lin = np.random.normal(loc=mean_lin, scale=std_lin, size=n_sims_lin)
        paths_lin[:, m] = paths_lin[:, m - 1] + random_changes_lin
        
    return paths_lin

np.random.seed(42) # random, nahoda
last_weight_lin = df['vaha_interpolated'].iloc[-1]  # Poslední známá váha
n_months_ahead_lin = 12 # pristich n mesicu

sims_lin = run_monte_carlo_lin(mean_change_lin, std_change_lin, last_weight_lin, n_months_lin=n_months_ahead_lin)

# percentil a odhady
p5_lin = np.percentile(sims_lin[:, -1], 5)
p50_lin = np.median(sims_lin[:, -1])
p95_lin = np.percentile(sims_lin[:, -1], 95)

print(f"Medián za posledních 6 měsíců je {p50_lin:.2f} kg v intervalu ({p5_lin:.2f}, {p95_lin:.2f}) kg")

# ==============================================================
# Grafy

fig = plt.figure(figsize=(16, 8))

# Levý - smazanim prazdnych
ax1 = fig.add_subplot(121)
ax1.plot(sims[:50].T, color='darkcyan', alpha=0.05)  # Prvních 50 cest
ax1.plot(np.median(sims, axis=0), color='teal', linewidth=2.5, label='Medián MC')
ax1.fill_between(range(n_months_ahead + 1), 
                 np.percentile(sims, 5, axis=0), 
                 np.percentile(sims, 95, axis=0), 
                 color='darkcyan', alpha=0.15, label='95% interval')
ax1.set_title("Monte Carlo simulace (s pročištěním prázdných měsíců)")
ax1.set_xlabel("Měsíce dopředu")
ax1.set_ylabel("Váha [kg]")

ax1.legend()
ax1.grid(True, linestyle=':', alpha=0.6)

# Pravý graf, po linearizaci chybejicicch odnot

ax2 = fig.add_subplot(122)
ax2.plot(sims_lin[:50].T, color='darkred', alpha=0.05)  # Prvních 50 cest
ax2.plot(np.median(sims_lin, axis=0), color='crimson', linewidth=2.5, label='Medián MC')
ax2.fill_between(range(n_months_ahead_lin + 1), 
                 np.percentile(sims_lin, 5, axis=0), 
                 np.percentile(sims_lin, 95, axis=0), 
                 color='darkred', alpha=0.15, label='95% interval')
ax2.set_title("Monte Carlo simulace (s linearizací / průměrováním okolí)")
ax2.set_xlabel("Měsíce dopředu")
ax2.set_ylabel("Váha [kg]")

ax2.legend()
ax2.grid(True, linestyle=':', alpha=0.6)

plt.suptitle('Metoda Monte Carlo')

plt.tight_layout()
plt.show()