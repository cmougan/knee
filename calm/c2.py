# %%
import pandas as pd
import seaborn as sns

# %%
a = pd.read_json("https://calmcode.io/challenge/message.json")

# %%
c = []
for i in range(0, len(set(a["i"]))):
    d = ""
    for j in range(0, len(set(a["j"]))):
        v = a[(a["i"] == i) & (a["j"] == j)]
        if v.empty == False:
            b = v["value"][v.index[0]]
            d = d + b
        else:
            d = d + " "
    c.append(d)
# %%
pd.DataFrame(c).to_csv("calm/message2.csv")

# %%
print(pd.DataFrame(c))
# %%
