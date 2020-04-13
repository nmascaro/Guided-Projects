#!/usr/bin/env python
# coding: utf-8

# In this course, we've been creating plots using pyplot and matplotlib directly. When we want to explore a new dataset by quickly creating visualizations, using these tools directly can be cumbersome. Thankfully, pandas has many methods for quickly generating common plots from data in DataFrames. Like pyplot, the plotting functionality in pandas is a wrapper for matplotlib. This means we can customize the plots when necessary by accessing the underlying Figure, Axes, and other matplotlib objects.
# 
# In this guided project, we'll explore how using the pandas plotting functionality along with the Jupyter notebook interface allows us to explore data quickly using visualizations. If you're new to either our guided projects or Jupyter notebook in general, you can learn more here. You can find the solutions to this guided project here.
# 
# We'll be working with a dataset on the job outcomes of students who graduated from college between 2010 and 2012. The original data on job outcomes was released by American Community Survey, which conducts surveys and aggregates the data. FiveThirtyEight cleaned the dataset and released it on their Github repo.
# 
# Each row in the dataset represents a different major in college and contains information on gender diversity, employment rates, median salaries, and more. Here are some of the columns in the dataset:
# 
# Rank - Rank by median earnings (the dataset is ordered by this column).
# Major_code - Major code.
# Major - Major description.
# Major_category - Category of major.
# Total - Total number of people with major.
# Sample_size - Sample size (unweighted) of full-time.
# Men - Male graduates.
# Women - Female graduates.
# ShareWomen - Women as share of total.
# Employed - Number employed.
# Median - Median salary of full-time, year-round workers.
# Low_wage_jobs - Number in low-wage service jobs.
# Full_time - Number employed 35 hours or more.
# Part_time - Number employed less than 35 hours.
# Using visualizations, we can start to explore questions from the dataset like:
# 
# Do students in more popular majors make more money?
# (Using scatter plots)
# How many majors are predominantly male? Predominantly female?
# (Using histograms)
# Which category of majors have the most students?
# (Using bar plots)
# 
# We'll explore how to do these and more while primarily working in pandas. Before we start creating data visualizations, let's import the libraries we need and remove rows containing null values.

# In[56]:


#Import pandas and matplotlib into the environment
import pandas as pd
import matplotlib.pyplot as plt
#Run the Jupyter magic %matplotlib inline so that plots are displayed inline.
get_ipython().magic('matplotlib inline')


# In[57]:


#Read the dataset into a DataFrame and start exploring the data.
recent_grads = pd.read_csv('recent-grads.csv')
recent_grads.iloc[0]


# In[58]:


recent_grads.head()


# In[59]:


recent_grads.tail()


# In[60]:


recent_grads.describe()


# In[61]:


# Drop rows with missing values. Matplotlib expects that columns of 
# values we pass in have matching lengths and missing values will 
# cause matplotlib to throw errors.
raw_data_count = 173
recent_grads = recent_grads.dropna()


# In[62]:


recent_grads.describe()


# In[63]:


cleaned_data_count = 172 


# Generate scatter plots in separate jupyter notebook cells to explore the following relations:
# -Sample_size and Median
# -Sample_size and Unemployment_rate
# -Full_time and Median
# -ShareWomen and Unemployment_rate
# -Men and Median
# -Women and Median
# 
# Use the plots to explore the following questions:
# -Do students in more popular majors make more money?
# -Do students that majored in subjects that were majority female make more money?
# -Is there any link between the number of full-time employees and median salary?

# In[64]:


#Sample_size and Median
ax = recent_grads.plot(x='Median', y='Sample_size', kind='scatter')


# In[65]:


#Sample_size and Unemployment_rate
ax = recent_grads.plot(x='Sample_size', y='Unemployment_rate', kind='scatter')


# In[66]:


#Full_time and Median
ax = recent_grads.plot(x='Full_time', y='Median', kind='scatter')


# In[67]:


#ShareWomen and Unemployment_rate
ax = recent_grads.plot(x='ShareWomen', y='Unemployment_rate', kind='scatter')


# In[68]:


#Men and Median
ax = recent_grads.plot(x='Men', y='Median', kind='scatter')


# In[69]:


#Women and Median
ax = recent_grads.plot(x='Women', y='Median', kind='scatter')


# In[70]:


#Do students in more popular majors make more money?
recent_grads.plot(x='Total', y='Median', kind='scatter')


