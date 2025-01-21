import pandas as pd
import plotly.express as px
import streamlit as st

data = pd.read_csv("data.csv")  # Replace with actual dataset
st.title("Data Visualization Dashboard")
fig = px.bar(data, x="Category", y="Sales")
st.plotly_chart(fig)
