#Structuring Data
#get unicorn companies dataset from EDA unicorn companies script file pushed here in this repository

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#load dataset int dataframe
companies = pd.read_csv("Unicorn_Companies.csv")

#Data Exploration
companies.head(10)
companies.shape

#There are 1074 rows and 10 columns in the dataset.
#According to this dataset, there are 1074 unicorn companies, as of March 2022. 
#This dataset shows 10 aspects of each company.

#Drop duplicates if any exist
companies.drop_duplicates().shape

#Shape returned after dropping is the same, meaning there is no duplicates

#types of columns
companies.dtypes

#The data type of the `Year Founded` column is `int64`. 
#The rest of the columns have the data type `object`.

#How to get insights on when a company was founded?
#Sort by year Founded, in ascending order to arrange the data
#from companies that were founded the earliest to companies that
#that were founded the latest.

#Sort the data
companies.sort_values(by="Year Founded",ascending=False).head(10)

#Determine the numbers of companies founded each year
companies["Year founded"].value_counts().sort_values(ascending=False)

#Historgam plot represents the count of samples based on particular features
sns.histplot(data=companies, x='Year Founded')
plt.title('Year Founded histogram');

#convert the Date Joined column to datetime
companies["Date Joined"]=pd.to_datetime(companies["Date Joined"])
companies.dtypes

#Create a Month Joined
companies["Month Joined"]= companies["Date Joined"].dt.month_name()
companies.head()

#Create Years to join, how many years it took companies to reach unicorn status
companies["Years to Join"] = companies["Date Joined"].dt.year -companies["Year Founded"]
companies.head()

#Specific year
companies_2021 = companies[companies["Date Joined"].dt.year == 2021]
companies_2021.head()

#Trend over time
companies_2021.insert(3, "Week Joined", companies_2021["date Joined"].dt.strftime('%Y-W%V'), True)
companies_by_week_2021 = companies_2021.groupby(by="Week Joined")["Company"].count().rest_index().rename(columns={"Company":"Company Count"})
companies_by_week_2021.head()

#Compare trend over time
#Filter by additional year to create
companies_2020 = companies[companies["Date Joined"].dt.year == 2020]
#Concatenate the new subset with the subset that you defined previously
companies_2020_2021 = pd.concat([companies_2020, companies_2021.drop(columns="Week Joined")])
#Add Quarter Joined column to companies 2021
companies_2020_2021["Quarter Joined"] = companies_2020_2021["Date Joined"].dt.to_period('Q').dt.strftime('%Y-Q%q')
#Convert the 'Valuation' column to numeric by removing $ and B and casting each value to data type float
companies_2020_2021["Valuation"] =  companies_2020_2021["Valuation"].str.strip("$B").astype(float)
#Group `companies_2020_2021` by `Quarter Joined`, 
#Aggregate by computing average `Funding` of companies that joined per quarter of each year.
#Save the resulting DataFrame in a new variable.
companies_by_quarter_2020_2021 = companies_2020_2021.groupby(by="Quarter Joined")["Valuation"].mean().reset_index().rename(columns={"Valuation":"Average Valuation"})
companies_by_quarter_2020_2021.head()

#Visualizing the time for companies to become Unicorn in respect to month joined
month_order = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", 
               "December"]
print(month_order)

sns.boxplot(x=companies['Month Joined'],y=companies['Year To Join'],order=month_order,showfliers=False)
plt.title('Distribution of years to become unicorn with respect to month joined')
plt.xticks(rotation=45,horizontalalignment='Right')
plt.show()

#Visualize the time for companies to become Unicorn in respect to year founded
plt.figure(figsize=(10,6))
sns.barplot(x=companies["Year Founded"], y=companies["Years To Join"], ci=False)
plt.title("Bar plot of years to join with respect to year founded")
plt.xlabel("Year founded")
plt.ylabel("Years to join unicorn status")
plt.xticks(rotation=45, horizontalalignment='right')
plt.show()

#Visualize the number of companies that joined per interval
plt.figure(figsize = (20, 5))
plt.bar(x=companies_by_week_2021['Week Joined'],height=companies_by_week_2021['Company Count'])
plt.plot()
plt.xlabel("Week number")
plt.ylabel("Number of companies")
plt.title("Number of companies that became unicorns per week in 2021")
plt.xticks(rotation = 45, horizontalalignment='right', fontsize=8)
plt.show()

