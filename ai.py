import copy
import math


class AI:

    def find_legal_move(self, g, func, timeout=None):
    #this function find the best turn according to situatuion on the board and
    #draw it on the tk
        set_of_possible_turns=[]
        #the function create copy of game to make all turns on copy
        #and not to change the real board
        game_copy=copy.deepcopy(g)
        for num_column,column in enumerate(game_copy.get_board()):
            #check if columns are not packed yet
            if None in column:
                set_of_possible_turns.append(num_column)
        if game_copy.get_last_move() is not None:
            #checkking for first turn
            turn=self.find_legal_move_helper(game_copy,set_of_possible_turns)
        else:
            turn=math.ceil(g.NUM_COLUMNS/2)
            self.make_move_on_Exp_desk(turn,game_copy)
        func(str(turn))
    def find_legal_move_helper(self, g,set_of_possible_turns):
        #this function find best turn according to
        #preference in next order from most priority-driven to less
        #1)find turn for finish the game(four dsiks of ai in a row)
        #2)find how to block sequense of 4 disk of opponent
        #3)find turn to make sequense of ai disk 3 in a row
        #4)find how to block sequense of opponent 3 in a row
        #5) find how to create sequense 2 in a row
        #6)check if the turn close to the middle of the board
        #7)in the end it checks if after best turn there is a situation that
        #opponent will win if he puts his disk on the disk that was puted by ai in last turn
        #for each of checking there is a value according to importance of it
        best_turn=None
        best_turn_value=-g.NUM_COLUMNS
        #to make sure that there will some turn
        good_turns_list_for_blocking=self.finding_dangerous_paths_blocking_list(g)
        for turn in set_of_possible_turns:
            self.make_move_on_Exp_desk(turn,g)
            g.last_move=g.get_last_move()
            value_of_turn=0
            value_of_turn-=self.finding_diference_betwen_columns(turn, g)
            paths=g.get_possible_paths()
            for turn_of_three_blocikng in good_turns_list_for_blocking[0]:
                if turn_of_three_blocikng==g.get_last_move():
                    #checking of #4
                    value_of_turn+=50
            for turn_of_four_blocking in good_turns_list_for_blocking[1]:
                if turn_of_four_blocking==g.get_last_move():
                    #checking of 2#
                    value_of_turn+=500

            for path in paths:
                ai_path_sequense=[]
                counter_for_path=0
                for i,disk in enumerate(path):
                    if g.get_player_at(disk[0], disk[1]) == g.get_current_player():
                        ai_path_sequense.append(disk)
                        if i != len(path) - 1:
                            if g.get_player_at(path[i+1][0], path[i+1][1])==g.get_current_player():
                                counter_for_path=2
                                ai_path_sequense.append(path[i+1])
                                if i!=len(path)-2:
                                    if g.get_player_at(path[i+2][0], path[i+2][1])==g.get_current_player():
                                        counter_for_path=3
                                        ai_path_sequense.append(path[i+2])
                                        if i!=len(path)-3:
                                            if g.get_player_at(path[i+3][0], path[i+3][1])==g.get_current_player():
                                                counter_for_path=4
                if counter_for_path==2:
                    if g.get_last_move() in ai_path_sequense:
                        #value for 5#
                        value_of_turn+=10
                if counter_for_path==3:
                    #value for 3#
                    if g.get_last_move() in ai_path_sequense:
                        value_of_turn+=100
                if counter_for_path==4:
                    #value for 1#
                    value_of_turn+=1000
            game_for_second_turn = copy.deepcopy(g)
            #check if after that turn doesn't appear winning turn and will block this turn
            #despite that he have good value,except turn that create four in a row sequense for ai
            if self.check_the_second_turn(game_for_second_turn, g, turn) and value_of_turn<900:
                value_of_turn-=500
            if value_of_turn>best_turn_value:
                best_turn_value=value_of_turn
                best_turn=turn
            g.set_board(g.get_last_move()[0], g.get_last_move()[1], None)
        return best_turn

    def check_the_second_turn(self,game_for_second_turn,g,turn):
        #this function checks if there is possibility to win to opponent
        #if he puts disk on last disk of ai
        self.make_move_on_Exp_desk(turn,game_for_second_turn)
        if game_for_second_turn.get_winner()==self.opponent_player_num(g):
            return True


    def opponent_player_num(self,g):
        #this function find number of opponent
        if g.get_current_player()==g.PLAYER_ONE:
            return g.PLAYER_TWO
        return g.PLAYER_ONE

    def finding_dangerous_paths_blocking_list(self,game_copy):
        #this function find all possible turns that will block sequenses of opponent 4 and 3 in a row
        opponent_number=self.opponent_player_num(game_copy)
        paths=game_copy.get_possible_paths()
        turns_for_three_in_a_row_blocking=[]
        turns_for_four_in_a_row_blocking=[]
        for path in paths:
            for i,disk in enumerate(path):
                #is num of disk in path
                #so after finding the disk of opponent
                #checks how many in sequense
                #and find if there is possible to block them
                if game_copy.get_player_at(disk[0], disk[1])==opponent_number and i!=len(path)-1:
                    if game_copy.get_player_at(path[i+1][0], path[i+1][1])==opponent_number:
                        if i!=len(path)-2:
                            if game_copy.get_player_at(path[i+2][0], path[i+2][1])==opponent_number:
                                if i!=len(path)-3:
                                    if game_copy.get_player_at(path[i+3][0], path[i+3][1]) is None:
                                        turns_for_four_in_a_row_blocking.append(path[i+3])
                                if i!=0:
                                    if game_copy.get_player_at(path[i-1][0], path[i-1][1]) is None:
                                        turns_for_four_in_a_row_blocking.append(path[i-1])
                                        break
                            elif game_copy.get_player_at(path[i+2][0], path[i+2][1]) is None:
                                turns_for_three_in_a_row_blocking.append(path[i+2])
                        if i!=0:
                            if game_copy.get_player_at(path[i - 1][0], path[i - 1][1]) is None:
                                turns_for_three_in_a_row_blocking.append(path[i - 1])
        return turns_for_three_in_a_row_blocking,turns_for_four_in_a_row_blocking

    def finding_diference_betwen_columns(self,column, g):
        #find how far the turn from the middle
        middle_column=math.ceil(len(g.get_board()[0])/2)
        return abs(middle_column-column)

    def make_move_on_Exp_desk(self, column,game_copy):
        #this function for making moves on experimental boards to save current situation on original board
        for row in range(len(game_copy.get_board()[column]) - 1 ,-1,-1):
            if game_copy.get_player_at(column, row) is None:
                game_copy.set_board(column, row, game_copy.get_current_player())
                game_copy.set_last_move(column,row)
                break