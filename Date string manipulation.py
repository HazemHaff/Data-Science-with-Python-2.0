#dataset, you can query and download the data from Google bigquery,
#We will work with 2016-2018 Lightning strike data from NOAA,

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df= pd.read_csv('NOAA1618')
df.head()

#Create new column
#We will convert the date column variable type to datetime
df['date'] = pd.to_datetime(df['date'])

#now we will create 4 columns, week, month, quarter and year.
#using datetime.strftime()
#%Y for year
#%V for the number of the week, so W%V means 'W'+'(number of week)'
#same goes for Quarter %q
#https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

df['week']=df['date'].dt.strftime('%Y-W%V')
df['month']=df['date'].dt.strftime('%Y-%m')
df['quarter']=df['date'].dt.to_period('Q').dt.strftime('%Y-Q%q')
df['year']=df['date'].df.strftime('%Y')

df.head(10)

##Plot the number of weekly lightning strikes in 2018

#create new dataframe just for 2018 data summed by week.
df_weekly2018=df[['data']=='2018'].groupby(['week']).sum().reset_index()
df_weekly2018.head()

#plot a bar graph of weekly strikes in 2018
plt.figure(figsize=(20,5))
plt.bar(x=df_weekly2018['week'],height=df_weekly2018['number_of_strikes'])
plt.plot()
plt.xlabel('Week number')
plt.ylable('Number of lightning strikes')
plt.title('Number of lightning strikes per week (2018)')
plt.xtick(rotation=45,fontsize=8)

plt.show()

##plot the number of quarterly lightning strikes from 2016-2018
df_byquarter=df['number_of_strikes'].div(1000000)
df_byquarter.head()

#group 2016 to 2018 data by quarter and sum.
df_byquarter=df.groupby(['quarter']).sum().reset_index()

df_byquarter['number_of_strikes_formatted']=df_byquarter['number_of_strikes'].div(1000000).round(1).astype(str)+'M'

df_byquarter.head()

#add labels
#https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.text.html

def addlables(x,y,lables):
    for i in range(len(x)):
        plt.text(i,y[i],lables[i],ha='center',va='bottom')

#plot
plt.figure(figsize=(15,5))
plt.bar(x=df_byquarter['quarter'],height=df_byquarter['number_of_strikes'])
addlables(df_byquarter['quarter'],df_byquarter['number_of_strikes'],df_byquarter['number_of_strikes_formatted'])
plt.plot()
plt.xlabel('Quarter')
plt.ylabel('Number of lightning strikes')
plt.title('number of lightning strikes per quarter (2016-2018)')
plt.show()

##grouped bar chart to compare year over year changes each quarter
df_byquarter['quarter_number']=df_byquarter['quarter'].str[-2:]
df_byquarter['year']=df_byquarter['quarter'].str[:4]
df_byquarter.head()

#plot
plt.figure(figsize=(15,5))
p=sns.barplot(
    data=df_byquarter,
    x='quarter_number',
    y='number_of_strikes',
    hue='year')
for b in p.patches:
    p.annotate(str(round(b.get_height()/1000000,1))+'M',
               (b.get_x()+b.get_width()/2.,b.get_height()+1.2e6),
               ha='center',va='bottom',
               xytext=(0,-12),
               textcoords='offset points')
plt.xtlabel('Quarter')
plt.ylabel('Number of lightning strikes')
plt.title('Number of lightning strikes per quarter (2016-2018)')
plt.show()