

import mcp

from services.image_service import archive_photo

@mcp.tool()
def archive_photo_tool(photo_path: str):
    return archive_photo(photo_path)