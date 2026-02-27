from amadeus import Client, ResponseError
import googlemaps
from src.config import Config

class TravelAgentAPI:
    def __init__(self):
        self.amadeus = Client(
            client_id=Config.AMADEUS_CLIENT_ID,
            client_secret=Config.AMADEUS_CLIENT_SECRET
        )
        self.gmaps = googlemaps.Client(key=Config.GMAPS_API_KEY)

    def get_flights(self, origin_iata: str, dest_iata: str, date: str) -> dict | None:
        try:
            response = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin_iata,
                destinationLocationCode=dest_iata,
                departureDate=date,
                adults=1,
                max=3
            )
            return response.data
        except ResponseError as e:
            print(f"Amadeus API Error: {e}")
            return None

    def get_drive_time(self, origin: str, destination: str) -> dict | None:
        try:
            result = self.gmaps.distance_matrix(origins=origin, destinations=destination)
            rows = result.get('rows', [])
            if rows and rows[0].get('elements'):
                element = rows[0]['elements'][0]
                return {
                    "distance": element['distance']['text'],
                    "duration": element['duration']['text']
                }
            return None
        except Exception as e:
            print(f"Google Maps API Error: {e}")
            return None
