import os
import pygame

class Piece(pygame.sprite.Sprite):
    def __init__(self, filename, cols, rows):
        pygame.sprite.Sprite.__init__(self)
        # Load the spritesheet image for chess pieces
        self.spritesheet = pygame.image.load(filename).convert_alpha()

        self.cols = cols
        self.rows = rows
        self.cell_count = cols * rows

        self.rect = self.spritesheet.get_rect()
        # Calculate the width and height of each individual cell (piece image) on the spritesheet
        w = self.cell_width = self.rect.width // self.cols
        h = self.cell_height = self.rect.height // self.rows

        # Create a list of rectangles, each representing the position and size of a piece on the spritesheet
        self.cells = list([(i % cols * w, i // cols * h, w, h) for i in range(self.cell_count)])

        # Mapping of piece names to their index on the spritesheet.
        # ALL pieces are now mapped to the 'white_pawn' index (5).
        # This makes every piece on the board appear as a white pawn.
        # If you wanted them all to be black pawns, you would use index 11.
        self.pieces = {
            "white_pawn":   5,
            "white_knight": 5, # Changed to white_pawn
            "white_bishop": 5, # Changed to white_pawn
            "white_rook":   5, # Changed to white_pawn
            "white_king":   5, # Changed to white_pawn
            "white_queen":  5, # Changed to white_pawn
            "black_pawn":   5, # Changed to white_pawn (originally 11)
            "black_knight": 5, # Changed to white_pawn
            "black_bishop": 5, # Changed to white_pawn
            "black_rook":   5, # Changed to white_pawn
            "black_king":   5, # Changed to white_pawn
            "black_queen":  5  # Changed to white_pawn
        }

    def draw(self, surface, piece_name, coords):
        # Get the sprite index for the given piece name from the modified dictionary
        piece_index = self.pieces[piece_name]
        # Draw the piece onto the surface at the specified coordinates,
        # using the calculated cell from the spritesheet.
        surface.blit(self.spritesheet, coords, self.cells[piece_index])
