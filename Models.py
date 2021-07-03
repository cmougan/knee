#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns

plt.style.use('seaborn-whitegrid')
sns.set(style='whitegrid', color_codes=True)


rcParams['axes.labelsize'] = 14
rcParams['xtick.labelsize'] = 12
rcParams['ytick.labelsize'] = 12
rcParams['figure.figsize'] = 16,8

warnings.filterwarnings('ignore')


# In[2]:


pain = pd.read_csv('data/pain.csv').drop(columns='Unnamed: 6')
pain.columns = pain.columns.str.replace(' ', '')
pain['date'] = pd.to_datetime(pain['date'] ,dayfirst=True)#.dt.strftime('%d/%m/%Y')
pain = pain.set_index('date')


# In[3]:


sports = pd.read_csv('data/sport.csv')
sports.columns = sports.columns.str.replace(' ', '')
sports['date'] = pd.to_datetime(sports['date'],dayfirst=True)
sports['sport'] = sports['sport'].str.strip()
sports = sports.set_index('date')


# In[4]:


pain.shape


# ## Crossfit

# In[5]:


cf = sports.reset_index().groupby(['date','sport']).sum().reset_index()
cf = cf[cf.sport=='CF']


# In[6]:


cf.columns = ['date', 'sport', 'total_intensity_CF', 'knee_intensity_CF', 'time']


# In[7]:


df = pain.join(cf.set_index('date').knee_intensity_CF)


# In[8]:


df.fillna(0,inplace=True)


# In[9]:


df['knee_intensity_CF_lag_1'] = df.knee_intensity_CF.shift(1)
df['knee_intensity_CF_lag_2'] = df.knee_intensity_CF.shift(2)
df['knee_intensity_CF_lag_3'] = df.knee_intensity_CF.shift(3)


# In[10]:


df.fillna(0,inplace=True)


# ## Kite

# In[11]:


kite = sports.reset_index().groupby(['date','sport']).sum().reset_index()
kite = kite[kite.sport=='Kite']


# In[12]:


kite.columns = ['date', 'sport', 'total_intensity_kite', 'knee_intensity_kite', 'time']


# In[13]:


df = df.join(kite.set_index('date').knee_intensity_kite)


# In[14]:


df.fillna(0,inplace=True)


# In[15]:


df['knee_intensity_kite_lag_1'] = df.knee_intensity_kite.shift(1)
df['knee_intensity_kite_lag_2'] = df.knee_intensity_kite.shift(2)
df['knee_intensity_kite_lag_3'] = df.knee_intensity_kite.shift(3)


# In[16]:


df.fillna(0,inplace=True)


# In[17]:


df


# ## Others

# In[18]:


aux = sports.reset_index().groupby(['date','sport']).sum().reset_index()
aux = aux[(aux.sport != 'CF') & (aux.sport != 'Kite')]


# In[19]:


aux.columns = ['date', 'sport', 'total_intensity_other', 'knee_intensity_other', 'time']


# In[20]:


df = df.join(aux.set_index('date').knee_intensity_other)


# In[21]:


df.fillna(0,inplace=True)


# In[22]:


df['knee_intensity_other_lag_1'] = df.knee_intensity_other.shift(1)
df['knee_intensity_other_lag_2'] = df.knee_intensity_other.shift(2)
df['knee_intensity_other_lag_3'] = df.knee_intensity_other.shift(3)


# In[23]:


df.fillna(0,inplace=True)


# ## Modeling

# In[24]:


from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

import shap
from sklearn.linear_model import Lasso
from sklearn.tree import DecisionTreeRegressor,plot_tree
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRFRegressor


# In[25]:


df = df.reset_index(drop=True)


# In[26]:


df.nsaids = df.nsaids.astype(bool)


# In[27]:


df.colageno = df.colageno.astype(bool)


# In[28]:


X_tr, X_te, y_tr, y_te = train_test_split(df.drop(columns='pain'), df[['pain']], test_size=0.1, random_state=42)


# ### Dummy

# In[29]:


mean_absolute_error(np.zeros_like(y_tr) + np.mean(y_tr).values, y_tr)


# In[30]:


