# %%
import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso,LinearRegression
from sklearn.metrics import mean_absolute_error,r2_score
from sklearn.dummy import DummyRegressor
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

# %%
data = [3.43,0.4303,2.0378,1,0.377,1.9759,0.3864]
y = [1.23,0.2647,1.4269,1,0.4801,1.3364,0.4685]
#data = [3.43,0.43,2.03,1,0.38,1.97,0.39]
#y = [1.546,0,1.7033,1,0,1.5761,0.5366]

# %%
df = pd.DataFrame(data = data,columns = ['ELISA'])

# %%
model = DummyRegressor()
model.fit(df,y)
print('r2',r2_score(model.predict(df),y))
print('r2 sqrt',np.sqrt(r2_score(model.predict(df),y)))
print('r2 **2',r2_score(model.predict(df),y)**2)
print('MAE',mean_absolute_error(model.predict(df),y))

# %%
model = LinearRegression()
model.fit(df,y)
print('r2',r2_score(model.predict(df),y))
print('r2 sqrt',np.sqrt(r2_score(model.predict(df),y)))
print('r2 **2',r2_score(model.predict(df),y)**2)
print('MAE',mean_absolute_error(model.predict(df),y))
# %%
'''
best = 100000
for i in np.linspace(0.0000000000000000001,0.01,20):
    model = Lasso(alpha=i)
    model.fit(df,y)
    print('r2',r2_score(model.predict(df),y))
    print('MAE',mean_absolute_error(model.predict(df),y))
    if mean_absolute_error(model.predict(df),y)<best:
        best = mean_absolute_error(model.predict(df),y)
        best_param = i
    
'''
# %%
plt.figure()
sns.scatterplot(x = data,y = model.predict(df),label='Preds')
sns.scatterplot(x = data,y = y,label='Real')
sns.lineplot(x = data,y = model.predict(df))
plt.ylabel('YY')
plt.xlabel('XX')
plt.title('TITLE')
plt.show()

# %%
