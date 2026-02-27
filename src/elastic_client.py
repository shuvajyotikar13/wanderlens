from elasticsearch import Elasticsearch
from src.config import Config

class LandmarkRetriever:
    def __init__(self):
        self.client = Elasticsearch(
            Config.ES_URL,
            api_key=Config.ES_API_KEY
        )

    def search_landmark(self, query_vector: list[float], top_k: int = 3) -> dict:
        """Performs a kNN vector search to identify the landmark."""
        query = {
            "knn": {
                "field": "image_embedding",
                "query_vector": query_vector,
                "k": top_k,
                "num_candidates": 100
            },
            "_source": ["landmark_name", "city", "coordinates", "historical_context"]
        }
        
        response = self.client.search(index=Config.ES_INDEX_NAME, body=query)
        
        if not response['hits']['hits']:
            raise ValueError("No matching landmarks found in Elasticsearch.")
            
        # Return the highest confidence hit
        return response['hits']['hits'][0]['_source']
