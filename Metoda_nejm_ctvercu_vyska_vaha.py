# Metodou nejmensich ctvercu (MNC) udelejte analyzu pomeru Vyska / vaha

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

# 1) otevreni souboru a vykresleni tabulky
df = pd.read_csv(r"MNC_vyska_vaha.csv",
                      sep = ';', # oddelovac
                      encoding = 'utf-8',                      
                      dtype={'Vyska': 'Int64',
                             'vaha': 'Int64', # i NaN hodnoty     
                             },
                                            )
# cesta, sep = oddelovac, dtype = oddeleni string a cisla (int), casu ()
pd.set_option('display.max_rows',3 )  # zobrazí všechny sloupce (colunmns) nebo radky (rows)
pd.set_option('display.width', 130)       # nastaví šířku pro hezký výpis
pd.options.display.float_format = '{:.2f}'.format # zamezeni cislum 200 jako 2e
print (df) #zobrazi CSV

# cisteni dat - prevod NaN na float
df_clean = df.dropna(subset=['Vyska', 'vaha']).copy()
df_clean['Vyska'] = df_clean['Vyska'].astype(float)
df_clean['vaha'] = df_clean['vaha'].astype(float)

# 1) prvotni vypocty

x = df_clean['Vyska']
y = df_clean['vaha']

# cisteni daat


# budeme hledat linearni funkci ve tvaru y = a * x + b

# 2) manualni zpusob
# a = sum (x[i] - mean_x) * (y[i] - mean_y) / sum (x[i] - mean_x) ** 2
# b = mean_y - a * mean_x

n = len(x)
mean_x = np.mean(x)
mean_y = np.mean(y)

cit = 0
jme = 0

for i in range(n):
    cit += (x.iloc[i] - mean_x) * (y.iloc[i] - mean_y)
    jme += (x.iloc[i] - mean_x) ** 2
    
a1 = cit / jme
b1 = mean_y - a1 * mean_x

print (f'Hledaná funkce má tvar $y = {a1:.2f} * x + {b1:.2f}$')

# 3) automaticky

a2, b2 = np.polyfit(x, y, 1)
print(f'NumPy polyfit (automaticky): $y = {a2:.2f} \cdot x + {b2:.2f}$')

# 4) graf
plt.figure(figsize=(9, 6))
sns.regplot(
    data=df_clean,
    x='Vyska',
    y='vaha',
    color='darkcyan',
    scatter_kws={'s': 80, 'alpha': 0.8},
    label = f'$y = {a2:.2f} * x + {b2:.2f}$',
    line_kws={'color': 'crimson', 'linewidth': 2}
)

plt.title("Lineární regrese (metoda nejmenších čtverců): Výška vs. Váha", fontsize=14)
plt.xlabel("Výška [cm]", fontsize=12)
plt.ylabel("Váha [kg]", fontsize=12)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.show()