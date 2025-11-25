from .models import Crop

class YieldCalculator:
    """
    Performs yield and profit calculation for a farm plot.
    """

    def calculate_total_yield(self, area_acres: float, crop: Crop) -> float:
        """
        Calculates total expected crop yield in kilograms.
        """
        return round(area_acres * crop.yield_rate, 2)

    def calculate_profit(self, total_yield: float, crop: Crop) -> float:
        """
        Calculates total profit based on yield and market price.
        """
        return round(total_yield * crop.price_per_kg, 2)
