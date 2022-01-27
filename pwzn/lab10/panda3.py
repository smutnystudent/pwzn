import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

cd = pd.read_csv('owid-energy-data.csv')
cdwegiel = cd.fillna(0).groupby('country').agg(wegiel=('coal_consumption', np.sum))
print('Sumaryczne zużycie węgla na przestrzeni lat:')
print(cdwegiel)
wbr = cd.loc[cd['country']=='United Kingdom']
fra = cd.loc[cd['country']=='France']
nie = cd.loc[cd['country']=='Germany']
wlo = cd.loc[cd['country']=='Italy']
wbr = wbr[['year', 'coal_consumption']].values
fra = fra[['year', 'coal_consumption']].values
nie = nie[['year', 'coal_consumption']].values
wlo = wlo[['year', 'coal_consumption']].values
wbr = np.array(wbr).transpose()
fra = np.array(fra).transpose()
nie = np.array(nie).transpose()
wlo = np.array(wlo).transpose()
plt.plot(wbr[0], wbr[1], label='Wielka Brytania')
plt.plot(fra[0], fra[1], label='Francja')
plt.plot(nie[0], nie[1], label='Niemcy')
plt.plot(wlo[0], wlo[1], label='Włochy')
plt.xlabel('Rok')
plt.ylabel('Zużycie węgla')
plt.legend()
plt.show()