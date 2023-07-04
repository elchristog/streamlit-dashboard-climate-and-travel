from operator import index
import streamlit as st
import plotly.express as px
import pandas as pd
import os 

st.set_page_config(page_title='CITIBikes', page_icon='🚲', layout='centered', initial_sidebar_state='auto')

if os.path.exists('./datos_clima_ny.csv'): 
    df_clima = pd.read_csv('datos_clima_ny.csv', index_col=None)
    df_viajes = pd.read_csv('travel_data.csv', index_col=None)

with st.sidebar: 
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
    st.title("Dashboard CITIBikes")
    choice = st.radio("Navegación", ["Clima","Viajes"])
    st.info("Este Dashboard ha sido desarrollado para la asignatura de Despliegue de Soluciones Analíticas de la Maestría en Inteligencia Analítica de Datos de la Universidad de los Andes, equipo Conformado por  Rebeca Gamboa, Yovany Gasca y Christian González")

if choice == "Clima":
    st.title("Clima CITIBikes")
    st.subheader("Clima historico en Nueva York según las estaciones del sistema de bicicletas públicas de la ciudad")
    col1, col2 = st.columns(2)
    with col1:
        year = st.multiselect("Año", df_clima['YEAR'].unique())
    with col2:
        station = st.multiselect("Estación", df_clima['STATION'].unique())
    
    st.dataframe(df_clima[df_clima['YEAR'].isin(year) & df_clima['STATION'].isin(station)], width=1000, height=200)

    st.subheader("Evolución de la temperatura máxima mensual por año y estación")
    sub_df = df_clima[df_clima['YEAR'].isin(year) & df_clima['STATION'].isin(station)]
    mean_max_temp_month = sub_df.groupby(['STATION','YEAR','MONTH'])['TMAX'].mean().reset_index()
    fig = px.line(mean_max_temp_month, x="MONTH", y="TMAX", color='STATION', facet_col='YEAR', facet_col_wrap=3)
    st.plotly_chart(fig, use_container_width=True)
    mean_min_temp_month = sub_df.groupby(['STATION','YEAR','MONTH'])['TMIN'].mean().reset_index()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Estaciones con mayor temperatura")
        fig = px.bar(mean_max_temp_month.groupby(['STATION'])['TMAX'].mean().reset_index().sort_values(by='TMAX', ascending=False).head(10), x='STATION', y='TMAX')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Estaciones con menor temperatura")
        fig = px.bar(mean_min_temp_month.groupby(['STATION'])['TMIN'].mean().reset_index().sort_values(by='TMIN', ascending=True).head(10), x='STATION', y='TMIN')
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Evolución de la temperatura máxima semanal por año y estación")
    mean_max_temp_week = sub_df.groupby(['STATION','YEAR','WEEK'])['TMAX'].mean().reset_index()
    fig = px.line(mean_max_temp_week, x="WEEK", y="TMAX", color='STATION', facet_col='YEAR', facet_col_wrap=3)
    st.plotly_chart(fig, use_container_width=True)
    mean_min_temp_week = sub_df.groupby(['STATION','YEAR','WEEK'])['TMIN'].mean().reset_index()



if choice == "Viajes": 
    st.title("Viajes CITIBikes")
    st.subheader("Historial de viajes en el sistema de bicicletas públicas de la ciudad de Nueva York")
    col1, col2 = st.columns(2)

    col1, col2 = st.columns(2)
    with col1:
        year_viajes = st.multiselect("Año", df_viajes['month'].unique())
    with col2:
        station_viajes = st.multiselect("Estación de origen", df_viajes['start_bike_station_name'].unique())

    st.dataframe(df_viajes[df_viajes['month'].isin(year_viajes) & df_viajes['start_bike_station_name'].isin(station_viajes)], width=1000, height=200)

    st.subheader("Evolución del promedio mensual de viajes por estación de origen")
    sub_df_viajes = df_viajes[df_viajes['month'].isin(year_viajes) & df_viajes['start_bike_station_name'].isin(station_viajes)]
    count_viajes_month = sub_df_viajes.groupby(['start_bike_station_name','month'])['tripduration'].count().reset_index()
    fig = px.line(count_viajes_month, x="month", y="tripduration", color='start_bike_station_name')
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Estaciones con mayor número de viajes")
        fig = px.bar(count_viajes_month.groupby(['start_bike_station_name'])['tripduration'].count().reset_index().sort_values(by='tripduration', ascending=False).head(10), x='start_bike_station_name', y='tripduration', labels={'start_bike_station_name':'Estación de origen', 'tripduration':'Número de viajes'})
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Estaciones con mayor duración de viajes")
        fig = px.bar(sub_df_viajes.groupby(['start_bike_station_name'])['tripduration'].mean().reset_index().sort_values(by='tripduration', ascending=False).head(10), x='start_bike_station_name', y='tripduration', labels={'start_bike_station_name':'Estación de origen', 'tripduration':'Duración promedio de viajes'})
        st.plotly_chart(fig, use_container_width=True)