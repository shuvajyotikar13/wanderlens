import json
import os
from elasticsearch import Elasticsearch
from src.config import ELASTIC_URL, ELASTIC_API_KEY # Adjust based on your config.py setup

# Initialize the Elasticsearch client
es_client = Elasticsearch(
    ELASTIC_URL,
    api_key=ELASTIC_API_KEY
)

def create_index_with_mapping(index_name: str = "wanderlens_destinations", mapping_file: str = "schemas/mapping.json"):
    """
    Reads the Elasticsearch mapping JSON file and creates the index if it doesn't exist.
    """
    try:
        # 1. Check if the index already exists to prevent overwrite errors
        if es_client.indices.exists(index=index_name):
            print(f"Index '{index_name}' already exists. Skipping creation.")
            return True

        # 2. Resolve the absolute path to the mapping file
        # This ensures it finds 'schemas/mapping.json' from the project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        full_mapping_path = os.path.join(project_root, mapping_file)

        # 3. Read the mapping JSON
        with open(full_mapping_path, 'r') as file:
            mapping_data = json.load(file)

        # 4. Create the index
        es_client.indices.create(index=index_name, body=mapping_data)
        print(f"Successfully created index '{index_name}' with schema from {mapping_file}")
        return True

    except FileNotFoundError:
        print(f"Error: Mapping file not found at {full_mapping_path}. Please ensure the schemas directory exists.")
        return False
    except Exception as e:
        print(f"Error creating Elasticsearch index: {e}")
        return False

# Example usage (you might call this from your orchestrator or a setup script)
if __name__ == "__main__":
    create_index_with_mapping()
