import unittest

from rushhour import Rushhour, Board, Car


class TestBoard(unittest.TestCase):

    def test_parsing_files(self):
        path = '../challenges/test.txt'
        cars = Rushhour.parse_file(path)
        self.assertEquals(len(cars), 1)

        red_car = cars[0]
        self.assertEquals(red_car.x, 4)
        self.assertEquals(red_car.y, 2)
        self.assertEquals(red_car.length, 2)
        self.assertEquals(red_car.orientation, Car.HORIZONTAL)

    def test_print_board(self):
        path = '../challenges/simple.txt'
        with open(path) as f:
            data = f.read()

            cars = Rushhour.parse_file(path)
            board = Board(cars)

            print("FILE")
            print(data)
            print("BOARD")
            print(board.print_board())
            self.assertEquals(board.print_board(), data)

    def test_board_parse_simple(self):
        path = '../challenges/simple.txt'
        cars = Rushhour.parse_file(path)
        a = None
        for car in cars:
            if car.name == 'A':
                a = car
                break

        self.assertEquals(a.x, 5)
        self.assertEquals(a.y, 0)
        self.assertEquals(a.length, 3)
        self.assertEquals(a.orientation, "vertical")

    def test_board_validation(self):
        path = '../challenges/simple.txt'
        cars = Rushhour.parse_file(path)
        board = Board(cars)

        self.assertTrue(board.is_valid())


if __name__ == '__main__':
    unittest.main()
