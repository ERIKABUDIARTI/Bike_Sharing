import streamlit as st
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

def background():
    st.set_page_config(layout="wide",
                       page_title="Analysis Dashboard",
                       page_icon=":rocket:",
                       initial_sidebar_state="expanded")
background()

st.write("""
        # :sparkles: Welcome to :bike: "Bike Sharing" :bike: Dashboard :sparkles:
        """)

#Add picture
bike_img = Image.open("bike.jpg")
idcamp_img = Image.open("IDCamp.jpg")

image_file = ["indosat.jpg", "dicoding.jpg"]
desired_width = 150
desired_height = 60


with st.sidebar:
    st.markdown("""
        <style>
            div {
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

    st.image (bike_img, use_column_width=True)

    st.header("""
              This Dashboard is deployed as one of the final projects of [IDCamp](https://www.idcamp.ioh.co.id/)
               """)
    st.image (idcamp_img, use_column_width=True)
    st.write('IDCamp is a scholarship program organized by Indosat Ooredoo Hutchison with the aim of cultivating young Indonesian developers ready to compete in the global digital economy.')
    st.write('The online training module for IDCamp is developed by Dicoding, which is a Google Authorized Training Partner in Indonesia.')
    st.write('In the development of its materials, Dicoding collaborates with Indosat Ooredoo Hutchison, utilizing use cases commonly encountered in the industrial world.')
    
    col1, col2 = st.columns(2)
    for idx, image_file in enumerate(image_file):
        iohd = Image.open(image_file)
        resized_img = iohd.resize((desired_width, desired_height))
        if idx == 0:
                col1.image(resized_img, use_column_width=True)
        else:
                col2.image(resized_img, use_column_width=True)
    
    st.write('Submitted by: [ERIKA BUDIARTI](https://www.linkedin.com/in/erika-budiarti/)')         

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
    fig1.update_layout(width=600, height=600)
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
    fig2.update_layout(width=600, height=600)
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
                 color_discrete_map={'Holiday': '#BEADFA', 'Workingday': '#8062D6'})
    fig3.update_xaxes(title_font=dict(size=15), tickfont=dict(size=12))
    fig3.update_yaxes(title_font=dict(size=15), tickfont=dict(size=12))
    fig3.update_layout(title='Total Rent of Holiday vs Workingday',title_font=dict(size=30))
    fig3.update_yaxes(range=[0, 2000000], dtick=250000, autorange=False)
    fig3.update_layout(showlegend=False)
    fig3.update_layout(width=600, height=600)
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
                 color_discrete_map={'Spring': '#FFC3A1', 'Summer': '#D3756B', 'Fall': '#A75D5D', 'Winter': '#F0997D'})
    fig4.update_xaxes(title_font=dict(size=15), tickfont=dict(size=12))
    fig4.update_yaxes(title_font=dict(size=15), tickfont=dict(size=12))
    fig4.update_layout(title='Total Rent of Each Season',title_font=dict(size=30))
    fig4.update_yaxes(range=[0, 650000], dtick=50000, autorange=False)
    fig4.update_layout(showlegend=False)
    fig4.update_layout(width=600, height=600)
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
    fig5 = px.line(bike_df, 
                   x='hr', 
                   y='cnt', 
                   color='weathersit', 
                   title='Total Rent of Different Weather',
                   color_discrete_map={'Clear or Partly Cloudy': '#4CB9E7', 'Misty or Few Clouds': '#A8DF8E', 'Light Snow or Light Rain': '#B15EFF', 'Heavy Rain or Ice Pallets': '#FE0000'})
    fig5.update_xaxes(title_text='Hour')
    fig5.update_yaxes(title_text='Total Rent')
    fig5.update_yaxes(range=[0, 275000], dtick=25000, autorange=False)
    fig5.update_xaxes(title_font=dict(size=15), tickfont=dict(size=12))
    fig5.update_yaxes(title_font=dict(size=15), tickfont=dict(size=12))
    fig5.update_layout(title='Total Rent of Different Weather',title_font=dict(size=30))
    fig5.update_layout(width=600, height=600)
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
    fig6 = px.line(bike_df, 
                   x='hr', 
                   y='cnt', 
                   color='weekday', 
                   title='Total Rent of Weekday',
                   color_discrete_map={'Sunday': '#4CB9E7', 'Monday': '#A8DF8E', 'Tuesday': '#B15EFF', 'Wednesday': '#FFB72B', 'Thursday': '#FE0000', 'Friday': '#FFABE1', 'Saturday': '#B3541E'})
    fig6.update_xaxes(title_text='Hour')
    fig6.update_yaxes(title_text='Total Rent')
    fig6.update_yaxes(range=[0, 60000], dtick=5000, autorange=False)
    fig6.update_xaxes(title_font=dict(size=15), tickfont=dict(size=12))
    fig6.update_yaxes(title_font=dict(size=15), tickfont=dict(size=12))
    fig6.update_layout(title='Total Rent of Each Day',title_font=dict(size=30))
    fig6.update_layout(width=600, height=600)
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
    width=600, height=600)


pair_plot = px.scatter_matrix(
    bike_df,
    dimensions=['temp', 'atemp', 'hum', 'windspeed'],
    color='cnt',
    color_continuous_scale=px.colors.sequential.YlOrBr,
    title='Nature Factors Influences on Total Rent',
    width=600, height=600)
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


def rfm_analysis(day_df):
    day_change = {0: 'sunday', 1: 'monday', 2: 'tuesday', 3: 'wednesday', 4: 'thursday', 5: 'friday', 6: 'saturday'}
    day_df["weekday"] = day_df["weekday"].map(day_change)
    rfm_df = day_df.groupby(by="weekday", as_index=False).agg({
        "dteday": "max",
        "instant": "count",
        "cnt": "sum"
    })

    rfm_df.columns = ["weekday", "max_order_timestamp", "frequency", "monetary"]
    rfm_df["max_order_timestamp"] = pd.to_datetime(rfm_df["max_order_timestamp"]).dt.date
    recent_date = pd.to_datetime(day_df["dteday"]).dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    rfm_df = rfm_df[["weekday", "recency", "frequency", "monetary"]].sort_values(by="recency", ascending=True)
    rfm_df.reset_index(drop=True, inplace=True)

    return rfm_df


if __name__ == "__main__":
    main()

    day_df = read_data('day.csv')
    rfm_df = rfm_analysis(day_df)

    # Display RFM Analysis
    st.markdown("<h2 style='text-align: center;'>RFM Analysis</h2>", unsafe_allow_html=True)
    col9, col10, col11 = st.columns(3)

    with col9:
        min_recency = round(rfm_df.recency.min(),0)
        avg_recency = round(rfm_df.recency.mean(),0)
        max_recency = round(rfm_df.recency.max(),0)
        st.metric("Minimal Recency", value=min_recency)
        st.metric("Average Recency", value=avg_recency)
        st.metric("Maximal Recency", value=max_recency)

    with col10:
        min_frequency = round(rfm_df.frequency.min(),0)
        avg_frequency = round(rfm_df.frequency.mean(),0)
        max_frequency = round(rfm_df.frequency.max(),0)
        st.metric("Minimal Frequency", value=min_frequency)
        st.metric("Average Frequency", value=avg_frequency)
        st.metric("Maximal Frequency", value=max_frequency)

    with col11:
        min_monetary = round(rfm_df.monetary.min(),0)
        avg_monetary = round(rfm_df.monetary.mean(),0)
        max_monetary = round(rfm_df.monetary.max(),0)
        st.metric("Minimal Monetary", value=min_monetary)
        st.metric("Average Monetary", value=avg_monetary)
        st.metric("Maximal Monetary", value=max_monetary)

    fig = go.Figure()

    fig_recency = go.Figure(go.Bar(
        x=rfm_df['weekday'], 
        y=rfm_df['recency'], 
        marker=dict(
            color=rfm_df['recency'],
            colorbar=dict(title='Recency'),
            colorscale='bluyl')),)
        
    fig_frequency = go.Figure(go.Bar(
        x=rfm_df['weekday'], 
        y=rfm_df['frequency'], 
        marker=dict(
            color=rfm_df['frequency'],
            colorbar=dict(title='Frequency'),
            colorscale='blugrn',)),)
        
    fig_monetary = go.Figure(go.Bar(
        x=rfm_df['weekday'], 
        y=rfm_df['monetary'], 
        marker=dict(
            color=rfm_df['monetary'],
            colorbar=dict(title='Monetary'),
            colorscale='bluyl',)),)
        
    fig_recency.update_layout(
        title='Recency Analysis',
        xaxis=dict(title='Weekday'),
        yaxis=dict(title='Recency', range=[0, max_recency], dtick=1, autorange=True),
        showlegend=True,
        width = 400,
        height = 600
    )

    fig_frequency.update_layout(
        title='Frequency Analysis',
        xaxis=dict(title='Weekday'),
        yaxis=dict(title='Frequency', range=[0, max_frequency], dtick=10, autorange=True),
        showlegend=True,
        width = 400, 
        height = 600
    )

    fig_monetary.update_layout(
        title='Monetary Analysis',
        xaxis=dict(title='Weekday'),
        yaxis=dict(title='Monetary', range=[0, max_monetary], dtick=100000, autorange=True),
        showlegend=True,
        width = 400,
        height = 600
    )
    
    col12, col13, col14 = st.columns(3)

    with col12:
        st.plotly_chart(fig_recency)
    with col13:
        st.plotly_chart(fig_frequency)
    with col14:
        st.plotly_chart(fig_monetary)

st.snow()



