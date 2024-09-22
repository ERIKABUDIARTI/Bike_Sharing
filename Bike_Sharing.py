import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='dark')
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

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
bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])
bike_df.resample('M', on='dteday').sum()


tab1, tab2, tab3, tab4 = st.tabs(["Total User", "Users by Nature Factors", "Users by Month and Hour", "RFM Analysis"])

with tab1:
    st.header("Daily Users")
    cola, colb, colc = st.columns(3)
    
    with cola:
        total_casual = bike_df.casual.sum()
        st.metric("Total Casual User", value=f'{total_casual:,}')
    
    with colb:
        total_registered = bike_df.registered.sum()
        st.metric("Total Registered User", value=f'{total_registered:,}')
        
    with colc:
        total_users = bike_df.cnt.sum()
        st.metric("Total Users", value=f'{total_users:,}')
    
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.lineplot(data=bike_df, x='dteday', y='cnt', ax=ax, color='#90CAF9')
    ax.set_title('Number of Users', fontsize=8)
    ax.set_xlabel('Date', fontsize=4)
    ax.set_ylabel('User Count', fontsize=4)
    ax.tick_params(axis='x', labelsize=4)  
    ax.tick_params(axis='y', labelsize=4) 
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)


with tab2:
    st.header("Nature Factor Influences on Total Rent")
    col1, col2 = st.columns(2)
    
    def weather_rent(bike_df):
        bike_df = bike_df.groupby(['weathersit']).agg({
            'cnt': 'sum'
        }).reset_index()
        bike_df['weathersit'] = bike_df['weathersit'].map({
            1: 'Clear or Partly Cloudy',
            2: 'Misty or Few Clouds',
            3: 'Light Snow or Light Rain',
            4: 'Heavy Rain or Ice Pallets'
        }) 
        sorted_bike_df = bike_df.sort_values(by='cnt', ascending=True)
        
        fig1 = px.bar(sorted_bike_df, 
                        x='weathersit', 
                        y='cnt', 
                        color='weathersit', 
                        title='Total Rent of Different Weather',
                        color_discrete_sequence= ['#a9def9', '#a9def9', '#a9def9', '#00bbf9'])
            
        fig1.update_xaxes(title_text='Weather')
        fig1.update_yaxes(title_text='Total Rent', range=[0, 275000], dtick=25000, autorange=False)
        fig1.update_xaxes(title_font=dict(size=15), tickfont=dict(size=12))
        fig1.update_yaxes(title_font=dict(size=15), tickfont=dict(size=12))
        fig1.update_layout(title='Total Rent of Different Weather', title_font=dict(size=30))
        fig1.update_layout(width=600, height=600)
        fig1.update_layout(showlegend=False)
        return fig1

    def season_rent(bike_df):
        bike_df = bike_df.groupby(['season']).agg({
            'cnt': 'sum'
        }).reset_index()
        bike_df['season'] = bike_df['season'].map({
            1: 'Spring',
            2: 'Summer',
            3: 'Fall',
            4: 'Winter'
        })
        sorted_bike_df = bike_df.sort_values(by='cnt', ascending=True) 
        
        fig2 = px.bar(bike_df, 
                    x='season', 
                    y='cnt', 
                    color='season', 
                    title='Total Rent of Different Season',
                    color_discrete_sequence= ['#efc3e6', '#efc3e6', '#efc3e6', '#f15bb5'])

        fig2.update_xaxes(title_text='Season')
        fig2.update_yaxes(title_text='Total Rent', range=[0, 275000], dtick=25000, autorange=False)
        fig2.update_xaxes(title_font=dict(size=15), tickfont=dict(size=12))
        fig2.update_yaxes(title_font=dict(size=15), tickfont=dict(size=12))
        fig2.update_layout(title='Total Rent of Different Weather', title_font=dict(size=30))
        fig2.update_layout(width=600, height=600)
        fig2.update_layout(showlegend=False)
        return fig2

    with col1:
        st.plotly_chart(weather_rent(bike_df))
    with col2:
        st.plotly_chart(season_rent(bike_df))


