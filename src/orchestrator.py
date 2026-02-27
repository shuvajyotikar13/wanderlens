from src.embeddings import EmbeddingService
from src.elastic_client import LandmarkRetriever
from src.travel_layer import TravelAgentAPI
from src.llm_agent import ItinerarySynthesizer

class AgenticOrchestrator:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.retriever = LandmarkRetriever()
        self.travel_api = TravelAgentAPI()
        self.synthesizer = ItinerarySynthesizer()

    def process_request(self, image_bytes: bytes, user_location: str, user_iata: str, travel_date: str) -> str:
        # Step 1: Image to Vector
        query_vector = self.embedder.get_image_embedding(image_bytes)
        
        # Step 2: Retrieve Landmark from Elasticsearch
        landmark_data = self.retriever.search_landmark(query_vector)
        dest_city = landmark_data['city']
        
        # Step 3: Agentic Routing Logic
        travel_data = {}
        
        # If the user is in the same country/region, check driving first
        drive_data = self.travel_api.get_drive_time(user_location, dest_city)
        if drive_data and "days" not in drive_data["duration"]:
            travel_data["road_trip"] = drive_data
        else:
            # Long distance: Fetch Flights
            # Note: In production, you'd map dest_city to its nearest IATA code
            dest_iata = "BOM" if dest_city.lower() == "mumbai" else "DEL" 
            travel_data["flights"] = self.travel_api.get_flights(user_iata, dest_iata, travel_date)
            
        # Step 4: LLM Synthesis
        final_itinerary = self.synthesizer.generate_itinerary(
            landmark_data=landmark_data,
            travel_data=travel_data,
            user_location=user_location
        )
        
        return final_itinerary
