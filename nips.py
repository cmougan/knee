# %%
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

url = "https://papers.nips.cc/paper/2017"
req = requests.get(url)
soup = BeautifulSoup(req.content, "html.parser")

# Find all li tag
datas = soup.find_all("li")
# %%
titles = []
for data in datas[2:]:
    titles.append(data.find("a").getText())

# %%
count = defaultdict()
keys = ["Shift", "shift"]
for i, title in enumerate(titles):
    if any(key in title for key in keys):
        count[i] = title

# %%
print("Total number of papers:", len(datas[2:]))
print("Papers with shift:", len(count))

# %%
