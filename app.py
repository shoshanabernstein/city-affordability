""" """
from analysis import rank_cities
from database import get_cities_by_country
import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(layout="wide")

st.title("🌍Where can I afford to live?")

salary = st.slider("Annual Salary ($)", 25000, 250000, 60000)

# Sidebar filters

# Get list of all countries
conn = sqlite3.connect('city_affordability.db')
query = "SELECT country FROM cities GROUP BY country"
all_countries = pd.read_sql_query(query, conn)
st.sidebar.header("🔍 Filters")

# Multiselect for countries
with st.container(border=True):
    countries = st.sidebar.multiselect("Countries", all_countries, default=["United States"])

show_affordable_only = st.sidebar.checkbox("Only Affordable Cities")

top_n = st.sidebar.slider("Top N Cities", 5, 20, 10)


# Data Frame to display the cities and their affordability
data = []
cities = get_cities_by_country(countries)

sorted_cities = rank_cities(cities)

for city in sorted_cities[:top_n]:
    monthly_cost = city["monthly_cost"]

    data.append(
        {
            "City": city['city'],
            "Monthly Cost ($)": monthly_cost,
            "Monthly": monthly_cost < salary / 12  # example logic
        }
    )

df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)