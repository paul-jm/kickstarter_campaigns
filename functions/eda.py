# Basics
import pandas as pd
import numpy as np

# EDA stuff
import matplotlib
import matplotlib.pyplot as plt

colors = ['#0174B4', '#1DA5EE', '#4AC7EB', '#379EA7', '#7195A9', '#ABC6D4', 
          '#E8BB99', '#5A895B', '#79B31D', '#EFCE2D', '#EF8E2D']

def pie_chart(df, 
              col_name, 
              title, 
              count = True, 
              sum_col = 'usd_pledged',
              colors = colors):

    if count == True:
        labels = list(df.groupby(col_name)[col_name].count().index)
        plot_labels = [string.replace('_', ' ') for string in labels]
        data = list(df.groupby(col_name)[col_name].count().values)
        
    else:
        labels = list(df.groupby(col_name)[sum_col].sum().index)
        plot_labels = [string.replace('_', ' ') for string in labels]
        data = list(df.groupby(col_name)[sum_col].sum().values)        

    plt.pie(data, colors = colors, labels = plot_labels, autopct='%1.0f%%', startangle=90, pctdistance=0.85)

    #draw circle
    centre_circle = plt.Circle((0,0),0.70,fc = 'white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title(title)
    plt.tight_layout()
    
    plt.show()
    
    plt.close()
        
    return fig 

def bar_chart_per_year(df, 
                           values,
                           columns,
                           aggfunc,
                           title, 
                           index = 'deadline_year'):
    
    """Produce bar chart"""
    
    df_agg = df.pivot_table(index = index, 
                             values = values, 
                             columns = columns, 
                             aggfunc = aggfunc)
    
    fig = df_agg.plot(kind='bar', figsize=(5, 3), rot=0, color = colors)
    matplotlib.rcParams.update({'font.size': 11})
    matplotlib.rcParams.update({'text.color': '#202C36'})
    # matplotlib.rcParams['font.sans-serif'] = 'Lato'
    fig.set_frame_on(False)
    fig.tick_params(bottom = False)
    fig.tick_params(left = False)
    
    plt.title(title)
    plt.show()
    
    return fig


def bar_chart_avg_per_year(df, 
                       values_num,
                       values_denom,
                       columns,
                       # aggfunc,
                       title, 
                       cat1_col = 'failed',
                       cat2_col = 'successful',
                       index = 'deadline_year'):
    
    """Produce bar chart, with avg per category"""
    
    df_sum_pledged = df.pivot_table(index = index, values = values_num, columns = columns, aggfunc='sum')
    df_sum_backers = df.pivot_table(index = index, values = values_denom, columns = columns, aggfunc ='sum')
    df_sum_pledged['failed_avg'] = df_sum_pledged['failed'] / df_sum_backers['failed']
    df_sum_pledged['successful_avg'] = df_sum_pledged['successful'] / df_sum_backers['successful']

    df_agg = df_sum_pledged[['failed_avg', 'successful_avg']]
    df_agg.columns = ['failed', 'successful']
    
    fig = df_agg.plot(kind='bar', figsize=(5, 3), rot=0, color = colors)
    matplotlib.rcParams.update({'font.size': 11})
    matplotlib.rcParams.update({'text.color': '#202C36'})
    # matplotlib.rcParams['font.sans-serif'] = 'Lato'
    fig.set_frame_on(False)
    fig.tick_params(bottom = False)
    fig.tick_params(left = False)
    
    plt.title(title)
    plt.show()
    
    return fig


def plot_importance_df(importance_df, 
                       title,
                      top = 10):
    
    
    fig = importance_df.iloc[:top].plot.bar(color = colors)
    matplotlib.rcParams.update({'font.size': 11})
    matplotlib.rcParams.update({'text.color': '#202C36'})
    # matplotlib.rcParams['font.sans-serif'] = 'Lato'
    fig.set_frame_on(False)
    fig.tick_params(bottom = False)
    fig.tick_params(left = False)
    
    plt.title(title)
    plt.show()
    
    return fig