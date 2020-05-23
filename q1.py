from pyecharts.charts import Bar
from pyecharts import options as opts
import pandas as pd


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


v1 = data1[['Year_of_Release','NA_Sales','EU_Sales','JP_Sales','Other_Sales','Global_Sales',]].groupby('Year_of_Release').sum().sort_values(by='Year_of_Release',ascending=False)
v1 = v1.reset_index().rename(columns = {'Year_of_Release':'Year'})

Year_list=list(v1['Year'])
NA_list=list(v1['NA_Sales'])
EU_list=list(v1['EU_Sales'])
JP_list=list(v1['JP_Sales'])
Other_list=list(v1['Other_Sales'])
Global_list=list(v1['Global_Sales'])

def two_decimal(x):
    for i in range(len(x)):
        a = x[i]
        a = round(a,2)
        x[i] = a
    return x

two_decimal(NA_list)
two_decimal(EU_list)
two_decimal(JP_list)
two_decimal(Other_list)
two_decimal(Global_list)


bar1 = (
       Bar()
       .add_xaxis(Year_list)
       .add_yaxis('NA Sales',NA_list,stack='stack1')
       .add_yaxis('EU Sales',EU_list,stack='stack1')
       .add_yaxis('JP Sales',JP_list,stack='stack1')
       .add_yaxis('Other Sales',Other_list,stack='stack1')
       .set_global_opts(
               title_opts=opts.TitleOpts(
                       title="Each Year's Total Sales in Areas(millions of units)",
                       pos_left='center'
                       ),
               datazoom_opts=opts.DataZoomOpts(),
               legend_opts=opts.LegendOpts(
                       pos_right = 100,
                       pos_top = 70,
                       orient = 'vertical'
                       ),
               )
       .set_series_opts(
               label_opts=opts.LabelOpts(
                       is_show=False,
                       )
               )
       .render("Each Year's Total Sales in Areas.html")
       )


bar2 = (
        Bar()
        .add_xaxis(Year_list)
        .add_yaxis('Global Sales',Global_list,category_gap='35%')
        .set_global_opts(
               title_opts=opts.TitleOpts(
                       title="Total global sales per year(millions of units)",
                       pos_left='center'
                       ),
               legend_opts=opts.LegendOpts(
                       pos_right = 100,
                       pos_top = 70,
                       orient = 'vertical'
                       ),
               datazoom_opts=opts.DataZoomOpts(),
               )
        .render("Total global sales per year.html")
        )
