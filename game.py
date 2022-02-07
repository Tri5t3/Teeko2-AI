import random
import copy
import operator
DEPTH_LIMIT = 1


def flip(list):
    c_list = copy.deepcopy(list)
    for i in c_list:
        i[1] = 4 - i[1]
    return c_list


def same_row(list):
    row_ind = list[0][0]
    for i in range(1, len(list)):
        if list[i][0] != row_ind:
            return False
    return True


def same_col(list):
    col_ind = list[0][1]
    for i in range(1, len(list)):
        if list[i][1] != col_ind:
            return False
    return True


def same_diag1(list):
    dif = list[0][0] - list[0][1]
    for i in range(1, len(list)):
        if list[i][0] - list[i][1] != dif or abs(list[i][0] - list[i][1]) >= 2:
            return False
    return True


def same_diag2(list):
    sum = list[0][0] + list[0][1]
    for i in range(1, len(list)):
        if list[i][0] + list[i][1] != sum or 2 >= list[i][0] + list[i][1] or list[i][0] + list[i][1] >= 6:
            return False
    return True


def same_diam(list):
    for i in range(1, 4):
        for j in range(1, 4):
            ind = 0
            for item in list:
                if (abs(item[0] - i) == 1) and (abs(item[1] - j) == 0):
                    ind += 1
                if (abs(item[0] - i) == 0) and (abs(item[1] - j) == 1):
                    ind += 1
            if ind == len(list):
                fourth = []
                if [i-1, j] not in list:
                    fourth = [i-1, j]
                if [i+1, j] not in list:
                    fourth = [i+1, j]
                if [i, j-1] not in list:
                    fourth = [i, j-1]
                if [i, j+1] not in list:
                    fourth = [i, j+1]
                return 1, fourth
    return 0, -1


def consecutive_row(list):
    for i in range(len(list)-1):
        if list[i+1][1] != list[i][1] + 1:
            return False
    return True


def consecutive_col(list):
    for i in range(len(list)-1):
        if list[i+1][0] != list[i][0] + 1:
            return False
    return True


def consecutive_diag1(list):
    for i in range(len(list)-1):
        if list[i+1][0] != list[i][0] + 1 or list[i+1][1] != list[i][1] + 1:
            return False, -1
    ind = -1
    if list == [[1, 1], [2, 2], [3, 3]]:  # [0,0] & [4,4]
        ind = 0
    if list == [[0, 0], [1, 1], [2, 2]]:  # [3,3]
        ind = 1
    if list == [[2, 2], [3, 3], [4, 4]]:  # [1,1]
        ind = 2
    if list == [[0, 1], [1, 2], [2, 3]]:  # [3,4]
        ind = 3
    if list == [[1, 2], [2, 3], [3, 4]]:  # [0,1]
        ind = 4
    if list == [[1, 0], [2, 1], [3, 2]]:  # [4,3]
        ind = 5
    if list == [[2, 1], [3, 2], [4, 3]]:  # [1,0]
        ind = 6
    return True, ind


def consecutive_diag2(list):
    for i in range(len(list)-1):
        if list[i+1][0] != list[i][0] + 1 or list[i+1][1] != list[i][1] - 1:
            return False
    return True


def find_move(succ, state):
    for i in range(5):
        for j in range(5):
            if succ[i][j] != ' ' and state[i][j] == ' ':
                return(i, j)


