from openai import OpenAI
import json
import cv2
import os
from typing import Dict, Any
import numpy as np


def llm_select_best(photo_scores: list[Dict[str, Any]]) -> str:
    prompt = f"""
You are a photo quality expert.

Choose the best image to keep.

Prioritize:
1. Sharpness (blur_score)
2. Resolution
3. File quality
4. Newer image if all else is equal

Return JSON only.
JSON format:
{{
    "pic2keep": str,
    "pic2archive": list[str],
    "reason": str
}}

Photos:

{photo_scores}

"""

    client = OpenAI()

    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )

    decision = response.output_text

    return json.loads(decision)


def score_image(path):
    """Score an image based on its quality.
    metrics: Resolution, Sharpness, Noise, Compression Artifacts, Color Accuracy, File Size
     - Resolution: Higher resolution images are generally of better quality.
        - Sharpness: Sharp images are usually of higher quality than blurry ones.
        - Noise: Images with less noise are typically of better quality.
        - Compression Artifacts: Images with fewer compression artifacts are generally of higher quality.
        - Color Accuracy: Images with accurate colors are usually of better quality.
        - File Size: smaller files may idicates cropping, which means it is after prossing, which may indicate better quality.

        return json with the following format:
        {
  "resolution":12000000,
  "blur":550,
  "size_mb":4.3, 
  "noise":0.2,
    "compression_artifacts":0.1,
    "color_accuracy":0.9,
    }
    
    """
    resolution = get_resolution(path)
    blur = get_blur(path)
    noise = get_noise(path)
    compression_artifacts = get_compression_artifacts(path)
    color_accuracy = get_color_accuracy(path)
    size_mb = get_size_mb(path)
    edited_time = os.path.getmtime(path)


    return {
        "resolution": resolution,
        "blur": blur,
        "size_mb": size_mb,
        "noise": noise,
        "compression_artifacts": compression_artifacts,
        "color_accuracy": color_accuracy,
        "edited_time": edited_time
    }

def get_resolution(path: str) -> int:
    """Return total pixel count: width * height."""
    image = cv2.imread(path)
    if image is None:
        raise ValueError(f"Could not read image: {path}")

    height, width = image.shape[:2]
    return int(width * height)


def get_blur(path: str) -> float:
    """
    Estimate sharpness using variance of the Laplacian.
    Higher value => sharper image.
    """
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Could not read image: {path}")

    return float(cv2.Laplacian(image, cv2.CV_64F).var())


def get_noise(path: str) -> float:
    """
    Rough noise estimate based on high-frequency residual energy.
    Lower is generally better.
    """
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Could not read image: {path}")

    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    residual = image.astype(np.float32) - blurred.astype(np.float32)

    noise_std = float(np.std(residual))
    return noise_std


def get_compression_artifacts(path: str) -> float:
    """
    Rough JPEG compression artifact estimate based on block boundary discontinuities.
    Higher value => more likely visible block artifacts.
    """
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Could not read image: {path}")

    h, w = image.shape

    if h < 16 or w < 16:
        return 0.0

    image = image.astype(np.float32)

    vertical_scores = []
    for x in range(8, w, 8):
        boundary_diff = np.abs(image[:, x] - image[:, x - 1]).mean()

        local_diffs = []
        if x - 2 >= 0:
            local_diffs.append(np.abs(image[:, x - 1] - image[:, x - 2]).mean())
        if x + 1 < w:
            local_diffs.append(np.abs(image[:, x + 1] - image[:, x]).mean())

        local_mean = np.mean(local_diffs) if local_diffs else 0.0
        vertical_scores.append(max(0.0, boundary_diff - local_mean))

    horizontal_scores = []
    for y in range(8, h, 8):
        boundary_diff = np.abs(image[y, :] - image[y - 1, :]).mean()

        local_diffs = []
        if y - 2 >= 0:
            local_diffs.append(np.abs(image[y - 1, :] - image[y - 2, :]).mean())
        if y + 1 < h:
            local_diffs.append(np.abs(image[y + 1, :] - image[y, :]).mean())

        local_mean = np.mean(local_diffs) if local_diffs else 0.0
        horizontal_scores.append(max(0.0, boundary_diff - local_mean))

    all_scores = vertical_scores + horizontal_scores
    return float(np.mean(all_scores)) if all_scores else 0.0


def get_color_accuracy(path: str) -> float:
    """
    Very rough color-quality proxy.
    Since true color accuracy requires a reference image or color chart,
    this returns a heuristic score in [0, 1] based on:
      - clipping penalty
      - oversaturation penalty
      - low-contrast penalty

    1.0 is better.
    """
    image = cv2.imread(path)
    if image is None:
        raise ValueError(f"Could not read image: {path}")

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)

    # Clipping: too many pixels near 0 or 255 often indicates poor tonal fidelity
    clipped_low = np.mean(image_rgb <= 3)
    clipped_high = np.mean(image_rgb >= 252)
    clipping_penalty = min(1.0, (clipped_low + clipped_high) * 4.0)

    # Saturation analysis in HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    saturation = hsv[:, :, 1] / 255.0
    value = hsv[:, :, 2] / 255.0

    oversat_penalty = max(0.0, float(np.mean(saturation) - 0.85)) / 0.15
    oversat_penalty = min(1.0, oversat_penalty)

    # Very low contrast may indicate washed out / poor tonal rendering
    luminance = 0.2126 * image_rgb[:, :, 0] + 0.7152 * image_rgb[:, :, 1] + 0.0722 * image_rgb[:, :, 2]
    contrast = float(np.std(luminance) / 64.0)
    low_contrast_penalty = max(0.0, 1.0 - min(1.0, contrast))

    penalty = 0.5 * clipping_penalty + 0.25 * oversat_penalty + 0.25 * low_contrast_penalty
    score = max(0.0, min(1.0, 1.0 - penalty))
    return float(score)


def get_size_mb(path: str) -> float:
    """Return file size in megabytes."""
    size_bytes = os.path.getsize(path)
    return round(size_bytes / (1024 * 1024), 3)
