import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
st.sidebar.image("https://www.american.edu/spa/data-science/images/datascience-hero.jpg",use_column_width=True)
DATE_TIME = "date/time"
DATA_URL = "https://github.com/yawerabbas/CollisionDetectionDashboard/raw/main/Motor_Vehicle_Collisions_-_Crashes.csv"

st.sidebar.success("Welcome to the Exploratory Data Analysis")

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
data['date/time'] = pd.to_datetime(data['date/time'])
# Display dataset summary
st.title("Motor Vehicle Collisions in NYC")
st.markdown("Exploratory Data Analysis")

# Show dataset summary
st.write("## Dataset Overview")
st.write(data.head())

# Basic statistics
st.write("## Basic Statistics")
st.write(data.describe())

# Hourly distribution
st.write("## Hourly Distribution of Collisions")
hourly_data = data.groupby(data['date/time'].dt.hour).size().reset_index(name='counts')
fig = px.bar(hourly_data, x='date/time', y='counts', labels={'date/time': 'Hour of the Day', 'counts': 'Number of Collisions'})
st.plotly_chart(fig)

# Severity of collisions
st.write("## Severity of Collisions")
st.write("### Number of Persons Injured and Killed")
injuries = data['number of persons injured'].sum()
fatalities = data['number of persons killed'].sum()
st.write(f"Total number of persons injured: {injuries}")
st.write(f"Total number of persons killed: {fatalities}")


# Contributing factors
st.write("## Contributing Factors to Collisions")
top_factors = data['contributing factor vehicle 1'].value_counts().head(10)
st.bar_chart(top_factors)


# Top locations and streets
st.write("## Top Locations and Streets for Collisions")
top_locations = data['borough'].value_counts().head(5)
st.write("### Top Boroughs")
st.bar_chart(top_locations)

top_streets = data['on street name'].value_counts().head(10)
st.write("### Top Streets")
st.bar_chart(top_streets)


# Interactive filters
st.sidebar.title("Interactive Filters")
boroughs = st.sidebar.multiselect("Select Boroughs", data['borough'].unique())
selected_data = data[data['borough'].isin(boroughs)]

st.write("## Filtered Data Overview")
st.write(selected_data.head())

# # Heatmap of collisions by hour and day of week
# st.write("## Heatmap of Collisions by Hour and Day of Week")
# data['day_of_week'] = data['date/time'].dt.day_name()
# data['hour'] = data['date/time'].dt.hour
# hour_day = data.groupby('day_of_week').size().reset_index(name='counts')
# heatmap_data = hour_day.pivot(index='date/time', columns='day_of_week', values='counts')
# fig = px.imshow(heatmap_data, labels=dict(color="Number of Collisions"), x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], y=range(24))
# fig.update_layout(title="Collisions Heatmap by Hour and Day of Week")
# st.plotly_chart(fig)

# Histogram of collisions by month
st.write("## Histogram of Collisions by Month")
data['Month'] = data['date/time'].dt.month_name()
monthly_collisions = data['Month'].value_counts().reset_index()

def month_no(month_name):
    months = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }
    return months.get(month_name)

# Add month number to the DataFrame
monthly_collisions['Month Number'] = monthly_collisions['Month'].apply(month_no)
monthly_collisions = monthly_collisions.sort_values('Month Number')
# monthly_collisions = monthly_collisions['Month', 'Collisions']
# print(monthly_collisions.columns)

fig = px.bar(monthly_collisions, x='Month', y='count', labels={'Month': 'Month', 'count': 'Number of Collisions'})
st.plotly_chart(fig)
# Slider for filtering number of injuries
st.write("## Filter Collisions by Number of Injuries")
min_injuries = st.slider("Minimum Number of Injuries", min_value=0, max_value=int(data['number of persons injured'].max()), value=0)
filtered_data = data[data['number of persons injured'] >= min_injuries]

st.write(f"### Collisions with {min_injuries} or more injuries")
st.write(filtered_data.head())

# Conclusion and next steps
st.title("Conclusion and Next Steps")
st.markdown("### Key Insights")
st.markdown("- The heatmap shows peaks in collisions during rush hours and weekdays.")
st.markdown("- Most collisions result in injuries rather than fatalities.")

st.markdown("### Recommendations")
st.markdown("- Implement stricter enforcement during high-collision hours.")
st.markdown("- Increase awareness campaigns on pedestrian and cyclist safety.")

st.markdown("### Next Steps")
st.markdown("- Perform detailed analysis on contributing factors to collisions.")
st.markdown("- Explore correlations with weather conditions and road visibility.")

# Optionally, show raw data
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.write(data)
