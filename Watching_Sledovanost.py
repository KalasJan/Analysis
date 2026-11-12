# Analysis of watching TV stations (data are random)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import skew, kurtosis, gaussian_kde

# 0) Open CSV file
df = pd.read_csv(r'Watching_Sledovanost.csv',
                      sep = ';', encoding = 'utf-8',
                      parse_dates=['Zacatek_vysilani', 'Cas_sledovani'])#oddeleni casu

# checking the file
pd.set_option('display.max_columns', None)  # show all columns
pd.set_option('display.max_rows', None) # show all rows
pd.set_option('display.width', 130)       # size, better looking
# print (df) #zobrazi CSV

# 1) Station / Program
station_program = pd.crosstab(
    index=df['Stanice'], 
    columns=df['Program'])
print(station_program)

plt.figure(figsize=(8, 6))
sns.heatmap(station_program, annot=True, cmap="Blues", fmt='.0f')
plt.title("1) Watching programs by Stations")
plt.tight_layout()
plt.show()

# 2) Premiere vs Repeat (repriza)
typ = df['Typ_poradu'].value_counts() # how many times


plt.figure(figsize=(6, 6))
plt.pie(
    typ, 
    labels=typ.index, 
    autopct='%1.1f%%',       # Percents
    startangle=90,           # Rotation of graph
    colors=['lightblue', 'lightgreen'], # Vlastní barvy (můžeš upravit)
    wedgeprops={'edgecolor': 'white', 'linewidth': 1.5} # Bílé ohraničení dílků
)

plt.title("2) Premiere vs Repeat")
plt.tight_layout()
plt.show()

# 3) station by location

order_location = ['pod 1000','1001 – 10000','10001 – 50000','50001 – 100000','100000-350000','Nad 350001']

station_location = pd.crosstab(
    index=df['Stanice'], 
    columns=df['Lokalita'])

station_location = station_location.reindex(columns=order_location, fill_value=0)

print(station_location)

plt.figure(figsize=(8, 6))
sns.heatmap(station_location, annot=True, cmap="Reds", fmt='.0f')
plt.title("3) Watching stations by location")
plt.tight_layout()
plt.show()

# 4) Delaying (difference between Zacatek_vysilani an Cas_sledovani)

df['Delay'] = (  
    df['Cas_sledovani'] - df['Zacatek_vysilani']
    ).dt.total_seconds()/60

zpetne = df[df['Delay'] > 0]

# maximum, minimum, average of delay

min_zpoz = zpetne['Delay'].min() # minimum
max_zpoz = zpetne['Delay'].max() # maximum
prum_zpoz = zpetne['Delay'].mean() # prumer
med_zpoz = zpetne['Delay'].median() # median

#prevod minut na hod:min
def minut_hours(mins):
    h = int(mins // 60) # hours
    m = int (mins % 60)
    return f'{h}:{m:02d}'

print (f'Delay was since {minut_hours(min_zpoz)} to {minut_hours(max_zpoz)}. Average {minut_hours(prum_zpoz)}.')

# graf rozlozeni zpetneho prehrani
# Standard deviation / smerodatna odchylka
So = np.std(zpetne['Delay'])
print(f'Standard deviation je {So:.2f}.')

# Skewness / koeficient sikmosti
sik = skew(zpetne['Delay'])
print(f'Skewness is {sik:.2f}.')

# Kurtosis / koeficient spicatosti
spi = kurtosis(zpetne['Delay'])
print(f'Kurtosis is {spi:.2f}.')

# graf rozdeleni
trying = gaussian_kde(zpetne['Delay'])
osa_x = np.linspace(min(zpetne['Delay'])-50, max(zpetne['Delay'])+50, 200) # since, to, many points
osa_y = trying(osa_x)*len(zpetne['Delay'])*100 # for %

plt.figure(figsize=(8,5))
plt.plot(osa_x, osa_y, color='green', lw=2)

plt.axvline(min_zpoz, color='green', linestyle='--', label='min') # min
plt.axvline(max_zpoz, color='red', linestyle='--', label='max') # max 
plt.axvline(prum_zpoz, color='blue', linestyle='-', label='average') # average
plt.axvline(med_zpoz, color='purple', linestyle='-', label='median') # median

plt.title('4) Delay distribution')
plt.xlabel('Delay (mins)')
plt.ylabel('Counts (v %)')
plt.xlim(min_zpoz-50, max_zpoz+50) # limit of x
plt.ylim(0, None) # down limit of y
plt.legend()
plt.show()

# 5) Convert CSV to JSON and XML

# a) JSON
json_file = 'Watching_Sledovanost.json'
df.to_json(json_file, orient='records', force_ascii=False, indent=4)
print(f"Data was exported to JSON: {json_file}")

# b) to XML
xml_file = 'Watching_Sledovanost.xml'
df.to_xml(xml_file, root_name='BroadcastLogs', row_name='LogEntry', xml_declaration=True, encoding='utf-8')
print(f"Data was exported to XML: {xml_file}")