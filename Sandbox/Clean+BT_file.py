
# coding: utf-8

# In[1]:

import pandas as pd
from sqlalchemy import create_engine


# In[2]:

BT_all = pd.read_csv('/users/jdlara/Documents/Box Sync/EPIC-Biomass/Biomass data/BillionTonUpdateForestResources/KDF_Frst_LOGTOF.dat', encoding='UTF-8', delimiter = ',', dtype = {'fcode':str})
BT_all = BT_all.fillna(0)
FIPS_all = pd.read_csv('/users/jdlara/Documents/Box Sync/EPIC-Biomass/Biomass data/BillionTonUpdateForestResources/fips_codes2.csv', encoding='UTF-8', dtype = {'State FIPS Code':str,'County FIPS Code':str})
FIPS_all['fcode'] = FIPS_all[['State FIPS Code', 'County FIPS Code']].apply(lambda x: ''.join(x), axis=1)
FIPS_all = FIPS_all.loc[FIPS_all['Entity Description'] == 'County']
FIPS_all = FIPS_all.set_index('fcode')


# In[3]:

df_join = BT_all.join(FIPS_all, on = 'fcode')


# In[4]:

engine = create_engine('postgresql+pg8000://jdlara:Bario-140@switch-db2.erg.berkeley.edu:5432/APL_CEC?ssl=true&sslfactory=org.postgresql.ssl.NonValidatingFactory')


# In[ ]:




# In[5]:

df_join.to_sql('KDF_Frst_LOGTOF', engine, schema='Billion_TON', if_exists = 'replace', chunksize = 10)


# In[ ]:


# In[ ]:



