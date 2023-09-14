# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use("seaborn-whitegrid")
from scipy import stats

# %%
# Read data
df = pd.read_csv("data/pain.csv", index_col=0)
# Drop last row
df = df.drop(df.tail(1).index)
# Parse dates
df.index = pd.to_datetime(df.index, format="%d-%m-%Y")
# Convert to numeric
df["knee_pain"] = pd.to_numeric(df["knee_pain"])

# %%
# Plot pain distribution
plt.figure(figsize=(10, 6))
sns.kdeplot(df["knee_pain"], shade=True, color="r", label="Dolor", alpha=0.5)
plt.vlines(df["knee_pain"].mean(), 0, 0.7, color="r", linestyles="--", label="Media")
plt.title("Distribucion diaria de dolor")
plt.xlabel("Dolor")
plt.ylabel("Densidad")
plt.savefig("images/painStats.png")
plt.legend()
plt.show()
# %%
surgery_date = pd.to_datetime("28-4-2023", format="%d-%m-%Y")
# %%
# Get 180 days before surgery
df_before = df.loc[
    (df.index > surgery_date - pd.Timedelta(days=90))
    & (df.index < surgery_date - pd.Timedelta(days=30))
]
# Get 180 days after surgery
df_after = df.loc[
    (df.index < surgery_date + pd.Timedelta(days=90))
    & (df.index > surgery_date + pd.Timedelta(days=30))
]

# Stats test that distributions are the same
pvalue = stats.ttest_ind(df_before["knee_pain"], df_after["knee_pain"])[1]
print("Ttest Pvalue: {:.2f}".format(pvalue))
# KS test
pvalue = stats.ks_2samp(df_before["knee_pain"], df_after["knee_pain"])[1]
print("KS test Pvalue: {:.2f}".format(pvalue))

# %%
# Plot pain distribution
plt.figure(figsize=(10, 6))
plt.title(
    "Dolor antes y despues(180d) de Artroscopia Pvalue={:.2f} -- No hay diferencia".format(
        pvalue
    )
)
sns.kdeplot(
    df_before["knee_pain"], fill=True, color="r", label="Dolor antes", alpha=0.1
)
sns.kdeplot(
    df_after["knee_pain"], fill=True, color="b", label="Dolor despues", alpha=0.1
)
plt.xlabel("Dolor Rodilla")
plt.ylabel("Densidad")
plt.legend()
plt.show()

# %%
# Data Aggregation
# Group by year and month
df["year"] = df.index.year
df["month"] = df.index.month


df_grouped = df.groupby(["year", "month"]).mean().reset_index()
# Year month feature
df_grouped["year-month"] = pd.to_datetime(
    df_grouped["year"].astype(str) + "-" + df_grouped["month"].astype(str)
)

# Remove first row
df_grouped = df_grouped.iloc[1:]


# %%
# Calculate the moving average with a window size of your choice (e.g., 3 months)
window_size = 4
df_grouped["smoothed_knee_pain"] = (
    df_grouped["knee_pain"].rolling(window=window_size).mean()
)

# Plot pain distribution with smoothing
plt.figure(figsize=(10, 6))
plt.title("Dolor mensual (con smoothing)")
# plt.plot(df_grouped["year-month"], df_grouped["knee_pain"], color="r", label="Dolor")
plt.plot(
    df_grouped["year-month"],
    df_grouped["smoothed_knee_pain"],
    color="b",
    label=f"Dolor ({window_size}-month MA)",
)
plt.xlabel("Mes")
plt.ylabel("Dolor Rodilla")
plt.legend()
plt.show()


# %%
window_size = 30
df["smoothed_knee_pain"] = (
    df["knee_pain"].rolling(window=window_size).mean()
)
# Plot pain distribution with smoothing
plt.figure(figsize=(10, 6))
plt.title("Dolor diario (con smoothing)")
plt.plot(
    df.index,
    df["smoothed_knee_pain"],
    color="b",
    label=f"Dolor ({window_size}-days MA)",
)
plt.xlabel("Mes")
plt.ylabel("Dolor Rodilla")
plt.legend()
plt.show()

# %%
