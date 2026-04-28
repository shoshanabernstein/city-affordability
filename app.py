import streamlit as st
import pandas as pd
from database import get_cities_by_country
from analysis import rank_cities
from ui import (
    show_header,
    show_filters,
    show_metrics,
    show_tabs,
    show_city_details,
    show_chart,
    show_ai_panel
)

st.set_page_config(page_title="Affordability App", layout="wide")

# --- HEADER ---
show_header()

countries, monthly_salary = show_filters()

# 3. DATA FLOW
cities = get_cities_by_country(countries)
sorted_cities = rank_cities(cities, monthly_salary)

# 4. UI OUTPUT
show_metrics(sorted_cities)
show_tabs(sorted_cities)
