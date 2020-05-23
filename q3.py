import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 13,8
from pyecharts import options as opts
from pyecharts.charts import Pie


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



#-------------------------The number of publisher------------------------------#
number = data1.Publisher.nunique()


#------------------------Get publishers which published more than 50 games---------#
publishers_data = data1['Publisher'].value_counts()[data1['Publisher'].value_counts()>50].reset_index()

#------------------------generate plot------------------------------#
plt.figure(figsize=(10,5))
sns.barplot(x='index',y='Publisher',data=publishers_data)
plt.xlabel('Publisher')
plt.ylabel('Published Game Number')
plt.xticks(rotation = 90)
plt.title('Publisher and Published Games')
plt.show()


#---------------Electronic Arts published more games than any other publishers, so take a look at EA------------#

# Pyechart's pie chart need lists as input:
EA_games = data1[data1["Publisher"]=="Electronic Arts"][['Genre','Name']].groupby('Genre').count()
EA_games = EA_games.reset_index().rename(columns = {'Name':'Game_Number'})
EA_dict = EA_games.set_index('Genre')['Game_Number'].to_dict()
genre_list = []
number_list = []
for key,value in EA_dict.items():
    genre_list.append(key)
    number_list.append(value)


# Generate pie chart:
p = (
     Pie()
     .add(
             '',
             [list(x) for x in zip(genre_list,number_list)],
             center=['35%','50%']
             )
     .set_global_opts(
             title_opts=opts.TitleOpts(title="EA 's Game Type"),
             legend_opts=opts.LegendOpts(pos_left='30%'),
             )
     .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}"))
     .render('EA Game Type.html')
     )
    
    
# -------------------------------------why EA likes to publish sports game------------------------------------------#

# Many games' global sales are below 10, they are not representative and if using a box plot, they will make it difficult to see the result:
data2 = data1[data1["Global_Sales"]>10]

# Generate the box plot:
plt.figure(figsize=(10,5))
sns.boxplot(x="Genre",y="Global_Sales",data=data2)
plt.title("Global Sales VS Genre")
plt.show()
