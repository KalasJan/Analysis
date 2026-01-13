# analyza sledovanosti (data jsou ilustracni)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import skew, kurtosis, gaussian_kde

# import csv:

sledovanost = pd.read_csv(r'C:\Users\kalas\Plocha\kody\Python code\Analýzy\Sledovanost\Sledovanost.csv',
                      sep = ';', encoding = 'utf-8',
                      parse_dates=['Cas_vysilani', 'Cas_sledovani'])#oddeleni casu
# cesta, sep = oddelovac, dtype = oddeleni string a cisla

pd.set_option('display.max_columns', None)  # zobrazí všechny sloupce
pd.set_option('display.max_rows', None) #zobrazeni vsech radku
pd.set_option('display.width', 130)       # nastaví šířku pro hezký výpis
#print (sledovanost) #zobrazi CSV

# 1) Pomer stanice/zpusob

stanice_zpusob = sledovanost.pivot_table(
                    index='Stanice', #radky
                    columns = 'Zpusob_sledovani', #sloupce
                    aggfunc = 'size', # pocet radku
                    fill_value = 0 #kombinace neexistuje
                        )
print(stanice_zpusob)

plt.subplot(1, 2, 2)
stanice_zpusob.plot(kind='bar', stacked=True, color=['lightgreen', 'lightblue', 'red', 'yellow'], edgecolor='black')
plt.title('Sledovanost jednotlivých stanic podle způsobu sledování')
plt.xlabel('Stanice') #osa x
plt.ylabel('Frekvence') #osa y
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5)) #legenda
plt.tight_layout()
plt.show()

#graficky jen jedna stanice
stanice_graf = 'Noe' #chceme sledovanost NOE
df_stanice = sledovanost[sledovanost['Stanice']==stanice_graf]
#radky, kde je vybrana stanice
data_graf = df_stanice['Zpusob_sledovani'].value_counts() # chceme jenom jednu stanici, ne obe
#print(data_graf) #vytiskne, kolikrat jsou jednotlive zpusoby

def show_count(pct, all_vals):
    total = sum(all_vals)
    # pct je procento, převedeme zpět na počet
    count = int(round(pct*total/100))
    return str(count) #pokud chci hodnoty


plt.figure(figsize=(8, 8))  # Nastavení velikosti grafu
plt.subplot(1, 1, 1)
plt.pie(
    data_graf,               # hodnoty
    labels=data_graf.index,  # názvy kategorií
    #autopct=lambda pct: show_count(pct, data_graf), # chci zobrazene hodnoty
   autopct='%1.0f%%', #procenta
    startangle=-90
        ) 

# chceme oboji
# def autopct_format(pct, all_vals):
    # pct = procento výseku
#    total = sum(all_vals)
#    count = int(round(pct * total / 100))
#    return f"{count} ({pct:.0f}%)"

#plt.figure(figsize=(8, 8))  # Nastavení velikosti grafu
#plt.subplot(1, 1, 1)
#plt.pie(
#    data_graf,               # hodnoty
#    labels=data_graf.index,  # názvy kategorií
#    autopct=lambda pct: autopct_format(pct, data_graf), # chci zobrazene hodnoty
#    startangle=-90) 

plt.title(f'Sledovanost {stanice_graf} podle způsobu příjmu.')
plt.axis('equal')
plt.show()


# 2) Mira prehravani
# Cas sledovani - cas_vysilani = 0 .. soubezne vysilani, 0-10 min je mirne zpozdeni, nad 10 min Zpetne prehrani

sledovanost['Zpozdeni_min'] = (  
    sledovanost['Cas_sledovani']-sledovanost['Cas_vysilani']
    ).dt.total_seconds()/60 #chceme zpozdeni "prehrano - vysilano, v minutach

hranice = [(sledovanost['Zpozdeni_min'] <= 0),
           (sledovanost['Zpozdeni_min'] > 0) & (sledovanost['Zpozdeni_min'] <= 10),
           (sledovanost['Zpozdeni_min'] >10) 
               ]

