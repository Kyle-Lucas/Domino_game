
#Recoding the whole game using WindSurf(v0.10)


import random
import os

class DominoGame:
    def __init__(self):
        self.tiles = []
        self.players = []
        self.board = []
        self.board_left = 0
        self.board_right = 0
        self.current_player = 0
        self.game_over = False

    def generate_tiles(self):
        """Generate all 28 domino tiles (0-0 through 6-6)"""
        self.tiles = []
        for i in range(0, 7):
            for k in range(i, 7):
                self.tiles.append(Tile(i, k, 0))  # 0 means unassigned
    
    def create_players(self):
        """Create 4 players"""
        player_names = ["Kalm", "Claire", "Akasha", "Shiva"]
        self.players = []
        for name in player_names:
            self.players.append(Player(name, 0))
    
    def assign_tiles(self):
        """Randomly assign 7 tiles to each of the 4 players"""
        for player_index in range(4):
            while self.players[player_index].tiles_assigned < 7:
                rand_tile = random.randint(0, 27)
                if self.tiles[rand_tile].assigned == 0:  # If tile is unassigned
                    self.tiles[rand_tile].assigned = player_index + 1  # Assign to player (1-4)
                    self.players[player_index].tiles_assigned += 1
    
    def setup_game(self):
        """Initialize the complete game setup"""
        self.generate_tiles()
        self.create_players()
        self.assign_tiles()

    def play_round(self):
        """Main game loop"""
        while not self.game_over:
            self.play_turn()
    
    def find_double_six(self):
        """Find who has the double-six tile to start the game"""
        for i, tile in enumerate(self.tiles):
            if tile.left == 6 and tile.right == 6:
                return tile.assigned
        return None
    
    def display_player_tiles(self, player_num):
        """Display all tiles for a specific player"""
        player = self.players[player_num - 1]
        print(f"\nTiles for {player.name}:")
        player_tiles = []
        for i, tile in enumerate(self.tiles):
            if tile.assigned == player_num:
                player_tiles.append((i, tile))
                print(f"  {i}: {tile}")
        return player_tiles
    
    def display_board(self):
        """Display the current game board"""
        print("\n" + "="*100)
        if self.board:
            board_str = ' '.join(self.board)
            print(board_str.center(100))
        else:
            print("Board is empty".center(100))
        print("="*100)
    
    def start_game(self):
        """Start the game with the player who has double-six"""
        starter = self.find_double_six()
        if not starter:
            print("No double-six found! Cannot start game.")
            return
        
        # Set the starting player
        self.current_player = starter - 1  # Convert to 0-based index
        
        # Place the double-six on the board
        for i, tile in enumerate(self.tiles):
            if tile.left == 6 and tile.right == 6 and tile.assigned == starter:
                self.board.append(str(tile))
                self.board_left = 6
                self.board_right = 6
                tile.assigned = 0  # Mark as played
                self.players[starter-1].tiles_assigned -= 1
                break
        
        print(f"\n{self.players[starter-1].name} starts with the double-six!")
        self.display_board()
        
        # Start the main game loop
        self.play_game()
    
    def can_play_tile(self, tile_index):
        """Check if a tile can be played on the current board"""
        if tile_index < 0 or tile_index >= len(self.tiles):
            return False
        
        tile = self.tiles[tile_index]
        if tile.assigned != self.current_player + 1:  # Player doesn't own this tile
            return False
        
        if not self.board:  # Empty board
            return True
        
        return tile.can_connect_to(self.board_left, self.board_right)
    
    def play_tile(self, tile_index):
        """Play a tile on the board"""
        if not self.can_play_tile(tile_index):
            print("Cannot play that tile!")
            return False
        
        tile = self.tiles[tile_index]
        
        # Determine where and how to place the tile
        if tile.left == self.board_left:
            # Place on left side, flipped
            self.board.insert(0, f"| {tile.right} | {tile.left} |")
            self.board_left = tile.right
        elif tile.right == self.board_left:
            # Place on left side, as is
            self.board.insert(0, str(tile))
            self.board_left = tile.left
        elif tile.left == self.board_right:
            # Place on right side, as is
            self.board.append(str(tile))
            self.board_right = tile.right
        elif tile.right == self.board_right:
            # Place on right side, flipped
            self.board.append(f"| {tile.right} | {tile.left} |")
            self.board_right = tile.left
        
        # Mark tile as played
        tile.assigned = 0
        self.players[self.current_player].tiles_assigned -= 1
        
        print(f"\n{self.players[self.current_player].name} played tile {tile_index}: {tile}")
        return True
    
    def next_turn(self):
        """Move to the next player's turn"""
        self.current_player = (self.current_player + 1) % 4
    
    def check_win_condition(self):
        """Check if any player has won (no tiles left)"""
        for player in self.players:
            if player.tiles_assigned == 0:
                self.game_over = True
                print(f"\n*** {player.name} WINS! ***")
                return True
        return False
    
    def player_has_valid_moves(self, player_num):
        """Check if a player has any valid moves"""
        for i, tile in enumerate(self.tiles):
            if tile.assigned == player_num and self.can_play_tile(i):
                return True
        return False
    
    def play_turn(self):
        """Handle a single player's turn"""
        current_player_num = self.current_player + 1
        player = self.players[self.current_player]
        
        print(f"\n--- {player.name}'s Turn ---")
        
        # Check if player has valid moves
        if not self.player_has_valid_moves(current_player_num):
            print(f"{player.name} has no valid moves and must pass.")
            self.next_turn()
            return
        
        # Display current board and player's tiles
        self.display_board()
        self.display_player_tiles(current_player_num)
        
        # For now, we'll simulate a move (you can add input later)
        # Find first valid tile and play it
        for i, tile in enumerate(self.tiles):
            if tile.assigned == current_player_num and self.can_play_tile(i):
                self.play_tile(i)
                break
        
        self.display_board()
        
        # Check win condition
        if not self.check_win_condition():
            self.next_turn()
    
    def play_game(self):
        """Main game loop"""
        turn_count = 0
        max_turns = 50  # Prevent infinite loops
        
        while not self.game_over and turn_count < max_turns:
            self.play_turn()
            turn_count += 1
            
            # Add a small pause for readability
            import time
            time.sleep(0.5)
        
        if turn_count >= max_turns:
            print("\nGame ended due to turn limit.")
        
        print("\n*** GAME OVER ***")