mean_absolute_error(np.zeros_like(y_te) + np.mean(y_te).values, y_te)


# ### Lasso

# In[31]:


clf = Lasso(alpha=0.1)


# In[32]:


clf.fit(X_tr,y_tr)


# In[33]:


mean_absolute_error(clf.predict(X_tr),y_tr)


# In[34]:


mean_absolute_error(clf.predict(X_te),y_te)


# In[35]:


print("Model coefficients:\n")
for i in range(X_tr.shape[1]):
    print(X_tr.columns[i], "=", clf.coef_[i].round(4))


# ### Decision tree

# In[36]:


dt = DecisionTreeRegressor(max_depth=3,criterion='mae')
dt.fit(X_tr,y_tr)


# In[37]:


print('Decision Tree Results')


# In[38]:


print('Train ',mean_absolute_error(dt.predict(X_tr),y_tr))


# In[39]:


print('Test ',mean_absolute_error(dt.predict(X_te),y_te))


# In[40]:


plt.figure()
plot_tree(dt, feature_names=X_te.columns, filled=True);
plt.savefig('images/dt.svg',format='svg')
plt.show()


# ### Random Forest

# In[41]:


rf = RandomForestRegressor(min_samples_leaf=3)
rf.fit(X_tr,y_tr)


# In[42]:


print('RF results')


# In[43]:


print('Train',mean_absolute_error(rf.predict(X_tr),y_tr))


# In[44]:


print('Test',mean_absolute_error(rf.predict(X_te),y_te))


# ### Xgboost

# In[45]:


xgb = XGBRFRegressor().fit(X_tr,y_tr)
print('XGB Results')
print('Train ',mean_absolute_error(xgb.predict(X_tr),y_tr))


# In[46]:


print('Test ',mean_absolute_error(xgb.predict(X_te),y_te))


# # Shift

# In[47]:


df['pain_shift'] = df.pain - df.pain.shift()
df = df.dropna().drop(columns = 'pain')
X_tr, X_te, y_tr, y_te = train_test_split(df.drop(columns='pain_shift'), df[['pain_shift']], test_size=0.1, random_state=42)


# ### Dummy

# In[48]:


mean_absolute_error(np.zeros_like(y_tr) + np.mean(y_tr).values, y_tr)


# In[49]:


mean_absolute_error(np.zeros_like(y_te) + np.mean(y_te).values, y_te)


# ### Lasso

# In[50]:


clf = Lasso(alpha=0.1)


# In[51]:


clf.fit(X_tr,y_tr)


# In[52]:


mean_absolute_error(clf.predict(X_tr),y_tr)


# In[53]:


mean_absolute_error(clf.predict(X_te),y_te)


# In[54]:


print("Model coefficients:\n")
for i in range(X_tr.shape[1]):
    print(X_tr.columns[i], "=", clf.coef_[i].round(4))


# ### Decision tree

# In[66]:


dt = DecisionTreeRegressor(max_depth=3,min_samples_leaf=2,criterion='mae')
dt.fit(X_tr,y_tr)


# In[67]:


print('Decision Tree Results')


# In[68]:


print('Train ',mean_absolute_error(dt.predict(X_tr),y_tr))


# In[69]:


print('Test ',mean_absolute_error(dt.predict(X_te),y_te))


# In[71]:


plt.figure()
plot_tree(dt, feature_names=X_te.columns, filled=True);
plt.savefig('images/dt_shift.svg',format='svg')
plt.show()


# ### Random Forest

# In[60]:


rf = RandomForestRegressor(min_samples_leaf=3)
rf.fit(X_tr,y_tr)


# In[61]:


print('RF results')


# In[62]:


print('Train',mean_absolute_error(rf.predict(X_tr),y_tr))


# In[63]:


print('Test',mean_absolute_error(rf.predict(X_te),y_te))


# ### Xgboost

# In[64]:


xgb = XGBRFRegressor().fit(X_tr,y_tr)
print('XGB Results')
print('Train ',mean_absolute_error(xgb.predict(X_tr),y_tr))


# In[65]:


print('Test ',mean_absolute_error(xgb.predict(X_te),y_te))


# In[ ]:




