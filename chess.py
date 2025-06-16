import pygame
from pygame.locals import *
import random

from piece import Piece
from utils import Utils

import time


class Chess(object):
    def __init__(self, screen, pieces_src, square_coords, square_length):
        # display surface
        self.screen = screen
        # create an object of class to show chess pieces on the board
        self.chess_pieces = Piece(pieces_src, cols=6, rows=2)
        # store coordinates of the chess board squares
        self.board_locations = square_coords
        # length of the side of a chess board square
        self.square_length = square_length
        # dictionary to keeping track of player turn
        self.turn = {"black": 0,
                     "white": 0}

        # list containing possible moves for the selected piece
        self.moves = []
        #
        self.utils = Utils()

        # mapping of piece names to index of list containing piece coordinates on spritesheet
        # These mappings are now based on Thai Chess piece names
        self.pieces = {
            "white_ขุน": 0,
            "white_เม็ด": 1,
            "white_โคน": 2,
            "white_ม้า": 3,
            "white_เรือ": 4,
            "white_เบี้ย": 5,
            "black_ขุน": 6,
            "black_เม็ด": 7,
            "black_โคน": 8,
            "black_ม้า": 9,
            "black_เรือ": 10,
            "black_เบี้ย": 11
        }

        # list containing captured pieces
        self.captured = []
        #
        self.winner = ""

        self.reset()

    def reset(self):
        # clear moves lists
        self.moves = []

        # randomize player turn
        x = random.randint(0, 1)
        if (x == 1):
            self.turn["black"] = 1
        elif (x == 0):
            self.turn["white"] = 1

        # two dimensonal dictionary containing details about each board location
        # storage format is [piece_name, currently_selected, x_y_coordinate]
        self.piece_location = {}
        x = 0
        for i in range(97, 105):  # 'a' to 'h'
            a = 8
            y = 0
            self.piece_location[chr(i)] = {}
            while a > 0:
                # [piece name, currently selected, board coordinates]
                self.piece_location[chr(i)][a] = ["", False, [x, y]]
                a = a - 1
                y = y + 1
            x = x + 1

        # Reset the board for Thai Chess
        # White pieces (bottom of the board)
        # Row 1 (actual index 7)
        self.piece_location['a'][1][0] = "white_เรือ"  # White Ruea (Rook)
        self.piece_location['b'][1][0] = "white_ม้า"  # White Ma (Knight)
        self.piece_location['c'][1][0] = "white_โคน"  # White Kon (Bishop)
        self.piece_location['d'][1][0] = "white_เม็ด"  # White Met (Queen)
        self.piece_location['e'][1][0] = "white_ขุน"  # White Khun (King)
        self.piece_location['f'][1][0] = "white_โคน"  # White Kon (Bishop)
        self.piece_location['g'][1][0] = "white_ม้า"  # White Ma (Knight)
        self.piece_location['h'][1][0] = "white_เรือ"  # White Ruea (Rook)

        # Row 2 (actual index 6) - Pawns in Thai Chess start on the 3rd rank
        # This means original row 7 in standard chess is now empty
        # The pawns are on row 3 (actual index 5)
        # So we clear row 2 for white pieces and place pawns on row 3
        # self.piece_location[chr(i)][2][0] = "" # Clear original row 2

        # Row 3 (actual index 5) - White Pawns
        for i in range(97, 105):  # 'a' to 'h'
            self.piece_location[chr(i)][3][0] = "white_เบี้ย"  # White Bia (Pawn)

        # Black pieces (top of the board)
        # Row 8 (actual index 0)
        self.piece_location['a'][8][0] = "black_เรือ"  # Black Ruea (Rook)
        self.piece_location['b'][8][0] = "black_ม้า"  # Black Ma (Knight)
        self.piece_location['c'][8][0] = "black_โคน"  # Black Kon (Bishop)
        self.piece_location['d'][8][0] = "black_เม็ด"  # Black Met (Queen)
        self.piece_location['e'][8][0] = "black_ขุน"  # Black Khun (King)
        self.piece_location['f'][8][0] = "black_โคน"  # Black Kon (Bishop)
        self.piece_location['g'][8][0] = "black_ม้า"  # Black Ma (Knight)
        self.piece_location['h'][8][0] = "black_เรือ"  # Black Ruea (Rook)

        # Row 7 (actual index 1) - Pawns in Thai Chess start on the 6th rank
        # This means original row 7 in standard chess is now empty
        # The pawns are on row 6 (actual index 2)
        # So we clear row 7 for black pieces and place pawns on row 6
        # self.piece_location[chr(i)][7][0] = "" # Clear original row 7

        # Row 6 (actual index 2) - Black Pawns
        for i in range(97, 105):  # 'a' to 'h'
            self.piece_location[chr(i)][6][0] = "black_เบี้ย"  # Black Bia (Pawn)

    #
    def play_turn(self):
        # white color
        white_color = (255, 255, 255)
        # create fonts for texts
        small_font = pygame.font.SysFont("comicsansms", 20)
        # create text to be shown on the game menu - Changed to Thai
        if self.turn["black"]:
            turn_text = small_font.render("ตา: ดำ", True, white_color)  # Turn: Black
        elif self.turn["white"]:
            turn_text = small_font.render("ตา: ขาว", True, white_color)  # Turn: White

        # show welcome text
        self.screen.blit(turn_text,
                         ((self.screen.get_width() - turn_text.get_width()) // 2,
                          10))

        # let player with black piece play
        if (self.turn["black"]):
            self.move_piece("black")
        # let player with white piece play
        elif (self.turn["white"]):
            self.move_piece("white")

    # method to draw pieces on the chess board
    def draw_pieces(self):
        transparent_green = (0, 194, 39, 170)
        transparent_blue = (28, 21, 212, 170)

        # create a transparent surface
        surface = pygame.Surface((self.square_length, self.square_length), pygame.SRCALPHA)
        surface.fill(transparent_green)

        surface1 = pygame.Surface((self.square_length, self.square_length), pygame.SRCALPHA)
        surface1.fill(transparent_blue)

        # loop to change background color of selected piece
        for val in self.piece_location.values():
            for value in val.values():
                # name of the piece in the current location
                piece_name = value[0]
                # x, y coordinates of the current piece
                piece_coord_x, piece_coord_y = value[2]

                # change background color of piece if it is selected
                if value[1] and len(value[0]) > 5:
                    # if the piece selected is a black piece
                    if value[0][:5] == "black":
                        self.screen.blit(surface, self.board_locations[piece_coord_x][piece_coord_y])
                        if len(self.moves) > 0:
                            for move in self.moves:
                                x_coord = move[0]
                                y_coord = move[1]
                                if x_coord >= 0 and y_coord >= 0 and x_coord < 8 and y_coord < 8:
                                    self.screen.blit(surface, self.board_locations[x_coord][y_coord])
                    # if the piece selected is a white piece
                    elif value[0][:5] == "white":
                        self.screen.blit(surface1, self.board_locations[piece_coord_x][piece_coord_y])
                        if len(self.moves) > 0:
                            for move in self.moves:
                                x_coord = move[0]
                                y_coord = move[1]
                                if x_coord >= 0 and y_coord >= 0 and x_coord < 8 and y_coord < 8:
                                    self.screen.blit(surface1, self.board_locations[x_coord][y_coord])

        # draw all chess pieces
        for val in self.piece_location.values():
            for value in val.values():
                # name of the piece in the current location
                piece_name = value[0]
                # x, y coordinates of the current piece
                piece_coord_x, piece_coord_y = value[2]
                # check if there is a piece at the square
                if (len(value[0]) > 1):
                    # draw piece on the board
                    self.chess_pieces.draw(self.screen, piece_name,
                                           self.board_locations[piece_coord_x][piece_coord_y])

    # method to find the possible moves of the selected piece
    def possible_moves(self, piece_name, piece_coord):
        # list to store possible moves of the selected piece
        positions = []
        # find the possible locations to put a piece
        if len(piece_name) > 0:
            # get x, y coordinate
            x_coord, y_coord = piece_coord

            # calculate moves for ขุน (Khun - King)
            if "ขุน" in piece_name:
                # Can move one square in any direction (like international chess king)
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        new_x, new_y = x_coord + dx, y_coord + dy
                        if 0 <= new_x < 8 and 0 <= new_y < 8:
                            positions.append([new_x, new_y])

            # calculate moves for เม็ด (Met - Queen/Counselor)
            elif "เม็ด" in piece_name:
                # Can move one square diagonally
                for dx in [-1, 1]:
                    for dy in [-1, 1]:
                        new_x, new_y = x_coord + dx, y_coord + dy
                        if 0 <= new_x < 8 and 0 <= new_y < 8:
                            positions.append([new_x, new_y])

            # calculate moves for โคน (Kon - Bishop/Noble)
            elif "โคน" in piece_name:
                # Can move one square diagonally, or one square forward
                # Diagonal moves
                for dx in [-1, 1]:
                    for dy in [-1, 1]:
                        new_x, new_y = x_coord + dx, y_coord + dy
                        if 0 <= new_x < 8 and 0 <= new_y < 8:
                            positions.append([new_x, new_y])

                # Forward move
                if "white" in piece_name:
                    if y_coord - 1 >= 0:
                        positions.append([x_coord, y_coord - 1])
                elif "black" in piece_name:
                    if y_coord + 1 < 8:
                        positions.append([x_coord, y_coord + 1])

            # calculate moves for ม้า (Ma - Knight)
            elif "ม้า" in piece_name:
                # Can move in an L-shape (2 squares in one direction, then 1 square perpendicular)
                # Similar to international chess knight, but slightly different movement rules are often applied in Thai chess variations.
                # Here, we'll stick to the "traditional" L-shape similar to international knight
                # to keep it consistent with the base code structure.
                knight_moves = [
                    (x_coord - 1, y_coord - 2), (x_coord + 1, y_coord - 2),
                    (x_coord - 2, y_coord - 1), (x_coord + 2, y_coord - 1),
                    (x_coord - 2, y_coord + 1), (x_coord + 2, y_coord + 1),
                    (x_coord - 1, y_coord + 2), (x_coord + 1, y_coord + 2)
                ]
                for new_x, new_y in knight_moves:
                    if 0 <= new_x < 8 and 0 <= new_y < 8:
                        positions.append([new_x, new_y])

            # calculate moves for เรือ (Ruea - Rook)
            elif "เรือ" in piece_name:
                # Can move any number of squares horizontally or vertically (like international chess rook)
                positions = self.linear_moves(positions, piece_name, piece_coord)

            # calculate moves for เบี้ย (Bia - Pawn)
            elif "เบี้ย" in piece_name:
                # White pawns move one square forward. After crossing the midline, they can also move one square diagonally forward.
                # Black pawns move one square forward. After crossing the midline, they can also move one square diagonally forward.

                # White pawn
                if "white" in piece_name:
                    # Move one square forward
                    if y_coord - 1 >= 0:
                        new_y = y_coord - 1
                        # Check if the square in front is empty or occupied by an enemy piece (for captures)
                        columnChar_forward = chr(97 + x_coord)
                        rowNo_forward = 8 - new_y
                        piece_in_front = self.piece_location[columnChar_forward][rowNo_forward][0]
                        if not piece_in_front:  # Only move forward if empty
                            positions.append([x_coord, new_y])

                    # Promotion: Not implemented in this version, pawns become promoted Khuns
                    # when reaching the opponent's 6th rank (row 3 for white, row 6 for black).

                    # Capturing diagonally
                    # Check left diagonal
                    if x_coord - 1 >= 0 and y_coord - 1 >= 0:
                        new_x, new_y = x_coord - 1, y_coord - 1
                        columnChar_diag = chr(97 + new_x)
                        rowNo_diag = 8 - new_y
                        diag_piece = self.piece_location[columnChar_diag][rowNo_diag][0]
                        if "black" in diag_piece:  # Capture enemy piece
                            positions.append([new_x, new_y])

                    # Check right diagonal
                    if x_coord + 1 < 8 and y_coord - 1 >= 0:
                        new_x, new_y = x_coord + 1, y_coord - 1
                        columnChar_diag = chr(97 + new_x)
                        rowNo_diag = 8 - new_y
                        diag_piece = self.piece_location[columnChar_diag][rowNo_diag][0]
                        if "black" in diag_piece:  # Capture enemy piece
                            positions.append([new_x, new_y])


                # Black pawn
                elif "black" in piece_name:
                    # Move one square forward
                    if y_coord + 1 < 8:
                        new_y = y_coord + 1
                        # Check if the square in front is empty or occupied by an enemy piece (for captures)
                        columnChar_forward = chr(97 + x_coord)
                        rowNo_forward = 8 - new_y
                        piece_in_front = self.piece_location[columnChar_forward][rowNo_forward][0]
                        if not piece_in_front:  # Only move forward if empty
                            positions.append([x_coord, new_y])

                    # Promotion: Not implemented in this version, pawns become promoted Khuns
                    # when reaching the opponent's 3rd rank (row 3 for white, row 6 for black).

                    # Capturing diagonally
                    # Check left diagonal
                    if x_coord - 1 >= 0 and y_coord + 1 < 8:
                        new_x, new_y = x_coord - 1, y_coord + 1
                        columnChar_diag = chr(97 + new_x)
                        rowNo_diag = 8 - new_y
                        diag_piece = self.piece_location[columnChar_diag][rowNo_diag][0]
                        if "white" in diag_piece:  # Capture enemy piece
                            positions.append([new_x, new_y])

                    # Check right diagonal
                    if x_coord + 1 < 8 and y_coord + 1 < 8:
                        new_x, new_y = x_coord + 1, y_coord + 1
                        columnChar_diag = chr(97 + new_x)
                        rowNo_diag = 8 - new_y
                        diag_piece = self.piece_location[columnChar_diag][rowNo_diag][0]
                        if "white" in diag_piece:  # Capture enemy piece
                            positions.append([new_x, new_y])

            # Filter out moves to squares occupied by own pieces
            to_remove = []
            for pos in positions:
                x, y = pos
                columnChar = chr(97 + x)
                rowNo = 8 - y
                des_piece_name = self.piece_location[columnChar][rowNo][0]
                if des_piece_name and des_piece_name.split('_')[0] == piece_name.split('_')[0]:
                    to_remove.append(pos)

            for i in to_remove:
                if i in positions:  # Ensure it's still in the list before removing
                    positions.remove(i)

        # return list containing possible moves for the selected piece
        return positions

    def move_piece(self, turn):
        # get the coordinates of the square selected on the board
        square = self.get_selected_square()

        # if a square was selected
        if square:
            # get name of piece on the selected square
            piece_name = square[0]
            # color of piece on the selected square
            piece_color = piece_name.split('_')[0] if piece_name else ""  # Handle empty piece_name
            # board column character
            columnChar = square[1]
            # board row number
            rowNo = square[2]

            # get x, y coordinates
            x, y = self.piece_location[columnChar][rowNo][2]

            # if there's a piece on the selected square
            if (len(piece_name) > 0) and (piece_color == turn):
                # find possible moves for thr piece
                self.moves = self.possible_moves(piece_name, [x, y])

                # change selection flag from all other pieces
                for k in self.piece_location.keys():
                    for key in self.piece_location[k].keys():
                        self.piece_location[k][key][1] = False

                # change selection flag of the selected piece
                self.piece_location[columnChar][rowNo][1] = True

            # If a square is clicked and a piece is already selected, try to move it
            elif self.moves:  # A piece is already selected and has possible moves
                clicked_pos = [x, y]  # The coordinates of the newly clicked square
                if clicked_pos in self.moves:
                    # Check if the destination square has an opponent's piece
                    current_piece_name = ""
                    current_piece_coords = []
                    for k in self.piece_location.keys():
                        for key in self.piece_location[k].keys():
                            if self.piece_location[k][key][1]:  # Find the currently selected piece
                                current_piece_name = self.piece_location[k][key][0]
                                current_piece_coords = self.piece_location[k][key][2]
                                break
                        if current_piece_name:
                            break

                    target_piece_name = self.piece_location[columnChar][rowNo][0]

                    if target_piece_name and target_piece_name.split('_')[0] != turn:
                        # Capture the piece
                        self.capture_piece(turn, [columnChar, rowNo], clicked_pos)
                    else:
                        # Move to an empty square or a square with own piece (which should be filtered out by possible_moves)
                        self.validate_move(clicked_pos)

                    # Clear moves and unselect all pieces after a move attempt
                    self.moves = []
                    for k in self.piece_location.keys():
                        for key in self.piece_location[k].keys():
                            self.piece_location[k][key][1] = False

    def get_selected_square(self):
        # get left event
        left_click = self.utils.left_click_event()

        # if there's a mouse event
        if left_click:
            # get mouse event
            mouse_event = self.utils.get_mouse_event()

            for i in range(len(self.board_locations)):
                for j in range(len(self.board_locations)):
                    rect = pygame.Rect(self.board_locations[i][j][0], self.board_locations[i][j][1],
                                       self.square_length, self.square_length)
                    collision = rect.collidepoint(mouse_event[0], mouse_event[1])
                    if collision:
                        selected = [rect.x, rect.y]
                        # find x, y coordinates the selected square
                        for k in range(len(self.board_locations)):
                            #
                            try:
                                l = None
                                l = self.board_locations[k].index(selected)
                                if l != None:
                                    # reset color of all selected pieces
                                    for val in self.piece_location.values():
                                        for value in val.values():
                                            # [piece name, currently selected, board coordinates]
                                            if not value[1]:
                                                value[1] = False

                                    # get column character and row number of the chess piece
                                    columnChar = chr(97 + k)
                                    rowNo = 8 - l
                                    # get the name of the
                                    piece_name = self.piece_location[columnChar][rowNo][0]

                                    return [piece_name, columnChar, rowNo]
                            except:
                                pass
        else:
            return None

    def capture_piece(self, turn, chess_board_coord, piece_coord):
        # get x, y coordinate of the destination piece
        x, y = piece_coord

        # get chess board coordinate
        columnChar, rowNo = chess_board_coord

        p = self.piece_location[columnChar][rowNo]

        # Check if the captured piece is a Khun (King)
        if "white_ขุน" == p[0]:  # If white king is captured
            self.winner = "ดำ"  # Black wins
            print("ดำ ชนะ!")  # Black wins!
        elif "black_ขุน" == p[0]:  # If black king is captured
            self.winner = "ขาว"  # White wins
            print("ขาว ชนะ!")  # White wins!

        # add the captured piece to list
        self.captured.append(p)
        # move source piece to its destination
        self.validate_move(piece_coord)

    def validate_move(self, destination):
        desColChar = chr(97 + destination[0])
        desRowNo = 8 - destination[1]

        for k in self.piece_location.keys():
            for key in self.piece_location[k].keys():
                board_piece = self.piece_location[k][key]

                if board_piece[1]:  # If this is the currently selected piece
                    # unselect the source piece
                    self.piece_location[k][key][1] = False
                    # get the name of the source piece
                    piece_name = self.piece_location[k][key][0]

                    # Move the source piece to the destination
                    self.piece_location[desColChar][desRowNo][0] = piece_name

                    # Remove source piece from its current position
                    self.piece_location[k][key][0] = ""

                    # Change turn
                    if (self.turn["black"]):
                        self.turn["black"] = 0
                        self.turn["white"] = 1
                    elif (self.turn["white"]):  # Corrected from "white" to self.turn["white"]
                        self.turn["black"] = 1
                        self.turn["white"] = 0

                    src_location = k + str(key)
                    des_location = desColChar + str(desRowNo)
                    print(f"{piece_name} moved from {src_location} to {des_location}")  # Changed to f-string

                    # Important: Once a piece is moved, break out of the loops
                    # to prevent further iteration over piece_location which might lead to unexpected behavior.
                    return

    # helper function to find diagonal moves (used by Ruea and Met for specific moves if applicable)
    def diagonal_moves(self, positions, piece_name, piece_coord):
        # reset x and y coordinate values
        x, y = piece_coord
        # find top left diagonal spots
        while (True):
            x = x - 1
            y = y - 1
            if (x < 0 or y < 0):
                break
            else:
                # Check for blocking pieces before adding to positions
                columnChar = chr(97 + x)
                rowNo = 8 - y
                p = self.piece_location[columnChar][rowNo][0]

                if p and p.split('_')[0] == piece_name.split('_')[0]:  # Blocked by own piece
                    break

                positions.append([x, y])

                if p and p.split('_')[0] != piece_name.split('_')[0]:  # Blocked by enemy piece (can capture)
                    break

        # reset x and y coordinate values
        x, y = piece_coord
        # find bottom right diagonal spots
        while (True):
            x = x + 1
            y = y + 1
            if (x > 7 or y > 7):
                break
            else:
                # Check for blocking pieces
                columnChar = chr(97 + x)
                rowNo = 8 - y
                p = self.piece_location[columnChar][rowNo][0]

                if p and p.split('_')[0] == piece_name.split('_')[0]:  # Blocked by own piece
                    break

                positions.append([x, y])

                if p and p.split('_')[0] != piece_name.split('_')[0]:  # Blocked by enemy piece (can capture)
                    break

        # reset x and y coordinate values
        x, y = piece_coord
        # find bottom left diagonal spots
        while (True):
            x = x - 1
            y = y + 1
            if (x < 0 or y > 7):
                break
            else:
                # Check for blocking pieces
                columnChar = chr(97 + x)
                rowNo = 8 - y
                p = self.piece_location[columnChar][rowNo][0]

                if p and p.split('_')[0] == piece_name.split('_')[0]:  # Blocked by own piece
                    break

                positions.append([x, y])

                if p and p.split('_')[0] != piece_name.split('_')[0]:  # Blocked by enemy piece (can capture)
                    break

        # reset x and y coordinate values
        x, y = piece_coord
        # find top right diagonal spots
        while (True):
            x = x + 1
            y = y - 1
            if (x > 7 or y < 0):
                break
            else:
                # Check for blocking pieces
                columnChar = chr(97 + x)
                rowNo = 8 - y
                p = self.piece_location[columnChar][rowNo][0]

                if p and p.split('_')[0] == piece_name.split('_')[0]:  # Blocked by own piece
                    break

                positions.append([x, y])

                if p and p.split('_')[0] != piece_name.split('_')[0]:  # Blocked by enemy piece (can capture)
                    break

        return positions

    # helper function to find horizontal and vertical moves (used by Ruea)
    def linear_moves(self, positions, piece_name, piece_coord):
        # reset x, y coordinate value
        x, y = piece_coord
        # horizontal moves to the left
        while (x > 0):
            x = x - 1
            # Check for blocking pieces before adding to positions
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo][0]

            if p and p.split('_')[0] == piece_name.split('_')[0]:  # Blocked by own piece
                break

            positions.append([x, y])

            if p and p.split('_')[0] != piece_name.split('_')[0]:  # Blocked by enemy piece (can capture)
                break

        # reset x, y coordinate value
        x, y = piece_coord
        # horizontal moves to the right
        while (x < 7):
            x = x + 1
            # Check for blocking pieces
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo][0]

            if p and p.split('_')[0] == piece_name.split('_')[0]:  # Blocked by own piece
                break

            positions.append([x, y])

            if p and p.split('_')[0] != piece_name.split('_')[0]:  # Blocked by enemy piece (can capture)
                break

                # reset x, y coordinate value
        x, y = piece_coord
        # vertical moves upwards
        while (y > 0):
            y = y - 1
            # Check for blocking pieces
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo][0]

            if p and p.split('_')[0] == piece_name.split('_')[0]:  # Blocked by own piece
                break

            positions.append([x, y])

            if p and p.split('_')[0] != piece_name.split('_')[0]:  # Blocked by enemy piece (can capture)
                break

        # reset x, y coordinate value
        x, y = piece_coord
        # vertical moves downwards
        while (y < 7):
            y = y + 1
            # Check for blocking pieces
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo][0]

            if p and p.split('_')[0] == piece_name.split('_')[0]:  # Blocked by own piece
                break

            positions.append([x, y])

            if p and p.split('_')[0] != piece_name.split('_')[0]:  # Blocked by enemy piece (can capture)
                break

        return positions
