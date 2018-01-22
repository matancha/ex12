import game
import copy
import math


class AI:
    def __init__(self):
        self.__last_move=None
        self.__experimental_board=None

    def find_legal_move(self, g, func, timeout=None):
        self.__experimental_board=copy.deepcopy(g.get_board())
        
        set_of_possible_turns=[]
        for num_column,column in enumerate(self.__experimental_board):
            if None in column:
                set_of_possible_turns.append(num_column)
        if self.__last_move is not None:
            turn=self.find_legal_move_helper(g,set_of_possible_turns)
        else:
            turn=math.floor(g.NUM_COLUMNS/2)
            self.make_move_on_Exp_desk(turn,g)
        func(str(turn))
    def find_legal_move_helper(self,g,set_of_possible_turns):
        best_turn=None
        best_turn_value=-g.NUM_COLUMNS
        previous_last_move=g.get_last_move()
        good_turns_list_for_blocking=self.finding_dangerous_paths_blocking_list(g)
        for turn in set_of_possible_turns:
            self.make_move_on_Exp_desk(turn,g)
            g.last_move=self.__last_move
            value_of_turn=0
            value_of_turn-=self.finding_diference_betwen_columns(turn)
            paths=g.get_possible_paths()
            for turn_of_three_blocikng in good_turns_list_for_blocking[0]:
                if turn_of_three_blocikng==self.__last_move:
                    value_of_turn+=50
            for turn_of_four_blocking in good_turns_list_for_blocking[1]:
                if turn_of_four_blocking==self.__last_move:
                    value_of_turn+=500

            for path in paths:
                ai_path_sequense=[]
                counter_for_path=0
                for i,disk in enumerate(path):
                    if self.__experimental_board[disk[0]][disk[1]] == g.get_current_player():
                        ai_path_sequense.append(disk)
                        if i != len(path) - 1:
                            if self.__experimental_board[path[i+1][0]][path[i+1][1]]==g.get_current_player():
                                counter_for_path=2
                                ai_path_sequense.append(path[i+1])
                                if i!=len(path)-2:
                                    if self.__experimental_board[path[i+2][0]][path[i+2][1]]==g.get_current_player():
                                        counter_for_path=3
                                        ai_path_sequense.append(path[i+2])
                                        if i!=len(path)-3:
                                            if self.__experimental_board[path[i+3][0]][path[i+3][1]]==g.get_current_player():
                                                counter_for_path=4


                if counter_for_path==2:
                    if self.__last_move in ai_path_sequense:
                        value_of_turn+=10
                if counter_for_path==3:
                    if self.__last_move in ai_path_sequense:
                        value_of_turn+=100
                if counter_for_path==4:
                    value_of_turn+=1000
            if value_of_turn>best_turn_value:
                best_turn_value=value_of_turn
                best_turn=turn
            self.__experimental_board[self.__last_move[0]][self.__last_move[1]]=None

        g.last_move=previous_last_move
        return best_turn

    def opponent_player_num(self,g):
        if g.get_current_player()==g.PLAYER_ONE:
            return g.PLAYER_TWO
        return g.PLAYER_ONE

    def finding_dangerous_paths_blocking_list(self,g):
        opponent_number=self.opponent_player_num(g)
        paths=g.get_possible_paths()
        turns_for_three_in_a_row_blocking=[]
        turns_for_four_in_a_row_blocking=[]
        for path in paths:
            for i,disk in enumerate(path):
                if self.__experimental_board[disk[0]][disk[1]]==opponent_number and i!=len(path)-1:
                    if self.__experimental_board[path[i+1][0]][path[i+1][1]]==opponent_number:
                        if i!=len(path)-2:
                            if self.__experimental_board[path[i+2][0]][path[i+2][1]]==opponent_number:
                                if i!=len(path)-3:
                                    if self.__experimental_board[path[i+3][0]][path[i+3][1]] is None:
                                        turns_for_four_in_a_row_blocking.append(path[i+3])
                                if i!=0:
                                    if self.__experimental_board[path[i-1][0]][path[i-1][1]] is None:
                                        turns_for_four_in_a_row_blocking.append(path[i-1])
                                        break
                            elif self.__experimental_board[path[i+2][0]][path[i+2][1]] is None:
                                turns_for_three_in_a_row_blocking.append(path[i+2])
                        if i!=0:
                            if self.__experimental_board[path[i - 1][0]][path[i - 1][1]] is None:
                                turns_for_three_in_a_row_blocking.append(path[i - 1])
        return turns_for_three_in_a_row_blocking,turns_for_four_in_a_row_blocking

    def finding_diference_betwen_columns(self,column):
        middle_column=math.floor(len(self.__experimental_board[0])/2)
        return abs(middle_column-column)

    def make_move_on_Exp_desk(self, column,g):
        for row in range(len(self.__experimental_board[column]) - 1 ,-1,-1):
            if self.__experimental_board[column][row] is None:
                self.__experimental_board[column][row] = g.get_current_player()
                self.__last_move =(column,row)
                break