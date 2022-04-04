# %%
import pandas as pd
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")
plt.style.use("seaborn-whitegrid")
# %%
df = pd.read_csv("Suspensos.csv", encoding="utf-8")
df = df[df["4EB"] != "Quintero Montero, Danelson"]
# %%
plt.figure()
plt.title('Total de suspensos por Alumno/a')
df.plot.bar(
    x="4EB",
    y=["SUSPENSOS EV 1","SUSPENSOS EV 2"],
    width=0.7,
    linewidth=1,
    edgecolor="black",
    color = ['yellow','cornflowerblue']
)
plt.savefig("suspensos.png")
plt.show()
# %%
plt.figure()
sns.barplot(x="4EB", y="SUSPENSOS EV 1", data=df)
plt.tick_params(axis="x", rotation=90)
plt.show()

plt.figure()
sns.barplot(x="4EB", y="SUSPENSOS EV 2", data=df)
plt.tick_params(axis="x", rotation=90)
plt.show()


# %%


"""
# %%
cols = ['GeH', 'LCL', 'MAC', 'MAP', 'ING', 'ByG', 'ECO', 'FyQ',
       'LAT', 'CAAP', 'IAEyE', 'EF', 'REL', 'VE', 'REV', 'CCI', 'MUS', 'FR2',
       'TIC', 'RMT', 'TEC (Esp)', 'ByG.1', 'FyQ.1', 'GeH.1', 'LCL.1', 'MAC.1',
       'MAP.1', 'ING.1', 'TEC', 'FR2.1', 'FyQ.2', 'GeH.2', 'LCL.2', 'MAT',
       'ING.2', 'EPVA', 'TEC.1', 'VE.1', 'ByG.2']
# %%
suspensos = defaultdict()
for index, row in df.iterrows():
    sus = 0
    for col in cols:
        if row[col]<5:
            sus = sus + 1

    suspensos[row['Alumno/a']] = sus

# %%
suspensos.pop('Quintero Montero, Danelson')
suspensos = pd.DataFrame.from_dict(suspensos, orient='index',columns = ['Suspensos']).reset_index()
# %%

suspensos.plot.bar()


# %%
plt.figure()
plt.title('Primera Evaluación')
sns.barplot(x='Suspensos', y='index', data=suspensos)
plt.tight_layout() 
plt.savefig('suspensos1.png')
plt.show()
# %%

# %%
"""
