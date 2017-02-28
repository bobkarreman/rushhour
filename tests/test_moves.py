import unittest

from collections import deque
from rushhour import Rushhour, Board


class TestMoves(unittest.TestCase):

    def test_moves_one_car(self):
        """
        Test if the board still contains all the cars when moving the cars around
        """

        cars = Rushhour.parse_file('challenges/provided.txt')
        board = Board(cars)

        seen = set()

        queue = deque()
        queue.append((None, board))

        idx = 0
        while len(queue) > 0:
            move, board = queue.popleft()
            """
            * * * * A A
            * * B B C C
            r r * * E F
            G G H H E F
            * * * I E F
            * * * I J J
            """
            if str(board) in seen:
                continue

            self.assertEqual(str(board).count('*'), 14)
            self.assertEqual(str(board).count('r'), 2)
            self.assertEqual(str(board).count('A'), 2)
            self.assertEqual(str(board).count('B'), 2)
            self.assertEqual(str(board).count('C'), 2)
            self.assertEqual(str(board).count('E'), 3)
            self.assertEqual(str(board).count('F'), 3)
            self.assertEqual(str(board).count('G'), 2)
            self.assertEqual(str(board).count('H'), 2)
            self.assertEqual(str(board).count('I'), 2)
            self.assertEqual(str(board).count('J'), 2)

            seen.add(str(board))

            if board.is_finished():
                return True

            new_boards = board.possibilities()
            queue.extend(new_boards)
            idx += 1

    def test_get_moves(self):
        """
        Test if all the moves that are possible are returned by the get_moves func

        * * B * * *
        * * B * * *
        * * * * r r
        * A * * * *
        * A * * * *
        * * C C * *

        """
        cars = Rushhour.parse_file('challenges/test_moves.txt')
        board = Board(cars)

        for car in cars:
            moves = board.get_moves(car)
            up_cnt = 0
            down_cnt = 0
            left_cnt = 0
            right_cnt = 0
            for x, y in moves:
                if x < 0:
                    left_cnt += 1
                if x > 0:
                    right_cnt += 1
                if y < 0:
                    up_cnt += 1
                if y > 0:
                    down_cnt += 1

            # r 4 moves left
            if car.name == 'r':
                self.assertEqual(len(moves), 4)
                self.assertEqual(up_cnt, 0)
                self.assertEqual(down_cnt, 0)
                self.assertEqual(left_cnt, 4)
                self.assertEqual(right_cnt, 0)

            # A 3 moves up 1 move down
            if car.name == 'A':
                self.assertEqual(len(moves), 4)
                self.assertEqual(up_cnt, 3)
                self.assertEqual(down_cnt, 1)
                self.assertEqual(left_cnt, 0)
                self.assertEqual(right_cnt, 0)

            # B 3 moves down
            if car.name == 'B':
                self.assertEqual(len(moves), 3)
                self.assertEqual(up_cnt, 0)
                self.assertEqual(down_cnt, 3)
                self.assertEqual(left_cnt, 0)
                self.assertEqual(right_cnt, 0)

            # C 2 moves left 2 moves right
            if car.name == 'C':
                self.assertEqual(len(moves), 4)
                self.assertEqual(up_cnt, 0)
                self.assertEqual(down_cnt, 0)
                self.assertEqual(left_cnt, 2)
                self.assertEqual(right_cnt, 2)

    def test_moving_cars(self):
        """
        Test if the board still contains all the cars when moving the cars around
            y
            |
            | 0 1 2 3 4 5
        x-----------------
           0| * * B * * *
           1| * * B * * *
           2| * * * * r r
           3| * A * * * *
           4| * A * * * *
           5| * * C C * *

        """
        cars = Rushhour.parse_file('challenges/test_moves.txt')
        board = Board(cars)

        for car in cars:
            # r 4 moves left
            if car.name == 'r':
                y = 2
                # Before
                self.assertEqual(' '.join(board.matrix[y]), '* * * * r r')

                # 1 Step left
                move, new_board = board.move_car(car, -1, 0)
                self.assertEqual(' '.join(new_board.matrix[y]), '* * * r r *')

                # 2 Step left
                move, new_board = board.move_car(car, -2, 0)
                self.assertEqual(' '.join(new_board.matrix[y]), '* * r r * *')

                # 3 Step left
                move, new_board = board.move_car(car, -3, 0)
                self.assertEqual(' '.join(new_board.matrix[y]), '* r r * * *')

                # 4 Step left
                move, new_board = board.move_car(car, -4, 0)
                self.assertEqual(' '.join(new_board.matrix[y]), 'r r * * * *')

            # A 3 moves up 1 move down
            if car.name == 'A':
                x = 1
                # Before
                self.assertEqual(board.matrix[3][x], 'A')
                self.assertEqual(board.matrix[4][x], 'A')

                # 1 step down
                move, new_board = board.move_car(car, 0, 1)
                self.assertEqual(new_board.matrix[4][x], 'A')
                self.assertEqual(new_board.matrix[5][x], 'A')

                # 1 step up
                move, new_board = board.move_car(car, 0, -1)
                self.assertEqual(new_board.matrix[2][x], 'A')
                self.assertEqual(new_board.matrix[3][x], 'A')

                # 2 step up
                move, new_board = board.move_car(car, 0, -2)
                self.assertEqual(new_board.matrix[1][x], 'A')
                self.assertEqual(new_board.matrix[2][x], 'A')

                # 3 step up
                move, new_board = board.move_car(car, 0, -3)
                self.assertEqual(new_board.matrix[0][x], 'A')
                self.assertEqual(new_board.matrix[1][x], 'A')

            # B 3 moves down
            if car.name == 'B':
                x = 2
                # Before
                self.assertEqual(board.matrix[0][x], 'B')
                self.assertEqual(board.matrix[1][x], 'B')

                # 1 step down
                move, new_board = board.move_car(car, 0, 1)
                self.assertEqual(new_board.matrix[1][x], 'B')
                self.assertEqual(new_board.matrix[2][x], 'B')

                # 2 step down
                move, new_board = board.move_car(car, 0, 2)
                self.assertEqual(new_board.matrix[2][x], 'B')
                self.assertEqual(new_board.matrix[3][x], 'B')

                # 3 step down
                move, new_board = board.move_car(car, 0, 3)
                self.assertEqual(new_board.matrix[3][x], 'B')
                self.assertEqual(new_board.matrix[4][x], 'B')

            # C 2 moves left 2 moves right
            if car.name == 'C':
                y = 5
                # Before
                self.assertEqual(' '.join(board.matrix[y]), '* * C C * *')

                # 1 Step left
                move, new_board = board.move_car(car, -1, 0)
                self.assertEqual(' '.join(new_board.matrix[y]), '* C C * * *')

                # 2 Step left
                move, new_board = board.move_car(car, -2, 0)
                self.assertEqual(' '.join(new_board.matrix[y]), 'C C * * * *')

                # 1 Step right
                move, new_board = board.move_car(car, 1, 0)
                self.assertEqual(' '.join(new_board.matrix[y]), '* * * C C *')

                # 2 Step right
                move, new_board = board.move_car(car, 2, 0)
                self.assertEqual(' '.join(new_board.matrix[y]), '* * * * C C')
if __name__ == '__main__':
    unittest.main()














