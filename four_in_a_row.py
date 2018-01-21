from tkinter import *
import tkinter.messagebox as messagebox
from game import Game
import math
from communicator import Communicator

WIN_MSG = 'Player {0} wins!'
COLOR_PLAYER1="green"
COLOR_PLAYER2="yellow"
DISK_SIZE=100


class GUI:

    def __init__(self, root, game, communicator, player):
        self.root = root
        self.game = game
        self.communicator = communicator
        self.player = player

        self.canvas = Canvas(self.root, bg="white", height=(Game.NUM_ROWS + 1) * DISK_SIZE,
                             width=Game.NUM_COLUMN * DISK_SIZE)
        self.canvas.bind('<Button-1>', self.callback)
        self.canvas.bind("<Enter>", self.entering)
        self.canvas.bind("<Motion>", self.move)
        self.canvas.bind("<Leave>", self.out_of)
        self.canvas.pack()

        self.communicator.bind_action_to_message(self.callback)
        self.dict_of_disks = {}
        self.list_of_items = []

        self.create_initial_screen()

    def create_initial_screen(self):

        for row in range(DISK_SIZE, (Game.NUM_ROWS + 1) * DISK_SIZE, DISK_SIZE):
            for column in range(0, Game.NUM_COLUMN * DISK_SIZE, DISK_SIZE):
                self.canvas.create_rectangle((column, row), (column + DISK_SIZE, row + DISK_SIZE), fill="orange")
                self.canvas.create_oval((column, row), (column + DISK_SIZE, row + DISK_SIZE), fill="white")

    def callback(self, event):
        last_turn = self.game.get_last_move()
        if hasattr(event, 'x'):
            column = self.calculating_column(event.x)
            if last_turn is None:
                if self.player != self.game.PLAYER_ONE:
                    messagebox.showinfo("Can't do this", 'what')
                    return
            elif self.game.get_player_at(last_turn[0], last_turn[1]) == self.player:
                messagebox.showinfo("Can't do this", 'what')
                return
        else:
            column = int(event[-1])

        try:
            self.game.make_move(column)
        except ValueError:
            messagebox.showinfo('illegal move', 'try again!')

        if hasattr(event, 'x'):
            self.communicator.send_message("Put disk in column {0}".format(column))

        color = self.get_color(self.game.get_current_player())
        start_column, start_row = self.get_coordinates(self.game.get_last_move())
        disk = self.canvas.create_oval((start_column, start_row),
                                       (start_column + DISK_SIZE, start_row + DISK_SIZE), fill=color)
        self.dict_of_disks[start_column, start_row] = disk

        if self.game.get_winner() is not None:
            label=Label(self.root, text=WIN_MSG.format(self.game.get_winner() + 1))
            label.pack()
            for coord in self.game.get_winning_path():
                disk = self.dict_of_disks[self.get_coordinates(coord)]
                self.canvas.itemconfig(disk, fill="red")
            messagebox.showinfo('Game over!', WIN_MSG.format(self.game.get_winner() + 1))
            self.canvas.delete(self.list_of_items[0])
            self.list_of_items.pop()

        self.game.set_current_player()
        # if not self.game.is_game_over():
        #     self.canvas.delete(self.list_of_items[-1])
        #     self.list_of_items.pop()
        #     item = self.canvas.create_oval(
        #         (self.calculating_column(event.x) * DISK_SIZE, 0,
        #          self.calculating_column(event.x) * DISK_SIZE + DISK_SIZE, DISK_SIZE),
        #         fill=self.get_color(self.game.get_current_player()))
        #     self.list_of_items.append(item)

    def get_color(self, current_player):
        return COLOR_PLAYER1 if current_player == self.game.PLAYER_ONE else COLOR_PLAYER2

    def entering(self, event):
        if not self.game.is_game_over():
            item=self.canvas.create_oval((self.calculating_column(event.x),0,
                                   self.calculating_column(event.x)+DISK_SIZE,DISK_SIZE),
                                  fill=self.get_color(self.game.get_current_player()))
            self.list_of_items.append(item)

    def move(self, event):
        if not self.game.is_game_over():
            self.canvas.delete(self.list_of_items[-1])
            self.list_of_items.pop()
            item = self.canvas.create_oval((self.calculating_column(event.x)*DISK_SIZE, 0,
                                     self.calculating_column(event.x)*DISK_SIZE + DISK_SIZE, DISK_SIZE),
                                    fill=self.get_color(self.game.get_current_player()))
            self.list_of_items.append(item)

    def calculating_column(self, x):
        return math.floor(x/DISK_SIZE)

    def out_of(self, event):
        if not self.game.is_game_over():
            self.canvas.delete(self.list_of_items[-1])
            self.list_of_items.pop()

    def get_coordinates(self, coord_tuple):
        return coord_tuple[0] * DISK_SIZE, coord_tuple[1] * DISK_SIZE + DISK_SIZE


def check_args(arg_list):
    if arg_list[1] not in ['ai', 'human']:
        return False

    return True


def main(argv):
    if not check_args(argv):
        return
    client = False
    game = Game()
    root = Tk()

    player_type = argv[1]
    port = int(argv[2])
    if len(argv) == 4:
        ip = argv[3]
        client = True

    if client:
        communicator = Communicator(root, port, ip)
        player = game.PLAYER_TWO
    else:
        communicator = Communicator(root, port)
        player = game.PLAYER_ONE

    communicator.connect()

    GUI(root, game, communicator, player)
    root.mainloop()

if __name__ == '__main__':
    main(sys.argv)