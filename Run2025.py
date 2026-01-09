# je dana tabulka behu za rok 2025
# mesic, den (pondeli,..), denni doba, vzdalenost, cas, typ behu, tepy, tempo, prevyseni, kroku
# ruzne analyzy - mesic x den, pomery vzdalenost a prevyseni atd.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np 

# 1) otevreni souboru a vykresleni tabulky
prehled = pd.read_csv(r'C:\Users\kalas\Plocha\kody\Python code\Analýzy\Run_2025\Run_2025.csv',
                      sep = ';', # oddelovac
                      decimal = ',', #jak chapat desetinne cislo
                      thousands = ' ',
                      encoding = 'utf-8',                      
                      dtype={'Vzdálenost': float,
                             'Průměrné tempo': str,
                             'Průměrný ST': int,
                             'Maximální ST': int,
                             'Celkový výstup': int,
                             'Kroky': int 
                             },
                      parse_dates=['Čas'], #oddeleni casu
                                            )
# cesta, sep = oddelovac, dtype = oddeleni string a cisla (int), casu ()
pd.set_option('display.max_columns', None)  # zobrazí všechny sloupce
pd.set_option('display.width', 130)       # nastaví šířku pro hezký výpis
pd.options.display.float_format = '{:.2f}'.format # zamezeni cislum 200 jako 2e
print (prehled) #zobrazi CSV

# prerovnani dnu v tydnu
den_poradi = ['Ráno a dopoledne', 'Odpoledne', 'Noc']
prehled['Denní doba'] = pd.Categorical(prehled['Den v týdnu'],
                                       categories=den_poradi,
                                       ordered=True)

tyden_poradi = ['pondělí','úterý','středa','čtvrtek','pátek','sobota','neděle']
prehled['Den v týdnu'] = pd.Categorical(prehled['Den v týdnu'],
                                       categories=tyden_poradi,
                                       ordered=True)

mesic_poradi = ['leden', 'únor', 'březen', 'duben', 'květen', 'červen', 'červenec', 'srpen',
                'září', 'říjen', 'listopad', 'prosinec']
prehled['Měsíc'] = pd.Categorical(prehled['Měsíc'],
                                       categories=mesic_poradi,
                                       ordered=True)

# 2) vzdalenosti, pocty aktivit podle mesice, dne a casu
vzdal_den_cas = prehled.pivot_table(
                    index='Měsíc', #radky
                    columns = 'Den v týdnu', #sloupce
                    values = 'Vzdálenost',
                    aggfunc= 'sum', #nebo count (pocet aktivit), mean (prumer)
                    fill_value = 0 # kombinace neexistuje
                        ) 
# zaokrouhleni sum (a mean):
vzdal_den_cas = vzdal_den_cas.round(2)

#vykresleni tab
plt.figure(figsize=(10,6))
sns.heatmap(vzdal_den_cas, annot=True, cmap="Blues", fmt = '.2f')
#annot = zobrazeni cisel vsude, cmap = podbarveni
plt.title("Běhy podle měsíce a dne v týdnu")
plt.show()

print(vzdal_den_cas) #zobrazeni jen tabulky


# 3) prumerne tempo podle casti dne a mesice
# prace s tempem na format m:ss
def prevod_na_sec(x):
    if pd.isna(x):
        return np.nan
    # pokud jde o Timestamp / Timedelta
    if isinstance(x, pd.Timestamp):
        h, m, s = x.hour, x.minute, x.second
        return h*3600 + m*60 + s
    # pokud je string
    if isinstance(x, str):
        parts = list(map(int, x.split(':')))
        if len(parts) == 2:   # m:ss
            return parts[0]*60 + parts[1]
        elif len(parts) == 3: # h:mm:ss
            return parts[0]*3600 + parts[1]*60 + parts[2]
    return np.nan

prehled['Tempo_sec'] = prehled['Průměrné tempo'].apply(prevod_na_sec)
#prevod tempa

#KT
df_plot = prehled.dropna(subset=['Tempo_sec'])
if df_plot.empty:
    print("Žádná platná data pro KT! Heatmapa nemůže být vykreslena.")
else:
    tempo_mesic_den = df_plot.pivot_table(
        index='Měsíc',
        columns='Den v týdnu',
        values='Tempo_sec',
        aggfunc='mean'
    )


