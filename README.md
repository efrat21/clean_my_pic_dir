The App:

1. Scans your photo folder.
3. Generates image fingerprints/embeddings.
4. Groups similar photos.
5. Compares quality.
6. Shows recommendations.
7. Deletes or archives duplicates.

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
 
 

