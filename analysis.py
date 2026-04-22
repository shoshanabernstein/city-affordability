NYC_AFFORDABILITY = 6000 # Baseline for comparison

# Function to rank cities by affordability
def rank_cities(cities):
    """Ranks cities by affordability based on the cost of living index."""
    cities_with_monthly_cost = []
    
    # Calculate the monthly cost for each city based on the cost of living index and the NYC affordability baseline
    for city_data in cities:
        monthly_cost = (city_data["cost_index"] / 100) * NYC_AFFORDABILITY
        
        cities_with_monthly_cost.append({
            "city": city_data["city"],
            "monthly_cost": monthly_cost,
            "remaining_budget": NYC_AFFORDABILITY - monthly_cost
        })
    return cities_with_monthly_cost

