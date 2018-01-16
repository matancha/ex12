class Game:

    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    NUM_COLUMN=8
    NUM_ROWS=6
    ERROR_ILLEGAL_MOVE= "illegal move"

    def __init__(self):
        self.board = self.create_board()
        self.curent_player=Game.PLAYER_ONE
        self.last_move=None

    def make_move(self, column):
        for row in range(len(self.board[column]) - 1 ,-1,-1):
            if self.board[column][row] is None:
                self.board[column][row] = self.get_current_player()
                self.last_move =(column,row)
                break
            if row==0:
                #TODO: New error object
                raise Exception(Game.ERROR_ILLEGAL_MOVE)
        # self.set_current_player()

    def get_winner(self):
        paths = self.get_possible_paths()
        for path in paths:
            current_counter=0
            for disk in path:
                if disk == self.curent_player:
                    current_counter+=1
                    if current_counter == 4:
                        return self.curent_player
                else:
                    current_counter=0
        for column in self.board:
            for disk in column:
                if disk is None:
                    return None

        return Game.DRAW

    def get_possible_paths(self):
        paths = []

        row_path = [self.board[column][self.last_move[1]] for column in range(len(self.board))]
        paths.append(row_path)
        column_path =[self.board[self.last_move[0]][row] for row in range(len(self.board[0]))]
        paths.append(column_path)
        diag1=[]
        diag2=[]
        row=0
        while row!=self.NUM_ROWS-1:
            row,column=self.last_move
            diag1.append(self.board[row][column])
            row+=1
            column+=1


        return paths

    def get_player_at(self, col, row):
        return self.board[col][row]

    def get_current_player(self):
        return self.curent_player

    def set_current_player(self):
        if self.get_current_player()==Game.PLAYER_ONE:
            self.curent_player=Game.PLAYER_TWO
        else:
            self.curent_player=Game.PLAYER_ONE



    def create_board(self):
        board=[]
        for column in range(Game.NUM_COLUMN):
            row=[]
            for rows in range(Game.NUM_ROWS):
                row.append(None)
            board.append(row)
        return board


game = Game()
game.make_move(3)
while game.get_winner() is None:
    game.set_current_player()
    for row in game.board:
        print(row, end="\n")
    next_move = input('Column to place in?')
    game.make_move(int(next_move))

