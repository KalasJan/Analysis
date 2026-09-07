# Vyreste problem obchodniho cestujiciho na 13 krajskych mestech CZ
# KVA, PLZ, CEB, JIH, BRN, ZLN, OVA, OLO, PCE, HKR, LIB, UNL, PHA
# zaciname v PHA a cilem je projet vsemi mesty tak, abychom skoncili v PHA a byla to nejkratsi trasa

import matplotlib.pyplot as plt
import pandas as pd

# import excelu (s matici vzdalenosti)
df = pd.read_excel("Distances.xlsx", index_col=0)
gps = pd.read_excel("GPS.xlsx", index_col = 0)

mesta = list(df.columns)
matice = df.to_numpy()

# index startovniho (a ciloveho) mesta
start_mesto = 'PHA'
start_idx = mesta.index(start_mesto)

# kontrola nahrani
print(f'Načteno měst: {len(mesta)}')
print(f'Startovní a cílové město: {start_mesto} (index {start_idx})')
print(mesta)

# vypomoc (aby nebyl skok typu CEB -> OVA)
def spocti_vzdalenost(trasa, m_mat):
  d = 0.0
  for i in range(len(trasa) - 1):
    d += m_mat[trasa[i], trasa[i + 1]]
  return d

# start
aktualni_idx = start_idx
neprojeta = set(range(len(mesta)))
neprojeta.remove(start_idx)

trasa_indexy = [start_idx]
celkova_vzdalenost = 0.0

# kazde dalsi mesto (metodou nejblizsiho)
while neprojeta:
  dalsi_idx = min(neprojeta, key=lambda m: matice[aktualni_idx, m])
  celkova_vzdalenost += matice[aktualni_idx, dalsi_idx]
  aktualni_idx = dalsi_idx
  trasa_indexy.append(aktualni_idx)
  neprojeta.remove(aktualni_idx)
  
trasa_indexy.append(start_idx)

# puvodni (klidne i pres celou republiku)
puvodni_vzdalenost = spocti_vzdalenost(trasa_indexy, matice)

# jmena misto indexu
trasa_mesta = [mesta[i] for i in trasa_indexy]
print(
    "Nalezená trasa (metodou nejbližšího souseda):",
    " -> ".join(trasa_mesta),
    f"({puvodni_vzdalenost:.2f} km)",
)
# vyhozeni dlouhych prejezdu (a krizeni)
def optimalizace_2opt(trasa, m_mat):
  nejlepsi_trasa = list(trasa)
  nejlepsi_vzdalenost = spocti_vzdalenost(nejlepsi_trasa, m_mat)
  zlepseni = True
  
  while zlepseni:
    zlepseni = False
    # Prochazime dvojice hran (start a konec ve stejném meste neměníme)
    for i in range(1, len(nejlepsi_trasa) - 2):
      for j in range(i + 1, len(nejlepsi_trasa) - 1):
        # Provedeme 2-opt swap (otooceni podsekvence mezi i a j)
        nova_trasa = (
            nejlepsi_trasa[:i]
            + nejlepsi_trasa[i : j + 1][::-1]
            + nejlepsi_trasa[j + 1 :]
        )
        nova_vzdalenost = spocti_vzdalenost(nova_trasa, m_mat)

        if nova_vzdalenost < nejlepsi_vzdalenost:
          nejlepsi_trasa = nova_trasa
          nejlepsi_vzdalenost = nova_vzdalenost
          zlepseni = True

  return nejlepsi_trasa, nejlepsi_vzdalenost


optimalizovana_trasa, optimalizovana_vzdalenost = optimalizace_2opt(
    trasa_indexy, matice
)

trasa_mesta = [mesta[i] for i in optimalizovana_trasa]
print('Optimalizovaná trasa:', ' -> '.join(trasa_mesta))
print(f'Nová celková vzdálenost po 2-opt: {optimalizovana_vzdalenost:.2f} km')

## 4A. Vizualizace v Matplotlibu (kruhove rozestavění mest)

# import numpy as np # zamerne az tady

# uhly = np.linspace(0, 2 * np.pi, len(mesta), endpoint=False)
# x = np.cos(uhly)
# y = np.sin(uhly)
# coords = {mesta[i]: (x[i], y[i]) for i in range(len(mesta))}

# fig, ax = plt.subplots(figsize=(8, 8))

# for i in range(len(optimalizovana_trasa) - 1):
#   m1 = mesta[optimalizovana_trasa[i]]
#   m2 = mesta[optimalizovana_trasa[i + 1]]
#   p1, p2 = coords[m1], coords[m2]
#   ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'm-', lw=2)

# for m, (px, py) in coords.items():
#   ax.plot(px, py, 'ko', markersize=8)
#   barva_textu = 'red' if m == f'{start_mesto}' else 'black'
#   ax.text(
#       px + 0.03,
#       py + 0.03,
#       m,
#       fontsize=12,
#       weight='bold',
#       color=barva_textu,
#   )

# ax.set_title(
#     f'TSP - 2-opt Optimalizovaná trasa ({optimalizovana_vzdalenost:.2f} km)',
#     fontsize=14,
# )
# ax.axis('off')
# plt.tight_layout()
# plt.show()

## 4B - vizualizace pres GPS souradnice
fig, ax = plt.subplots(figsize=(10, 6))

coords = {}
for m in mesta:
  # Explicitne vytáhneme sloupec 'WE' jako X (West - East) a 'NS' jako Y (North - South)
  x_val = gps.loc[m, 'WE']
  y_val = gps.loc[m, 'NS']
  coords[m] = (x_val, y_val)

# vykresleni optimalni trasy
for i in range(len(optimalizovana_trasa) - 1):
  m1 = mesta[optimalizovana_trasa[i]]
  m2 = mesta[optimalizovana_trasa[i + 1]]
  p1, p2 = coords[m1], coords[m2]
  ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'm-', lw=2)

# vykresleni jednotlivych mest
for m, (px, py) in coords.items():
  ax.plot(px, py, 'ko', markersize=8)
  barva_textu = 'red' if m == start_mesto else 'black'
  ax.text(
      px + 0.03,
      py + 0.03,
      m,
      fontsize=12,
      weight='bold',
      color=barva_textu,)
  
ax.set_title(
    f'TSP - Geografická trasa ČR / 2-opt ({optimalizovana_vzdalenost:.2f} km)',
    fontsize=14,
)
ax.set_xlabel('Zeměpisná délka (WE, Z-V)')
ax.set_ylabel('Zeměpisná šířka (NS, S-J)')
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()