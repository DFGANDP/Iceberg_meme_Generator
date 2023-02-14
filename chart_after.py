import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('przerobione_recznie_ankieta.xlsx')


print(df.columns)
df['Zaokraglone'] = df['Zaokraglone'].astype(int)
value_counts = df['Zaokraglone'].value_counts()
value_counts = value_counts.sort_index()
print(value_counts)

# KOLOWY
value_counts.plot.pie(figsize=(5, 5), autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')  
plt.show()

# SLUPKOWY
value_counts.plot.bar(figsize=(8, 5))
plt.xlabel('Level')
plt.ylabel('Counts')
plt.show()

#KOLUMNOWY
value_counts.plot.barh(figsize=(8, 5))
plt.xlabel('Counts')
plt.ylabel('Level')
plt.show()

#LINIOWY
value_counts.plot.line(figsize=(8, 5))
plt.xlabel('Level')
plt.ylabel('Counts')
plt.show()



#HISTOGRAM
df['Level'].plot.hist(bins=10, figsize=(8, 5))
plt.xlabel('Level')
plt.ylabel('Counts')
plt.show()

#ROZKLAD
df['Level'].plot.kde(figsize=(8, 5))
plt.xlabel('Level')
plt.ylabel('Density')
plt.show()
