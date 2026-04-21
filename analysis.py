NYC_AFFORDABILITY = 6000 # Baseline for comparison

def rank_cities(cities):
    """Ranks cities by affordability based on the cost of living index."""
    cities_with_monthly_cost = []
    
    for city in cities:
        cities_with_monthly_cost.append({
            "city": city['city'],
            "monthly_cost": (city['cost_index'] / 100) * NYC_AFFORDABILITY,
            "remaining_budget": NYC_AFFORDABILITY - (city['cost_index'] / 100) * NYC_AFFORDABILITY
        })
    
    return cities_with_monthly_cost