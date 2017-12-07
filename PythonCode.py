
# coding: utf-8

# In[1]:

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import csv
import numpy as np


# In[2]:

# create list of emails texts, each element is a separate email text
import pandas as pd
df = pd.read_csv("Emails.csv")
doc_set = df['RawText'].tolist()
dateOfEmail = df["MetadataDateSent"].tolist() #dates emails were sent
temp = []


for date in dateOfEmail: #extracting only the year
    if (date!=date): #checking nan values, we assume it's 2009 from exploring the data
        temp+=['2009']
    else:
        temp += [date[:4]]
dateOfEmail = temp #final list with years for each email


# In[3]:

# format the cities and countries and subcountries data: 
#each is its own list to check... ony unique values
def convertToLower(places): #convert all elements of list to lower case
    final = []
    for place in places:
        final += [place.lower()]
    return final
        
df2 = pd.read_csv('cities2.csv')
cities = (convertToLower((df2['city'].tolist())))#lowercasse set of all cities
countries = (convertToLower((df2['country'].tolist())))#lowercase set of all countries


# In[4]:

#will use duplicate data for future purposes
cities2 = (convertToLower((df2['city'].tolist())))#lowercasse set of all cities
countries2 = (convertToLower((df2['country'].tolist())))#lowercase set of all countries


# In[5]:

#removing stop words from cities and countries

import nltk
from nltk.corpus import stopwords
set(stopwords.words('english'))

for word in cities:
    if (word in set(stopwords.words('english'))):
        cities.remove(word)
cities = set(cities)

for word in countries:
    if (word in set(stopwords.words('english'))):
        countries.remove(word)
countries = set(countries)


# In[6]:


#loop through each element in doc_set, check if any word in it is part of the countriesandcities list
def getCountry(word): #takes a city and returns the country
    index = cities2.index(word) #gets the index of that city
    if (countries2[index].lower()=='united states of america'): #does not add america to list
        return 0
    return countries2[index] #returns the corresponding index from the countries table

#not places that were included in places database... in context, they are not places
# I read through emails with these places names in them and realized they were not places in context
'''notPlacesInAmerica = ['circle','young','alice','tyler','spencer','hobbs','mcgrath','flint','eugene',
             'helena','jackson','bryan','wallace','laurel','gary','mitchell','teller','mobile','lead',
            'elmira','billings','price','sidney','lamar','sherman','hobbs','casper','paterson','monroe']
'''
notPlaces = ['young','tours','progress','guide','brits','george','york','man','gay','buy','nice',
              'reading','mary','gender','san','gore','nancy','georgetown','florida','mango','clare']


''' looping through the words in the email and checking if it's a place
    if it's a city, adds to list of cities, and finds the corresponding country and add to country list
    if it's a country, adds to country list and add a blank for city list'''
def findPlacesInEmail(email):
    finalCityList = [] # list of places mentioned in that email
    finalCountryList = []
    words = email.split() # splits into individual words
    for word in words:
        word = word.lower()
        if (word in cities and getCountry(word)!=0 and word not in notPlaces): # not adding the united states
            finalCityList += [word] #it's a city
            #need to find corresponding country from 
            finalCountryList += [getCountry(word)]
        if (word in countries and word != 'united states of america'): #not including united states
            finalCountryList += [word]
            finalCityList += [""]
    return (finalCityList, finalCountryList)
        

#go through each email in data and get list of cities and countries, and add it back to final list
# also create a list of dates associated with when the places were mentioned
listOfCities = []
listOfCountries = []
listOfDates = []
for email in doc_set: 
    listOfCities  += findPlacesInEmail(email)[0] #the cities in that email
    listOfCountries += findPlacesInEmail(email)[1] #the countries corresponding to those cities (or possibly mentioned by themselves)
    currentIndex = doc_set.index(email)
    listOfDates += [dateOfEmail[currentIndex]] * len(findPlacesInEmail(email)[0])


# In[44]:

#pd.Series(listOfCountries).value_counts()
#pd.Series(listOfCities).value_counts()


# In[11]:

#camel casing the countries

import re
def capitalizeWords(s):
  return re.sub(r'\w+', lambda m:m.group(0).capitalize(), s)

for i in range(len(listOfCountries)): #camel casing the countries
    listOfCountries[i]= capitalizeWords(listOfCountries[i])


# In[15]:

import csv
#outputs the city or country metioned (if city, then  also the country it's in) and the date email was sent where it was mentioned

with open("finalCountries.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for i in range(len(listOfCountries)):
        writer.writerow([listOfCountries[i],listOfCities[i],listOfDates[i]])   

