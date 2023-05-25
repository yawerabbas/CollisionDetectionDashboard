import streamlit as st
import pandas as pd
import numpy as np 
data_url = ("/home/yawer/Documents/Projects/DS_app/nypd-motor-vehicle-collisions.csv")
st.title("Motot Vehicle Collision in Newyork City")
st.markdown("This is a web based application")

@st.cache (persist=True)
def load_data(nrows):
    data = pd.read_csv(data_url,nrows=nrows,parse_dates=[['CRASH_DATE','CRASH_TIME']])
    data.dropna(subset=['LATITUDE','LONGITUTDE'],inplace=True)
    lowercase = lambda x : str(x).lower()
    data.rename(lowercase,axis='column',inplace=True)
    data.rename(columns={'crash_data_crash_time':'date/time'},inplace= True)

    return data
data = load_data(100000)
st.subheader('Raw Data')
st.write(data)