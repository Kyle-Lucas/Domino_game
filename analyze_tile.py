"""
Script to analyze the user's Tile0.png example and understand the correct tile format
"""

from PIL import Image
import os

def analyze_tile_example():
    """Analyze the user's Tile0.png to understand correct format"""
    
    try:
        # Load the example tile
        tile_example = Image.open('Tile0.png')
        print(f"Loaded Tile0.png - Size: {tile_example.size}")
        print(f"Format: {tile_example.format}")
        print(f"Mode: {tile_example.mode}")
        
        # Also load the original tile set for comparison
        tile_set = Image.open('Tile_Set.jpg')
        print(f"\nOriginal Tile_Set.jpg - Size: {tile_set.size}")
        
        # Calculate aspect ratio
        example_width, example_height = tile_example.size
        aspect_ratio = example_width / example_height
        print(f"\nTile0.png aspect ratio: {aspect_ratio:.2f} (width/height)")
        
        # Suggest better cropping approach
        print("\n=== ANALYSIS RESULTS ===")
        print(f"Your example tile dimensions: {example_width} x {example_height}")
        print(f"This gives us the correct individual tile size to aim for.")
        
        # Now we need to figure out how tiles are arranged in Tile_Set.jpg
        set_width, set_height = tile_set.size
        print(f"\nTile_Set.jpg dimensions: {set_width} x {set_height}")
        
        # Calculate how many tiles could fit based on the example size
        tiles_per_row = set_width // example_width
        tiles_per_col = set_height // example_height
        
        print(f"Based on your example tile size:")
        print(f"  Possible tiles per row: {tiles_per_row}")
        print(f"  Possible tiles per column: {tiles_per_col}")
        print(f"  Total possible tiles: {tiles_per_row * tiles_per_col}")
        
        return example_width, example_height
        
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
        return None, None
    except Exception as e:
        print(f"Error analyzing tile: {e}")
        return None, None

def create_manual_cropping_guide():
    """Create a guide for manual tile positioning"""
    
    tile_width, tile_height = analyze_tile_example()
    
    if tile_width is None:
        return
    
    print("\n=== MANUAL CROPPING GUIDE ===")
    print("Since automatic grid detection failed, here's what we need to do:")
    print("1. Examine Tile_Set.jpg manually to identify tile positions")
    print("2. Create a mapping of each domino tile's exact coordinates")
    print("3. Use those coordinates to crop each tile individually")
    
    print(f"\nEach tile should be approximately {tile_width} x {tile_height} pixels")
    print("We need to locate all 28 domino tiles (0-0 through 6-6)")
    
    # Generate the list of all domino tiles we need
    domino_tiles = []
    for i in range(7):
        for j in range(i, 7):
            domino_tiles.append((i, j))
    
    print(f"\nTiles we need to find and crop:")
    for i, (left, right) in enumerate(domino_tiles):
        print(f"  {i+1:2d}. tile_{left}_{right}")
    
    print("\nNext steps:")
    print("1. Manually identify where each tile is located in Tile_Set.jpg")
    print("2. Create a coordinate mapping for precise cropping")
    print("3. Use those coordinates to extract each tile correctly")

if __name__ == "__main__":
    print("Domino Tile Analysis Script")
    print("=" * 40)
    create_manual_cropping_guide()
