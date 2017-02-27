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
        queue.append(board)

        idx = 0
        while len(queue) > 0:
            board = queue.popleft()
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

if __name__ == '__main__':
    unittest.main()
