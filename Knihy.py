# máme CSV soubor s 30 knihami ruznych delek, jazyka i zanru

# otevreni souboru a vykresleni tabulky
import pandas as pd

prehled = pd.read_csv(r'C:\Users\kalas\Plocha\kody\Python code\Knihy\Knihy.csv',
                      sep = ';', encoding = 'utf-8',
                      dtype={'Stran': int, 'Rok vydání': int} )
# cesta, sep = oddelovac, dtype = oddeleni string a cisla

pd.set_option('display.max_columns', None)  # zobrazí všechny sloupce
pd.set_option('display.width', 130)       # nastaví šířku pro hezký výpis
#print (prehled) #zobrazi CSV


# 1) pridani knihy do zaznamu
nova_kniha = { #zaznamy
        'Autor': 'Clear, J.',
        'Název': 'Atomové návyky',
        'Nakladatelství': 'Jan Melvil',
        'Žánr': 'Osobní rozvoj',
        'Počet stran': 288,
        'Rok vydání': 2018,
        'Vazba': 'Měkká',
        'Jazyk': 'CZ'
            }
prehled = pd.concat(
    [prehled, #kam
    pd.DataFrame([nova_kniha])],#jakym zpusobem pridat
    ignore_index=True) #prepocitani indexu - srovnani abecedne
    



# 2) Kolik tam je zanru a kolikrát se tam kazdy vyskytuje
zanry = prehled.groupby('Žánr').size()
print (zanry)



# 3) kolik tam je nakladatelstvi (bez udani poctu vyskytu))
nakladatelstvi = prehled['Nakladatelství'].nunique()
print(r'Celkem se objevuje', nakladatelstvi, 'ruznych nakladatelství.')



# 4) seskupeni zanr - nakladatelstvi
nakladatel_zanr = prehled.pivot_table(
                    index='Nakladatelství', #radky
                    columns = 'Žánr', #sloupce
                    aggfunc = 'size', # pocet radku
                    fill_value = 0 #kombinace neexistuje
                        ) 
print(nakladatel_zanr) #zobrazeni jen tabulky
#vykresleni tabulky se zvyraznenim Maximum/minimum
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
sns.heatmap(nakladatel_zanr, annot=True, fmt="d", cmap="Blues")
#annot = zobrazeni cisel vsude, fmt = D - cele cislo, cmap = podbarveni
plt.title("Počet knih podle Nakladatelství a Žánru")
plt.show()



# 5) Kolik knih je v kazdem rozsahu: do 150, 15-200, 201-250, 251-300, 301-350, 350+

# definujeme hranice (do 150, 151- ...)
hranice = [0, 150, 200, 250, 300, 350, float('inf')] # musi tam byt omezeni zdola (0) a shora (float)

#novy sloupec s kategoriemi (nase intervaly)
intervaly = ['Do 150', '151-200', '201-250', '251-300', '301-350', '351+']
stran = pd.cut(
        prehled['Počet stran'], #odkud to brát
        bins = hranice, 
        labels = intervaly,
        right = True # 2000 v intervalu 151-200, false = 200 je zacatek noveho intervalu
                )
pocet_knih_stran = stran.value_counts().sort_index() #serazeni intervaly, ne cetnosti
print(pocet_knih_stran)

# graficky  - kolacovy graf
plt.figure(figsize=(8, 8))  # Nastavení velikosti grafu
plt.subplot(1, 1, 1)
plt.pie(pocet_knih_stran, # pocet v kazde kategorii
        labels=pocet_knih_stran.index,# kategorie, intervaly
        autopct='%01.2f%%', # vysledek v %
        startangle=-90)
plt.title('Koláčový graf: Relativní četnosti knih podle rozsahu')
plt.axis('equal') # aby to byl kruh
plt.show()

#stejny graf, jen misto % bude cetnost
def show_count(pct, all_vals):
    total = sum(all_vals)
    # pct je procento, převedeme zpět na počet
    count = int(round(pct*total/100))
    return str(count)

plt.pie(
    pocet_knih_stran,               # hodnoty
    labels=pocet_knih_stran.index,  # názvy kategorií
    autopct=lambda pct: show_count(pct, pocet_knih_stran),
    startangle=-90
        ) 

plt.title('Koláčový graf: Absolutní četnosti knih podle rozsahu')
plt.axis('equal')
plt.show()



# 6) Prumerny, minimalni, maximalni rozsah

prumer = prehled['Počet stran'].mean()
minimum = prehled['Počet stran'].min()
maximum = prehled['Počet stran'].max()
print ('Nejkratší kniha má', minimum, 'stran. Nejdelší naopak', maximum, 'stran a průměrný počet je', prumer, '.')



# 7) autor x jazyk
autor_jazyk = prehled.pivot_table(
                    index='Autor', #radky
                    columns = 'Jazyk', #sloupce
                    aggfunc = 'size', # pocet radku
                    fill_value = 0 #kombinace neexistuje
                        ) 
print(autor_jazyk) #zobrazeni jen tabulky



# 8) Serad knihy od nedelsi po nejkratsi
srovnani = prehled.sort_values (
            by = 'Počet stran', # podle čeho srovnáváme
            ascending = True # od nejmensi ; False = od nejvetsi
                )
print (srovnani[['Autor', 'Název', 'Počet stran']])


# 9) prumerny pocet stran podle vazby a nakladatelstvi
prumer_stran = prehled.pivot_table(
                index='Nakladatelství', # řádky
                columns='Vazba', # sloupce
                values='Počet stran', # co agregujeme
                aggfunc='mean', # průměr
                # fill_value = 0 pro dalsi vypocty by 0 mohla hazet chybu
                    )
print (prumer_stran)


