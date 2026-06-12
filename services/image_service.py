import os
import shutil

def archive_photo(photo_path: str, archive_dir: str = "archive") -> str:
    """Move a photo file into an archive directory and return the new path."""
    if not os.path.isfile(photo_path):
        raise FileNotFoundError(f"Photo not found: {photo_path}")

    os.makedirs(archive_dir, exist_ok=True)
    dest_path = os.path.join(archive_dir, os.path.basename(photo_path))
    shutil.move(photo_path, dest_path)
    return dest_path