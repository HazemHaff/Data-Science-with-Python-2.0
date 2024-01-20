#INTRO
'''
A firm wants insights into unicorn companies that are valued at over one billion dollars. 
The data you will use for this task provides information on over 1,000 unicorn companies, 
including their industry, country, year founded, and select investors.
'''

#Get the data:https://www.kaggle.com/datasets/mysarahmadbhat/unicorn-companies


#Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

#Load Dataset into Dataframe
companies = pd.read_csv("Unicorn_Companies.csv")

#First 20 Raws of the Dataframe
companies.head(10)
#Size of data, how many values
companies.size
#Sape of the frame, in other word Dimension, how many rows and columns
companies.shape
#Information about the dataset, data type of each column and how many nulls
companies.info()
#Descriptive statistics
companies.describe()

#Convert Date Joined column to datetime(replace Date Joined with the new converted date joined)
companies["Date Joined"]=pd.to_datetime(companies["Date Joined"])
companies.info()

#Create a Year Joined Column from Date Joined Column
companies["Year Joined"]=companies["Date Joined"].dt.year
companies.head()

#Sometimes, in order to conduct EDA, and due to time and resource constraints, We need to take a Sample from the Data
companies_Sample=companies.sample(n=50,random_state=42) #n= size of sample, random state insure reproduibility

##Visualize the time it took companies to each Unicorn state,

#Create a new column for years it took companies to reach unicorn state
companies_Sample["years_till_unicorn"]=companies_Sample["Year Joined"] - companies_Sample["Year Founded"]
#Group it by industry, for each industry, getthe max value in the "years_till_unicorn" column.
grouped = (companies_Sample[["Industry","years_till_unicorn"]]
           .groupby("Industry")
           .max()
           .sort_values(by="years_till_unicorn")
           )
grouped

#create a bar plot, with industry column as the categories of the bar, and the difference in years
plt.bar(grouped.index, grouped["years_till_unicorn"])
plt.title("Bar plot of maximum years taken by companies to become Unicorn per industry(from sample)")
plt.xlable("Industry")
plt.ylable("Maximum number of years")
plt.xticks(rotation=45, horizontalalignment='riight')
plt.show()

#Visualize the maximum unicorn company valuation per industry

#create a column representing company valuation as metric data
companies_Sample["valuation_billions"]=companies_Sample["Valuation"]
companies_Sample["valuation_billions"]=companies_Sample["valuation_billions"].str.replace("$","")
companies_Sample["valuation_billions"]=companies_Sample["valuation_billions"].str.replace("B","")
companies_Sample["valuation_billions"]=companies_Sample["valuation_billions"].astype("int")
companies_Sample.head()

#Prepare data for visualization
grouped=(companies_Sample[["Industry","valuation_billions"]]
         .groupby("Industry")
         .max()
         .sort_values(by="valuation_billions")
         )
grouped

#Create bar plot, Industry column as categories, new valuation as height of the bars
plt.bar(grouped.index,grouped["valuation_billions"])
plt.title("Bar plot of maximum unicorn company valuation per industry (from sample)")
plt.xlabel("Industry")
plt.ylalbe("Maximum valuation in billions of dollars")
plt.xticks(rotation=45, horizontalalignment="right")
plt.show()

#findings
'''
- There are 1074 unicorn companies represented in this dataset.
- Some companies took longer to reach unicorn status but have accrued high valuation as of March 2022. Companies could take longer to achieve unicorn status for a number of reasons, including requiring more funding or taking longer to develop a business model. 

**What recommendations would you share with stakeholders based on these findings?**

It may be helpful to focus more on industry specifics. Next steps to consider:
- Identify the main industries that the investing firm is interested in investing in. 
- Select a subset of this data that includes only companies in those industries. 
- Analyze that subset more closely. Determine which companies have higher valuation but do not have as many investors currently. They may be good candidates to consider investing in. 
'''