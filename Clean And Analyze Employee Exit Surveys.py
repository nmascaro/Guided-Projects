#!/usr/bin/env python
# coding: utf-8

# In this guided project, we'll work with exit surveys from employees of the Department of Education, Training and Employment (DETE) and the Technical and Further Education (TAFE) institute in Queensland, Australia.
# 
# In this project, we'll play the role of data analyst and pretend our stakeholders want to know the following:
# 
# -Are employees who only worked for the institutes for a short period of time resigning due to some kind of dissatisfaction? What about employees who have been there longer?
# -Are younger employees resigning due to some kind of dissatisfaction? What about older employees?
# 
# They want us to combine the results for both surveys to answer these questions. However, although both used the same survey template, one of them customized some of the answers. Let's start by reading the datasets into pandas and exploring them.

# In[105]:


#Import pandas and NumPy, read datasets into pandas
import pandas as pd
import numpy as np

dete_survey = pd.read_csv("dete_survey.csv")
tafe_survey = pd.read_csv("tafe_survey.csv")


# In[106]:


#Let's take an initial look into the dataframes

dete_survey.head()
dete_survey.info()
dete_survey.isnull().sum()


# In[107]:


tafe_survey.head()
tafe_survey.info()
tafe_survey.isnull().sum()


# After a brief look at the properties of these datasets, I have a few initial observations:
# 
# - Both datasets have missing values, however tafe_survey has significantly more, this may be due to these survey questions being optional or conditional upon a previous question that wasn't answered in a way that met that condition. 
# -The dete_survey contains "Not Stated" missing values but aren't represented as "Nan" so those need to get cleaned up
# -defe_survey has 822 rows and 56 columns, tafe_survey has 702 rows and 72 columns. Lots of the columns have similar values but are named differently; this will definitely be a step later on I can already tell. This shouldn't be too much of an issue as we don't have to use all of the columns, I might just need some but let's keep going and find out!

# In[108]:


#let's reread in dete_survey again and fix those NaN values(or soon to be NaN):

dete_survey = pd.read_csv("dete_survey.csv",na_values = "Not Stated")

#and we'll drop a few unnecessary columns, save into a new variable to stay safe:

dete_survey_updated = dete_survey.drop(dete_survey.columns[28:49],axis=1)
tafe_survey_updated = tafe_survey.drop(tafe_survey.columns[17:66],axis=1)


# So the main columns we're concerned with for our final analysis are:
# dete_survey: ID, SeperationType, Cease Date, DETE Start Date, Age, and Gender.
# tafe_survey: Record ID, Reason for ceasing employment, CESSATION YEAR, 	LengthofServiceOverall, Overall Length of Service at Institute (in years), CurrentAge, Current Age, Gender, What is your gender?
# 
# It's obvious we'll have to rename columns to a standardized format and combine the data properly so we can perform a clean analysis of both datasets.

# In[109]:


#Rename the remaining columns in the dete_survey_updated dataframe.
dete_survey_updated.columns = dete_survey_updated.columns.str.replace('.','').str.replace('\s+', '_').str.strip().str.lower()
print(dete_survey_updated.columns)


# In[110]:



# Update column names to match the names in dete_survey_updated
updated_cols = {'Record ID': 'id', 'CESSATION YEAR': 'cease_date', 'Reason for ceasing employment': 'separationtype', 'Gender. What is your Gender?': 'gender', 'CurrentAge. Current Age': 'age',
       'Employment Type. Employment Type': 'employment_status',
       'Classification. Classification': 'position',
       'LengthofServiceOverall. Overall Length of Service at Institute (in years)': 'institute_service',
       'LengthofServiceCurrent. Length of Service at current workplace (in years)': 'role_service'}
tafe_survey_updated = tafe_survey_updated.rename(updated_cols, axis = 1)

# Check that the specified column names were updated correctly
tafe_survey_updated.columns


# In the last screen, we renamed the columns that we'll use in our analysis. Next, let's remove more of the data we don't need.
# 
# Recall that our end goal is to answer the following question:
# 
# Are employees who have only worked for the institutes for a short period of time resigning due to some kind of dissatisfaction? What about employees who have been at the job longer?
# 
# If we look at the unique values in the separationtype columns in each dataframe, we'll see that each contains a couple of different separation types. For this project, we'll only analyze survey respondents who resigned, so their separation type contains the string 'Resignation'.

