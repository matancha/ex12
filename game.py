

class Game:

    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    NUM_COLUMN=7
    NUM_ROWS=6
    ERROR_ILLEGAL_MOVE= "illegal move"
    WINNING_STREAK = 4
    RIGHT_DIAG_DIRECTION = (-1, 1)
    LEFT_DIAG_DIRECTION = (-1,-1)

    def __init__(self):
        self.board = self.create_board()
        self.current_player = Game.PLAYER_ONE
        self.__last_move = None
        self.__winner = False
        self.__winning_path = []

    def get_last_move(self):
        #this function returns last turn that was made
        return self.__last_move

    def get_winning_path(self):
        #this function returns paths of coordinstes
        #for distinguishing it on gui
        return self.__winning_path

    def set_last_move(self, col, row):
        #this function changes lst turn for copies of game in ai
        self.__last_move = col, row

    def set_board(self, col, row, val):
        #this function for changing value on the board for copies in ai
        self.board[col][row] = val

    def is_game_over(self):
        #this function checks if there is a winner
        return self.__winner

    def make_move(self, column):
        #this function make move on the board if the column is appropriate
        #else raise exeption
        if self.__winner:
            raise Exception(Game.ERROR_ILLEGAL_MOVE)
        for row in range(len(self.board[column])-1, -1, -1):
            #order of checking coordinates in list is reversed
            #because we have to check from the last row of chosen column to the first one
            if self.board[column][row] is None:
                self.board[column][row] = self.get_current_player()
                self.__last_move =(column,row)
                break
            if row == 0:
                #TODO: New error object
                raise Exception(Game.ERROR_ILLEGAL_MOVE)

    def get_winner(self):
        #this function checks if there is a winner or the result is draw
        #in case that already all columns are full and there is no winner
        paths = self.get_possible_paths()
        for path in paths:
            self.__winning_path = []
            for column, row in path:
                if self.board[column][row] == self.current_player:
                    self.__winning_path.append((column, row))
                    if len(self.__winning_path) == Game.WINNING_STREAK:
                        self.__winner = True
                        return self.current_player
                else:
                    self.__winning_path = []
        for column in self.board:
            for disk in column:
                if disk is None:
                    return None
        return Game.DRAW

    def get_possible_paths(self):
        #this function get possible paths of last turn
        #in 2 diagonals vertical,horizontal directions to find sequenses of numbers in a row
        paths = []
        row_path = [(column, self.__last_move[1]) for column in range(len(self.board))]
        paths.append(row_path)
        column_path =[(self.__last_move[0], row) for row in range(len(self.board[0]))]
        paths.append(column_path)

        right_diag = self.path_in_direction(Game.RIGHT_DIAG_DIRECTION)
        left_diag = self.path_in_direction(Game.LEFT_DIAG_DIRECTION)
        paths.append(right_diag)
        paths.append(left_diag)

        return paths

    def path_in_direction(self, direction):
        #this function return path according to inputed direction
        direction_path = []
        self.get_half_path(self.__last_move, direction_path, direction)
        self.get_half_path(self.__last_move, direction_path, direction, reversed=True)
        return direction_path

    def get_half_path(self, coordinate_tuple, path, direction, reversed=False):
        #this function for returning half of diagonal path
        if not self.is_in_board(coordinate_tuple):
            return

        if reversed is True:
            if coordinate_tuple not in path:
                path.append(coordinate_tuple)
            self.get_half_path((coordinate_tuple[0]-direction[0], coordinate_tuple[1]-direction[1]), path,
                               direction, reversed)
        else:
            self.get_half_path((coordinate_tuple[0]+direction[0], coordinate_tuple[1]+direction[1]), path,
                               direction, reversed)
            if coordinate_tuple not in path:
                path.append(coordinate_tuple)

    def is_in_board(self, coordinate_tuple):
        #this function check if coordinate of some coordinates in path are in range
        if (coordinate_tuple[0] >= 0 and coordinate_tuple[0] <= len(self.board)-1
            and coordinate_tuple[1] >= 0 and coordinate_tuple[1] <= len(self.board[0])-1):
            return True
        return False

    def get_player_at(self, col, row):
        #this function returns value of board
        #according to column and row was inputed
        return self.board[col][row]

    def get_current_player(self):
        #this function returns curent player of the game
        #which of turn is now
        return self.current_player

    def set_current_player(self):
        #this function for changing the current player
        if self.get_current_player()==Game.PLAYER_ONE:
            self.current_player=Game.PLAYER_TWO
        else:
            self.current_player=Game.PLAYER_ONE

    def create_board(self):
        #this function create empty board
        board = []
        for column in range(Game.NUM_COLUMN):
            row = []
            for rows in range(Game.NUM_ROWS):
                row.append(None)
            board.append(row)
        return board
    def get_board(self):
        #returns the current board
        return self.board