# From the above scatter plot, there seems to be a weak negative correlation with popularity of major and median salary

# In[71]:


#Do students that majored in subjects that were 
#majorly female make more money?
recent_grads.plot(x='ShareWomen', y='Median', kind='scatter')


# There is a weak but negative correlation between concentration of women in a particular major and the median salary associated with that major.

# In[72]:


#Is there any link between the number 
#of full-time employees and median salary?
recent_grads.plot(x='Full_time', y='Median', kind='scatter')


# There appears to be a negative correlation. This implies as the labor market supply increases, the median salary tends to decrease. This can be due to a few factors but most likely simple labor supply/demand dynamics.

# Generate histograms in separate jupyter notebook cells to explore the distributions of the following columns:
# -Sample_size
# -Median
# -Employed
# -Full_time
# -ShareWomen
# -Unemployment_rate
# -Men
# -Women

# Generate histograms in separate jupyter notebook cells to explore the distributions of the following columns: Sample_size, Median, Employed, Full_time, ShareWomen, Unemployment_rate, Men, Women
# 
# Use the plots to explore the following questions:
# 
# -What percent of majors are predominantly male? Predominantly female?
# To determine this, lets look
# 
# -What's the most common median salary range?

# In[73]:


recent_grads['Sample_size'].hist(bins=25, range=(0,5000))


# In[74]:


recent_grads['Median'].plot(kind='hist')


# In[75]:


recent_grads['Employed'].hist(bins=25, range=(0,5000))


# In[76]:


recent_grads['Full_time'].hist(bins=25, range=(0,5000))


# In[77]:


recent_grads['ShareWomen'].plot(kind='hist')


# In[78]:


recent_grads['Unemployment_rate'].plot(kind='hist')


# In[79]:


recent_grads['Men'].hist(bins=25, range=(0,5000))


# In[80]:


recent_grads['Women'].hist(bins=25, range=(0,5000))


# In[81]:


#Instead of seperate cells, we could also do a for loop, "for" fun:
cols = ['Sample_size', 'Median', 'Employed', 'Full_time', 'ShareWomen', 'Unemployment_rate', 'Men', 'Women']

fig, ax = plt.subplots(figsize=(12,30))
plt.xticks([])
plt.yticks([])

for i in range(8):
    ax = fig.add_subplot(8,1,i+1)
    ax = recent_grads[cols[i]].hist(bins=10)


# Use the plots to explore the following questions:
# 
# -What percent of majors are predominantly male? Predominantly female?
# To determine this, lets look at the x values on the ShareWomen plot with x values above 50% or 0.5. From looking at those values we can add them up and ddetermine the total percentage. 0.5-0.6 is about 23, 0.6-0.7 is 25, 0.7-0.8 is about 29, 0.8-0.9 is about 11, 0.9-1.0 is about 12. Adding these up, we get: 23+25+29+11+12= 100 out of 172 majors, so approximately 58% of all majors are predominantly women. Retroactively this means that 42% of all majors are predominately male.
# 
# -What is the most common median salary range?
# Very obvious from the histogram, it is the range from $30,000-$40,000

# 4. Pandas, Scatter Matrix Plot
# 
# This step focusses on utilizing the scatter_matrix from the pandas.plotting module

# In[82]:


import pandas.plotting as scatter


# In[85]:


#Create a 2 by 2 scatter matrix plot using the Sample_size and Median columns.
scatter.scatter_matrix(recent_grads[['Sample_size', 'Median']], figsize=(10,10))


# In[86]:


#Create a 3 by 3 scatter matrix plot using the Sample_size, Median, and Unemployment_rate columns
scatter.scatter_matrix(recent_grads[['Sample_size', 'Median','Unemployment_rate']], figsize=(10,10))


# In[89]:


#Use bar plots to compare the percentages of women (ShareWomen) from the first ten rows 
#and last ten rows of the recent_grads dataframe.
recent_grads.head(10).plot.bar(x='ShareWomen', y='Total')


# In[90]:


recent_grads.tail(10).plot.bar(x='ShareWomen', y='Total')


# In[93]:


# Use bar plots to compare the unemployment rate (Unemployment_rate) from the first ten rows 
# and last ten rows of the recent_grads dataframe.
recent_grads.head(10).plot.bar(x='Unemployment_rate', y='Full_time')


# In[92]:


recent_grads.tail(10).plot.bar(x='Unemployment_rate', y='Full_time')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




