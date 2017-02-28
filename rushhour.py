import sys
from collections import deque
from datetime import datetime


class Car(object):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'

    def __init__(self, name, x, y, length, orientation=None):
        self.name = name
        self.x = x
        self.y = y
        self.length = length
        self.orientation = orientation

    def is_horizontal(self):
        return self.orientation == self.HORIZONTAL

    def is_vertical(self):
        return self.orientation == self.VERTICAL


class Board(object):
    SIZE = 6  # Size of the board
    EXIT = (2, 5)  # Location of the exit on the board (y, x)
    PLAYING_CAR = 'r'  # Letter used for the Playing Car (the red car)
    EMPTY_CHAR = '*'  # Letter used for empty fields in the board

    def __init__(self, cars):
        self.cars = set(cars)
        self.matrix = self._generate_matrix()

    def __str__(self):
        return self.print_board()

    def is_valid(self):
        """
        Check if all cars are valid
        """
        for car in self.cars:
            if car.x >= self.SIZE or car.y >= self.SIZE or car.length <= 1:
                return False
        return True

    def is_finished(self):
        """ If the slot before the exit is r it means the red car is in front of the exit """
        y, x = self.EXIT
        return self.matrix[y][x] == self.PLAYING_CAR

    def _generate_matrix(self):
        # Initialize matrix with empty slots
        matrix = [[self.EMPTY_CHAR for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        for car in self.cars:
            for i in range(car.length):
                if car.is_vertical():
                    matrix[car.y + i][car.x] = car.name
                else:
                    matrix[car.y][car.x + i] = car.name

        return matrix

    def print_board(self):
        output = ""
        for row in self.matrix:
            output += "%s\n" % " ".join(row)
        return output

    def slot_free(self, x, y):
        # print("Slot free:", x, y)
        """ Checks if a slot is in use by a car """
        try:
            return self.matrix[y][x] == self.EMPTY_CHAR
        except IndexError:
            # If the slot is not inside the grid consider it not free to move to
            return False

    def move_car(self, car, move_x, move_y):
        """ Moves the car and returns a new Board """
        move = (car, move_x, move_y)
        new_cars = set()
        for c in self.cars:
            if c is car:
                new_cars.add(Car(c.name, c.x + move_x, c.y + move_y, c.length, c.orientation))
            else:
                new_cars.add(Car(c.name, c.x, c.y, c.length, c.orientation))
        new_board = Board(new_cars)
        return move, new_board

    def get_moves(self, car):
        """
        Get all moves the car can make, if a car can move multiple squares all those moves are returned as separate moves.
        Making it possible to group those moves into one "slide"
        """
        moves = []

        if car.is_horizontal():
            # Can move left
            for i in range(car.x):
                move_x = -1 * (i + 1)
                if not self.slot_free(car.x + move_x, car.y):
                    break
                moves.append((move_x, 0))

            # Can move right
            for i in range(self.SIZE - car.x - (car.length - 1)):
                move_x = i + 1
                if not self.slot_free((car.x + car.length - 1) + move_x, car.y):
                    break
                moves.append((move_x, 0))
        else:
            # Can move up
            for i in range(car.y):
                move_y = -1 * (i + 1)
                if not self.slot_free(car.x, car.y + move_y):
                    break
                moves.append((0, move_y))

            # Can move down
            for i in range(self.SIZE - car.y - (car.length - 1)):
                move_y = i + 1
                if not self.slot_free(car.x, (car.y + car.length - 1) + move_y):
                    break
                moves.append((0, move_y))
        return moves

    def possibilities(self):
        """
        Returns a list of moves (move, board) that are all possible from the current state of this board.
        """
        moves = []
        for car in self.cars:
            for move_x, move_y in self.get_moves(car):
                moves.append(self.move_car(car, move_x, move_y))
        return moves


class Rushhour(object):
    def __init__(self):
        pass

    @staticmethod
    def parse_file(path):
        """ Load a game definition file and return a list of cars """
        with open(path) as f:
            data = f.read()
            car_map = {}
            for y, row in enumerate(data.split('\n')[:6]):
                for x, column in enumerate(row.split(" ")[:6]):
                    if column != Board.EMPTY_CHAR:
                        if column not in car_map:
                            car_map[column] = Car(column, x, y, 1)
                        else:
                            car = car_map[column]
                            car.orientation = Car.VERTICAL if x == car.x else Car.HORIZONTAL
                            car.x = min(x, car.x)
                            car.y = min(y, car.y)
                            car.length += 1
            return list(car_map.values())

    @staticmethod
    def find_solution(start_board):
        """
        Use a BFS (bread first search) algorithm to find the shortest path to the solution for the given board.

        An some other algorithms that could be used are A* or Dijkstra
        Which adds more complexity, that could be used to add a weight to certain moves but not needed in this case.
        ref: http://www.redblobgames.com/pathfinding/a-star/implementation.html
        """
        seen = set()
        paths = {}

        queue = deque()
        queue.append((None, start_board))

        idx = 0
        while len(queue) > 0:
            # Get first item from the queue
            move, board = queue.popleft()

            # If board is already seen skip it (there was a faster way to get to that board)
            if str(board) in seen:
                continue

            seen.add(str(board))

            if board.is_finished():
                print("We found a solution by checking %s boards!" % idx)
                print("Paths length", len(paths))
                return Rushhour.reconstruct_path(start_board, board, move, paths)

            possibilities = board.possibilities()
            queue.extend(possibilities)

            # Keep track of the path
            for _, next_board in possibilities:
                paths[next_board] = (move, board)

            idx += 1
            if idx > 100000:
                print('More then 100000 moves stopping')
                break
        return None

    @staticmethod
    def reconstruct_path(start_board, end_board, last_move, paths):
        """ Returns a list of moves needed to solve the puzzle"""
        solution_path = []
        board = end_board
        solution_path.append((last_move, end_board))
        while board != start_board:
            move, board = paths[board]
            solution_path.append((move, board))
        solution_path.append((None, start_board))
        solution_path.reverse()
        return solution_path


def play_solution(board, solution_path):
    print('-------------- START --------------')
    print(board.print_board())

    for move, board in solution_path:
        if move:
            car, x, y = move
            steps = 0
            direction = "left"
            if x < 0:
                direction = "left"
                steps = x * -1
            elif x > 0:
                direction = "right"
                steps = x
            elif y < 0:
                direction = "up"
                steps = y * -1
            elif y > 0:
                direction = "down"
                steps = y

            print('--------------------------------')
            print("Move car %s %s steps %s" % (car.name, steps, direction))
            print(board.print_board())


def main(path):
    cars = Rushhour.parse_file(path)
    board = Board(cars)

    start = datetime.now()
    solution_path = Rushhour.find_solution(board)
    delta = datetime.now() - start

    if solution_path:
        play_solution(board, solution_path)
        print('--------------------------------')
        print("Solution found in %s seconds and %s steps" % (delta.total_seconds(), len(solution_path)))
    else:
        print('No solution found :-(')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide challenge to parse")
    else:
        main(sys.argv[1])