class Tile:
    def __init__(self, left, right, assigned):
        self.left = left
        self.right = right
        self.assigned = assigned

    def display(self):
        """Display this tile in a nice format"""
        print(f' | {self.left} | {self.right} | ')
    
    def __str__(self):
        """String representation of the tile"""
        return f'| {self.left} | {self.right} |'
    
    def can_connect_to(self, board_left, board_right):
        """Check if this tile can connect to either end of the board"""
        return (self.left == board_left or self.left == board_right or 
                self.right == board_left or self.right == board_right)

class Player:
    def __init__(self, name, tiles_assigned):
        self.name = name
        self.tiles_assigned = tiles_assigned
    
    def __str__(self):
        return f"Player: {self.name} (Tiles: {self.tiles_assigned})"


#### D E B U G  S P A C E #####


#### M A I N  ####

# Create a new game instance
game = DominoGame()

# Set up the game (generate tiles, create players, assign tiles)
game.setup_game()

# Display the initial setup
print("DOMINO GAME SETUP COMPLETE!")
print(f"Generated {len(game.tiles)} tiles")
print("Players:")
for i, player in enumerate(game.players):
    print(f"  {i+1}. {player}")

# Start and play the game!
print("\n" + "="*50)
print("STARTING DOMINO GAME!")
print("="*50)

game.start_game()

