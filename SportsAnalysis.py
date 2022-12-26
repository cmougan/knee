# %%
import numpy as np
import pandas as pd

import os

os.chdir("/Users/cmougan/Desktop/knee")

import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
from utils import gradientbars

plt.style.use("seaborn-whitegrid")
sns.set(style="whitegrid", color_codes=True)
rcParams["axes.labelsize"] = 14
rcParams["xtick.labelsize"] = 12
rcParams["ytick.labelsize"] = 12
rcParams["figure.figsize"] = 16, 8

import warnings

warnings.filterwarnings("ignore")
# %%
# Read Files
pain = pd.read_csv("data/pain.csv", skipinitialspace=True)
pain.columns = pain.columns.str.replace(" ", "")
pain["date"] = pd.to_datetime(pain["date"], dayfirst=True)  # .dt.strftime('%d/%m/%Y')
pain = pain.set_index("date")
pain["year"] = pain.index.year
pain["week"] = pain.index.week
pain["week"] = pain["week"].apply(lambda x: "{0:0>2}".format(x))
pain["month"] = pain.index.month
pain["month"] = pain["month"].apply(lambda x: "{0:0>2}".format(x))
pain.loc[
    (pain.week == 52) & (pain.year == 2022), "week"
] = 1  # First week fo 2022 problems
pain["yearWeek"] = pain["year"].astype(str) + pain["week"].astype(str)


sports = pd.read_csv("data/sport.csv", skipinitialspace=True)
sports.columns = sports.columns.str.replace(" ", "")
sports["date"] = pd.to_datetime(sports["date"], dayfirst=True)
sports["sport"] = sports["sport"].str.strip()
sports["year"] = sports.date.dt.year
sports["week"] = sports.date.dt.week
sports["week"] = sports["week"].apply(lambda x: "{0:0>2}".format(x))
sports["month"] = sports.date.dt.month
sports["month"] = sports["month"].apply(lambda x: "{0:0>2}".format(x))
sports.loc[
    (sports.week == 52) & (sports.year == 2022), "week"
] = 1  # First week fo 2022 problems
sports["yearWeek"] = sports["year"].astype(str) + sports["week"].astype(str)
sports["yearMonth"] = sports["year"].astype(str) + sports["month"].astype(str)

sports = sports.set_index("date")

full = pd.merge(pain.reset_index(), sports.reset_index())
full["week"] = full.date.dt.week
full["month"] = full.date.dt.month
full["week"] = full["week"].apply(lambda x: "{0:0>2}".format(x))
full["month"] = full["month"].apply(lambda x: "{0:0>2}".format(x))
full["year"] = full.date.dt.year
full.loc[
    (full.week == 52) & (full.year == 2022), "week"
] = 1  # First week fo 2022 problems
full["yearWeek"] = full["year"].astype(str) + full["week"].astype(str)
full["yearMonth"] = full["year"].astype(str) + full["month"].astype(str)


# %%
# Util function
def func(pct, allvals):
    absolute = int(np.round(pct / 100.0 * np.sum(allvals)))
    return "{:.1f}%\n({:d} h)".format(pct, absolute)


aux = sports[sports["year"] == 2022].groupby(["sport"])["time"].sum()
aux
aux = aux.sort_values()
aux = aux / 60
colors = sns.color_palette("pastel")[0 : aux.shape[0]]
# Create pie chart
plt.figure()
explode = np.zeros(len(aux.values))
explode = np.clip(explode, 0.05, 0.05)
print(len(explode))
plt.pie(
    aux.values,
    labels=aux.index,
    autopct=lambda pct: func(pct, aux.values),
    shadow=True,
    explode=explode,
)
plt.savefig("images/accumulated_sport.png")
# %%
vals = sports.groupby(["date"]).time.sum().values
plt.figure()
plt.title("Distribution de tiempo diaro de deporte practicado")
sns.kdeplot(vals, shade=True, color="r", label="Minutos Deporte")
plt.vlines(vals.mean(), 0, 0.01, color="k", linestyle="--", label="Media")
plt.legend()
plt.savefig("images/sportTimeDistribution.png")
plt.show()


# %%
## Total hours of Sport
print("Average daily sport in mins: ", sports["time"].sum() / pain.shape[0])
## Still days
print("Still days: ", sports[sports["sport"] == "None"].shape[0])
# %%
# Kite
aux = sports.groupby(["yearMonth", "sport"]).sum().reset_index()
aux = pd.merge(aux, aux[aux["sport"] == "Kite"], on="yearMonth", how="left").fillna(0)

fig, ax = plt.subplots()
bar = ax.bar(aux.yearMonth.values, aux.time_y.values)
gradientbars(bar)
plt.title("Kite Monthly Time")
plt.ylabel("Time (mins)")
plt.xlabel("Semana")
ax.tick_params(axis="x", rotation=45)


# %%
# Crossfit
aux = sports.groupby(["yearMonth", "sport"]).sum().reset_index()
aux = pd.merge(aux, aux[aux["sport"] == "CF"], on="yearMonth", how="left").fillna(0)

fig, ax = plt.subplots()
bar = ax.bar(aux.yearMonth.values, aux.time_y.values)
gradientbars(bar)
plt.title("CrossFit Monthly Time")
plt.ylabel("Time (mins)")
plt.xlabel("Semana")
ax.tick_params(axis="x", rotation=45)

# %%
# Natacion
aux = sports.groupby(["yearMonth", "sport"]).sum().reset_index()
aux = pd.merge(aux, aux[aux["sport"] == "Swim"], on="yearMonth", how="left").fillna(0)
fig, ax = plt.subplots()
bar = ax.bar(aux.yearMonth.values, aux.time_y.values)
gradientbars(bar)
plt.title("Swim Monthly Time")
plt.ylabel("Time (mins)")
plt.xlabel("Semana")
ax.tick_params(axis="x", rotation=45)

# %%
#  Surf
aux = sports.groupby(["yearMonth", "sport"]).sum().reset_index()
aux = pd.merge(aux, aux[aux["sport"] == "Surf"], on="yearMonth", how="left").fillna(0)
fig, ax = plt.subplots()
bar = ax.bar(aux.yearMonth.values, aux.time_y.values)
gradientbars(bar)
plt.title("Surf Monthly Time")
plt.ylabel("Time (mins)")
plt.xlabel("Semana")
ax.tick_params(axis="x", rotation=45)

# %%
