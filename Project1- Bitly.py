#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


#create path for txt file
path = 'Desktop/example.txt'


# In[3]:


#convert json string to DataFrame.
import json
df = [json.loads(line) for line in open(path)]


# In[4]:


df = pd.DataFrame(df)


# In[5]:


df.head()


# In[6]:


#show 10 largest tz's value (tz: timezone)
df['tz'].value_counts()


# In[7]:


# how many NaN values in column tz
df['tz'].isnull().sum()


# In[8]:


#check how many values in tz column are empty
(df['tz'].fillna('Missing') =='').sum()


# In[9]:


# form filter of empty values
empty_values = (df['tz'].fillna('Missing') =='')


# In[10]:


# convert empty value to 'Unknown'
df.loc[empty_values,'tz'] = 'Unknown'


# In[11]:


#plot 10 biggest values in tz column
import seaborn as sns
results_tz = df['tz'].value_counts().head(10)


# In[12]:


sns.barplot(x = results_tz.values,y = results_tz.index)


# In[13]:


#show values of 'a' column ('a' - agent)
df['a']


# In[14]:


#split values in 'a' column and get the 1st element. Then get 8 biggest values from that.
results_a = (pd.Series((str(x)).split()[0] for x in df['a'])).value_counts().head(8)


# In[15]:


#There are NaN value in results_a, name it by unknown.
results_a.index = ['Mozilla/5.0', 'Mozilla/4.0', 'GoogleMaps/RochesterNY', 'Unknown',
       'Opera/9.80', 'TEST_INTERNET_AGENT', 'GoogleProducer', 'Mozilla/6.0']


# In[16]:


results_a


# In[17]:


#plot 8 biggest agents
sns.barplot(x=results_a.values,y=results_a.index)


# In[18]:


# insert new column named 'os' ('operating system') with conditional logic, if there is string 'Windows' in values of column 'a' ,the according values for column 'os' will be Windowns
import numpy as np
df['os'] = np.where(df['a'].str.contains('Windows'),'Windows','Not Windows')


# In[19]:


#cal the size of column by dividing into 2 groups.
df.groupby('os').size()


# In[20]:


#group by 2 columns tz and os
by_tz_os = df.groupby(['tz', 'os'])


# In[21]:


# generate multi index Series with .size() and sum of each index
by_tz_os.size()


# In[22]:


# fill any NaN with value 0 and bring index of os become a column
agg_counts = by_tz_os.size().unstack().fillna(0)


# In[23]:


agg_counts


# In[24]:


#find index of 10 largest data, beacuse there are 2 columns, we need to group them so to find the sum of 2 columns
index_of10 = agg_counts.sum(1).nlargest(10).index


# In[25]:


#now break them back into 2 index (multiindex)
count_subset = agg_counts.loc[index_of10].stack()


# In[26]:


count_subset


# In[27]:


count_subset.name = 'total'


# In[28]:


# conver Series into DataFrame
count_subset = pd.DataFrame(count_subset)


# In[29]:


#reset index
count_subset.reset_index(inplace=True)


# In[30]:


count_subset


# In[31]:


#plot data by bar chart to see top timezone by Windows and non-Windows users
import seaborn as sns


# In[32]:


sns.barplot(x='total', y='tz', hue='os',  data=count_subset)


# In[33]:


count_subset.head()


# In[34]:


#Plot percenatge of Windows users in top 10 timezone
dff = count_subset


# In[35]:


dff = dff.set_index(['tz','os']).unstack()


# In[36]:


dff.head(2)


# In[37]:


dff.columns = ['Not Windows','Windows']


# In[38]:


dff['% Windows'] = dff['Windows']/(dff['Windows'] + dff['Not Windows'])


# In[39]:


dff['% Not Windows'] = (1- dff['% Windows'])


# In[40]:


dff.head()


# In[41]:


sns.barplot(y=dff.index, x = dff['% Windows'],data=dff)


# In[42]:


count_subset.head()


# In[43]:


#function of calculating % for Windows and non-Windows users:
def norm_total(group):
    group['normed_total'] = group.total/group.total.sum()
    return group


# In[44]:


#group by column tz and cal sum of 'total' values
count_subset.groupby('tz')['total'].sum()


# In[45]:


results2 = count_subset.groupby('tz').apply(norm_total)


# In[46]:


results2


# In[47]:


# plot the ratio of agent in top 10 timezone:


# In[48]:


df['agent'] = pd.Series(str(x).split()[0] for x in df['a'])


# In[49]:


df_agent_tz = df.groupby(['tz','agent']).size().unstack()


# In[50]:


results_a.drop(index='Unknown',inplace=True)


# In[51]:


df_agent_tz = df_agent_tz.loc[(y for y in results_tz.index),(x for x in results_a.index )]


# In[52]:


df_agent_tz = df_agent_tz.stack()


# In[53]:


#reset index
df_agent_tz = df_agent_tz.reset_index()


# In[54]:


df_agent_tz


# In[55]:


df_agent_tz.columns =['tz', 'agent', 'total']


# In[56]:


sns.barplot(x='total',y='tz', hue='agent',data= df_agent_tz,dodge= False)


# In[ ]:




