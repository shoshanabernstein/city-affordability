""" """
from analysis import rank_cities
from database import get_cities_by_country
import streamlit as st
import pandas as pd
import sqlite3

st.title("🌍Where can I afford to live?")

# Slider for number of rows
salary = st.slider("Annual Salary ($)", 25000, 250000, 60000)

# Get list of all countries
conn = sqlite3.connect('city_affordability.db')
query = "SELECT country FROM cities GROUP BY country"
all_counties = pd.read_sql_query(query, conn)

# Multiselect for countries
with st.container(border=True):
    countries = st.multiselect("Countries", all_counties, default="United States")

# Data Frame to display the cities and their affordability
data = []
cities = get_cities_by_country(countries)
for city, cost in cities.items():
    data.append(
        {
            "City": city,
            "Monthly Cost ($)": cost,
            "Affordable": cost < salary / 12  # example logic
        }
    )

df = pd.DataFrame(data)

st.dataframe(df)