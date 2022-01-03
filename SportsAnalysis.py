# %%
import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns

import os
os.chdir('/Users/cmougan/Desktop/knee')

plt.style.use("seaborn-whitegrid")
sns.set(style="whitegrid", color_codes=True)


rcParams["axes.labelsize"] = 14
rcParams["xtick.labelsize"] = 12
rcParams["ytick.labelsize"] = 12
rcParams["figure.figsize"] = 16, 8

warnings.filterwarnings("ignore")

# %%


pain = pd.read_csv("data/pain.csv").drop(columns="Unnamed: 6")
pain.columns = pain.columns.str.replace(" ", "")
pain["date"] = pd.to_datetime(pain["date"], dayfirst=True)  # .dt.strftime('%d/%m/%Y')
pain = pain.set_index("date")


# %%


sports = pd.read_csv("data/sport.csv")
sports.columns = sports.columns.str.replace(" ", "")
sports["date"] = pd.to_datetime(sports["date"], dayfirst=True)
sports["sport"] = sports["sport"].str.strip()
sports = sports.set_index("date")


# %%


sports.sort_values(by="time", ascending=False)


# ## Sports

# In[4]:


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


# In[5]:


sports = sports.reset_index()
sports["week"] = sports.date.dt.week

# %%
aux = sports.groupby(["sport"])["time"].sum()
aux = aux.sort_values()
aux = aux / 60
# %%
def func(pct, allvals):
    absolute = int(np.round(pct / 100.0 * np.sum(allvals)))
    return "{:.1f}%\n({:d} h)".format(pct, absolute)


# %%
colors = sns.color_palette("pastel")[0 : aux.shape[0]]

# create pie chart
plt.figure()
plt.pie(aux.values, labels=aux.index, autopct=lambda pct: func(pct, aux.values))
plt.show()

# %%
## Total hours of Sport
sports['time'].sum()/pain.shape[0]

# ### Kite

# In[6]:


aux = sports.groupby(["sport", "week"]).sum().reset_index()
aux = aux[aux["sport"] == "Kite"]

fig, ax = plt.subplots()
bar = ax.bar(aux.week.values, aux.time.values)
gradientbars(bar)
plt.title("Kite Weekly Time")
plt.ylabel("Time (mins)")
plt.xlabel("Semana")
plt.show()


# In[7]:


aux = sports.groupby(["sport", "week"]).sum().reset_index()
aux = aux[aux["sport"] == "Kite"]

fig, ax = plt.subplots()
bar = ax.bar(aux.week.values, aux.total_intensity.values)
gradientbars(bar)
plt.title("Kite Weekly Total Intensity")
plt.ylabel("Intensity accumulated")
plt.xlabel("Semana")
plt.show()


# In[8]:


aux = sports.groupby(["sport", "week"]).sum().reset_index()
aux = aux[aux["sport"] == "Kite"]

fig, ax = plt.subplots()
bar = ax.bar(aux.week.values, aux.knee_intensity.values)
gradientbars(bar)
plt.title("Kite Weekly Knee Intensity")
plt.ylabel("Knee Intensity accumulated")
plt.xlabel("Semana")
plt.show()


# ### Crossfit

# In[9]:


aux = sports.groupby(["sport", "week"]).sum().reset_index()
aux = aux[aux["sport"] == "CF"]

fig, ax = plt.subplots()
bar = ax.bar(aux.week.values, aux.time.values)
gradientbars(bar)
plt.title("CrossFit Weekly Time")
plt.ylabel("Time (mins)")
plt.xlabel("Semana")
plt.show()


# In[10]:


aux = sports.groupby(["sport", "week"]).sum().reset_index()
aux = aux[aux["sport"] == "CF"]

fig, ax = plt.subplots()
bar = ax.bar(aux.week.values, aux.total_intensity.values)
gradientbars(bar)
plt.title("Crossfit Weekly Total Intensity")
plt.ylabel("Intensity accumulated")
plt.xlabel("Semana")
plt.show()


# In[11]:


aux = sports.groupby(["sport", "week"]).sum().reset_index()
aux = aux[aux["sport"] == "CF"]

fig, ax = plt.subplots()
bar = ax.bar(aux.week.values, aux.knee_intensity.values)
gradientbars(bar)
plt.title("Crossfit Weekly knee Intensity")
plt.ylabel("Intensity accumulated")
plt.xlabel("Semana")
plt.show()


# ### Natacion

# In[12]:


aux = sports.groupby(["sport", "week"]).sum().reset_index()
aux = aux[aux["sport"] == "Swim"]

fig, ax = plt.subplots()
bar = ax.bar(aux.week.values, aux.time.values)
gradientbars(bar)
plt.title("Swim Weekly Time")
plt.ylabel("Time (mins)")
plt.xlabel("Semana")
plt.show()


# In[13]:


aux = sports.groupby(["sport", "week"]).sum().reset_index()
aux = aux[aux["sport"] == "Swim"]

fig, ax = plt.subplots()
bar = ax.bar(aux.week.values, aux.total_intensity.values)
gradientbars(bar)
plt.title("Swim Weekly Total Intensity")
plt.ylabel("Intensity accumulated")
plt.xlabel("Semana")
plt.show()


# In[14]:


aux = sports.groupby(["sport", "week"]).sum().reset_index()
aux = aux[aux["sport"] == "Swim"]

fig, ax = plt.subplots()
bar = ax.bar(aux.week.values, aux.knee_intensity.values)
gradientbars(bar)
plt.title("Swim Weekly Knee Intensity")
plt.ylabel("Intensity accumulated")
plt.xlabel("Semana")
plt.show()


# In[ ]:


# ### Surf


# In[25]:


aux = sports.groupby(["sport", "week"]).sum().reset_index()
aux = aux[aux["sport"] == "Surf"]
aux = aux[aux.week > 20]
fig, ax = plt.subplots()
bar = ax.bar(aux.week.values, aux.time.values)
gradientbars(bar)
plt.title("Surf Weekly Time")
plt.ylabel("Time (mins)")
plt.xlabel("Semana")
plt.show()


# In[16]:


aux = sports.groupby(["sport", "week"]).sum().reset_index()
aux = aux[aux["sport"] == "Surf"]

fig, ax = plt.subplots()
bar = ax.bar(aux.week.values, aux.total_intensity.values)
gradientbars(bar)
plt.title("Surf Weekly Total Intensity")
plt.ylabel("Intensity accumulated")
plt.xlabel("Semana")
plt.show()


# In[17]:


aux = sports.groupby(["sport", "week"]).sum().reset_index()
aux = aux[aux["sport"] == "Surf"]

fig, ax = plt.subplots()
bar = ax.bar(aux.week.values, aux.knee_intensity.values)
gradientbars(bar)
plt.title("Surf Weekly Knee Intensity")
plt.ylabel("Intensity accumulated")
plt.xlabel("Semana")
plt.show()
