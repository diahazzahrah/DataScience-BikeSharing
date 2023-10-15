import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns   
import streamlit as st 

sns.set(style='white')

# Load cleaned data
df = pd.read_csv("dashboard/main_data.csv")


# Set Page Web
st.set_page_config(page_title="Bike Sharing",
                   page_icon="📶",
                   layout="wide")

# ----- SIDEBAR -----
st.sidebar.image("6647729.jpg", width=250)


st.sidebar.header("Filter:")
st_filter = st.sidebar.multiselect(
    "Season:",
    options=df["season"].unique(),
    default=df["season"].unique()
)

year_filter = st.sidebar.multiselect(
    "Year:",
    options=df["year"].unique(),
    default=df["year"].unique()
)

temp_filter = st.sidebar.slider(
    "Temperature °C:",
    min_value=df["temp"].min(),  
    max_value=df["temp"].max(), 
)

df_selection = df.query(
    "season == @st_filter & year == @year_filter & temp >= @temp_filter"
)



# ----- MAINPAGE -----
with st.columns(2)[0]:
     st.title("DASHBOARD BIKE SHARING 🚴")
     st.markdown("##")

median_temp = round(df_selection["temp"].median(), 1)
average_atemp = round(df_selection["atemp"].mean(), 2)
average_hum = round(df_selection["hum"].mean(), 2)
count_sum = df_selection["count"].sum()

left_column, left1_column, mid_column,  right_column = st.columns(4)
with left_column:
    st.subheader("Total Users:")
    st.subheader(count_sum)
    st.write('count of total rental bikes including both casual and registered')
with left1_column:
    st.subheader("Median Temp °C:")
    st.subheader((median_temp)*100)
    st.write('Normalized temperature in Celsius')
with mid_column:
    st.subheader("Average Atemp:")
    st.subheader((average_atemp)*100)
    st.write('Normalized feeling temperature in Celsius')
with right_column:
    st.subheader("Average Hum:")
    st.subheader((average_hum)*100)  
    st.write('Normalized humidity')  

st.markdown("-----")


# ----- CHART -----

#CASUAL
def create_casual(df):
    casual_season = df.groupby("season").casual.sum().sort_values(ascending=False).reset_index()
    return casual_season
sum_casual_df = create_casual(df)
st.subheader("Most and Lowest From Perfoming Season by Number Casual")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(25, 7))

colors = [ "#04364A","#176B87","#64CCC5",  "#DAFFFB", "#D3D3D3"]

sns.barplot(x="casual", y="season", data=sum_casual_df , palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Most Performing Season", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

sns.barplot(x="casual", y="season", data=sum_casual_df .sort_values(by="casual", ascending=True), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Lowest Performing Season", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)
st.pyplot(fig)
st.caption('From 2011 - 2012 data, fall has more users and spring has the fewest users. This is seen from casual users.')

#REGISTERED
def create_registered(df):
    registered_season = df.groupby("season").registered.sum().sort_values(ascending=False).reset_index()
    return registered_season
sum_registered_df = create_registered(df)
st.subheader("Most and Lowest From Perfoming Season by Number Registered")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(25, 7))

colors = [ "#04364A","#176B87","#64CCC5",  "#DAFFFB", "#D3D3D3"]
sns.barplot(x="registered", y="season", data=sum_registered_df, palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Most Performing Season", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

sns.barplot(x="registered", y="season", data=sum_registered_df.sort_values(by="registered", ascending=True), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Lowest Performing Season", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)
st.pyplot(fig)
st.caption('From 2011 - 2012 data, fall has more users and spring has the fewest users. This is seen from registered users.')


# CHART 2
# Data Frame 
#1
st.subheader('History Bike Sharing')
col1, col2 = st.columns(2)
def create_season_count(df):
    byseason_df = df.groupby(by="season").instant.nunique().reset_index()
    byseason_df.rename(columns={
    "instant": "count"
    }, inplace=True)
    return byseason_df
season_count = create_season_count(df)
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors_season = ["#04364A","#176B87", "#64CCC5" , "#DAFFFB", "#D3D3D3"]
    sns.barplot(
        y="count",
        x="season",
        data=season_count.sort_values(by="count", ascending=False),
        palette=colors_season
    )
    ax.set_title("Count of Season by Bike Sharing Dataset", loc="center", fontsize=25)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=17)
    st.pyplot(fig)

#2 
def create_weather_count(df):
    byweathersit_df = df.groupby(by="weathersit").instant.nunique().reset_index()
    byweathersit_df.rename(columns={
    "instant": "count"
    }, inplace=True)
    return byweathersit_df
weather_count = create_weather_count(df)
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        y="count",
        x="weathersit",
        data=weather_count.sort_values(by="count", ascending=False),
        palette=colors_season
    )
    ax.set_title("Count of Weathersit by Bike Sharing Dataset", loc="center", fontsize=25)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=17)
    st.pyplot(fig)
    


def create_holiday_count(df):
    byholiday_df = df.groupby(by="holiday").instant.nunique().reset_index()
    byholiday_df.rename(columns={
    "instant": "count"
    }, inplace=True)
    return byholiday_df
holiday_count = create_holiday_count(df)
col3, col4 = st.columns(2)
with col3:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors_season = ["#04364A","#176B87", "#64CCC5", "#DAFFFB", "#D3D3D3"]
    sns.barplot(
    y="count",
    x="holiday",
    data=holiday_count.sort_values(by="count", ascending=False),
    palette=colors_season
    )
    ax.set_title("Count of Holiday by Bike Sharing Dataset", loc="center", fontsize=25)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=17)
    st.pyplot(fig)

def create_year_count(df):
    byyear_df = df.groupby(by="year").instant.nunique().reset_index()
    byyear_df.rename(columns={
    "instant": "count"
    }, inplace=True)
    return byyear_df
year_count = create_year_count(df)
with col4:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    sns.barplot(
        y="count",
        x="year",
        data=year_count.sort_values(by="count", ascending=False),
        palette=colors_season
    )
    ax.set_title("Count of Year by Bike Sharing Dataset", loc="center", fontsize=25)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=17)
    st.pyplot(fig)

st.caption('Based on the data available, users of this bike sharing system in 2011 and 2012 experienced an increase. This is supported by other data such as the fall season with weather conditions when it is clear, few clouds, partly cloudy during holiday conditions. Of course, these data have an influence in increasing user interest in using bike sharing')




st.caption('Copyright (c) Diah Siti Fatimah Azzahrah')
