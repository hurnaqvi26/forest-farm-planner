class Crop:
    """Represents a crop with yield rate and market price."""

    def __init__(self, name: str, yield_rate: float, price_per_kg: float):
        """
        :param name: Crop name (e.g., Wheat)
        :param yield_rate: Expected yield (kg per acre)
        :param price_per_kg: Market price ($ per kg)
        """
        self.name = name
        self.yield_rate = yield_rate
        self.price_per_kg = price_per_kg

    def __str__(self):
        return f"{self.name} (Yield={self.yield_rate}, Price={self.price_per_kg})"
