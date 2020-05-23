from pyecharts.charts import Bar,Grid
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

#---------------------------processing data I need--------------------------------#
# Total global sales in years
v3 = data1[['Year_of_Release','Global_Sales']].groupby('Year_of_Release').sum().sort_values(by='Year_of_Release',ascending=False)
v3 = v3.reset_index().rename(columns = {'Year_of_Release':'Year','Global_Sales':'Total_Sales'})

# Mean global sales in years
v4 = data1[['Year_of_Release','Global_Sales']].groupby('Year_of_Release').mean().sort_values(by='Year_of_Release',ascending=False)
v4 = v4.reset_index().rename(columns = {'Year_of_Release':'Year','Global_Sales':'Mean_Sales'})

# Each year's total number of published games:
v5 = data1['Year_of_Release'].value_counts()
v5 = v5.reset_index().rename(columns = {'index':'Year','Year_of_Release':'Count'}).sort_values(by='Year',ascending=False)


year_list=list(v3['Year'])
sum_list=list(v3['Total_Sales'])
mean_list=list(v4['Mean_Sales'])
count_list=list(v5['Count'])

def two_decimal(x):
    for i in range(len(x)):
        a = x[i]
        a = round(a,2)
        x[i] = a
    return x

two_decimal(sum_list)
two_decimal(mean_list)


#------------------------------end processing-------------------------------------#

#------------------------------visualization---------------------------------#

bar = (
       Bar()
       .add_xaxis(year_list)
       .add_yaxis(
               'Total Sales',
               sum_list,
               yaxis_index=1,
               color='orange'
               )
       .add_yaxis(
               'Game numbers',
               count_list,
               yaxis_index=0,
               color='#5793f3'
               )
       .extend_axis(
               yaxis=opts.AxisOpts(
                       name='Total Sales',
                       type_='value',
                       min_=0,
                       max_=1500,
                       position='right',
#                       axisline_opts=opts.AxisLineOpts(
#                               linestyle_opts=opts.LineStyleOpts(color='#5793f3')
#                               ),
                       axislabel_opts=opts.LabelOpts(formatter="{value} million(s)"),
                       )
               )
       .extend_axis(
               yaxis=opts.AxisOpts(
                       type_='value',
                       name='Mean_Sales',
                       min_=0,
                       max_=4.5,
                       position='left',
#                       axisline_opts=opts.AxisLineOpts(
#                               linestyle_opts=opts.LineStyleOpts(color='gray')
#                               ),
                       splitline_opts=opts.SplitLineOpts(
                               is_show=True,
                               linestyle_opts=opts.LineStyleOpts(opacity=1)
                               )
                       )
               )
       .set_global_opts(
               yaxis_opts=opts.AxisOpts(
                       name='Game numbers',
                       min_=0,
                       max_=1500,
                       position='right',
                       offset=135,
#                       axisline_opts=opts.AxisLineOpts(
#                               linestyle_opts=opts.LineStyleOpts(color='#d14a61')
#                               )
                       ),
               title_opts=opts.TitleOpts(title='Why?'),
               tooltip_opts=opts.TooltipOpts(trigger='axis',axis_pointer_type='cross'),
               datazoom_opts=opts.DataZoomOpts(),
               )
       .set_series_opts(
               label_opts=opts.LabelOpts(is_show=False)
               )
       
       )
                    
bar2 = (
        Bar()
        .add_xaxis(year_list)
        .add_yaxis(
                'Mean Sales',
                mean_list,
                yaxis_index=2,
                label_opts=opts.LabelOpts(is_show=False)
                )
        )

bar.overlap(bar2)
grid = Grid()
grid.add(
        bar,
        opts.GridOpts(pos_left='5%',pos_right='20%'),
        is_control_axis_index=True
        )
grid.render('Why total sales are growing when mean sales are reducing.html')
