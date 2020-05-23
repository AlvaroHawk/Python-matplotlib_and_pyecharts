import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 13,8


main_file_location = 'Target1.csv'

#--------------------access dataset and clear unuse data-----------------------------#
data1 = pd.read_csv(main_file_location)
# replace NaN value with 'Unspecified' in the last six columns and give it to 'data1_clearNaN'
data1_clearNaN = data1[['Critic_Score','Critic_Count','User_Score','User_Count','Developer','Rating']].fillna('Unspecified')
# Use data1_clearNaN to mearge the original data's last six columns,so the new data will only have NaN value in 'Year_of_Release' column:
data1[['Critic_Score','Critic_Count','User_Score','User_Count','Developer','Rating']] = data1_clearNaN
# drop rows that don't have a specific year.
data1 = data1.dropna(axis=0)
# after dropping NaN values, I can change this column's type to int:
data1['Year_of_Release'] = data1['Year_of_Release'].astype('int')
# drop data belongs to year 2020 and year 2017
# because there are only 4 games in these two year in this dataset,and also the aim is before year 2016.
list1 = list(data1['Year_of_Release'].unique())
list1.remove(2020)
list1.remove(2017)
data1 = data1[data1['Year_of_Release'].isin(list1)]
#------------------------------end clearing-------------------------------------#


#-----------------------------simple analysis-------------------------------------#
# Each year's total sales:
a1 = data1[['Year_of_Release','Global_Sales']].groupby('Year_of_Release').sum().sort_values(by='Year_of_Release',ascending=False)
a1 = a1.reset_index().rename(columns = {'Year_of_Release':'Year'})

# Each year's total number of published games:
a2 = data1['Year_of_Release'].value_counts()
a2 = a2.reset_index().rename(columns = {'index':'Year','Year_of_Release':'Count'})


# Each year's most popular platform(which had the most games):
year_list = data1['Year_of_Release'].unique()
platform_list = []
number_list = []
for i in year_list:
    a3 = data1[data1['Year_of_Release'] == i]
    a3_name = a3.groupby(['Year_of_Release','Platform'])['Name'].count().idxmax()
    a3_number = a3.groupby(['Year_of_Release','Platform'])['Name'].count().max()
    platform_list.append(a3_name[1])
    number_list.append(a3_number)
a3=pd.DataFrame({'Year':year_list,'Platform':platform_list,'Games':number_list})
a3 = a3.sort_values(by='Year',ascending=False)
a3 = a3.reset_index().drop(['index'],axis=1)


# Publisher who published the most games in each year:
year_list = data1['Year_of_Release'].unique()
publisher_list = []
number_list = []
for i in year_list:
    a4 = data1[data1['Year_of_Release'] == i]
    a4_name = a4.groupby(['Year_of_Release','Publisher'])['Name'].count().idxmax()
    a4_number = a4.groupby(['Year_of_Release','Publisher'])['Name'].count().max()
    publisher_list.append(a4_name[1])
    number_list.append(a4_number)
a4=pd.DataFrame({'Year':year_list,'Publisher':publisher_list,'Published_games':number_list})
a4 = a4.sort_values(by='Year',ascending=False).reset_index().drop(['index'],axis=1)

# which genre of game is the most welcomed in each year:
year_list = data1['Year_of_Release'].unique()
genre_list = []
number_list = []
for i in year_list:
    a5 = data1[data1['Year_of_Release'] == i]
    a5_name = a5.groupby(['Year_of_Release','Genre'])['Name'].count().idxmax()
    a5_number = a5.groupby(['Year_of_Release','Genre'])['Name'].count().max()
    genre_list.append(a5_name[1])
    number_list.append(a5_number)
a5=pd.DataFrame({'Year':year_list,'Genre':genre_list,'Count':number_list})
a5 = a5.sort_values(by='Year',ascending=False).reset_index().drop(['index'],axis=1)

# In each year, which game is the most popular one:
a6 = data1.iloc[data1.groupby('Year_of_Release')['Global_Sales'].idxmax()][['Year_of_Release','Name','Platform','Global_Sales']]
a6 = a6.groupby('Year_of_Release').max().sort_values(by='Year_of_Release',ascending=False)
a6 = a6.reset_index().rename(columns = {'Year_of_Release':'Year'})


#----------------------------end simple analysis-------------------------------------#




# Different Genres of Game Sales in Areas
plt.figure(figsize=(10,5))
data1.groupby('Genre')['NA_Sales','EU_Sales','JP_Sales','Other_Sales'].mean().plot(kind='bar')
plt.legend()
plt.title('Different Genres of Game Sales in Areas')
plt.show()


#------Question one: why are the mean global sales falling year by year when the total sales are growing?-------#
# 
plt.figure(figsize=(10,5))
b1 = data1[['Year_of_Release','Global_Sales']].groupby('Year_of_Release').sum().sort_values(by='Year_of_Release').plot(kind='bar')
plt.title('Total Global Sales in Each Year')
plt.show()

# Mean Global Sales in Each Year
plt.figure(figsize=(10,5))
sns.pointplot(x='Year_of_Release',y='Global_Sales',data=data1,ci=0,color='red',estimator = np.mean)
plt.title('Mean Global Sales in Each Year')
plt.xticks(rotation=60)
plt.show()

# Number of Games in Each Year
plt.figure(figsize=(10,5))
sns.countplot(x='Year_of_Release',data=data1)
plt.xticks(rotation = 60)
plt.title('Number of Games in Each Year')
plt.show()
# Reason: The number of published games are growing yearly.
# In the past, it's a big cake with a few knifes.
# Nowadays, it's still a big cake, but with a huge amount of knifes wishing to share a bite.
