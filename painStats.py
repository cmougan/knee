# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use("seaborn-whitegrid")
from scipy import stats

# %%
df = pd.read_csv("data/pain.csv")
# %%
# Plot pain distribution
plt.figure(figsize=(10, 6))
sns.kdeplot(df["pain"], shade=True, color="r", label="Dolor", alpha=0.5)
plt.vlines(df["pain"].mean(), 0, 0.7, color="r", linestyles="--", label="Media")
plt.title("Distribucion diaria de dolor")
plt.xlabel("Dolor")
plt.ylabel("Densidad")
plt.savefig("images/painStats.png")
plt.legend()
plt.show()
# %%
stats.percentileofscore(df["pain"], 0.1)
# %%
stats.percentileofscore(df["pain"], 2.1)
# %%
