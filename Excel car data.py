#!/usr/bin/env python
# coding: utf-8

# Here, we have a sample of 50,000 records of used car listings from the eBay-Germany site. DataQuest has added some dirt to a clean dataset, and it is my task in this project to clean it and analyze the used car listings.

# In[2]:


#import needed libraries, NumPy and pandas
import pandas as pd
import numpy as np
#Read the autos.csv into pandas
autos = pd.read_csv("autos.csv", encoding = "Latin-1")


# In[3]:


autos.info()
autos.head()


# After importing the data, intially I notice there are a few columns with null values: vehicleType,gearbox,model,fuelType,notRepairedDamage. The notRepairedDamage column has almost 10,000 null values, which is understandable as those particular cars are likely just undamaged vehicles and the seller didn't specify. It should also be noted that the column names are using camelcase and not Python's preferred snakecase.

# In[4]:


print(autos.columns)


# In[5]:


autos.columns = (['date_crawled', 'name', 'seller', 'offer_type', 'price', 'abtest',
       'vehicle_type', 'registration_year', 'gearbox', 'powerPS', 'model',
       'odometer', 'registration_month', 'fuel_type', 'brand',
       'unrepaired_damage', 'ad_created', 'no_of_pictures', 'postal_code',
       'last_seen'])


# In[6]:


autos.head()


# You'll notice in the cells above I changed the camelcase column headers to snakecase, to make it easier to work with in Python. I did this simply by printing the array of column headers, copying it into the next cell,  changing the relevant column names to snakecase, and assigning all of that to "autos.columns" to cement the changes (don't forget to drop that dtype statement otherwise it won't run properly. DataQuest also had me alter a few names entirely.

# In[7]:


autos.describe(include='all')


# After a frustrating few minutes only getting numeric data-type columns from the df.describe() attribute, and some strategic googling, I now know to include the parameter (include='all')to display all data types. Obviously for some columns, we see a NaN value.
# 
# There are a few columns that have essentially 1 of 2 unique value types, so these are candidates to be dropped: seller, offer_Type, abtest, gearbox, unrepaired_damage. These are likely "Y/N" type questions in the seller form when the post is being made initially. So depending on each column's relevancy, we may be able to drop a few.
# 
# You'll also notice some columns have numeric data stored as strings, and I'll need to clean them as well: date_Crawled,price,odometer(this will be fun since it has units attached to it), date_Crawled. Let's go ahead and clean up the price and odometer columns!

# In[8]:


autos.rename({'odometer':'odometer_km'},axis=1, inplace= True)
autos["price"] = (autos["price"].astype(str)
                                .str.replace(',','')
                                .str.replace('$','')
                                .astype(int))
autos["odometer_km"] = (autos["odometer_km"].astype(str)
                                            .str.replace(',','')
                                            .str.replace('km','')
                                            .astype(int)
                       )
autos.head()


# In[9]:


#Let's double check the output to make sure the changes were made
print(autos[['odometer_km','price']])


# Now that our output is good, I'll investigate the odometer_km and price columns just a little more to see if I have any outliers that can skew my results. First I'll do the odometer_km column:

# In[10]:


autos['odometer_km'].unique().shape


# In[11]:


autos['odometer_km'].describe()


# In[12]:


autos['odometer_km'].value_counts().head().sort_index(ascending=True)


# In[13]:


autos['odometer_km'].value_counts().tail().sort_index(ascending=True)


# In[14]:


# Now for price:
autos['price'].unique().shape


# In[15]:


autos['price'].describe()


# In[16]:


autos['price'].value_counts().sort_index(ascending=True)


# As you can see above, when we ran: autos['price'].value_counts().head().sort_index(ascending=True)
# we discovered some outliers. There are 1421 counts of a $0 price. Now common sense tells me there aren't 1421 vehicles being given away for free (if I'm wrong I need to be learning German and not Python), so we can go ahead and remove those rows:

# In[17]:


autos = autos[autos["price"].between(1,351000)]


# In[18]:


autos['price'].value_counts()


# As you can see, we now have these outliers removed and can move on. Let's check the distribution of dates and registration year data.

