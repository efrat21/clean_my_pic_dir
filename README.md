The App:

Scans your photo folder.
Generates image fingerprints/embeddings.
Groups similar photos.
Compares quality.
Shows recommendations.
Deletes or archives duplicates.

Architecture:

User
 ↓
Claude / ChatGPT
 ↓
MCP Client
 ↓
Photo MCP Server
 ├── scan_folder()
 ├── get_image_hash()
 ├── get_image_embedding()
 ├── compare_images()
 ├── move_to_archive()
 └── delete_photo()
 
 

