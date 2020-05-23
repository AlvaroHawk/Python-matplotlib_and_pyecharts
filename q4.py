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


#-------------------------Platform and Game Name------------------#

# The number of Platform:
data1.Platform.nunique()

# The number of published games on each platform:
plt.figure(figsize=(15,5))
sns.countplot(x='Platform',data=data1)
plt.title('Games in Platforms')
plt.show()


# ------------------------PS2 and Ds have more games than other platforms,so take a look at them--------#
# PS2:
plt.figure(figsize=(15,5))
PS2_games = data1[data1['Platform'] == "PS2"]
sns.barplot(x="Genre",y="NA_Sales",data=PS2_games,color="red",label="NA",estimator=np.mean)
sns.barplot(x="Genre",y="EU_Sales",data=PS2_games,color="gray",label="EU",estimator=np.mean)
sns.barplot(x="Genre",y="JP_Sales",data=PS2_games,color="yellow",label="JP",estimator=np.mean)
plt.ylabel("Sales")
plt.legend()
plt.title("PS2 Game Sales in Areas")
plt.show()

# DS:
plt.figure(figsize=(15,5))
DS_games = data1[data1["Platform"]=="DS"]
sns.barplot(x="Genre",y="NA_Sales",data=DS_games,color="red",label="NA",estimator=np.mean)
sns.barplot(x="Genre",y="EU_Sales",data=DS_games,color="gray",label="EU",estimator=np.mean)
sns.barplot(x="Genre",y="JP_Sales",data=DS_games,color="yellow",label="JP",estimator=np.mean)
plt.ylabel("Sales")
plt.legend()
plt.title("DS Game Sales in Areas")
plt.show()