# In[19]:


autos['date_crawled'].value_counts(normalize=True, dropna=False).sort_index()


# In[20]:


autos['ad_created'].value_counts(normalize=True, dropna=False).sort_index()


# In[21]:


autos['last_seen'].value_counts(normalize=True, dropna=False).sort_index()


# In[22]:


autos['registration_year'].describe()


# In[23]:


autos['registration_year'].value_counts().sort_index()


# Noticing the distribution of registration years, it appears that we have some time traveing cars. Using my best judgement, I'm going to cutoff all values above 2017 (the year after this dataset is taken from, models are usually released a year ahead of time so there are probably some very new cars available on eBay) and below 1900, when cars were truly becoming a thing.

# In[24]:


autos = autos[autos['registration_year'].between(1900,2017)]


# In[25]:


autos['registration_year'].value_counts(normalize=True).sort_index()


# And voilla! There we have it, the outliers have been removed, and we can now see the cleaner distribution of values we have above. 
# Now let's move onto the brand column. We're going to use aggregation to explore and understand it a bit more.

# In[34]:


autos["brand"].value_counts(normalize=True)


# We're going to work through the top 20 brands, as per the instructions. Now to create an empty dictionary to hold the aggregated data, and construct a for loop that will sotre the mean price for that brand as the value, and the brand name as the key. We'll finish by printing the dictionary.

# In[44]:


popular_cars_price={}
brands = autos["brand"].value_counts(normalize=True).head(20)
popular_brands = brands.index
 
for brand in popular_brands:
    top_brands = autos[autos["brand"] == brand]
    mean_price = top_brands ["price"].mean()
    popular_cars_price[brand] = int(mean_price)   
    
print(popular_cars_price)

## sort highest to lowest price
sorted(popular_cars_price.items(), key=lambda x: x[1], reverse=True)


# Now we have our aggregated data, stored and sorted in a dictionary. We can easily see the ranking of the top brands, and the mean price for each brand. This info is very useful in a few contexts, depending on how we want to use it. For example, if we wanted to use this data as part of an algorithim that targeted used car advertisements to demographics within a certain price point.

# Instructions for final step:
# 
# 
# 
# Assign the other series as a new column in this dataframe.
# Pretty print the dataframe, and write a paragraph analyzing the aggregate data.
# 
# Let's get it done!

# In[56]:


#Use the loop method from the last screen to calculate the mean mileage 
#and mean price for each of the top brands, storing the results in a
#dictionary.

popular_cars_mileage={}
brands = autos["brand"].value_counts(normalize=True).head(20)
popular_brands = brands.index
 
for brand in popular_brands:
    top_brands = autos[autos["brand"] == brand]
    mean_mileage = top_brands ["odometer_km"].mean()
    popular_cars_mileage[brand] = int(mean_mileage)   
    
print(popular_cars_mileage)

## sort highest to lowest price
sorted(popular_cars_mileage.items(), key=lambda x: x[1], reverse=True)


# In[57]:


# store mean_prices into dataframe
brand_mean_prices = pd.Series(popular_cars_price).sort_values(ascending=False)
price_dataframe = pd.DataFrame(brand_mean_prices, columns=["mean_price"])
print("Mean price of popular car brands \n")
price_dataframe


# In[58]:


#store mean_mileage into dataframe
brand_mean_mileage = pd.Series(popular_cars_mileage).sort_values(ascending=False)
mileage_dataframe = pd.DataFrame(brand_mean_mileage, columns=["mean_mileage"])
print("Mean mileage of popular car brands \n")
mileage_dataframe


# In[46]:


#Convert both dictionaries to series objects, using the series constructor.
PCP_series = pd.Series(popular_cars_price)
PCM_series = pd.Series(popular_cars_mileage)


# In[59]:


## combine the dataframs and sort results
combined_cars_df = pd.concat([price_dataframe, mileage_dataframe], axis=1)
sorted_cars_df =combined_cars_df.sort_values(["mean_mileage"], ascending=False)
sorted_cars_df


# And there we have it! We've aggregated data on mean price and mileage from the top brands and have displayed them in a pretty table format!

# In[ ]:




