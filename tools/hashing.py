from PIL import Image
import imagehash
import mcp

@mcp.tool()
def get_hash(path):
    image = Image.open(path)
    return str(imagehash.phash(image))