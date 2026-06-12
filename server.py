from mcp.server.fastmcp import FastMCP
from services.quality_service import score_image
from services.similarity_service import find_similar_photos
from tools.filesystem import scan_folder
from tools.archive import archive_photo
from tools.quality import select_best_photo

mcp = FastMCP("PhotoCleaner")

mcp.tool()(scan_folder) 
mcp.tool()(find_similar_photos) 
mcp.tool()(score_image) 
mcp.tool()(select_best_photo) 
mcp.tool()(archive_photo)

if __name__ == "__main__": 
    mcp.run()