# In[111]:


dete_survey_updated['separationtype'].value_counts()


# In[112]:


tafe_survey_updated['separationtype'].value_counts()


# In[113]:


# Update all separation types containing the word "resignation" to 'Resignation'
dete_survey_updated['separationtype'] = dete_survey_updated['separationtype'].str.split('-').str[0]

# Check the values in the separationtype column were updated correctly
dete_survey_updated['separationtype'].value_counts()


# In[114]:


# Select only the resignation separation types from each dataframe
dete_resignations = dete_survey_updated[dete_survey_updated['separationtype'] == 'Resignation'].copy()
tafe_resignations = tafe_survey_updated[tafe_survey_updated['separationtype'] == 'Resignation'].copy()


# So what I just did was standardize the 3 different 'resignation' types in dete_survey_updated, selected only resignation separation types, and assigned it to dete_resignations. I did the same selection and reassigning to tafe_resignations
# 
# Now, before we start cleaning and manipulating the rest of our data, let's verify that the data doesn't contain any major inconsistencies (to the best of our knowledge). When you're working with real world data, don't assume that the data you're analyzing isn't corrupted in some way!
# 
# It may not always be possible to catch all of these errors, but by making sure the data seems reasonable to the best of our knowledge, we can stop ourselves from completing a data analysis project that winds up being useless because of bad data.

# In[115]:


dete_resignations['cease_date'].value_counts()


# In[116]:


# Extract the years and convert them to a float type
dete_resignations['cease_date'] = dete_resignations['cease_date'].str.split('/').str[-1]
dete_resignations['cease_date'] = dete_resignations['cease_date'].astype("float")

# Check the values again and look for outliers
dete_resignations['cease_date'].value_counts()


# In[117]:


dete_resignations['cease_date'].value_counts().sort_index(ascending=True)


# In[118]:


dete_resignations['dete_start_date'].value_counts().sort_index(ascending=True)


# In[119]:


tafe_resignations['cease_date'].value_counts().sort_index(ascending=True)


# From the work we did in the last screen, we can verify:
# 
# There aren't any major issues with the years.
# The years in each dataframe don't span quite the same number of years. We'll leave it up to your discretion to drop any years you don't think are needed for the analysis.
# 
# You may have noticed that the tafe_resignations dataframe already contains a "service" column, which we renamed to institute_service. In order to analyze both surveys together, we'll have to create a corresponding institute_service column in dete_resignations.

# In[120]:


#Create an institute_service column in dete_resignations

dete_resignations['institute_service']= dete_resignations['cease_date']-dete_resignations['dete_start_date']


# Next, we'll identify any employees who resigned because they were dissatisfied.
# 
# Below are the columns we'll use to categorize employees as "dissatisfied" from each dataframe. 
# 
# tafe_survey_updated:
# Contributing Factors. Dissatisfaction
# Contributing Factors. Job Dissatisfaction
# 
# detesurveyupdated:
# job_dissatisfaction
# dissatisfaction_with_the_department
# physical_work_environment
# lack_of_recognition
# lack_of_job_security
# work_location
# employment_conditions
# work_life_balance
# workload
# 
# If the employee indicated any of the factors above caused them to resign, we'll mark them as dissatisfied in a new column.

# In[121]:


tafe_resignations['Contributing Factors. Dissatisfaction'].value_counts()


# In[122]:


tafe_resignations['Contributing Factors. Job Dissatisfaction'].value_counts()


# In[123]:


#Update the values in the contributing factors columns to be either True, False, or NaN
def update_vals(x):
    if x == '-':
        return False
    elif pd.isnull(x):
        return np.nan
    else:
        return True
tafe_resignations['dissatisfied'] = tafe_resignations[['Contributing Factors. Dissatisfaction', 'Contributing Factors. Job Dissatisfaction']].applymap(update_vals).any(1, skipna=False)
tafe_resignations_up = tafe_resignations.copy()

# Check the unique values after the updates
tafe_resignations_up['dissatisfied'].value_counts(dropna=False)


# In[124]:


# Update the values in columns related to dissatisfaction to be either True, False, or NaN
dete_resignations['dissatisfied'] = dete_resignations[['job_dissatisfaction',
       'dissatisfaction_with_the_department', 'physical_work_environment',
       'lack_of_recognition', 'lack_of_job_security', 'work_location',
       'employment_conditions', 'work_life_balance',
       'workload']].any(1, skipna=False)
dete_resignations_up = dete_resignations.copy()
dete_resignations_up['dissatisfied'].value_counts(dropna=False)


# In[126]:


#Create copies to avoid SettingWithCopy warning
dete_resignations_up = dete_resignations.copy()
tafe_resignations_up = tafe_resignations.copy()


# To recap, we've accomplished the following:
# 
# Renamed our columns,
# Dropped any data not needed for our analysis,
# Verified the quality of our data,
# Created a new institute_service column,
# Cleaned the Contributing Factors columns,
# Created a new column indicating if an employee resigned because they were dissatisfied in some way.
# 
# Now, we're finally ready to combine our datasets! Our end goal is to aggregate the data according to the institute_service column, so when you combine the data, think about how to get the data into a form that's easy to aggregate.

# In[127]:


# First, let's add a column to each dataframe 
# that will allow us to easily distinguish between the two.
dete_resignations_up['institute'] = 'DETE'
tafe_resignations_up['institute'] = 'TAFE'


# In[128]:


#Combine the dataframes
combined = pd.concat([dete_resignations_up, tafe_resignations_up], ignore_index=True)
#Drop columns with less than 500 non-null values
combined_updated = combined.dropna(thresh=500,axis=1).copy()


# Now that we've combined our dataframes, we're almost at a place where we can perform some kind of analysis! First, though, we'll have to clean up the institute_service column. This column is tricky to clean because it currently contains values in a couple different forms. To analyze the data, we'll convert these numbers into categories. We'll base our anlaysis on this article, which makes the argument that understanding employee's needs according to career stage instead of age is more effective.
# 
# We'll use the slightly modified definitions below:
# 
# New: Less than 3 years at a company
# Experienced: 3-6 years at a company
# Established: 7-10 years at a company
# Veteran: 11 or more years at a company

# In[129]:


#Look at unique values first to understand big-picture
combined_updated['institute_service'].value_counts(dropna=False).sort_values(ascending=False)


# In[130]:


# Extract the years of service and convert the type to float
combined_updated['institute_service_up'] = combined_updated['institute_service'].astype('str').str.extract(r'(\d+)')
combined_updated['institute_service_up'] = combined_updated['institute_service_up'].astype('float')

# Check the years extracted are correct
combined_updated['institute_service_up'].value_counts()


# In[131]:


#Create a function to map values into the above categories
def service_levels(years):
    if years >= 11:
        return "Veteran"
    elif 7 <= years < 11:
        return "Established"
    elif 3 <= years < 7:
        return "Experienced"
    elif pd.isnull(years):
        return np.nan
    else:
        return "New"

#Apply function to instutue_service column
combined_updated['service_cat'] = combined_updated['institute_service_up'].apply(service_levels)


# In[132]:


combined_updated['service_cat'].value_counts()


# So, per the comments, I wrote a sorting function to categorize the extracted years from the 'institute_service_up' column and created a new 'service_cat' column for the returned values. This will be a really simple and effective way to visualize the different buckets of employees (or former employees, technically) for our analysis.

# In[133]:


# Verify the unique values
combined_updated['dissatisfied'].value_counts(dropna=False)


# In[135]:


#So we still have NaN values, let's fix those by replacing them with the
#most frequently occuring value: False 
combined_updated['dissatisfied'] = combined_updated['dissatisfied'].fillna(False)
combined_updated['dissatisfied'].value_counts(dropna=False)


# In[140]:


#Use df.pivot_table to calculate the percentage of dissatisfied employees in each group
service_cat_pvtable = combined_updated.pivot_table(values='dissatisfied',index='service_cat')
#Plot the results
get_ipython().magic('matplotlib inline')
service_cat_pvtable.plot(kind='bar',rot=30)


# From the initial analysis above, we can tentatively conclude that employees with 7 or more years of service are more likely to resign due to some kind of dissatisfaction with the job than employees with less than 7 years of service. However, we need to handle the rest of the missing data to finalize our analysis.
