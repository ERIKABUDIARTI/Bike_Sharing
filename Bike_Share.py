from turtle import title
import streamlit as st
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
import plotly.figure_factory as ff
import plotly.express as px
#import plotly.subplots as sp
import plotly.graph_objects as go

def background():
    st.set_page_config(layout="wide",
                       page_title="Analysis Dashboard",
                       page_icon=":rocket:",
                       initial_sidebar_state="expanded")
background()

st.write("""
        # :sparkles: Welcome to Data Analysis Dashboard :sparkles:
        """)

st.write("""
        # :bike:  This app analyzes "Bike Sharing" dataset  :bike:
        """)

def read_data(csv):
    bike_df = pd.read_csv(csv)
    return bike_df

bike_df = read_data("bike_data.csv")

def total_hourly_rent(bike_df):
    start_hour = 0
    end_hour = 23
    filtered_df = bike_df[
        (bike_df['hr'] >= start_hour) & (bike_df['hr'] <= end_hour)]
    total_sewa = filtered_df['cnt'].sum()
    total_monthly_rent = bike_df.groupby('hr').agg({
        'cnt': 'sum'
    }).reset_index()  
    fig1 = px.bar(total_monthly_rent, x='hr', y='cnt', color='hr',color_continuous_scale='reds')
    fig1.update_xaxes(title_text='Hour')
    fig1.update_yaxes(title_text='Total Rent')
    fig1.update_layout(title='Total Hourly Rent',title_font=dict(size=30))
    fig1.update_layout(showlegend=False)
    fig1.update_layout(width=1000, height=600)
    return fig1

def total_monthly_rent(bike_df):
    start_month = 1
    end_month = 12
    filtered_df = bike_df[
        (bike_df['mnth'] >= start_month) & (bike_df['mnth'] <= end_month)]
    total_sewa = filtered_df['cnt'].sum()
    total_monthly_rent = bike_df.groupby('mnth').agg({
        'cnt': 'sum'
    }).reset_index()
    fig2 = px.bar(total_monthly_rent, x='mnth', y='cnt', color='mnth')
    fig2.update_xaxes(title_text='Month')
    fig2.update_yaxes(title_text='Total Rent')
    fig2.update_layout(title='Total Monthly Rent',title_font=dict(size=30))
    fig2.update_layout(showlegend=False)
    fig2.update_layout(width=1000, height=600)
    return fig2

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(total_hourly_rent(bike_df))
with col2:
    st.plotly_chart(total_monthly_rent(bike_df))





def holiday_rent(bike_df):
    bike_df['category'] = bike_df['holiday'].apply(lambda x: 'Holiday' if x else 'Workingday')
    bike_df = bike_df.groupby(['category','yr']).agg({
        'cnt': 'sum'
    }).reset_index()
    bike_df['yr'] = bike_df['yr'].map({
        0: '2011',
        1: '2012'
    })
    fig3 = px.bar(bike_df, 
                 x='category', 
                 y='cnt', 
                 color='category',
                 facet_col = 'yr',
                 labels={'yr': 'Year', 'cnt': 'Total Rent'}, 
                 color_discrete_map={'Holiday': '#016A70', 'Workingday': '#D2DE32'})
    fig3.update_xaxes(title_font=dict(size=15), tickfont=dict(size=12))
    fig3.update_yaxes(title_font=dict(size=15), tickfont=dict(size=12))
    fig3.update_layout(title='Total Rent of Holiday vs Workingday',title_font=dict(size=30))
    fig3.update_layout(showlegend=False)
    fig3.update_layout(width=1000, height=600)
    return fig3


