from tkinter import *
from game import Game
import math
COLOR_PLAYER1="green"
COLOR_PLAYER2="yellow"
DISK_SIZE=100
game=Game()
def callback(event):
    column=math.floor(event.x/DISK_SIZE)
    print(event.x,column)
    game.make_move(column)
    if game.get_winner() is not None:
        label=Label(root,text='Player {0} wins!'.format(game.get_winner()+1))
        label.pack()

    last_turn=game.get_last_move()

    current_player=game.get_current_player()
    color = COLOR_PLAYER1 if current_player == game.PLAYER_ONE else COLOR_PLAYER2
    start_column, start_row = get_coordinates(last_turn)
    canv.create_oval((start_column, start_row),(start_column+DISK_SIZE, start_row+DISK_SIZE),fill=color)
    game.set_current_player()
def get_coordinates(last_turn):
    return (last_turn[0]*DISK_SIZE,last_turn[1]*DISK_SIZE+DISK_SIZE)
root=Tk()
# button=Button(root,text="1",comand=print_it(event))
# button.pack()
canv=Canvas(root, bg="white",height=(Game.NUM_ROWS+1)*DISK_SIZE,width=Game.NUM_COLUMN*DISK_SIZE)
# for frme in range(0, Game.NUM_COLUMN*100,100):
#     button=Button(root,text=int(frme/100))
#     button.bind("<Button-1>",print_it)
#     button.pack()
canv.pack()
for row in range(DISK_SIZE, (Game.NUM_ROWS+1)*DISK_SIZE,DISK_SIZE):
    for column in range(0, Game.NUM_COLUMN*DISK_SIZE,DISK_SIZE):
        canv.create_rectangle((column,row),(column+DISK_SIZE,row+DISK_SIZE),fill="orange")
canv.bind('<Button-1>', callback)
root.mainloop()