with tab3:
    st.header("Users by Month and Hour")
    col1, col2 = st.columns(2)

    def total_monthly_rent(bike_df):
        start_month = 1
        end_month = 12
        filtered_df = bike_df[
            (bike_df['mnth'] >= start_month) & (bike_df['mnth'] <= end_month)]
        total_sewa = filtered_df['cnt'].sum()
        total_monthly_rent = bike_df.groupby('mnth').agg({
            'cnt': 'sum'
        }).reset_index()
        fig1 = px.bar(total_monthly_rent, x='mnth', y='cnt')
        # Mengatur warna batang secara manual
        fig1.update_traces(marker_color='blue')
        fig1.update_xaxes(title_text='Month')
        fig1.update_yaxes(title_text='Total Rent')
        fig1.update_layout(title='Total Monthly Rent',title_font=dict(size=30))
        fig1.update_layout(showlegend=False)
        fig1.update_layout(width=600, height=600)
        return fig1

    def total_hourly_rent(bike_df):
        start_hour = 0
        end_hour = 23
        filtered_df = bike_df[
            (bike_df['hr'] >= start_hour) & (bike_df['hr'] <= end_hour)]
        total_sewa = filtered_df['cnt'].sum()
        total_monthly_rent = bike_df.groupby('hr').agg({
            'cnt': 'sum'
        }).reset_index()
        fig2 = px.bar(total_monthly_rent, x='hr', y='cnt')
        # Mengatur warna batang secara manual
        fig2.update_traces(marker_color='red')
        fig2.update_xaxes(title_text='Hour')
        fig2.update_yaxes(title_text='Total Rent')
        fig2.update_layout(title='Total Monthly Rent',title_font=dict(size=30))
        fig2.update_layout(showlegend=False)
        fig2.update_layout(width=600, height=600)
        return fig2

    with col1:
        st.plotly_chart(total_hourly_rent(bike_df))
    with col2:
        st.plotly_chart(total_monthly_rent(bike_df))

def main():
    bike_df = read_data('bike_data.csv')
    total_hourly_rent(bike_df)
    total_monthly_rent(bike_df)
    weather_rent(bike_df)
    season_rent(bike_df)

with tab4:
    st.header("RFM Analysis")
    cola, colb, colc = st.columns(3)

    def rfm_analysis(bike_df):
        hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
        bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])
    
        bike_df.groupby(by="hr").agg({
        "cnt": ["sum"]
        })
        current_date = max(hour_df['dteday'])
        
        rfm_df = bike_df.groupby('registered').agg({
            'dteday': lambda x: (current_date - x.max()).days,
            'instant': 'count',
            'cnt': 'sum'
        }).reset_index()
    
        rfm_df.columns = ['registered', 'Recency', 'Frequency', 'Monetary']
        return rfm_df


    if __name__ == "__main__":
        main()
        day_df = read_data('day.csv')
        hour_df = read_data('hour.csv')
        bike_df = read_data('bike_data.csv')
        rfm_df = rfm_analysis(bike_df)


    with cola:
        min_recency = round(rfm_df.Recency.min(),0)
        avg_recency = round(rfm_df.Recency.mean(),0)
        max_recency = round(rfm_df.Recency.max(),0)
        st.metric("Minimal Recency", value=min_recency)
        st.metric("Average Recency", value=avg_recency)
        st.metric("Maximal Recency", value=max_recency)

    with colb:
        min_frequency = round(rfm_df.Frequency.min(),0)
        avg_frequency = round(rfm_df.Frequency.mean(),0)
        max_frequency = round(rfm_df.Frequency.max(),0)
        st.metric("Minimal Frequency", value=min_frequency)
        st.metric("Average Frequency", value=avg_frequency)
        st.metric("Maximal Frequency", value=max_frequency)

    with colc:
        min_monetary = round(rfm_df.Monetary.min(),0)
        avg_monetary = round(rfm_df.Monetary.mean(),0)
        max_monetary = round(rfm_df.Monetary.max(),0)
        st.metric("Minimal Monetary", value=min_monetary)
        st.metric("Average Monetary", value=avg_monetary)
        st.metric("Maximal Monetary", value=max_monetary)

    # Create columns in Streamlit
    col1, col2, col3 = st.columns(3)
    
    # Plot Recency
    with col1:
        fig, ax = plt.subplots(figsize=(6, 6))
        sns.histplot(rfm_df['Recency'], bins=30, kde=True, ax=ax, color='blue')
        ax.set_title('Recency Distribution')
        ax.set_xlabel('Recency')
        ax.set_ylabel('Count')
        ax.grid(True)
        st.pyplot(fig)
    
    # Plot Frequency
    with col2:
        fig, ax = plt.subplots(figsize=(6, 6))
        sns.histplot(rfm_df['Frequency'], bins=30, kde=True, ax=ax, color='green')
        ax.set_title('Frequency Distribution')
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Count')
        ax.grid(True)
        st.pyplot(fig) 
    
    # Plot Monetary
    with col3:
        fig, ax = plt.subplots(figsize=(6, 6))
        sns.histplot(rfm_df['Monetary'], bins=30, kde=True, ax=ax, color='red')
        ax.set_title('Monetary Distribution')
        ax.set_xlabel('Monetary')
        ax.set_ylabel('Count')
        ax.grid(True)
        st.pyplot(fig)    

st.caption(f"Copyright © 2023-2024 All Rights Reserved [ERIKA BUDIARTI](https://www.linkedin.com/in/erika-budiarti/)")
st.snow()
