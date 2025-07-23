"""
Script to crop individual domino tiles from Tile_Set.jpg
This will create separate image files for each domino tile (0-0 through 6-6)
"""

from PIL import Image
import os

def crop_domino_tiles():
    """
    Crop individual domino tiles from Tile_Set.jpg
    Assumes the tile set is arranged in a grid format
    """
    
    # Load the tile set image
    try:
        tile_set = Image.open('Tile_Set.jpg')
        print(f"Loaded Tile_Set.jpg - Size: {tile_set.size}")
    except FileNotFoundError:
        print("Error: Tile_Set.jpg not found!")
        return
    except Exception as e:
        print(f"Error loading image: {e}")
        return
    
    # Create tiles directory if it doesn't exist
    tiles_dir = 'tiles'
    if not os.path.exists(tiles_dir):
        os.makedirs(tiles_dir)
        print(f"Created directory: {tiles_dir}")
    
    # Get image dimensions
    width, height = tile_set.size
    print(f"Image dimensions: {width} x {height}")
    
    # Domino tiles are typically arranged in a 7x8 grid (28 tiles total)
    # Let's try to detect the grid automatically
    
    # For a standard domino set, we have tiles from 0-0 to 6-6
    # That's 28 tiles total, often arranged as 7 columns x 4 rows or 4 columns x 7 rows
    
    # Let's try different grid configurations
    possible_grids = [
        (7, 4),  # 7 columns, 4 rows
        (4, 7),  # 4 columns, 7 rows
        (14, 2), # 14 columns, 2 rows
        (2, 14), # 2 columns, 14 rows
        (28, 1), # All in one row
        (1, 28)  # All in one column
    ]
    
    print("Trying different grid configurations...")
    
    # Let's start with the most common: 7x4 grid
    cols, rows = 7, 4
    tile_width = width // cols
    tile_height = height // rows
    
    print(f"Using grid: {cols} columns x {rows} rows")
    print(f"Each tile size: {tile_width} x {tile_height}")
    
    # Generate all domino combinations (0-0 through 6-6)
    domino_tiles = []
    for i in range(7):
        for j in range(i, 7):
            domino_tiles.append((i, j))
    
    print(f"Total domino tiles to extract: {len(domino_tiles)}")
    
    # Crop each tile
    tile_index = 0
    for row in range(rows):
        for col in range(cols):
            if tile_index >= len(domino_tiles):
                break
                
            # Calculate crop coordinates
            left = col * tile_width
            top = row * tile_height
            right = left + tile_width
            bottom = top + tile_height
            
            # Crop the tile
            tile_crop = tile_set.crop((left, top, right, bottom))
            
            # Get the domino values for this tile
            left_val, right_val = domino_tiles[tile_index]
            
            # Save the cropped tile
            filename = f"{tiles_dir}/tile_{left_val}_{right_val}.jpg"
            tile_crop.save(filename)
            
            print(f"Saved: {filename} (position {col}, {row})")
            
            tile_index += 1
        
        if tile_index >= len(domino_tiles):
            break
    
    print(f"\nSuccessfully extracted {tile_index} domino tiles!")
    print(f"Tiles saved in '{tiles_dir}' directory")
    
    # Create a mapping file for easy reference
    create_tile_mapping(domino_tiles[:tile_index])

def create_tile_mapping(domino_tiles):
    """Create a Python file with tile filename mappings"""
    
    mapping_content = '''"""
Domino tile image mappings
This file contains mappings from domino values to image filenames
"""

# Dictionary mapping (left, right) values to image filenames
TILE_IMAGES = {
'''
    
    for left_val, right_val in domino_tiles:
        mapping_content += f"    ({left_val}, {right_val}): 'tiles/tile_{left_val}_{right_val}.jpg',\n"
    
    mapping_content += '''}

def get_tile_image(left, right):
    """Get the image filename for a domino tile"""
    return TILE_IMAGES.get((left, right), None)

def get_all_tile_images():
    """Get all tile image filenames"""
    return list(TILE_IMAGES.values())
'''
    
    with open('tile_mappings.py', 'w') as f:
        f.write(mapping_content)
    
    print("Created tile_mappings.py for easy image access")

def preview_extraction():
    """Preview what the extraction will look like without actually cropping"""
    try:
        tile_set = Image.open('Tile_Set.jpg')
        width, height = tile_set.size
        
        print("=== TILE EXTRACTION PREVIEW ===")
        print(f"Source image: Tile_Set.jpg ({width} x {height})")
        
        # Try 7x4 grid
        cols, rows = 7, 4
        tile_width = width // cols
        tile_height = height // rows
        
        print(f"Grid configuration: {cols} columns x {rows} rows")
        print(f"Each tile will be: {tile_width} x {tile_height} pixels")
        
        # Show what tiles will be extracted
        domino_tiles = []
        for i in range(7):
            for j in range(i, 7):
                domino_tiles.append((i, j))
        
        print(f"Will extract {len(domino_tiles)} tiles:")
        for i, (left, right) in enumerate(domino_tiles):
            row = i // cols
            col = i % cols
            print(f"  tile_{left}_{right}.jpg (row {row}, col {col})")
            
    except Exception as e:
        print(f"Error in preview: {e}")

if __name__ == "__main__":
    print("Domino Tile Cropping Script")
    print("=" * 40)
    
    # First show preview
    preview_extraction()
    
    print("\n" + "=" * 40)
    print("Proceeding with automatic extraction...")
    crop_domino_tiles()
