class Crop:
    def __init__(self, name, yield_rate, price_per_kg):
        self.name = name
        self.yield_rate = yield_rate
        self.price_per_kg = price_per_kg

class YieldCalculator:
    def calculate_total_yield(self, area, crop):
        return area * crop.yield_rate

    def calculate_profit(self, adjusted_yield, crop):
        return adjusted_yield * crop.price_per_kg


class WeatherAdjustment:
    def adjust_yield(self, base_yield, weather):
        weather = weather.lower()
        if weather == "excellent":
            return base_yield * 1.2
        elif weather == "good":
            return base_yield * 1.1
        elif weather == "poor":
            return base_yield * 0.8
        return base_yield


class SoilRecommender:
    recommendations = {
        "loamy": ["Wheat", "Corn", "Soy"],
        "sandy": ["Melons", "Peanuts"],
        "clay": ["Rice", "Cotton"]
    }

    def get_recommendations(self, soil_type):
        return self.recommendations.get(soil_type.lower(), [])