#Visualize the average valuation over the quarters
companies_by_quarter_2020_2021['Quarter Number'] = companies_by_quarter_2020_2021['Quarter Joined'].str[-2:]
companies_by_quarter_2020_2021['Year Joined'] = companies_by_quarter_2020_2021['Quarter Joined'].str[:4]
plt.figure(figsize = (10, 5))
sns.barplot(x=companies_by_quarter_2020_2021['Quarter Number'],
            y=companies_by_quarter_2020_2021['Average Valuation'],
            hue=companies_by_quarter_2020_2021['Year Joined'])
plt.plot()
plt.xlabel("Quarter number")
plt.ylabel("Average valuation (billions of dollars)")
plt.title("Average valuation of companies that became unicorns per quarter in 2020 vs. 2021")
plt.show()




#Observations

'''
Observations from a grouped bar plot of average valuation of companies that became unicorns per quarter in 2020 vs. 2021:
In each quarter, the average valuation of companies that joined unicorn status was higher in 2020 than in 2021. 
In 2020, Q3 was the quarter with the highest average valuation of companies that reached unicorn status, and there was a trend of increase from Q1 to Q2 and from Q2 to Q3. 
In 2021, Q1 was the quarter with the highest average valuation of companies that reached unicorn status, and there was a trend of decrease across the quarters.

Potential bias:

If there were bias in terms of which cities and countries were taken into account when collecting the data, then the analysis would be more representative of the cities and countries that are in the dataset than those that are not.
If the dataset did not include certain industries, then the analysis would be more representative of the industries that are included and may not reflect trends in those that are excluded from the data. 
If the dataset had time gaps, (e.g., if companies that joined in certain windows of time were not included in the data), then that may have affected the patterns observed, depending on how salient the gaps were.
Another point of bias pertains to the nature of time data; there have been fewer years to collect data on companies that were founded more recently than for companies that were founded longer ago.

Potential next steps with EDA: 

Analyze the data with respect to industries of unicorn companies at different datetime intervals.
Analyze the data with respect to cities or countries where unicorn companies were founded at different datetime intervals.
Clean the data as needed.

Possible questions:

How many rounds of funding did each company require and when did this funding take place?
Have any of these unicorn companies acquired other companies along the way? If so, which companies acquired other companies, which companies did they acquire, and when did the acquisitions take place?

# Considerations
What are some key takeaways that you learned from this lab?**

Functions in the `pandas` library can be used for data manipulation in order to reorganize and structure the data.
Converting strings that contain dates to datetime format allow you to extract individual components from the data, such as month and year.
Structuring the data in specific ways allows you to observe more trends and zoom in on parts of the data that are interesting to you.
Functions in the `matplotlib.pyplot` module and the `seaborn` library can be used to create visualizations to gain further insight after structuring the data.

What findings would you share with others?**

There are 1074 unicorn companies represented in this dataset.
2015 is the year when the most number of unicorn companies were founded. 
Many of the unicorn companies that were founded in 2021 were founded in the United States and belong to "Fintech", "E-commerce & direct-to-consumer", and "Internet software & services" industries. 
The box plot created shows that companies that become unicorns in the months of September and October have a smaller median value for how long it took to become unicorns.
One of the bar plots created shows that the average valuation of companies that joined in 2020 is highest in the third quarter of the year, whereas the average valuation of companies that joined in 2021 is highest in the first quarter of the year.

What recommendations would you share with stakeholders based on these findings?**

According to data analysis that was conducted on a dataset of 1074 unicorn companies, companies that joined in the months of September and October tended to take less time to become unicorns.
Another finding was that many of the unicorn companies that were founded in 2021 were founded in the United States and belong to "Fintech", "E-commerce & direct-to-consumer", and "Internet software & services" industries. So if the stakeholders want to invest in companies founded in 2021, it would be a good idea to consider companies that belong to these industries, as they may be strong candidates for becoming unicorns.
It was also discovered that the average valuation of companies that joined in 2021 is highest in the first quarter of the year, and the average valuation of companies that joined in 2020 is the third quarter of the year. When considering companies that newly join in the future, it would be worth closely looking at companies that join in the first and third quarters of the year. 
The data can be analyzed further to gather more insights that are specific to the interests of the investing firm and the stakeholders. 
'''