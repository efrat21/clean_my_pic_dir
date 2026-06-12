
import mcp

from services.quality_service import llm_select_best, score_image


@mcp.tool()
def select_best_photo(photo_group: list):
    """
    Select best image from a similar-photo group.
    """

    photo_scores = []

    for photo in photo_group:
        score = score_image(photo)
        photo_scores.append(score)

    return llm_select_best(photo_scores)    