#tempo na m:ss
def sec_na_mss(x):
    if pd.isna(x):
        return ""
    minutes = int(x // 60)
    seconds = int(round(x % 60))  # zaokrouhlíme na nejbližší sekundu
    return f"{minutes}:{seconds:02d}"

tempo_labels = tempo_mesic_den.applymap(sec_na_mss)

# vykresleni
plt.figure(figsize=(12,6))
sns.heatmap(
    tempo_mesic_den,     # hodnoty v sekundách pro barvy
    annot=tempo_labels,  # textové m:ss anotace
    fmt='',
    cmap='magma_r' #inverzni barvy, cim mensi hodnota, tim tmavsi
)
plt.title("Průměrné tempo podle měsíce a dne")
plt.ylabel("Měsíc")
plt.xlabel("Den")
plt.show()

# 4) Zakladni statistiky
aktivit = df_plot.shape[0] #pocet aktivit
prumer_rok_km = prehled['Vzdálenost'].mean()
celkem_km = prehled['Vzdálenost'].sum()
celkem_vys = prehled['Celkový výstup'].sum()
celkem_kroku = prehled['Kroky'].sum()

print(f'Celkem se uběhlo {celkem_km:,.2f}. Průměrně, tedy {prumer_rok_km:,.2f} a nastoupalo se {celkem_vys:,} m. A to v {aktivit} aktivit i s {celkem_kroku:,} kroků'.replace(',', ' '))

# 5) korelace: Vzdalenost - prumerny srdecni tep
df_scatter = df_plot.dropna(subset=['Vzdálenost', 'Průměrný ST']) #vybere platne hodnoty

plt.figure(figsize=(10,6))
sns.scatterplot(
    data=df_scatter,
    x='Vzdálenost',
    y='Průměrný ST',
    s=110,          # velikost teček
    color='blue',  # barva teček
    alpha=0.7      # průhlednost
)
plt.title("Vzdálenost vs. průměrný tep")
plt.xlabel("Vzdálenost [km]")
plt.ylabel("Průměrný tep [bpm]")
plt.grid(True, linestyle=':', color='gray', alpha=0.5)  # tečkovaná mřížka
plt.show()

#5b) korelace vzdalenost do 30 km - prumerny tep
df_scatter = df_plot[
    (df_plot['Vzdálenost'] < 30) &
    (df_plot['Průměrný ST'].notna())
]
plt.figure(figsize=(10,6))
sns.scatterplot(
    data=df_scatter,
    x='Vzdálenost',
    y='Průměrný ST',
    s=110,          # velikost teček
    color='blue',  # barva teček
    alpha=0.7      # průhlednost
)
plt.title("Vzdálenost vs. průměrný tep")
plt.xlabel("Vzdálenost [km]")
plt.ylabel("Průměrný tep [bpm]")
plt.grid(True, linestyle=':', color='gray', alpha=0.5)  # tečkovaná mřížka
plt.show()

# 6) Pocet aktivit podle vzdalenosti a prevyseni
# udelame hranice vzdalenosti
hran_vzd = [0, 5, 7, 10, 15, 21, 42, 50, 80, 100, 150, float('inf')] # musi tam byt omezeni zdola (0) a shora (float)
intervaly_vzd = ['0-5 km', '5-7 km', '7-10 km', '10-15 km','15-21 km', '21-42 km', '42-50 km','50-80 km', '80-100 km', '100-150 km', '150+']
dist = pd.cut(
        prehled['Vzdálenost'], #odkud to brát
        bins = hran_vzd, 
        labels = intervaly_vzd,
        right = True # 200 v intervalu 151-200, false = 200 je zacatek noveho intervalu
                )
rozlozeni_vzd = dist.value_counts().sort_index() #serazeni intervaly, ne cetnosti
print(rozlozeni_vzd)

#hranice prevyseni
hran_prev = [0, 100, 150, 200, 300, 500, 1000, float('inf')] # musi tam byt omezeni zdola (0) a shora (float)
intervaly_prev = ['0-100 m', '100-150 m', '150-200 m', '200-300 m', '300-500 m', '500-1000','nad 1 km']
prev = pd.cut(
        prehled['Celkový výstup'], #odkud to brát
        bins = hran_prev, 
        labels = intervaly_prev,
        right = True # 200 v intervalu 151-200, false = 200 je zacatek noveho intervalu
                )
rozlozeni_prev = prev.value_counts().sort_index() #serazeni intervaly, ne cetnosti
print(rozlozeni_prev)

# heatmapa medianu tempa a poctu aktivit
pocet_aktivit = prehled.pivot_table(
    index = dist, #osa x
    columns = prev, #osa y
    values = 'Vzdálenost',
    aggfunc = 'count'   
    )

plt.figure(figsize=(14,7))
sns.heatmap(
    pocet_aktivit,  # co ma zobrazit
    annot=True,     # zobrazí počet v každé buňce
    fmt='d',        # celé číslo
    cmap='Reds'    # libovolná barevná škála
)
plt.title("Počet aktivit podle vzdálenosti a převýšení")
plt.xlabel("Vzdálenost [km]")
plt.ylabel("Převýšení [m]")
plt.show()


