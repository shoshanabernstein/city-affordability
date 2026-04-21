""" Creates a SQLite database and inserts the city affordability data into it. """
import sqlite3
from scraper import get_cities

# Create the database
def create_database():
    conn = sqlite3.connect('city_affordability.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY,
            city TEXT,
            cost_of_living_index REAL
        )
    ''')
    
    conn.commit()
    conn.close()

# Insert the city data into the database
def insert_cities(cities):
    with sqlite3.connect('city_affordability.db') as conn:
        c = conn.cursor()
        
        for city in cities:
            c.execute('''
                INSERT INTO cities (city, cost_of_living_index) VALUES (?, ?)
            ''', (city['city'], city['cost_index']))
   
if __name__ == "__main__":
    create_database()
    cities = get_cities()
    insert_cities(cities)