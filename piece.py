import os
import pygame

class Piece(pygame.sprite.Sprite):
    def __init__(self, filename, cols, rows):
        pygame.sprite.Sprite.__init__(self)
        # Mapping Thai chess piece names to existing sprite sheet indices.
        # Note: The visual representation will still be the international chess pieces
        # unless a new 'pieces.png' with Thai chess pieces is provided.
        self.pieces = {
            "white_ขุน":   0, # White King (visually King)
            "white_เม็ด":   1, # White Met (Queen, visually Queen)
            "white_โคน":   2, # White Kon (Bishop, visually Bishop)
            "white_ม้า":   3, # White Ma (Knight, visually Knight)
            "white_เรือ":   4, # White Ruea (Rook, visually Rook)
            "white_เบี้ย":   5, # White Bia (Pawn, visually Pawn)
            "black_ขุน":   6, # Black King (visually King)
            "black_เม็ด":   7, # Black Met (Queen, visually Queen)
            "black_โคน":   8, # Black Kon (Bishop, visually Bishop)
            "black_ม้า":   9, # Black Ma (Knight, visually Knight)
            "black_เรือ":   10, # Black Ruea (Rook, visually Rook)
            "black_เบี้ย":   11 # Black Bia (Pawn, visually Pawn)
        }
        self.spritesheet = pygame.image.load(filename).convert_alpha()

        self.cols = cols
        self.rows = rows
        self.cell_count = cols * rows

        self.rect = self.spritesheet.get_rect()
        w = self.cell_width = self.rect.width // self.cols
        h = self.cell_height = self.rect.height // self.rows

        self.cells = list([(i % cols * w, i // cols * h, w, h) for i in range(self.cell_count)])

    def draw(self, surface, piece_name, coords):
        # Retrieve the piece index using the Thai piece name
        piece_index = self.pieces[piece_name]
        surface.blit(self.spritesheet, coords, self.cells[piece_index])

