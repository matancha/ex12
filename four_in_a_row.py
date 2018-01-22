from tkinter import *
import tkinter.messagebox as messagebox
from game import Game
import math
from communicator import Communicator
from ai import AI

PLAYER_TYPE_ARGUMENT = 1
PORT_ARGUMENT = 2
IP_ARGUMENT = 3
MAXIMUM_PORT_NUMBER = 65535

# Options are: "white", "black", "red", "green", "blue", "cyan", "yellow", and "magenta"
BOARD_COLOR = "orange"
EMPTY_SPACE_COLOR = "white"
BACKGROUND_COLOR = "white"
WINNING_DISK_COLOR = "red"
COLOR_PLAYER_ONE = "green"
COLOR_PLAYER_2 = "yellow"

WIN_MSG = 'Player {0} wins!'
DISK_SIZE = 100


class GUI:

    def __init__(self, root, game, communicator, player, ai=None):
        self.__root = root
        self.__game = game
        self.__communicator = communicator
        self._player = player
        self.__ai = ai

        self.__canvas = Canvas(self.__root, bg=BACKGROUND_COLOR, height=(Game.NUM_ROWS + 1) * DISK_SIZE,
                               width=Game.NUM_COLUMNS * DISK_SIZE)
        self.__canvas.bind('<Button-1>', self.play_turn)
        self.__canvas.bind("<Enter>", self.entering)
        self.__canvas.bind("<Motion>", self.move)
        self.__canvas.bind("<Leave>", self.out_of)
        self.__canvas.pack()

        self.__communicator.bind_action_to_message(self.play_turn_message)
        self.__dict_of_disks = {}
        self.__list_of_items = []

        self._create_initial_screen()

        if self.__ai is not None and self.__game.get_current_player() == self._player:
            self.__ai.find_legal_move(self.__game, self.play_turn_ai)

    def _create_initial_screen(self):

        for row in range(DISK_SIZE, (Game.NUM_ROWS + 1) * DISK_SIZE, DISK_SIZE):
            for column in range(0, Game.NUM_COLUMNS * DISK_SIZE, DISK_SIZE):
                self.__canvas.create_rectangle((column, row), (column + DISK_SIZE, row + DISK_SIZE), fill=BOARD_COLOR)
                self.__canvas.create_oval((column, row), (column + DISK_SIZE, row + DISK_SIZE), fill=EMPTY_SPACE_COLOR)

    def play_turn(self, event):
        last_turn = self.__game.get_last_move()
        column = self.calculating_column(event.x)
        if self.__ai is not None:
            messagebox.showinfo("You're not playing!", 'AI game, cannot be controlled by player')
        elif last_turn is None:
            if self._player != self.__game.PLAYER_ONE:
                messagebox.showinfo("Not your turn!", 'Wait for other player to make move')
                return
        elif self.__game.get_player_at(last_turn[0], last_turn[1]) == self._player:
            messagebox.showinfo("Not your turn!", 'Wait for other player to make move')
            return

        try:
            self.__game.make_move(column)
        except ValueError:
            messagebox.showinfo('illegal move', 'try again!')

        self._place_disk_on_board()
        self.__communicator.send_message("Put disk in column {0}".format(column))
        self._handle_end_game()
        self.__game.set_current_player()

    def play_turn_ai(self, column):

        self.__game.make_move(int(column))
        self._place_disk_on_board()
        self.__communicator.send_message("Put disk in column {0}".format(column))
        self._handle_end_game()
        self.__game.set_current_player()

    def play_turn_message(self, message):

        column = int(message[-1])
        self.__game.make_move(int(column))
        self._place_disk_on_board()
        self._handle_end_game()
        self.__game.set_current_player()

        if self.__ai is not None:
            self.__ai.find_legal_move(self.__game, self.play_turn_ai)

    def _handle_end_game(self):

        status = self.__game.get_winner()

        if status is not None:
            if status == self.__game.PLAYER_ONE or status == self.__game.PLAYER_TWO:
                for coord in self.__game.get_winning_path():
                    disk = self.__dict_of_disks[self._get_coordinates(coord)]
                    self.__canvas.itemconfig(disk, fill=WINNING_DISK_COLOR)
                msg = WIN_MSG.format(status + 1)
            else:
                msg = 'Draw!'

            messagebox.showinfo('Game over!', msg)
            self.__canvas.delete(self.__list_of_items[0])
            self.__list_of_items.pop()


    def _place_disk_on_board(self):
        color = self._get_color(self.__game.get_current_player())
        start_column, start_row = self._get_coordinates(self.__game.get_last_move())
        disk = self.__canvas.create_oval((start_column, start_row),
                                         (start_column + DISK_SIZE, start_row + DISK_SIZE), fill=color)
        self.__dict_of_disks[start_column, start_row] = disk

    def _get_color(self, current_player):
        return COLOR_PLAYER_ONE if current_player == self.__game.PLAYER_ONE else COLOR_PLAYER_2

    def entering(self, event):
        if not self.__game.is_game_over():
            item=self.__canvas.create_oval((self.calculating_column(event.x), 0,
                                            self.calculating_column(event.x) + DISK_SIZE, DISK_SIZE),
                                           fill=self._get_color(self.__game.get_current_player()))
            self.__list_of_items.append(item)

    def move(self, event):
        if not self.__game.is_game_over():
            self.__canvas.delete(self.__list_of_items[-1])
            self.__list_of_items.pop()
            item = self.__canvas.create_oval((self.calculating_column(event.x) * DISK_SIZE, 0,
                                              self.calculating_column(event.x) * DISK_SIZE + DISK_SIZE, DISK_SIZE),
                                             fill=self._get_color(self.__game.get_current_player()))
            self.__list_of_items.append(item)

    def calculating_column(self, x):
        return math.floor(x/DISK_SIZE)

    def out_of(self, event):
        if not self.__game.is_game_over():
            self.__canvas.delete(self.__list_of_items[-1])
            self.__list_of_items.pop()

    def _get_coordinates(self, coord_tuple):
        return coord_tuple[0] * DISK_SIZE, coord_tuple[1] * DISK_SIZE + DISK_SIZE


def check_args(arg_list):
    if len(arg_list) < 3 or len(arg_list) > 4 or arg_list[PLAYER_TYPE_ARGUMENT] not in ['ai', 'human'] or \
        not arg_list[PORT_ARGUMENT].isdigit() or \
                    int(arg_list[PORT_ARGUMENT]) < 0 or int(arg_list[PORT_ARGUMENT]) > MAXIMUM_PORT_NUMBER:
        print('Illegal program arguments')
        return False

    return True


def main(argv):
    if not check_args(argv):
        return
    client = False
    game = Game()
    root = Tk()

    player_type = argv[PLAYER_TYPE_ARGUMENT]
    port = int(argv[PORT_ARGUMENT])
    if len(argv) == 4:
        ip = argv[IP_ARGUMENT]
        client = True
    if player_type == 'ai':
        ai = AI()

    if client:
        communicator = Communicator(root, port, ip)
        player = game.PLAYER_TWO
        if player_type == 'human':
            GUI(root, game, communicator, player)
        else:
            GUI(root, game, communicator, player, ai)
    else:
        communicator = Communicator(root, port)
        player = game.PLAYER_ONE
        if player_type == 'human':
             GUI(root, game, communicator, player)
        else:
             GUI(root, game, communicator, player, ai)

    communicator.connect()
    root.mainloop()


if __name__ == '__main__':
    main(sys.argv)