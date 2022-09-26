# %%
import pandas as pd
import seaborn as sns

# %%
a = pd.read_csv("https://calmcode.io/challenge/message.csv")
# %%
sns.scatterplot(x="x", y="y", data=a)
