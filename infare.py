import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

@st.cache_data
def load_data():
    data = pd.read_csv("data1.csv")
    data = data.drop_duplicates()
    data["year"]  = pd.to_datetime(data["start_date"]).dt.year
    data["start_date"] = pd.to_datetime(data["start_date"])
    data["end_date"] = pd.to_datetime(data["end_date"])
    mask  = (data["start_date"] >= "2024-03-15") & (data["start_date"] <= "2025-12-25")
    data = data[mask]
    return data

@st.cache_data
def load_market_shares():
    market_share = pd.read_excel("market_share.xlsx")
    return market_share
st.set_page_config(layout="wide")
market_share = load_market_shares()

data = load_data()


min_data = data.groupby(["from","to","carrier","start_date"],as_index=False)["price"].min()
col1,col2 = st.columns([1,1])
with col1:
    origin = st.selectbox(label ="Origin: ",options = min_data["from"].unique())
with col2:
    dest = st.selectbox(label = "Destination: ",options = min_data["to"].unique())

mask = (min_data["from"] == origin)& (min_data["to"] == dest)
masked_data = min_data[mask]
q1 = masked_data["price"].quantile(0.25)
q3=masked_data["price"].quantile(0.75)
IQR = q3-q1
outliers = masked_data[(masked_data["price"]<q1-1.2*IQR) | (masked_data["price"]> q3+1.2*IQR)]
data_cleaned = masked_data.drop(outliers.index)
carriers = market_share[(market_share["origin"] == origin) & (market_share["destination"] == dest)]["carrier"]


fig = px.line(data_frame = data_cleaned[(data_cleaned["carrier"].isin(carriers))] ,x="start_date",y="price",color = "carrier",markers=True,
              title= "Prices",
              labels = {
                  "price" : "Price",
                  "start_date" : "Date"
              }
              )

st.plotly_chart(fig,use_container_width=True,theme="streamlit")

#st.line_chart(data=data_cleaned[(data_cleaned["carrier"].isin(carriers))],x="start_date",y="price",color = "carrier")




