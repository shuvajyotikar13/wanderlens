from vertexai.generative_models import GenerativeModel
import vertexai
from src.config import Config

vertexai.init(project=Config.GCP_PROJECT_ID, location=Config.GCP_LOCATION)

class ItinerarySynthesizer:
    def __init__(self):
        self.model = GenerativeModel("gemini-1.5-pro-preview-0409")

    def generate_itinerary(self, landmark_data: dict, travel_data: dict, user_location: str) -> str:
        prompt = f"""
        You are an expert travel agent. The user wants to travel from {user_location} 
        to {landmark_data['landmark_name']} in {landmark_data['city']}.
        
        Landmark Context: {landmark_data['historical_context']}
        
        Logistical Data Retrieved:
        {travel_data}
        
        Please synthesize this into a structured, highly engaging travel itinerary. 
        Include the history of the location, the best routing option based on the data, 
        and practical travel tips.
        """
        response = self.model.generate_content(prompt)
        return response.text
