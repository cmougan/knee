# %%
import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns

plt.style.use("seaborn-whitegrid")
sns.set(style="whitegrid", color_codes=True)

rcParams["axes.labelsize"] = 14
rcParams["xtick.labelsize"] = 12
rcParams["ytick.labelsize"] = 12
rcParams["figure.figsize"] = 16, 8

warnings.filterwarnings("ignore")


def gradientbars(bars):
    grad = np.atleast_2d(np.linspace(0, 1, 256)).T
    ax = bars[0].axes
    lim = ax.get_xlim() + ax.get_ylim()
    for bar in bars:
        bar.set_zorder(1)
        bar.set_facecolor("none")
        x, y = bar.get_xy()
        w, h = bar.get_width(), bar.get_height()
        ax.imshow(grad, extent=[x, x + w, y, y + h], aspect="auto", zorder=0)
    ax.axis(lim)


# %%
# Read files
pain = pd.read_csv("data/pain.csv", skipinitialspace=True).drop(columns="Unnamed: 6")
pain.columns = pain.columns.str.replace(" ", "")
pain["date"] = pd.to_datetime(pain["date"], dayfirst=True)  # .dt.strftime('%d/%m/%Y')
pain = pain.set_index("date")
pain["year"] = pain.index.year
pain["week"] = pain.index.week
pain["week"] = pain["week"].apply(lambda x: "{0:0>2}".format(x))
pain.loc[
    (pain.week == 52) & (pain.year == 2022), "week"
] = 1  # First week fo 2022 problems
pain["yearWeek"] = pain["year"].astype(str) + "-" + pain["week"].astype(str)


sports = pd.read_csv("data/sport.csv", skipinitialspace=True)
sports.columns = sports.columns.str.replace(" ", "")
sports["date"] = pd.to_datetime(sports["date"], dayfirst=True)
sports["sport"] = sports["sport"].str.strip()
sports = sports.set_index("date")

full = pd.merge(pain.reset_index(), sports.reset_index())
full["week"] = full.date.dt.week
full["week"] = full["week"].apply(lambda x: "{0:0>2}".format(x))
full["year"] = full.date.dt.year
full.loc[
    (full.week == 52) & (full.year == 2022), "week"
] = 1  # First week fo 2022 problems
full["yearWeek"] = full["year"].astype(str) + "-" + full["week"].astype(str)

# %%
# ## Images


# Plot Weekly pain and accumulated knee work
# Data wrangling
aux = pain.reset_index()
aux = aux.groupby(["yearWeek"]).sum().reset_index()

# Init plot
fig, ax = plt.subplots()
plt.title("Dolor Semanal Acumulado y carga de entrenamiento en rodilla")
plt.ylabel("Unidades de Dolor")
plt.xlabel("Año-Semana")
# Weekly pain
bar = ax.bar(aux.yearWeek.values, aux.pain.values, label="Dolor Semanal")
gradientbars(bar)
# Plot PRPs
date1 = "2021-18"
date2 = "2021-27"
plt.bar(x=date1, height=22, width=0.1, color="k", label="PRP")
plt.bar(x=date2, height=22, width=0.1, color="k", label="PRP")
plt.plot(
    full.groupby("yearWeek").knee_intensity.sum() / 3, label="Entrenamiento rodilla"
)
ax.tick_params(axis="x", rotation=45)
plt.legend()
plt.savefig("images/dolor_semanal_carga.png")


# %%
aux = sports.groupby(["date", "sport"]).agg("sum").reset_index()
aux = pd.merge(pain.reset_index(), aux, on="date")
aux2 = pd.merge(aux[aux["sport"] == "Kite"], pain, on="date", how="right").fillna(0)
aux3 = pd.merge(aux[aux["sport"] == "CF"], pain, on="date", how="right").fillna(0)

fig, (ax1, ax2, ax3) = plt.subplots(3)
fig.suptitle("Vertically stacked subplots")
ax1.plot(aux.date, aux.pain)
ax2.bar(aux2.date, aux2.time)
ax3.bar(aux3.date, aux3.time)
plt.close()

# %%
aux = pd.merge(sports.reset_index(), pain.reset_index(), on="date")

aux.groupby(["date", "sport"]).sum().reset_index()
# Compute the correlation matrix
corr = aux.corr()

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))
plt.title("Matriz de correlacion entre variables")
# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(
    corr,
    mask=mask,
    cmap=cmap,
    vmax=0.3,
    center=0,
    square=True,
    linewidths=0.5,
    cbar_kws={"shrink": 0.5},
)
plt.savefig("images/corr.png")


# %%
post = pain[pain.index > "2021-05-06"].pain.values
pre = pain[pain.index < "2021-05-06"].pain.values

plt.figure()
plt.xlabel("Pain")
plt.ylabel("Frecuency of pain distribution")
sns.kdeplot(post, label="post prp")
sns.kdeplot(pre, label="pre prp")
plt.legend()
plt.title("Pain distribution before and after PRP")
plt.savefig("images/pain_distribution.png")

# %%
colag = pain[pain["colageno"] == True].pain.values
no_colag = pain[pain["colageno"] == False].pain.values

plt.figure()
plt.xlabel("Pain")
plt.ylabel("Frecuency of pain distribution")
sns.kdeplot(colag, label="Tomando Colágeno")
sns.kdeplot(no_colag, label="Sin Colágeno")
plt.legend()
plt.title("Pain distribution with and without colageno")
plt.savefig("images/colageno_distribution.png")

# %%
