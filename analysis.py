NYC_BASELINE_COST = 5000  # used ONLY for conversion


def rank_cities(cities, salary):
    """Ranks cities by affordability based on user salary."""
    
    results = []

    for city_data in cities:
        monthly_cost = (city_data["cost_of_living_index"] / 100) * NYC_BASELINE_COST
        remaining = salary - monthly_cost
        score = remaining / salary  # normalized affordability

        results.append({
            "city": city_data["city"],
            "country": city_data["country"],
            "monthly_cost": round(monthly_cost, 2),
            "remaining_monthly_budget": round(remaining, 2),
            "score": round(score, 3),
            "status": get_status(remaining),
            "cost_of_living_index": city_data["cost_of_living_index"]
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)

def get_status(remaining):
    if remaining < 0:
        return "❌ Unaffordable – You are over budget"

    elif remaining < 200:
        return "🔴 Critical – Almost nothing left (high financial strain)"

    elif remaining < 500:
        return "🟠 Very Tight – Limited discretionary spending"

    elif remaining < 1000:
        return "🟡 Tight – Manageable but cautious spending needed"

    elif remaining < 2000:
        return "🟢 Comfortable – Good balance of expenses and savings"

    elif remaining < 4000:
        return "💚 Very Comfortable – Strong savings potential"

    else:
        return "💎 Luxury – High surplus, very affordable lifestyle"