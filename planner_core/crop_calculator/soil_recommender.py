class SoilRecommender:

    recommendations = {
        "loamy": ["Wheat", "Soybean", "Sugarcane", "Cotton"],
        "sandy": ["Groundnut", "Carrot", "Potato"],
        "clay": ["Rice", "Paddy", "Sugarcane"]
    }
class SoilRecommender:
    """
    Recommends crops based on soil type.
    """

    recommendations = {
        "loamy": ["Wheat", "Soybean", "Sugarcane", "Cotton"],
        "sandy": ["Groundnut", "Carrot", "Potato"],
        "clay": ["Rice", "Paddy", "Sugarcane"]
    }

    def get_recommendations(self, soil_type: str):
        soil_type = soil_type.lower().strip()
        return self.recommendations.get(soil_type, ["No recommendations found"])

    def get_recommendations(self, soil_type: str):
        soil_type = soil_type.lower().strip()
        return self.recommendations.get(soil_type, ["No recommendations found"])