class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def count(self, state):
        b_count = 0
        r_count = 0
        my_count = 0
        for row in state:
            for item in row:
                if item != ' ':
                    if item == self.pieces[0]:
                        b_count += 1
                    elif item == self.pieces[1]:
                        r_count += 1
        total_count = b_count + r_count
        if self.my_piece == self.pieces[0]:
            my_count = b_count
        else:
            my_count = r_count
        opp_count = total_count - my_count
        return my_count, opp_count, total_count

    def find_coordinate(self, state):
        my_coord = []
        opp_coord = []
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == self.my_piece:
                    my_coord.append([i, j])
                if state[i][j] == self.opp:
                    opp_coord.append([i, j])
        return my_coord, opp_coord

    def succ(self, state, piece):
        states = []
        _, _, total = self.count(state)
        drop_phase = True if total < 8 else False
        # print("Drop phase:", drop_phase)
        if drop_phase:
            for i in range(len(state)):
                for j in range(len(state[0])):
                    if state[i][j] == ' ':
                        statecopy = copy.deepcopy(state)
                        statecopy[i][j] = piece
                        states.append(statecopy)
            return states

        if not drop_phase:
            for i in range(len(state)):
                for j in range(len(state[0])):
                    if state[i][j] == piece:
                        statecopy = copy.deepcopy(state)
                        statecopy[i][j] = ' '

                        x_s = [i-1, i-1, i-1, i, i, i+1, i+1, i+1]
                        y_s = [j-1, j, j+1, j-1, j+1, j-1, j, j+1]
                        # delete illegal entries
                        illegals = []
                        for index in range(len(x_s)):
                            if x_s[index] < 0 or x_s[index] > 4 or y_s[index] < 0 or y_s[index] > 4:
                                illegals.append(index)
                        illegals.reverse()
                        for index in illegals:
                            x_s.pop(index)
                            y_s.pop(index)

                        for index in range(len(x_s)):
                            x = x_s[index]
                            y = y_s[index]
                            # print("X:", x, "Y:", y)
                            copy2 = copy.deepcopy(statecopy)
                            if copy2[x][y] == ' ':
                                copy2[x][y] = piece
                                states.append(copy2)
            return states

    def moves_to_win(self, state, piece):
        for succ in self.succ(state, piece):
            if self.game_value(succ) != 0:
                return 1
        for succ in self.succ(state, piece):
            for succ2 in self.succ(succ, piece):
                if self.game_value(succ2) != 0:
                    return 2
        # for succ in self.succ(state, piece):
        #     for succ2 in self.succ(succ, piece):
        #         for succ3 in self.succ(succ2, piece):
        #             if self.game_value(succ3) != 0:
        #                 return 3
        return 4

    def heuristic_game_value(self, state):
        # return random.uniform(-1, 1)
        endpoint = self.game_value(state)
        if endpoint == 1 or endpoint == -1:
            return endpoint

        my_count, opp_count, total_count = self.count(state)

        if my_count == 1 and state[2][2] == self.my_piece:
            return 1

        # drop phase
        if total_count < 8:
            # definitely win scenarios
            for index in range(len(state)):
                if state[index][1] == state[index][2] == state[index][3] == self.my_piece and state[index][0] == state[index][4] == ' ' and my_count == 3:
                    return 1
                if state[index][1] == state[index][2] == state[index][3] == self.opp and state[index][0] == state[index][4] == ' ' and opp_count == 3:
                    return -1
                if state[1][index] == state[2][index] == state[3][index] == self.my_piece and state[0][index] == state[4][index] == ' ' and my_count == 3:
                    return 1
                if state[1][index] == state[2][index] == state[3][index] == self.opp and state[0][index] == state[4][index] == ' ' and opp_count == 3:
                    return -1
            if state[1][1] == state[2][2] == state[3][3] == self.my_piece and state[0][0] == state[4][4] == ' ' and my_count == 3:
                return 1
            if state[1][1] == state[2][2] == state[3][3] == self.opp and state[0][0] == state[4][4] == ' ' and opp_count == 3:
                return -1
            if state[1][3] == state[2][2] == state[3][1] == self.my_piece and state[0][4] == state[4][0] == ' ' and my_count == 3:
                return 1
            if state[1][3] == state[2][2] == state[3][1] == self.opp and state[0][4] == state[4][0] == ' ' and opp_count == 3:
                return -1

        my_coord, opp_coord = self.find_coordinate(state)
        to_ret = 0

        if opp_count == 4:
            mvs = self.moves_to_win(state, self.opp)
            to_ret -= 1/(mvs+1)
        if my_count == 4:
            mvs = self.moves_to_win(state, self.my_piece)
            to_ret += 1/(mvs+1)

        if opp_count == 3:
            if same_col(opp_coord) or same_row(opp_coord) or same_diag1(opp_coord) or same_diag2(opp_coord):
                to_ret -= 0.6
                if same_col(opp_coord):
                    if consecutive_col(opp_coord):
                        to_ret -= 0.1
                if same_row(opp_coord):
                    if consecutive_row(opp_coord):
                        to_ret -= 0.1

                tf, ind = consecutive_diag1(opp_coord)
                if tf:
                    # print("CONS DIAG1")
                    to_ret -= 0.1

                    if ind == 0:
                        if state[0][0] == self.my_piece or state[4][4] == self.my_piece:
                            to_ret += 0.03
                    if ind == 1:
                        if state[3][3] == self.my_piece:
                            to_ret += 0.03
                    if ind == 2:
                        if state[1][1] == self.my_piece:
                            to_ret += 0.03
                    if ind == 3:
                        if state[3][4] == self.my_piece:
                            to_ret += 0.03
                    if ind == 4:
                        if state[0][1] == self.my_piece:
                            to_ret += 0.03
                    if ind == 5:
                        if state[4][3] == self.my_piece:
                            to_ret += 0.03
                    if ind == 6:
                        if state[1][0] == self.my_piece:
                            to_ret += 0.03

                tf, ind = consecutive_diag1(flip(opp_coord))
                if tf:
                    copystate = copy.deepcopy(state)
                    for row in state:
                        row.reverse()
                    # print("CONS DIAG1")
                    to_ret -= 0.1

                    if ind == 0:
                        if state[0][0] == self.my_piece or state[4][4] == self.my_piece:
                            to_ret += 0.03
                    if ind == 1:
                        if state[3][3] == self.my_piece:
                            to_ret += 0.03
                    if ind == 2:
                        if state[1][1] == self.my_piece:
                            to_ret += 0.03
                    if ind == 3:
                        if state[3][4] == self.my_piece:
                            to_ret += 0.03
                    if ind == 4:
                        if state[0][1] == self.my_piece:
                            to_ret += 0.03
                    if ind == 5:
                        if state[4][3] == self.my_piece:
                            to_ret += 0.03
                    if ind == 6:
                        if state[1][0] == self.my_piece:
                            to_ret += 0.03
                    state = copy.deepcopy(copystate)
                # return to_ret

            tf, fourth = same_diam(opp_coord)
            if tf == 1:
                to_ret -= 0.7
                if state[fourth[0]][fourth[1]] == self.my_piece:
                    to_ret += 0.05
                # return to_ret

        if my_count == 3:
            if same_col(my_coord) or same_row(my_coord) or same_diag1(my_coord) or same_diag2(my_coord):
                # if same_col(my_coord):
                #     print("1")
                # if same_row(my_coord):
                #     print("2")
                # if same_diag1(my_coord):
                #     print("3")
                # if same_diag2(my_coord):
                #     print("4")
                to_ret += 0.6
                if same_col(my_coord):
                    if consecutive_col(my_coord):
                        # print("CONS COL")
                        to_ret += 0.1
                if same_row(my_coord):
                    if consecutive_row(my_coord):
                        # print("CONS ROW")
                        to_ret += 0.1

                tf, ind = consecutive_diag1(my_coord)
                if tf:
                    # print("CONS DIAG1")
                    to_ret += 0.1

                    if ind == 0:
                        if state[0][0] == self.opp or state[4][4] == self.opp:
                            to_ret -= 0.03
                    if ind == 1:
                        if state[3][3] == self.opp:
                            to_ret -= 0.03
                    if ind == 2:
                        if state[1][1] == self.opp:
                            to_ret -= 0.03
                    if ind == 3:
                        if state[3][4] == self.opp:
                            to_ret -= 0.03
                    if ind == 4:
                        if state[0][1] == self.opp:
                            to_ret -= 0.03
                    if ind == 5:
                        if state[4][3] == self.opp:
                            to_ret -= 0.03
                    if ind == 6:
                        if state[1][0] == self.opp:
                            to_ret -= 0.03

                tf, ind = consecutive_diag1(flip(my_coord))
                if tf:
                    copystate = copy.deepcopy(state)
                    for row in state:
                        row.reverse()
                    # print("CONS DIAG1")
                    to_ret += 0.1

                    if ind == 0:
                        if state[0][0] == self.opp or state[4][4] == self.opp:
                            to_ret -= 0.03
                    if ind == 1:
                        if state[3][3] == self.opp:
                            to_ret -= 0.03
                    if ind == 2:
                        if state[1][1] == self.opp:
                            to_ret -= 0.03
                    if ind == 3:
                        if state[3][4] == self.opp:
                            to_ret -= 0.03
                    if ind == 4:
                        if state[0][1] == self.opp:
                            to_ret -= 0.03
                    if ind == 5:
                        if state[4][3] == self.opp:
                            to_ret -= 0.03
                    if ind == 6:
                        if state[1][0] == self.opp:
                            to_ret -= 0.03
                    state = copy.deepcopy(copystate)
                # return to_ret
            tf, fourth = same_diam(my_coord)
            if tf == 1:
                to_ret += 0.7
                if state[fourth[0]][fourth[1]] == self.opp:
                    to_ret -= 0.05
                # return to_ret

        if opp_count == 2:
            if same_col(opp_coord) or same_row(opp_coord) or same_diag1(opp_coord) or same_diag2(opp_coord):
                to_ret -= 0.4
                if same_col(opp_coord):
                    if consecutive_col(opp_coord):
                        to_ret -= 0.02
                if same_row(opp_coord):
                    if consecutive_row(opp_coord):
                        to_ret -= 0.02
                if consecutive_diag1(opp_coord):
                    to_ret -= 0.02
                if consecutive_diag2(opp_coord):
                    to_ret -= 0.02
                # return to_ret
            # tf, fourth = same_diam(opp_coord)
            # if tf == 1:
            #     to_ret -= 0.42
            #     if state[fourth[0]][fourth[1]] == self.my_piece:
            #         to_ret += 0.05
                # return to_ret

        if my_count == 2:
            if same_col(my_coord) or same_row(my_coord) or same_diag1(my_coord) or same_diag2(my_coord):
                to_ret = 0.4
                if same_col(my_coord):
                    if consecutive_col(my_coord):
                        # print("CONS COL")
                        to_ret += 0.02
                if same_row(my_coord):
                    if consecutive_row(my_coord):
                        # print("CONS ROW")
                        to_ret += 0.02
                if consecutive_diag1(my_coord):
                    # print("CONS DIAG1")
                    to_ret += 0.02
                if consecutive_diag2(my_coord):
                    # print("CONS DIAG2")
                    to_ret += 0.02
                # return to_ret
            # tf, fourth = same_diam(my_coord)
            # if tf == 1:
            #     to_ret += 0.42
            #     if state[fourth[0]][fourth[1]] == self.opp:
            #         to_ret -= 0.05

        if opp_count == 1:
            cord = opp_coord[0]
            dis = abs(cord[0] - 2) + abs(cord[1] - 2)
            to_ret -= 0.1
            to_ret += dis * 0.01
            # return to_ret

        if my_count == 1:
            cord = my_coord[0]
            dis = abs(cord[0] - 2) + abs(cord[1] - 2)
            to_ret += 0.1
            to_ret -= dis * 0.01
            # return to_ret

        return to_ret

    def max_value(self, state, depth):
        if self.game_value(state) != 0:
            return self.game_value(state)
        if depth >= DEPTH_LIMIT:
            return self.heuristic_game_value(state)
        else:
            alpha = -999
            for scene in self.succ(state, self.my_piece):
                alpha = max(alpha, self.min_value(scene, depth+1))
        return alpha

    def min_value(self, state, depth):
        if self.game_value(state) != 0:
            return self.game_value(state)
        if depth >= DEPTH_LIMIT:
            return self.heuristic_game_value(state)
        else:
            beta = 999
            for scene in self.succ(state, self.opp):
                beta = min(beta, self.max_value(scene, depth+1))
        return beta

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        count = 0
        for row in state:
            for item in row:
                if item != ' ':
                    count += 1
        drop_phase = True if count < 8 else False   # TODO: detect drop phase

        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            move = []
            alpha = -999
            move_from = [-1, -1]
            move_2 = [-1, -1]
            for succ in self.succ(state, self.my_piece):
                val = self.min_value(succ, 1)
                if alpha <= val:
                    move_from = find_move(state, succ)
                    move_2 = find_move(succ, state)
                    alpha = val
            move.insert(0, move_from)
            move.insert(0, move_2)
            return move

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        move = []
        # (row, col) = (random.randint(0, 4), random.randint(0, 4))
        # while not state[row][col] == ' ':
        #     (row, col) = (random.randint(0, 4), random.randint(0, 4))

        alpha = -999
        move_2 = [-1, -1]
        for succ in self.succ(state, self.my_piece):
            val = self.min_value(succ, 1)
            # print("VAL:", val)
            # print(succ)
            if alpha <= val:
                move_2 = find_move(succ, state)
                # print(move_2)
                alpha = val
        move.insert(0, move_2)

        # ensure the destination (row,col) tuple is at the beginning of the move list
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception(
                    'Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and diamond wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # TODO: check \ diagonal wins
        if state[0][0] == state[1][1] == state[2][2] == state[3][3] != ' ':
            return 1 if state[0][0] == self.my_piece else -1
        if state[1][1] == state[2][2] == state[3][3] == state[4][4] != ' ':
            return 1 if state[1][1] == self.my_piece else -1
        if state[0][1] == state[1][2] == state[2][3] == state[3][4] != ' ':
            return 1 if state[0][1] == self.my_piece else -1
        if state[1][0] == state[2][1] == state[3][2] == state[4][3] != ' ':
            return 1 if state[1][0] == self.my_piece else -1

        # TODO: check / diagonal wins
        if state[0][4] == state[1][3] == state[2][2] == state[3][1] != ' ':
            return 1 if state[0][4] == self.my_piece else -1
        if state[1][3] == state[2][2] == state[3][1] == state[4][0] != ' ':
            return 1 if state[1][3] == self.my_piece else -1
        if state[0][3] == state[1][2] == state[2][1] == state[3][0] != ' ':
            return 1 if state[0][3] == self.my_piece else -1
        if state[1][4] == state[2][3] == state[3][2] == state[4][1] != ' ':
            return 1 if state[1][4] == self.my_piece else -1

        # TODO: check diamond wins
        for i in range(1, 4):
            for j in range(1, 4):
                if state[i-1][j] != ' ' and state[i-1][j] == state[i][j-1] == state[i][j+1] == state[i+1][j]:
                    return 1 if state[i-1][j] == self.my_piece else -1

        return 0  # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################


def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at " +
                  chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move(
                        [(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from " +
                  chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                      (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
