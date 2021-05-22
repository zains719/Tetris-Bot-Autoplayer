from board import Direction, Rotation
from random import Random
import time

Left = 1
Right = 2
Down = 3
Anticlockwise = 4
Clockwise = 5

class Player:
    def choose_action(self, board):
        raise NotImplementedError


class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def choose_action(self, board):
        print("cells: ", board.cells)
        print("falling: ", board.falling.cells)
        print("next: ", board.next.cells)
        #time.sleep(1)
        for x,y in board.falling.cells:
            print(x,y)
        return self.random.choice([
            Direction.Left,
            Direction.Right,
            Direction.Down,
            Rotation.Anticlockwise,
            Rotation.Clockwise,
        ])

class ZainsPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def get_target_pos(self, board, xpos):
        for ypos in range(board.height):
            #checks for previous placed block
            for x,y in board.cells:
                if xpos == x and ypos == y:
                    target_pos = xpos,ypos-1
                    return target_pos
            target_pos = xpos,ypos
        return target_pos

    def move_to_target(self, board, target_pos):
        #moves shape to target pos
        while target_pos[0] != board.falling.left:
            if target_pos[0] < board.falling.left:
                return Direction.Left
            elif target_pos[0] > board.falling.left:
                return Direction.Right
        return Direction.Down

    def get_best_target_pos(self, board, target_positions):
        max_y = 0
        best_target = None
        for target in target_positions:
            if target[1] > max_y:
                max_y = target[1]
                best_target = target
        return best_target

    def choose_action(self, board):
        #creates list of target positions for every 'x' column
        target_pos = []
        for x in range(board.width):
            target_pos.append(self.get_target_pos(board, x))
        #gets best target
        best_target = self.get_best_target_pos(board, target_pos)

        return self.move_to_target(board, best_target)

#SelectedPlayer = RandomPlayer
SelectedPlayer = ZainsPlayer
