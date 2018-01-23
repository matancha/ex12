#############################################################
# FILE : four_in_a_row.py
# WRITERS : Matan Toledano , matancha , 313591935
#           Ilya Bogov , molodoy , 342522471
# EXERCISE : intro2cs ex12 2017-2018
# DESCRIPTION: Runs the main flow of four_in_a_row in GUI
# mode.
#############################################################

from tkinter import *
import tkinter.messagebox as messagebox
from game import Game
import math
from communicator import Communicator
from ai import AI

PLAYER_TYPE_ARGUMENT = 1
AI_ARGUMENT = 'ai'
HUMAN_ARGUMENT = 'human'
PORT_ARGUMENT = 2
IP_ARGUMENT = 3
MAXIMUM_PORT_NUMBER = 65535

# Options are: "white", "black", "red", "green", "blue", "cyan", "yellow", and "magenta"
BOARD_COLOR = "orange"
EMPTY_SPACE_COLOR = "white"
BACKGROUND_COLOR = "white"
WINNING_DISK_COLOR = "red"
COLOR_PLAYER_ONE = "green"
COLOR_PLAYER_TWO = "yellow"

WIN_MSG = 'Player {0} wins!'
GAME_OVER_TITLE = 'Game over!'
DRAW_MSG = 'Draw!'
NOT_TURN_MSG = 'Wait for other player to make move'
NOT_TURN_TITLE = "Not your turn!"
UNPLAYABLE_MSG = 'AI game, cannot be controlled by player'
UNPLAYABLE_TITLE = "You're not playing!"
ILLEGAL_ARGUMENTS_MSG = 'Illegal program arguments.'
PROTOCOL_MSG = "Put disk in column {0}"
ILLEGAL_MOVE_MSG = 'try again!'
ILLEGAL_MOVE_TITLE = 'illegal move'
SCREEN_TITLE = 'Player {0}'
DISK_SIZE = 100


