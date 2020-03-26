# -*- coding: utf-8 -*-
"""main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_KzpxPsl8B2T4hE_Z2liSu1xzHxbA5KE
"""

import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt
# =============================================================================
# from datetime import datetime
# import folium
# from folium import plugins
# from folium.plugins import MarkerCluster
# =============================================================================

sns.set_style('darkgrid')

df = pd.read_csv('US_WeatherEvents_2016-2019.csv')

df.head()

df.describe()

df.info()

df.isnull().sum()

print(df.Type.unique())
print(df.Severity.unique())
print(len(df.AirportCode.unique()))
print(df.TimeZone.unique())
print(len(df.County.unique()))
print(len(df.State.unique()))
# print(df.EventId.unique())

## Plot these for better visualization
weather_type_df = df['Type'].value_counts(ascending=True)

## Some formatting to make it look nicer
fig=plt.figure(figsize=(18, 16))
plt.title("Frequency of Weathers")
plt.xlabel("Frequency of Weather")
plt.ylabel("Type of Weather")
ax = weather_type_df.plot(kind='barh')
ax.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

df["StartTime(UTC)"] = pd.to_datetime(df["StartTime(UTC)"], format="%Y-%m-%d %H:%M:%S")
df["Hour"] = df["StartTime(UTC)"].map(lambda x: x.hour)
df["Month"] = df["StartTime(UTC)"].map(lambda x: x.month)
df["Year"] = df["StartTime(UTC)"].map(lambda x: x.year)

df.Type = df.Type.astype('category').cat.codes
df.Severity = df.Severity.astype('category').cat.codes

df.info()

df.drop(['ZipCode', 'City', 'LocationLat', 'LocationLng', 'EventId'], axis=1, inplace=True)

df.head()

weather_categories = df['Type'].value_counts()
weather_category_names = weather_categories.index

def plot_temporal_feature(df, time_feature, crime_category_names, xaxis_formatter=None, xtick_inc=None):
    
    # Set figure size
    fig = plt.figure(figsize=(50, 100))
    
    for i in range(len(crime_category_names)):
        p = plt.subplot(10, 4, i+1)
        crime = crime_category_names[i]
        cur_crime_data = df[df.Type == crime]
        temporal_data = cur_crime_data[time_feature].value_counts().sort_index()
        sns.lineplot(data=temporal_data)
        if xtick_inc:
            plt.xticks(np.arange(df[time_feature].unique().min(),df[time_feature].unique().max()+1, xtick_inc))
        plt.tick_params(axis = 'both', which = 'major', labelsize = 13)
        if xaxis_formatter:
            p.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: xaxis_formatter(x)))
    #     p.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
        plt.ylabel("Frequency of Weather", fontsize=25)
        time_feature_str = str(time_feature).capitalize()
        plt.xlabel(time_feature_str, fontsize=25)
        plt.title("%s (%s)" % (crime, 'per '+ time_feature_str), fontsize=30)
    
    # fig.savefig('visualizations/%s.png' % time_feature_str, bbox_inches='tight')

plot_temporal_feature(df, 'Year', weather_category_names, xtick_inc=3)

