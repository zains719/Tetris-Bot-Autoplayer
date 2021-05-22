from board import Direction, Rotation
from random import Random
import random
import time

last_score = 0
collumn_heights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Left = 1
Right = 2
Down = 3
Anticlockwise = 4
Clockwise = 5

class Player:
    def choose_action(self, board):
        raise NotImplementedError

class ZainsPlayer(Player):

    #calculates height of each collumn
    def calc_collumn_heights(self, board):
        for x in range(board.width):
            for y in range(board.height, 0, -1):
                if (x, y) in board.cells:
                    collumn_heights[x] = board.height - y

    #calculates total height of all collumns
    def calc_total_height(self, board):
        self.calc_collumn_heights(board)
        total_height = 0
        for collumn in collumn_heights:
            total_height += collumn
        return total_height

    def set_last_score(self, board):
        global last_score
        last_score = board.score

    def calc_change_in_score(self, board):
        global last_score
        moves_score = board.score
        change_in_score = moves_score - last_score
        return change_in_score

    #counts total size of rifts on board after block is placed
    def calc_rifts(self, board):
        rifts = 0
        self.calc_collumn_heights(board)
        for x in range(board.width - 1):
            if collumn_heights[x] > collumn_heights[x + 1]:
                rifts += collumn_heights[x] - collumn_heights[x + 1]
            else:
                rifts += collumn_heights[x + 1] - collumn_heights[x]
        return rifts

    #counts num of spaces down from bottom of last block placed till next block
    def calc_blockades(self, board):
        blockades = 0
        for x, y in board.cells:
            carry_on = True
            count = 1
            while carry_on == True:
                if ((x, y + count) not in board.cells) and (count + y != 24):
                    blockades += 1
                    count += 1
                else:
                    carry_on = False
        return blockades

    def calc_holes(self, board):
        holes = 0
        for (x, y) in board.cells:
            count = 1
            for y in range(24):
                if (x, y + count) not in board.cells:
                    holes += 1
                    count += 1
        return holes

    def calc_clears(self, board, length_of_cells_before):
        clears = 0
        length_of_cells_after = len(board.cells) - 4
        if length_of_cells_before != length_of_cells_after:
            if (length_of_cells_after < length_of_cells_before):
                clears += (length_of_cells_before - length_of_cells_after) / 10
        return clears

    #scores last move made
    def calc_score(self, board):
        #clears = self.calc_clears(board, length_of_cells_before)
        #holes = self.calc_holes(board)
        change_in_score = self.calc_change_in_score(board)
        blockades = self.calc_blockades(board)
        rifts = self.calc_rifts(board)
        total_height = self.calc_total_height(board)
        score = (change_in_score * 0.1) + (blockades * -0.55) + (rifts * -0.25) + (total_height * -0.7)
        return score  

    def calc_num_different_rotations(self, board):
        shape = board.falling.shape
        '''if shape == shape.Z or shape == shape.S:
            return 2
        elif shape == shape.T or shape == shape.L or shape == shape.J or shape == shape.I:
            return 4
        else:
            return 1'''
        if shape == shape.O:
            return 1
        else:
            return 4                                                         

    #moves shape taregt_rotations and to target_pos on cloned board
    def move_to_target(self, board, sandbox, target_pos, taregt_rotations):
        for i in range(0, taregt_rotations):
            try:
                sandbox.rotate(Rotation.Clockwise)
            except:
                pass
        left_of_shape = board.falling.left
        while target_pos != left_of_shape:
            if target_pos < left_of_shape:
                left_of_shape -= 1
                try:
                    sandbox.move(Direction.Left)
                except:
                    pass
            elif target_pos > left_of_shape:
                left_of_shape += 1
                try:
                    sandbox.move(Direction.Right)
                except:
                    pass
        try:
            sandbox.move(Direction.Drop)
        except:
            pass

    #finds best score for next move    
    def choose_next_action(self, board, sandbox):
        best_score = -100000
        #finds best next move
        for target_pos in range(board.width):
            for target_num_of_rotations in range(0, 4):
                sandbox2 = sandbox.clone()
                self.move_to_target(board, sandbox2, target_pos, target_num_of_rotations)
                #length_of_cells_before = len(board.cells)
                score = self.calc_score(sandbox2)
                if score > best_score:
                    best_score = score
                    best_target_pos = target_pos
                    best_target_num_of_rotations = target_num_of_rotations
        #does next best move
        self.move_to_target(board, sandbox, best_target_pos, best_target_num_of_rotations)

    #returns list of all best moves
    def make_best_move(self, board, best_target_pos, best_num_of_rotations):
        do_moves = []
        #appends best num of rotatations
        for i in range(best_num_of_rotations):
            do_moves.append(Rotation.Clockwise)
        
        #appends all moves that move shape to target pos
        left_of_shape = board.falling.left
        #print("target pos: ", best_target_pos)
        while best_target_pos != left_of_shape:
            if best_target_pos < left_of_shape:
                left_of_shape -=1
                do_moves.append(Direction.Left)
            elif best_target_pos > left_of_shape:
                left_of_shape +=1
                do_moves.append(Direction.Right)
        do_moves.append(Direction.Drop)
        return do_moves
            
    def choose_action(self, board):
        #time.sleep(1)
        #calculate score of board before move is made
        self.set_last_score(board)
        #calculate possible num of rotations with current shape
        different_num_rotations = self.calc_num_different_rotations(board)
        best_score = -100000
        #for all possible positions
        for target_pos in range(board.width):
            #for all number of rotations
            for target_num_of_rotations in range(0, different_num_rotations):
                sandbox = board.clone()
                #move shape to target_pos and do target_num_of_rotations
                self.move_to_target(board, sandbox, target_pos, target_num_of_rotations)
                #move next shape to best target_pos and do target_num_of_rotations
                self.choose_next_action(board, sandbox)
                #scores board after original and next best moves made
                #length_of_cells_before = len(board.cells)
                score = self.calc_score(sandbox)
                #determines best score
                if score > best_score:
                    best_score = score
                    best_target_pos = target_pos
                    best_num_of_rotations = target_num_of_rotations

        #time.sleep(1)
        #do best move
        return self.make_best_move(board, best_target_pos, best_num_of_rotations)
                    
SelectedPlayer = ZainsPlayer