volba = ['Souběžné sledování', 'Mírné zpoždění', 'Zpětné přehrání']

sledovanost['Doba_zpozdeni'] = np.select(
    hranice, volba, default='Nezname'
    )

celkem = len(sledovanost) # celkem zaznamu

# a) kolik je "Prehravani soubezne"
soubezne = (sledovanost['Doba_zpozdeni'] == 'Souběžné sledování').sum()
# hodnoty sjou 1 (true nebo 0 (false)

pomer = soubezne / celkem * 100 # v procenteh

print(f'Počet souběžného vysílání je {soubezne}, coz je {pomer: .2f}%')


# b) jake je nejmensi, nejvetsi, prumerne a median Zpetneho prehrani?
zpetne = sledovanost[sledovanost['Doba_zpozdeni'] == 'Zpětné přehrání']

pocet_zp = len(zpetne)
pomer_zp = pocet_zp / celkem * 100 # v procenteh

if np.issubdtype(zpetne['Zpozdeni_min'].dtype, np.timedelta64):
    zpetne['Zpozdeni_min'] = zpetne['Zpozdeni_min'].dt.total_seconds() / 60  # minuty #prevod na minuty

print(f'Počet souběžného vysílání je {pocet_zp}, coz je {pomer_zp: .2f}%')

# maximum, minimum, prumer zpetneho prehravani v minutach
min_zpoz = zpetne['Zpozdeni_min'].min() # minimum
max_zpoz = zpetne['Zpozdeni_min'].max() # maximum
prum_zpoz = zpetne['Zpozdeni_min'].mean() # prumer
med_zpoz = zpetne['Zpozdeni_min'].median() # median

#prevod minut na hod:min
def minut_hours(mins):
    h = int(mins // 60) #hodiny
    m = int (mins % 60)
    return f'{h}:{m:02d}'

print (f'Zpětné přehrání bylo od {minut_hours(min_zpoz)} po {minut_hours(max_zpoz)}. Průměrně {minut_hours(prum_zpoz)}.')

# graf rozlozeni zpetneho prehrani
# smerodatna odchylka
So = np.std(zpetne['Zpozdeni_min'])
print(f'Směrodatná odchylka je {So:.2f}.')

# koeficient sikmosti
sik = skew(zpetne['Zpozdeni_min'])
print(f'Koeficient sikmosti je {sik:.2f}.')

# koeficient spicatosti
spi = kurtosis(zpetne['Zpozdeni_min'])
print(f'Koeficient spicatosti je {spi:.2f}.')

# graf rozdeleni
odhad = gaussian_kde(zpetne['Zpozdeni_min'])
osa_x = np.linspace(min(zpetne['Zpozdeni_min'])-50, max(zpetne['Zpozdeni_min'])+50, 200) # od, do, pocet bodu
osa_y = odhad(osa_x)*len(zpetne['Zpozdeni_min'])*100 #abychom meli procenta

plt.figure(figsize=(8,5))
plt.plot(osa_x, osa_y, color='green', lw=2)

plt.axvline(min_zpoz, color='green', linestyle='--', label='min') # zdurazneni minimalni hodnoty
plt.axvline(max_zpoz, color='red', linestyle='--', label='max') #zdurazneni maximalni hodnoty
plt.axvline(prum_zpoz, color='blue', linestyle='-', label='průměr') # zdurazneni prumeru
plt.axvline(med_zpoz, color='purple', linestyle='-', label='medián') #zdurazneni medianu

plt.title('Rozdělení zpoždění – Zpětné přehrání')
plt.xlabel('Zpoždění (minuty)')
plt.ylabel('Počet záznamů (v %)')
plt.xlim(min_zpoz-50, max_zpoz+50) #omezeni osy x
plt.ylim(0, None) # dolni onezeni osy y
plt.legend()
plt.show()
