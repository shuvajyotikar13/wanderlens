import os
from src.embeddings import MultiModalEmbedder
from src.elastic_client import es_client, create_index_with_mapping
from src.llm_agent import TravelAgent  # Assuming this exists in llm_agent.py

class WanderLensOrchestrator:
    def __init__(self):
        self.embedder = MultiModalEmbedder()
        self.agent = TravelAgent()
        
        # Ensure the index is ready on startup
        create_index_with_mapping()

    def handle_user_query(self, user_text: str = None, image_path: str = None):
        """
        Coordinates the RAG (Retrieval-Augmented Generation) flow.
        """
        # 1. Generate Multimodal Embedding
        print(f"Generating embedding for: {user_text or 'Image input'}...")
        query_vector = self.embedder.get_embeddings(text=user_text, image_path=image_path)
        
        if not query_vector:
            return "Sorry, I couldn't process the input for search."

        # 2. Vector Search in Elasticsearch
        # This finds the top 3 most similar destinations from your schema
        search_results = self.search_destinations(query_vector)
        
        # 3. Synthesize Final Response with Gemini
        # We pass the search results as 'context' to the LLM
        final_itinerary = self.agent.generate_itinerary(
            user_intent=user_text, 
            context_data=search_results
        )
        
        return final_itinerary

    def search_destinations(self, vector: list, top_k: int = 3):
        """
        Performs the KNN (K-Nearest Neighbor) search in Elasticsearch.
        """
        query = {
            "field": "embedding",
            "query_vector": vector,
            "k": top_k,
            "num_candidates": 100
        }
        
        response = es_client.knn_search(
            index="wanderlens_destinations",
            knn=query,
            source=["destination_name", "description", "price_range", "category"]
        )
        
        # Format the hits for the LLM
        return [hit["_source"] for hit in response["hits"]["hits"]]

# Test the flow
if __name__ == "__main__":
    orchestrator = WanderLensOrchestrator()
    # Example: User provides a prompt
    result = orchestrator.handle_user_query(user_text="A quiet mountain retreat for hiking")
    print(f"\n--- AI RECOMMENDATION ---\n{result}")
