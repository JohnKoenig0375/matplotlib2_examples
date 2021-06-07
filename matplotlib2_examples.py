#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Title: Matplotlib Example Code 2
Date: 06JUN2021
Author: John Koenig
Purpose: Provide example code for advanced matplotlib plots
    - 2 x 1 Advanced Line Plots with custom colors and shared axis
    - 3 x 2 Small Multiple of Line Plots with combined legend
    
Inputs: various datasets
Outputs: 
    - background_checks_v1.png
    - NYC_test_scores_v1.png
    
Notes:
     For Data Visalization Class (Regis University)
     Summer 2021
    
'''

#%%
# import libraries

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

import matplotlib.lines as mlines

dpi = 300

# if you are on windows, you are going to have to change the file path to
# windows style
project_dir = r'/home/md33a/Python Projects/matplotlib2_examples/'
data_dir = project_dir + r'data/'
output_dir = project_dir + r'output/'

#%%
# US Firearm Background Checks
# BuzzFeed (via GitHub)
# https://github.com/BuzzFeedNews/nics-firearm-background-checks

df1_filename = 'nics-firearm-background-checks.csv'
df1 = pd.read_csv(data_dir + df1_filename)
df1_head = df1.iloc[:100,:]
columns = list(df1.columns)

# get total permit applications by state
states_list = df1['state'].unique()
total_apps_list = []

for state in states_list:
    state_df_tmp = df1[df1['state'] == state]
    total_apps_list.append(state_df_tmp['totals'].sum())

state_totals_df = pd.DataFrame([states_list, total_apps_list]).T
state_totals_df.columns = ['State', 'Total Permit Applications']
state_totals_df.sort_values(['Total Permit Applications'], ascending=False, inplace=True)
state_totals_df.index = range(len(state_totals_df))
state_totals_df = state_totals_df.iloc[:49,:]

# get time index
time_index = df1[df1['state'] == 'Alabama']['month'].to_list()
time_index.reverse()

year_ticks = []
year_ticklabels = []

for t in time_index:
    year = t[:4]
    month = t[-2:]
    
    if month == '01':
        year_ticks.append(t)
        year_ticklabels.append(year)

#  extract top 5 highest and top 5 lowest
top5_list = state_totals_df.iloc[:5,0].to_list()
bottom5_list = state_totals_df.iloc[-5:,0].to_list()

# prepare top 5 highest data
top5_totals = pd.DataFrame()

for state in top5_list:
    totals_series_tmp = df1[df1['state'] == state]['totals'].sort_values()
    totals_series_tmp.index = range(len(totals_series_tmp))
    top5_totals = pd.concat([top5_totals, totals_series_tmp], axis=1)

top5_totals.columns = top5_list
top5_totals.index = time_index

# prepare top 5 lowest data
bottom5_totals = pd.DataFrame()

for state in bottom5_list:
    totals_series_tmp = df1[df1['state'] == state]['totals'].sort_values()
    totals_series_tmp.index = range(len(totals_series_tmp))
    bottom5_totals = pd.concat([bottom5_totals, totals_series_tmp], axis=1)

bottom5_totals.columns = bottom5_list
bottom5_totals.index = time_index

# create 2x1 line plots with shared x axis (different y axis)
fig, [ax0, ax1] = plt.subplots(2, 1, figsize=(12,6), sharex=True)

# super title is placed on the Figure object (covers entire figure because of the multiple plots)
fig.suptitle('Top 5 vs. Bottom 5 US States\nby Firearm Background Check Totals (1998-2021)', fontsize=18)
fig.subplots_adjust(top=0.87)  # make room for fig title

# set line colors
colors1 = ['cornflowerblue',
           'forestgreen',
           'orangered',
           'fuchsia',
           'darkorange']

colors2 = ['dodgerblue',
           'limegreen',
           'tomato',
           'orchid',
           'gold']

# set custom color cyclers
custom_cycler1 = (cycler(color=colors1))
custom_cycler2 = (cycler(color=colors2))

ax0.set_prop_cycle(custom_cycler1)
ax1.set_prop_cycle(custom_cycler2)

# Top 5
ax0.plot(top5_totals, label='Inline label')
ax0.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
ax0.legend(labels= top5_list, title="Top 5", loc='upper left')

# Bottom 5
ax1.plot(bottom5_totals, label='Inline label')
ax1.set_yticks([2500, 5000, 7500, 10000])
ax1.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
ax1.set_xticks(year_ticks)
ax1.set_xticklabels(year_ticklabels, fontsize=10)
ax1.set_xlabel('Year', fontsize=14)
ax1.legend(labels= bottom5_list, title="Bottom 5", loc='upper left')

fig.text(.04, .3, "Firearm Background Checks", fontsize=14, rotation=90)  # add a shared y axis label

# annotate presidental elections
elections_list = [1, 5, 9, 13, 17, 21]
elections_labels = ['Bush', 'Bush', 'Obama', 'Obama', 'Trump', 'Biden']
election_label_x_locations = [.182, .308, .427, .551, .68, .806]
elections_colors= ['red', 'red', 'blue', 'blue', 'red', 'blue']

# draw vertical lines
for i in range(len(elections_list)):
    ax0.axvline(x=year_ticks[elections_list[i]], color=elections_colors[i], linestyle='--')
    ax1.axvline(x=year_ticks[elections_list[i]], color=elections_colors[i], linestyle='--')

for i in range(len(elections_labels)):
    fig.text(election_label_x_locations[i], .485, elections_labels[i], fontsize=10, color=elections_colors[i])

#plt.tight_layout()

plot1_filename = 'background_checks_v1.png'
fig.savefig(output_dir + plot1_filename, dpi=dpi)

#%%
# NYC Math Test Results by Grade - Citywide - by Race-Ethnicity
# data.gov
# https://catalog.data.gov/dataset/2006-2011-nys-math-test-results-by-grade-citywide-by-race-ethnicity

df2_filename = '2006_-_2011_NYS_Math_Test_Results_by_Grade_-_Citywide_-_by_Race-Ethnicity.csv'
df2 = pd.read_csv(data_dir + df2_filename)
df2_head = df2.iloc[:100,:]
columns = list(df2.columns)

level_columns = ['Level 1 %',
                 'Level 2 %',
                 'Level 3 %',
                 'Level 4 %']

level_labels = ['Lowest',
                ' ',
                '  ',        # I had to add spaces to these empty labels
                'Highest']

# create color cycler
colors3 = ['blue',
           'green',
           'purple',
           'orange']

# set custom color cycle
custom_cycler3 = (cycler(color=colors3))

# set default color cycler (same for all ax after this)
default_cycler = cycler(color=colors3)
plt.rc('axes', prop_cycle=default_cycler)

# filter down to "All Grades" rows
all_grades_df = df2[df2['Grade'] == 'All Grades']

# get list of years
years_list = list(all_grades_df['Year'].unique())

# ge list of ethnic groups
ethnic_list = list(all_grades_df['Category'].unique())

# create plot
fig, ax = plt.subplots(3, 2, figsize=(10,10), sharex=True, sharey=True)

# iterate through years 2006-2011
for i in range(len(years_list)):
    all_grades_df_tmp = all_grades_df[all_grades_df['Year'] == years_list[i]]
    
    
    for ethnic in ethnic_list:
        ethnic_df_tmp = all_grades_df_tmp[all_grades_df_tmp['Category'] == ethnic]
        
        levels_tmp = ethnic_df_tmp[level_columns].T.iloc[:,0].to_list()
        
        if (i % 2 == 0):
            ax[int(i/2), 0].plot(level_labels, levels_tmp)
            ax[int(i/2), 0].set_title(years_list[i], fontsize=14)
            ax[int(i/2), 0].yaxis.set_major_formatter(mpl.ticker.PercentFormatter())
        else:
            ax[int(i/2), 1].plot(level_labels, levels_tmp)
            ax[int(i/2), 1].set_title(years_list[i], fontsize=14)

fig.suptitle('NYS Test Scores in NYC by Year and Ethnicity: 2006-2011', fontsize=22)
fig.subplots_adjust(top=0.92)  # make room for fig title

fig.text(.06, .3, "Percentage of Student Scores by Category", fontsize=16, rotation=90)  # add a shared y axis label

# create legend
handles = [mlines.Line2D([], [], color='blue'),
           mlines.Line2D([], [], color='green'),
           mlines.Line2D([], [], color='purple'),
           mlines.Line2D([], [], color='orange')]

fig.legend(handles, ethnic_list, loc='right', fontsize=12)
fig.subplots_adjust(right=.85)  # make room for fig legend

plot2_filename = 'NYC_test_scores_v1.png'
fig.savefig(output_dir + plot2_filename, dpi=dpi)
