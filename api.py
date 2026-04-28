import requests
import streamlit as st

def get_country_info(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    res = requests.get(url)

    if res.status_code != 200:
        return None

    data = res.json()[0]

    return {
        "name": data["name"]["common"],
        "capital": data.get("capital", ["N/A"])[0],
        "population": data["population"],
        "region": data["region"],
        "flag": data["flags"]["png"]
    }

def country_card(info):
    st.subheader(f"🌍 {info['name']}")

    col1, col2, col3 = st.columns([1, 2, 3])

    with col1:
        st.image(info["flag"], width=120)

    with col2:
        col1.metric("Population", f"{info['population']:,}")
        col2.metric("Region", info["region"])
        col3.metric("Capital", info["capital"])

