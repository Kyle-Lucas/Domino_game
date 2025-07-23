"""
Improved Domino Tile Cropping Tool
This script provides multiple approaches for accurately cropping domino tiles
"""

from PIL import Image, ImageTk
import os
import json

def create_coordinate_template():
    """Create a template file for manual coordinate input"""
    
    # Generate all domino combinations
    domino_tiles = []
    for i in range(7):
        for j in range(i, 7):
            domino_tiles.append((i, j))
    
    # Create coordinate template
    coordinates = {}
    for left, right in domino_tiles:
        tile_name = f"tile_{left}_{right}"
        coordinates[tile_name] = {
            "left": 0,    # x coordinate of left edge
            "top": 0,     # y coordinate of top edge  
            "width": 115, # width based on your example
            "height": 208 # height based on your example
        }
    
    # Save template to JSON file
    with open('tile_coordinates.json', 'w') as f:
        json.dump(coordinates, f, indent=4)
    
    print("Created tile_coordinates.json template file")
    print("You can edit this file to specify exact coordinates for each tile")
    print("\nExample entry:")
    print('{')
    print('    "tile_0_0": {')
    print('        "left": 100,   # x position where tile starts')
    print('        "top": 50,     # y position where tile starts') 
    print('        "width": 115,  # tile width')
    print('        "height": 208  # tile height')
    print('    }')
    print('}')

def crop_from_coordinates():
    """Crop tiles using coordinates from JSON file"""
    
    if not os.path.exists('tile_coordinates.json'):
        print("Error: tile_coordinates.json not found!")
        print("Run create_coordinate_template() first")
        return
    
    try:
        # Load coordinates
        with open('tile_coordinates.json', 'r') as f:
            coordinates = json.load(f)
        
        # Load source image
        tile_set = Image.open('Tile_Set.jpg')
        print(f"Loaded Tile_Set.jpg - Size: {tile_set.size}")
        
        # Create tiles directory
        tiles_dir = 'tiles'
        if not os.path.exists(tiles_dir):
            os.makedirs(tiles_dir)
        
        # Crop each tile
        cropped_count = 0
        for tile_name, coords in coordinates.items():
            left = coords['left']
            top = coords['top'] 
            width = coords['width']
            height = coords['height']
            
            # Skip if coordinates are still default (0,0)
            if left == 0 and top == 0:
                print(f"Skipping {tile_name} - coordinates not set")
                continue
            
            # Calculate crop box
            right = left + width
            bottom = top + height
            
            # Crop the tile
            tile_crop = tile_set.crop((left, top, right, bottom))
            
            # Save as PNG to preserve quality
            filename = f"{tiles_dir}/{tile_name}.png"
            tile_crop.save(filename)
            
            print(f"Cropped: {filename}")
            cropped_count += 1
        
        print(f"\nSuccessfully cropped {cropped_count} tiles!")
        
        # Create mapping file
        create_tile_mapping_from_coords(coordinates)
        
    except Exception as e:
        print(f"Error cropping tiles: {e}")

def create_tile_mapping_from_coords(coordinates):
    """Create tile mapping file from coordinates"""
    
    mapping_content = '''"""
Domino tile image mappings
This file contains mappings from domino values to image filenames
"""

# Dictionary mapping (left, right) values to image filenames
TILE_IMAGES = {
'''
    
    # Generate all domino combinations in order
    domino_tiles = []
    for i in range(7):
        for j in range(i, 7):
            domino_tiles.append((i, j))
    
    for left_val, right_val in domino_tiles:
        tile_name = f"tile_{left_val}_{right_val}"
        if tile_name in coordinates:
            mapping_content += f"    ({left_val}, {right_val}): 'tiles/{tile_name}.png',\n"
    
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
    
    print("Created tile_mappings.py")

def create_sample_coordinates():
    """Create a sample with a few tiles to demonstrate the format"""
    
    sample_coords = {
        "tile_0_0": {
            "left": 50,
            "top": 100, 
            "width": 115,
            "height": 208,
            "note": "Double blank - usually top-left area"
        },
        "tile_6_6": {
            "left": 200,
            "top": 300,
            "width": 115, 
            "height": 208,
            "note": "Double six - usually bottom-right area"
        }
    }
    
    with open('sample_coordinates.json', 'w') as f:
        json.dump(sample_coords, f, indent=4)
    
    print("Created sample_coordinates.json with example format")

def quick_crop_known_tiles():
    """Quick crop for tiles we can easily identify"""
    
    try:
        tile_set = Image.open('Tile_Set.jpg')
        
        # Create tiles directory
        tiles_dir = 'tiles'
        if not os.path.exists(tiles_dir):
            os.makedirs(tiles_dir)
        
        # Use your Tile0.png as the 0-0 tile (double blank)
        if os.path.exists('Tile0.png'):
            tile0 = Image.open('Tile0.png')
            tile0.save(f'{tiles_dir}/tile_0_0.png')
            print("Copied Tile0.png as tile_0_0.png")
        
        print("Quick crop completed!")
        print("Now you need to manually locate and specify coordinates for the remaining 27 tiles")
        
    except Exception as e:
        print(f"Error in quick crop: {e}")

def show_instructions():
    """Show detailed instructions for manual cropping"""
    
    print("=== DOMINO TILE CROPPING INSTRUCTIONS ===")
    print()
    print("Since your Tile_Set.jpg has a complex layout, here are your options:")
    print()
    print("OPTION 1: Manual Coordinate Input")
    print("1. Run: create_coordinate_template()")
    print("2. Open tile_coordinates.json in a text editor")
    print("3. For each tile, specify the exact left, top coordinates")
    print("4. Run: crop_from_coordinates()")
    print()
    print("OPTION 2: Use Image Editor")
    print("1. Open Tile_Set.jpg in an image editor (Paint, GIMP, etc.)")
    print("2. Crop each tile manually to 115x208 pixels")
    print("3. Save as: tile_0_0.png, tile_0_1.png, etc.")
    print("4. Place all files in a 'tiles' folder")
    print()
    print("OPTION 3: Hybrid Approach")
    print("1. Use your existing Tile0.png as tile_0_0.png")
    print("2. Manually crop a few more key tiles (like tile_6_6)")
    print("3. Use coordinates for the rest")
    print()
    print("Your tile dimensions should be: 115 x 208 pixels")
    print("File format: PNG (better quality than JPG)")

if __name__ == "__main__":
    print("Improved Domino Tile Cropping Tool")
    print("=" * 50)
    
    show_instructions()
    
    print("\nAvailable functions:")
    print("- create_coordinate_template(): Create JSON template for coordinates")
    print("- create_sample_coordinates(): Create sample coordinate file")
    print("- crop_from_coordinates(): Crop tiles using JSON coordinates")
    print("- quick_crop_known_tiles(): Copy your Tile0.png and set up structure")
    print("- show_instructions(): Show these instructions again")
    
    print("\nStarting with quick setup...")
    quick_crop_known_tiles()
    create_coordinate_template()
    create_sample_coordinates()
