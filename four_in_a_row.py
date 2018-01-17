from tkinter import *
from game import Game
import math
COLOR_PLAYER1="green"
COLOR_PLAYER2="yellow"
DISK_SIZE=100
game=Game()
def callback(event):
    column=calculating_column(event.x)
    game.make_move(column)

    last_turn = game.get_last_move()
    color = get_color(game.get_current_player())
    start_column, start_row = get_coordinates(last_turn)
    disk = canv.create_oval((start_column, start_row), (start_column + DISK_SIZE, start_row + DISK_SIZE), fill=color)
    dict_of_disks[start_column, start_row] = disk

    if game.get_winner() is not None:
        label=Label(root,text='Player {0} wins!'.format(game.get_winner()+1))
        label.pack()
        for coord in game.get_winning_path():
            disk = dict_of_disks[get_coordinates(coord)]
            canv.itemconfig(disk, fill="red")

    game.set_current_player()
list_of_items=[]
def get_color(current_player):
    return COLOR_PLAYER1 if current_player == game.PLAYER_ONE else COLOR_PLAYER2
def entering(event):
    item=canv.create_oval((calculating_column(event.x),0,calculating_column(event.x)+DISK_SIZE,DISK_SIZE),fill=get_color(game.get_current_player()))
    list_of_items.append(item)
def move(event):
    canv.delete(list_of_items[-1])
    list_of_items.pop()
    item = canv.create_oval((calculating_column(event.x)*DISK_SIZE, 0, calculating_column(event.x)*DISK_SIZE + DISK_SIZE, DISK_SIZE),
                            fill=get_color(game.get_current_player()))
    list_of_items.append(item)

def calculating_column(x):
    return (math.floor(x/DISK_SIZE))

def out_of(event):
    canv.delete(list_of_items[-1])
    list_of_items.pop()
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
dict_of_disks={}
for row in range(DISK_SIZE, (Game.NUM_ROWS+1)*DISK_SIZE,DISK_SIZE):
    for column in range(0, Game.NUM_COLUMN*DISK_SIZE,DISK_SIZE):
        canv.create_rectangle((column,row),(column+DISK_SIZE,row+DISK_SIZE),fill="orange")
        canv.create_oval((column,row),(column+DISK_SIZE,row+DISK_SIZE),fill="white")
canv.bind('<Button-1>', callback)
canv.bind("<Enter>",entering)
canv.bind("<Motion>",move)
canv.bind("<Leave>",out_of)
root.mainloop()


# if __name__ == '__main__':
#     main()