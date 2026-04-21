import scraper
import database
import analysis

def main():
    get_cities_by_country = database.get_cities_by_country("United States")
    ranked_cities = analysis.rank_cities(get_cities_by_country)
    for city in ranked_cities:
        print(f"{city['city']}: Monthly Cost = {city['monthly_cost']:.2f}, Remaining Budget = {city['remaining_budget']:.2f}")

if __name__ == "__main__":
    main()