class GUI:

    def __init__(self, root, game, communicator, player, ai=None):
        self.__root = root
        self.__game = game
        self.__communicator = communicator
        self.__player = player
        self.__ai = ai

        self.__canvas = Canvas(self.__root, bg=BACKGROUND_COLOR, height=(Game.NUM_ROWS + 1) * DISK_SIZE,
                               width=Game.NUM_COLUMNS * DISK_SIZE)
        self.__canvas.bind('<Button-1>', self.play_turn)
        self.__canvas.bind("<Enter>", self.enter_canvas)
        self.__canvas.bind("<Motion>", self.move_cursor)
        self.__canvas.bind("<Leave>", self.out_of_canvas)
        self.__canvas.pack()

        self.__communicator.bind_action_to_message(self.play_turn_message)
        self.__dict_of_disks = {}
        self.__list_of_items = []

        self.__root.title(SCREEN_TITLE.format(self.__player + 1))
        self._create_initial_screen()

        if self.__ai is not None and self.__game.get_current_player() == self.__player:
            self.__ai.find_legal_move(self.__game, self.play_turn_ai)

    def _create_initial_screen(self):
        """
        Create screen at start of game
        """
        for row in range(DISK_SIZE, (Game.NUM_ROWS + 1) * DISK_SIZE, DISK_SIZE):
            for column in range(0, Game.NUM_COLUMNS * DISK_SIZE, DISK_SIZE):
                self.__canvas.create_rectangle((column, row), (column + DISK_SIZE, row + DISK_SIZE), fill=BOARD_COLOR)
                self.__canvas.create_oval((column, row), (column + DISK_SIZE, row + DISK_SIZE), fill=EMPTY_SPACE_COLOR)

    def play_turn(self, event):
        """
        Plays out course of turn, if it's the player's turn when he clicks the mouse. Places disk according
        to where the player clicked on.
        """
        last_turn = self.__game.get_last_move()
        column = self._calculating_column(event.x)
        if self.__ai is not None:
            messagebox.showinfo(UNPLAYABLE_TITLE, UNPLAYABLE_MSG)
            return
        elif last_turn is None:
            if self.__player != self.__game.PLAYER_ONE:
                messagebox.showinfo(NOT_TURN_TITLE, NOT_TURN_MSG)
                return
        elif self.__game.get_player_at(last_turn[0], last_turn[1]) == self.__player:
            messagebox.showinfo(NOT_TURN_TITLE, NOT_TURN_MSG)
            return

        try:
            self.__game.make_move(column)
        except ValueError:
            messagebox.showinfo(ILLEGAL_MOVE_TITLE, ILLEGAL_MOVE_MSG)
            return

        self._place_disk_on_board()
        self.__communicator.send_message(PROTOCOL_MSG.format(column))
        if self.__game.get_winner() is not None:
            self._handle_end_game()
            return
        self.__game.set_current_player()

    def play_turn_ai(self, column):
        """
        Gets column and plays out course of turn.
        """
        self.__game.make_move(int(column))
        self._place_disk_on_board()
        self.__communicator.send_message(PROTOCOL_MSG.format(column))
        if self.__game.get_winner() is not None:
            self._handle_end_game()
            return
        self.__game.set_current_player()

    def play_turn_message(self, message):
        """
        Gets a message from other player, parses it to get the last turn and mirrors it on the board.
        :param message:
        :return:
        """
        column = int(message[-1])
        self.__game.make_move(int(column))
        self._place_disk_on_board()
        if self.__game.get_winner() is not None:
            self._handle_end_game()
            return
        self.__game.set_current_player()

        if self.__ai is not None:
            self.__ai.find_legal_move(self.__game, self.play_turn_ai)

    def _handle_end_game(self):
        """
        Checks if game is over. The game is over if: 1. One of the players won. 2. There are no more legal moves
        - Draw. If the game is won, colors the disks involved in the victory.
        """
        status = self.__game.get_winner()

        if status is not None:
            if status == self.__game.PLAYER_ONE or status == self.__game.PLAYER_TWO:
                for coord in self.__game.get_winning_path():
                    disk = self.__dict_of_disks[self._get_coordinates(coord)]
                    self.__canvas.itemconfig(disk, fill=WINNING_DISK_COLOR)
                msg = WIN_MSG.format(status + 1)
            else:
                msg = DRAW_MSG

            messagebox.showinfo(GAME_OVER_TITLE, msg)
            if self.__list_of_items:
                self._delete_cursor()

    def _place_disk_on_board(self):
        """
        Places disk on board, with the player's color.
        """
        color = self._get_color(self.__game.get_current_player())
        start_column, start_row = self._get_coordinates(self.__game.get_last_move())
        disk = self.__canvas.create_oval((start_column, start_row),
                                         (start_column + DISK_SIZE, start_row + DISK_SIZE), fill=color)
        self.__dict_of_disks[start_column, start_row] = disk

    def _get_color(self, current_player):
        return COLOR_PLAYER_ONE if current_player == self.__game.PLAYER_ONE else COLOR_PLAYER_TWO

    def enter_canvas(self, event):
        """
        When cursor enters canvas, draw an oval in the player's color
        """
        if not self.__game.is_game_over():
            item=self.__canvas.create_oval((self._calculating_column(event.x), 0,
                                            self._calculating_column(event.x) + DISK_SIZE, DISK_SIZE),
                                           fill=self._get_color(self.__player))
            self.__list_of_items.append(item)

    def move_cursor(self, event):
        """
        When cursor is moved, deletes the previous cursor and draws a new one according to the mouse's x
        coordinate
        """
        if not self.__game.is_game_over():
            self._delete_cursor()
            item = self.__canvas.create_oval((self._calculating_column(event.x) * DISK_SIZE, 0,
                                              self._calculating_column(event.x) * DISK_SIZE + DISK_SIZE, DISK_SIZE),
                                             fill=self._get_color(self.__player))
            self.__list_of_items.append(item)

    def _delete_cursor(self):
        """
        Removes current cursor
        """
        self.__canvas.delete(self.__list_of_items[-1])
        self.__list_of_items.pop()

    def _calculating_column(self, x):
        """
        Calculates the column according to x coordinate
        """
        return math.floor(x/DISK_SIZE)

    def out_of_canvas(self, event):
        """
        Removes cursor if it goes out of canvas
        """
        if not self.__game.is_game_over():
            if self.__list_of_items:
                self._delete_cursor()

    def _get_coordinates(self, coord_tuple):
        """
        Gets game coordinates, returns x and y on canvas
        """
        return coord_tuple[0] * DISK_SIZE, coord_tuple[1] * DISK_SIZE + DISK_SIZE


def check_args(arg_list):
    """
    Checks if args are valid
    """
    if len(arg_list) < 3 or len(arg_list) > 4 or arg_list[PLAYER_TYPE_ARGUMENT] not in [AI_ARGUMENT, HUMAN_ARGUMENT] \
        or not arg_list[PORT_ARGUMENT].isdigit() or \
                    int(arg_list[PORT_ARGUMENT]) < 0 or int(arg_list[PORT_ARGUMENT]) > MAXIMUM_PORT_NUMBER:
        print(ILLEGAL_ARGUMENTS_MSG)
        return False

    return True


def main(argv):
    if not check_args(argv):
        return
    client = False

    player_type = argv[PLAYER_TYPE_ARGUMENT]
    port = int(argv[PORT_ARGUMENT])
    if len(argv) == 4:
        ip = argv[IP_ARGUMENT]
        client = True

    game = Game()
    root = Tk()
    if player_type == AI_ARGUMENT:
        ai = AI()

    if client:
        communicator = Communicator(root, port, ip)
        player = game.PLAYER_TWO
    else:
        communicator = Communicator(root, port)
        player = game.PLAYER_ONE

    if player_type == HUMAN_ARGUMENT:
        GUI(root, game, communicator, player)
    else:
        GUI(root, game, communicator, player, ai)

    communicator.connect()
    root.mainloop()


if __name__ == '__main__':
    main(sys.argv)