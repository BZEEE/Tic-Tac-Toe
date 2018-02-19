
# V1 implements only a single player 'X' who can select 
# tiles using a regular cursor. A tile flashes when an 
# occupied tile is selected, but there is no win or draw
# indication at the end. The game runs until the player 
# closes the window.
from uagame import Window
import pygame, time, random
from pygame.locals import *

# User-defined functions

def main():

    window = Window('Tic Tac Toe', 500, 400)
    window.set_auto_update(False)
    game = Game(window)
    game.play()
    window.close()

# User-defined classes

class Game:
# An object in this class represents a complete game.

    def __init__(self, window):
        # Initialize a Game.
        # - self is the Game to initialize
        # - window is the uagame window object
        self.window = window
        self.bg_color = pygame.Color('black')
        self.fg_color_str = "green"
        self.pause_time = 0.04 # smaller is faster game
        self.close_clicked = False
        self.continue_game = True
        Tile.set_window(window) # call the class method inside the Tile Class
        
        self.board = []
        self.cursor_x = Cursor('cursor_x.txt')
        self.cursor_o = Cursor('cursor_o.txt')
        self.cursor_x.activate()
        self.player_x = 'X'
        self.player_o = 'O'
        self.turn = self.player_x
        self.filled = []
        self.flashers = []
        self.create_board()
        
        
        def create_board(self):
            for row_index in range(0,3):
                row = self.create_row(row_index)
                self.board.append(row)
                
        def create_row(self, row_index):
            row = []
            width = self.window.get_width() // 3
            height = self.window.get_height // 3
            y = height * row_index
            for col_index in range(0,3):
                #create a tile
                x = width * col_index
                atile = Tile(x, y, width, height)
                row.append(atile)
            return row
                

        def play(self):
            # Play the game until the player presses the close box.
            # - self is the Game that should be continued or not.

            while not self.close_clicked:
                self.handle_event()
            
                self.draw()
                if self.continue_game:
                    self.update()
                    self.decide_continue()
                time.sleep(self.pause_time) # set game velocity by pausing

        def handle_event(self):
            # Handle each user event by changing the game state
            # appropriately.
            # - self is the Game whose events will be handled

            event = pygame.event.poll()
            if event.type == QUIT:
                self.close_clicked = True
            if event.type == MOUSEBUTTONUP and self.continue_game:
                self.handle_mouse_up(event)
                
        def handle_mouse_up(self, event):
            for row in self.board:
                for tile in row:
                    if tile.select(event.pos, self.turn):
                        # add tile too filled
                        self.filled.append(tile)
                        # change turn
                        self.change_turn()
                        
        def change_turn(self):
            if self.turn == self.player_x:
                self.turn = self.player_o
                self.cursor_o.activate()
            else:
                self.turn = player_x
                self.cursor_x.activate()
                
        def draw(self):
            # Draw all game objects.
            # - self is the Game to draw
            self.window.clear()
            #the method choose_flasher will choose the tile that will flash from self.flashers
            self.choose_flasher()
            for row in self.board:
                for tile in row:
                    tile.draw()
            self.window.update()
            
        def choose_flasher():
            if len(self.flashers) != 0:
                tile = random.choice(self.flashers)
                tile.flash

        def update(self):
            # Update the game objects.
            # - self is the Game to update
            pass
        
        def is_diagonal_win(self):
            diagonal_win = False
            diagonal1 = [self.board[0][0], self.board[1][1], self.board[2][2]]
            diagonal2 = [self.board[2][0], self.board[1][1], self.board[0][2]]
            if self.is_list_win(diagonal1) or self.is_list_win(diagonal2):
                diagonal_win = True
            return diagonal_win
        
        def is_column_win(self):
            column_win = False
            for col_index in range(3):
                column = []
                for row_index in range(3):
                    tile = self.board[row_index][col_index]
                    column.appen(tile)
                if self.is_list_win(column):
                    column_win = True
            return column_win
        
        def is_row_win(self):
            row_win = False
            for row in self.boards:
                #what is this row?
                #this row is a list of 3 Tile objects
                if is_list_win(row):
                    row_win = True
            return row_win
                
        def is_list_win(self, alist):
            # - alist is a list of 3 Tile objects
            list_win = False
            if alist[0] == alist[1] == alist[2]:
                # == operator is going to call __eq__ method in the Tile class
                self.flashers = alist
                list_win = True
            return list_win
        
        def is_tie(self):
            tie = False
            if len(self.filled) == 9:
                tie = True
                self.flashers = self.filled
            return tie
        
        def is_win(self):
            win = False
            if self.is_row_win() or self.is_column_win() or self.is_diagonal_win():
                win = True
            return win
        
        def decide_continue(self):
            # Check and remember if the game should continue
            # - self is the Game to check
            if self.is_win() or self.is_tie():
                self.continue_game = False

class Tile:
    # class attributes
    window = None
    border_size = 3
    border_color = 'white'
    font_size = 133
    
    @classmethod
    def set_window(cls, window):
        cls.window = window
    def __init__(self, x, y, width, height):
        self.flashing = False
        self.content = ''
        self.rect = pygame.Rect(x, y, width, height)
    def draw(self):
        surface = Tile.window.get_suface()
        if self.flashing:
            #draw a white rectangle
            pygame.draw.rect(surface, pygame.Color(Tile.border_color), self.rect)
            self.flashing = False
        else:
            #draw a black rectangle with a white border
            self.draw_content()
            pygame.draw.rect(surface, pygame.Color(Tile.border_color), self.rect, Tile.border_size)
            
    def draw_content(self):
        # consider location, size, and color
        Tile.window.set_font_color(Tile.border_color)
        Tile.window.set_font_size(Tile.font_size)
        string_width = Tile.window.get_string_width(self.content)
        string_height = Tile.window.get_font_height()
        left_over_x = self.rect.width - string_width
        left_over_y = self.rect.height - string_height
        x = self.rect.x + left_over_x
        y = self.rect.y + left_over_y
        Tile.window.draw_string(self.content, x, y)
        
    def select(self, position, player):
        # position is the (x,y) location of the mouse click
        valid_click = False
        if self.rect.collidepoint(position):
            if self.content == '':
                self.content = player
                valid_click = True
            else:
                self.flashing = True
        return valid_click
                
    def __eq__(self, other_tile):
        if self.content != '' and self.content == other_tile:
            return True
        else:
            return False
        
    def flash(self):
        self.flashing = True
        
class Cursor:
    def __init__(self, filename):
        # step 1 open a file
        # - use built in function to open a file
        # modes 'r' = read mode, 'w' = write mode, 'a' = append mode
        # infile is this type of object (TextIOWrapper)
        infile = open(filename, 'r')
        
        # step 2 read the file
        # .read() is a method inside the TextIOWrapper class
        # content is of type str, gives you back a string
        content = infile.read()
        
        # step 3 split the content and convert into a list of strings, split()
        list_of_strings = content.splitlines()
        # step 4 use a pygame function to generate the data and the mask
        # returns a tuple of the data (position 1) and the mask (position 2)
        compiled = pygame.cursors.compile(list_of_strings, black='$', white='*')
        self.data = compiled[0]
        self.mask = compiled[1]
        width = len(list_of_strings[0])
        height = len(list_of_strings)
        self.size = (width, height)
        self.hotspot = (width // 2, height // 2)
    
        
    def activate(self):
        # us
        pygame.mouse.set_cursor(self.size, self.hotspot, self.data, self.mask)
        
main()
