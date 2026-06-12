import mcp
from sentence_transformers import SentenceTransformer

from services.similarity_service import find_similar_photos

@mcp.tool()
def find_similar_photos_tool(image: bytes) -> list[float]:
    return find_similar_photos(image, 0.95)