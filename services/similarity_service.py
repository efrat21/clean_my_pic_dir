import mcp
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
from PIL import Image
from sentence_transformers import SentenceTransformer
import numpy as np


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

def embed_image(image: bytes) -> list[float]:
    model = SentenceTransformer(
        "clip-ViT-B-32"
    )
    embedding = model.encode(image)
    return embedding.tolist()


def find_similar_photos(
    folder: str,
    similarity_threshold: float
):
    """
    Returns groups of visually similar photos.

    Example:
    [
        [
            "img1.jpg",
            "img2.jpg"
        ],
        [
            "img5.jpg",
            "img6.jpg",
            "img7.jpg"
        ]
    ]
    """

    folder_path = Path(folder)

    image_paths = [
        str(f)
        for f in folder_path.iterdir()
        if f.suffix.lower() in IMAGE_EXTENSIONS
    ]

    if len(image_paths) < 2:
        return []

    # Generate embeddings
    embeddings = []

    for path in image_paths:
        embeddings.append(embed_image(path))

    embeddings = np.array(embeddings)

    # Similarity matrix
    similarity_matrix = cosine_similarity(embeddings)

    visited = set()
    groups = []

    for i in range(len(image_paths)):

        if i in visited:
            continue

        current_group = [image_paths[i]]
        visited.add(i)

        for j in range(i + 1, len(image_paths)):

            if similarity_matrix[i][j] >= similarity_threshold:
                current_group.append(image_paths[j])
                visited.add(j)

        if len(current_group) > 1:
            groups.append(current_group)

    return groups