def season_rent(bike_df):
    bike_df = bike_df.groupby(['season','yr']).agg({
        'cnt': 'sum'
    }).reset_index()
    bike_df['season'] = bike_df['season'].map({
        1: 'Spring',
        2: 'Summer',
        3: 'Fall',
        4: 'Winter'
    })
    bike_df['yr'] = bike_df['yr'].map({
        0: '2011',
        1: '2012'
    })
    fig4 = px.bar(bike_df, 
                 x='season', 
                 y='cnt', 
                 color='season',
                 facet_col = 'yr',
                 labels={'yr': 'Year', 'cnt': 'Total Rent'}, 
                 color_discrete_map={'Spring': '#F47C7C', 'Summer': '#F7F48B', 'Fall': '#A1DE93', 'Winter': '#70A1D7'})
    fig4.update_xaxes(title_font=dict(size=15), tickfont=dict(size=12))
    fig4.update_yaxes(title_font=dict(size=15), tickfont=dict(size=12))
    fig4.update_layout(title='Total Rent of Each Season',title_font=dict(size=30))
    fig4.update_layout(showlegend=False)
    fig4.update_layout(width=1000, height=600)
    return fig4


col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(holiday_rent(bike_df))
with col4:
    st.plotly_chart(season_rent(bike_df))





def weather_rent(bike_df):
    bike_df = bike_df.groupby(['weathersit','hr']).agg({
        'cnt': 'sum'
    }).reset_index()
    bike_df['weathersit'] = bike_df['weathersit'].map({
        1: 'Clear or Partly Cloudy',
        2: 'Misty or Few Clouds',
        3: 'Light Snow or Light Rain',
        4: 'Heavy Rain or Ice Pallets'
    }) 
    fig5 = px.line(bike_df, x='hr', y='cnt', color='weathersit', title='Total Rent of Different Weather')
    fig5.update_xaxes(title_text='Hour')
    fig5.update_yaxes(title_text='Total Rent')
    fig5.update_xaxes(title_font=dict(size=15), tickfont=dict(size=12))
    fig5.update_yaxes(title_font=dict(size=15), tickfont=dict(size=12))
    fig5.update_layout(title='Total Rent of Weather',title_font=dict(size=30))
    fig5.update_layout(width=1000, height=600)
    fig5.update_layout(legend_title_text='Weather Situation')
    return fig5
    

def weekday_rent(bike_df):
    bike_df = bike_df.groupby(['weekday','hr']).agg({
        'cnt': 'sum'
    }).reset_index()
    bike_df['weekday'] = bike_df['weekday'].map({
        0: 'Sunday',
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday'
    })
    fig6 = px.line(bike_df, x='hr', y='cnt', color='weekday', title='Total Rent of Weekday')
    fig6.update_xaxes(title_text='Hour')
    fig6.update_yaxes(title_text='Total Rent')
    fig6.update_xaxes(title_font=dict(size=15), tickfont=dict(size=12))
    fig6.update_yaxes(title_font=dict(size=15), tickfont=dict(size=12))
    fig6.update_layout(title='Total Rent of Each Day',title_font=dict(size=30))
    fig6.update_layout(width=1000, height=600)
    fig6.update_layout(legend_title_text='WeekDay')
    return fig6
    

col5, col6 = st.columns(2)
with col5:
    st.plotly_chart(weather_rent(bike_df))

with col6:
    st.plotly_chart(weekday_rent(bike_df))





correlation_matrix = bike_df.corr(numeric_only=True)
heatmap_title = 'Correlation Heatmap'
heatmap_fig = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.index,
    colorscale='Greens',
    colorbar=dict(title='Correlation'),
))
heatmap_fig.update_layout(
    title=heatmap_title,
    title_font=dict(size=30),
    xaxis=dict(title='Variables'),
    yaxis=dict(title='Variables'),
    width=1000, height=1000)


pair_plot = px.scatter_matrix(
    bike_df,
    dimensions=['temp', 'atemp', 'hum', 'windspeed'],
    color='cnt',
    color_continuous_scale=px.colors.sequential.YlGnBu,
    title='Pair Plot of Nature Factors Influences on Total Rent',
    width=1000, height=1000)
pair_plot.update_layout(title={'font':{'size':30}})


col7, col8 = st.columns(2)
with col7:
    st.plotly_chart(pair_plot)
with col8:
    st.plotly_chart(heatmap_fig)




def main():
    bike_df = read_data('bike_data.csv')
    total_hourly_rent(bike_df)
    total_monthly_rent(bike_df)
    holiday_rent(bike_df)
    season_rent(bike_df)
    weather_rent(bike_df)
    weekday_rent(bike_df)

if __name__ == "__main__":
    main()
