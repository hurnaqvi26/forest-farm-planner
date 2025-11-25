class WeatherAdjustment:
    """
    Applies weather impact factor to a yield.
    """

    weather_factors = {
        "sunny": 1.0,
        "cloudy": 0.9,
        "rainy": 1.1,
        "storm": 0.7
    }

    def adjust_yield(self, base_yield: float, condition: str):
        """
        Adjusts yield based on weather condition.
        """
        factor = self.weather_factors.get(condition.lower(), 1.0)
        return round(base_yield * factor, 2)
