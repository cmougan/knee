# %%
from PIL import Image
import requests
from io import BytesIO

response = requests.get('https://calmcode.io/challenge/ghost.png')
img = Image.open(BytesIO(response.content))
# %%
img
# %%
import torch
# %%
