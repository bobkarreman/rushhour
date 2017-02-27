import sys


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
                            car.orientation = Car.VERTICAL if x == car.x else Car.VERTICAL
                            car.x = min(x, car.x)
                            car.y = min(y, car.y)
                            car.length += 1
            return list(car_map.values())


def main(path):
    cars = Rushhour.parse_file(path)
    board = Board(cars)

    print("Board:")
    print(board.print_board())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide challenge to parse")
    else:
        main(sys.argv[1])
