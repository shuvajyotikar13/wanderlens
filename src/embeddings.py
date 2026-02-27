import vertexai
from vertexai.vision_models import MultiModalEmbeddingModel, Image
from src.config import PROJECT_ID, LOCATION # Managed in your config.py

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

class MultiModalEmbedder:
    def __init__(self, model_name: str = "multimodalembedding@001"):
        """Initializes the Vertex AI Multimodal Embedding model."""
        self.model = MultiModalEmbeddingModel.from_pretrained(model_name)

    def get_embeddings(self, text: str = None, image_path: str = None):
        """
        Generates a 1408-dimension vector from text, an image, or both.
        """
        image = None
        if image_path:
            # Load the image from a local path or GCS URI
            image = Image.load_from_file(image_path)

        try:
            embeddings = self.model.get_embeddings(
                image=image,
                contextual_text=text
            )
            
            # Return the multimodal vector as a list of floats
            # .image_embedding and .text_embedding are aligned in the same space
            if image and text:
                return embeddings.image_embedding # Combined context
            elif image:
                return embeddings.image_embedding
            else:
                return embeddings.text_embedding
                
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return None

# Simple test execution
if __name__ == "__main__":
    embedder = MultiModalEmbedder()
    vector = embedder.get_embeddings(text="Tropical beach resort with private pool")
    print(f"Vector Length: {len(vector)}") # Should be 1408
