""" Creates a SQLite database and inserts the city affordability data into it. """
import sqlite3
from scraper import scrape_cities

# Create the database
def create_database():
    with sqlite3.connect('city_affordability.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS cities (
                id INTEGER PRIMARY KEY,
                city TEXT,
                country TEXT,
                cost_of_living_index REAL
            )
        ''')
        
        conn.commit()

# Insert the city data into the database
def insert_cities(cities):
    with sqlite3.connect('city_affordability.db') as conn:
        c = conn.cursor()
        
        for city in cities:
            c.execute('''
                INSERT INTO cities (city, country, cost_of_living_index) VALUES (?, ?, ?)
            ''', (city['city'], city['country'], city['cost_index']))
   
        conn.commit()

# Function to get cities by country
def get_cities_by_country(countries):
    """Returns a list of cities in the specified countries."""
    with sqlite3.connect('city_affordability.db') as conn:
        c = conn.cursor()
        placeholders = ",".join(["?"] * len(countries))
        query = f"""
                SELECT city, cost_of_living_index
                FROM cities WHERE country IN ({placeholders})
                """
        c.execute(query, countries)
        rows = c.fetchall()
        
        cities = []

        for row in rows:
                city, cost_index = row

                cities.append({
                    "city": city,
                    "cost_index": cost_index
                })

    return cities
    
# Main function to create the database and insert the city data
if __name__ == "__main__":
    create_database()
    cities = scrape_cities()
    insert_cities(cities)