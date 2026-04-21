"""Scrapes city information from numbeo.com """
import requests
from bs4 import BeautifulSoup

def get_cities():
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # make a GET request to the numbeo cost of living rankings page and parse the HTML using BeautifulSoup
    response = requests.get("https://www.numbeo.com/cost-of-living/rankings.jsp", headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')  

    # create an empty list to store the city data
    data = []
    table = soup.find('table', id='t2')
    rows = table.find_all('tr')[1:]

    # for each row in the table, add it to the data list as a dictionary with the city name and cost of living index
    for row in rows:
        city = row.find_all('td')[1].text.strip()
        cost_of_living_index = row.find_all('td')[3].text.strip()
        # only add the city to the data list if it has a cost of living index
        if city and cost_of_living_index:
            data.append({
                "city": city,
                "cost_index": cost_of_living_index
            })

    return data
