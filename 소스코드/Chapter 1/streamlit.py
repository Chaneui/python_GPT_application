import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit 대시보드 제목
st.title("Car Sales Dashboard")

# CSV 파일 불러오기
df = pd.read_csv("car_sales.csv")

# Streamlit sidebar에 selectbox 위젯 생성
vehicle_types = df['Vehicle_type'].unique()
selected_vehicle_type = st.sidebar.selectbox("Select Vehicle Type", vehicle_types)

# 선택한 Vehicle_type에 따라 데이터 필터링
filtered_df = df[df['Vehicle_type'] == selected_vehicle_type]

# Plotly를 사용하여 scatter plot 생성
fig = px.scatter(
    filtered_df, 
    x='Horsepower', 
    y='Fuel_efficiency', 
    color='Manufacturer', 
    title=f'Horsepower vs Fuel Efficiency for {selected_vehicle_type}',
    labels={
        'Horsepower': 'Horsepower',
        'Fuel_efficiency': 'Fuel Efficiency'
    }
)

# Streamlit 대시보드에 그래프 표시
st.plotly_chart(fig)
