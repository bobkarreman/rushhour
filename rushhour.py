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
        return self.matrix[y][x] == self.EMPTY_CHAR

    def move_car(self, car, x, y):
        """ Moves the car and returns a new Board """
        new_cars = set()
        for c in self.cars:
            if c is car:
                new_cars.add(Car(c.name, x, y, c.length, c.orientation))
            else:
                new_cars.add(Car(c.name, c.x, c.y, c.length, c.orientation))
        new_board = Board(new_cars)
        return new_board

    def possibilities(self):
        """ Returns a list of boards (moves) that are all possible from the current state of this board """
        boards = []
        for car in self.cars:
            if car.is_horizontal():
                # Can move left
                if car.x - 1 >= 0 and self.slot_free(car.x - 1, car.y):
                    # print("Car %s can move Left" % car.name, car.x-1, car.y)
                    boards.append(self.move_car(car, car.x - 1, car.y))

                # Can move right
                if car.x + car.length < self.SIZE and self.slot_free(car.x + car.length, car.y):
                    # print("Car %s can move Right" % car.name, car.x + 1, car.y)
                    boards.append(self.move_car(car, car.x + 1, car.y))
            else:
                # Can move up
                if car.y - 1 >= 0 and self.slot_free(car.x, car.y - 1):
                    # print("Car %s can move Up" % car.name, car.x, car.y -1)
                    boards.append(self.move_car(car, car.x, car.y - 1))

                # Can move down
                if car.y + car.length < self.SIZE and self.slot_free(car.x, car.y + car.length):
                    # print("Car %s can move Down" % car.name, car.x, car.y + 1)
                    boards.append(self.move_car(car, car.x, car.y + 1))
        return boards


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
    def find_solution(board):
        """
        Use a BFS (bread first search) algorithm to find the shortest path to the solution for the given board.

        An some other algorithms that could be used are A* or Dijkstra
        Which adds more complexity, that could be used to add a weight to certain moves but not needed in this case.
        ref: http://www.redblobgames.com/pathfinding/a-star/implementation.html
        """
        # TODO: Keep track of the path to the solution
        seen = set()

        queue = deque()
        queue.append(board)

        idx = 0
        while len(queue) > 0:
            # Get first item from the queue
            board = queue.popleft()

            # If board is already seen skip it (there was a faster way to get to that board)
            if str(board) in seen:
                continue

            seen.add(str(board))

            if board.is_finished():
                print("We found a solution by checking %s boards!" % idx)
                return True

            new_boards = board.possibilities()
            queue.extend(new_boards)

            idx += 1
            if idx > 100000:
                print('More then 100000 moves stopping')
                break
        return False


def main(path):
    cars = Rushhour.parse_file(path)
    board = Board(cars)

    print("Board:")
    print(board.print_board())

    start = datetime.now()
    is_finished = Rushhour.find_solution(board)
    delta = datetime.now() - start

    if is_finished:
        print("Solution found in %s seconds" % delta.total_seconds())
    else:
        print('No solution found :-(')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide challenge to parse")
    else:
        main(sys.argv[1])
