import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Google Cloud
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")
    
    # Elasticsearch
    ES_URL = os.getenv("ES_URL")
    ES_API_KEY = os.getenv("ES_API_KEY")
    ES_INDEX_NAME = os.getenv("ES_INDEX_NAME", "landmarks-v1")
    
    # Travel APIs
    AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
    AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")
    GMAPS_API_KEY = os.getenv("GMAPS_API_KEY")
