import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import time
# from flask import Flask
# app = Flask(__name__)

# if app == '__main__':
#     app.run(debug=True)


# DATA_URL = ("C:/Users/user/Documents/Coding/Python/StreamlitWebApp/Motor_Vehicle_Collisions_-_Crashes.csv")

# push to heroku
st.sidebar.image("https://www.american.edu/spa/data-science/images/datascience-hero.jpg",use_column_width=True)

st.sidebar.success("Welcome to the Visualization Panel")
DATE_TIME = "date/time"
DATA_URL = "https://github.com/yawerabbas/CollisionDetectionDashboard/raw/main/Motor_Vehicle_Collisions_-_Crashes.csv"


st.title("Motor Vehicles Collision in New York City")
st.markdown("This application is streamlit dashboard that can be used to analyze motor vehicle collision in NYC")
st.markdown("This may take a while as the CSV file is 185MB")

# @app.route("/").
@st.cache_data(persist=True)
def load_data(rows):
    data = pd.read_csv(DATA_URL, nrows= rows,encoding='utf-8',parse_dates=[['CRASH DATE', 'CRASH TIME']])
    # data.seek(0)
    data.dropna(subset =['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase,axis='columns',inplace=True)
    data.rename(columns={'crash date_crash time':'date/time'},inplace=True)
    return data

data = load_data(100000)
with st.spinner('Wait for it...'):
    time.sleep(5)
st.success('Done!')

# for use with dropdown
original_data = data

# analyze to table
st.header("Where are the most people injured in NYC?")
injured_people = st.slider("Number of persons injured in NYC",0,19)

st.map(data[data['number of persons injured']> injured_people][['latitude', 'longitude']].dropna(how="any"))

# visualize on 2D map
st.header("How many collisons occur during a given time of day?")
# hour = st.selectbox("Hour to look at",range(0,24),1)
hour = st.slider("Hour to look at",0,23)
# hour = st.sidebar.slider("Hour to look at",0,23)
data = data[data['date/time'].dt.hour == hour]


# visualize 3D map
st.markdown("Vehicle collision between %i:00 and %i:00" %(hour,(hour+1) % 24))
midpoint = (np.average(data['latitude']), np.average(data['longitude']))

st.write(pdk.Deck(
    map_style = "mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    # add a layer to visualize on 3d map
    layers = [
        pdk.Layer(
            "HexagonLayer",
            data = data[['date/time','latitude','longitude']],
            get_position = ['longitude','latitude'],
            radius = 100,
            extruded = True,
            pickable = True,
            elevation_scale = 4,
            elevation_range = [0,1000],
        ),
    ],
))

# chart and histogram
st.subheader("Breakdown of collision by %i:00 and %i:00" %(hour,(hour+1) %24))
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour <(hour+1))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0,60))[0]
chart_data = pd.DataFrame({'minute':range(60), 'crashes':hist})
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute','crashes'], height=400)
st.write(fig)

# make a dropdown search
st.header("Top 5 dangerous streets affected by types")
select = st.selectbox("Affected by type of people", ['Pedestrians', 'Cyclists', 'Motorists'])

if select == 'Pedestrians':
    pass
    st.write(original_data[original_data['number of pedestrians injured'] >= 1][['on street name', 'number of pedestrians injured']].sort_values(by=['number of pedestrians injured'], ascending=False).dropna(how='any')[:5])
elif select == 'Cyclists':
    st.write(original_data[original_data["number of cyclist injured"] >= 1][['on street name', 'number of cyclist injured']].sort_values(by=['number of cyclist injured'], ascending=False).dropna(how='any')[:5])
elif select == 'Motorists':
    st.write(original_data[original_data["number of motorist injured"] >= 1][['on street name', 'number of motorist injured']].sort_values(by=['number of motorist injured'], ascending=False).dropna(how='any')[:5])


if st.checkbox("Show Raw Data",False):
    st.subheader("Raw Data")
    st.write(data)


