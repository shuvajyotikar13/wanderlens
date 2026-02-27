from vertexai.vision_models import MultiModalEmbeddingModel, Image
from src.config import Config
import vertexai

vertexai.init(project=Config.GCP_PROJECT_ID, location=Config.GCP_LOCATION)

class EmbeddingService:
    def __init__(self):
        self.model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")

    def get_image_embedding(self, image_bytes: bytes) -> list[float]:
        """Converts raw image bytes into a 1408-dimensional vector."""
        img = Image(image_bytes)
        embeddings = self.model.get_embeddings(
            image=img,
            dimension=1408
        )
        return embeddings.image_embedding
