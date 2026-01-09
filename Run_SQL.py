# Tetstovaci SQL (na soubor s bezeckymi aktivitami)

import pandas as pd
import sqlite3

#nacteni CSV (puvodniho)
sou = pd.read_csv(r'C:\Users\kalas\Plocha\kody\Python code\Analýzy\Run_2025\Run_2025.csv',
                  sep = ';', # oddelovac
                  decimal = ',', #jak chapat desetinne cislo
                  thousands = ' ',
                  encoding = 'utf-8')

# zjednoduseni nazvu (vymazani mezer a diakritiky)
sou.columns = [c.replace(' ', '_').replace('á','a').replace('é', 'e').
               replace('ě', 'e').replace('í', 'i').replace('ý', 'y').replace('Č', 'C')
               for c in sou.columns]

# ulozeni do "SQL pameti"
DOK = sqlite3.connect(':memory:')  # ':memory:' = jen v RAM

# CSV (puvodni) se ulozi do "nove" tabulky, se kterou se bude dal pracovat
sou.to_sql('behy', DOK, index=False, if_exists='replace')
# index - neukladani DF jako sloupec; if_exist - pokud by existovala,  prepise se

# samotny SQL dotaz:
    
# 1) celkem km a prevyseni podle dni v tydnu
query1 = '''
SELECT Den_v_tydnu, sum(Vzdalenost), sum(Celkovy_vystup)
FROM behy
WHERE Vzdalenost < 20 and Vzdalenost > 5
GROUP BY Den_v_tydnu
'''

#vysledky dotazu
vysledek1 = pd.read_sql_query(query1, DOK)
print(vysledek1)

#2) vsechny behy nad 40 km
query2 = '''
SELECT Mesic, Den_v_tydnu, Vzdalenost, Celkovy_vystup, Cas
FROM behy
WHERE Vzdalenost > 40
ORDER BY Vzdalenost DESC
'''

#vysledky dotazu
vysledek2 = pd.read_sql_query(query2, DOK)
print(vysledek2)