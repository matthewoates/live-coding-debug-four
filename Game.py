#!/usr/bin/env python3

import unittest

class Game():
    def __init__(self):
        self.ROWS = 6
        self.COLS = 7
        self.playerTurn = 1

        self.board = [
            #A  B  C  D  E  F  G
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]
        self.moveHistory = []
        self.isP1Turn = True

    def canMove(self, col):
        return col and not self.board[col][0]

    def move(self, col):
        for row in range(self.ROWS - 1, 0, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.playerTurn
                # it's the other player's turn
                self.playerTurn = 2 if (self.playerTurn == 1) else 1
                self.moveHistory.append(col)

                return

    def getPiece(self, row, col):
        if row < 0 or col < 0 or row >= self.ROWS or col >= self.COLS:
            return None

        return self.board[row][col]

    def undo(self):
        col = self.moveHistory.pop()

        for row in range(0, self.ROWS):
            if self.board[row][col] != 0:
                self.board[row][col] = 0

                return

    # return:
    #   0 if the game is still going
    #   1 if p1 has won
    #   2 if p2 has won
    def whoWon(self):
        col = self.moveHistory[-1]
        row = 0

        while self.board[row][col] == 0:
            row += 1

        # (row, col) is where the last move was
        directions = (
            (-1, -1),
            (0, -1),
            (1, -1),
            (1, 0),
            (1, 1),
            (1, 0),
            (1, -1)
        )

        for (dRow, dCol) in directions:
            player = self.getPiece(row, col)

            if self.getPiece(row + dRow, col + dCol) == player and self.getPiece(row + dRow * 2, col + dCol * 2) == player and self.getPiece(row + dRow * 3, col + dCol * 3) == player:
                return player

        return 0

class TestGame(unittest.TestCase):
    def test_can_move_col_d(self):
        g = Game()

        self.assertTrue(g.canMove(3))

    # def test_can_move_all_cols(self):
    #     g = Game()

    #     for col in range(g.COLS):
    #         self.assertTrue(g.canMove(col))

    def test_player_turn_changes(self):
        g = Game()

        self.assertEqual(g.playerTurn, 1)
        g.move(3)
        self.assertEqual(g.playerTurn, 2)
        g.move(3)
        self.assertEqual(g.playerTurn, 1)

    # def test_filling_col(self):
    #     # there are 6 rows, so we should be able to move
    #     # 6 times in a column
    #     g = Game()

    #     for t in range(g.ROWS):
    #         g.move(3)
    #         self.assertNotEqual(g.getPiece(g.ROWS - 1 - t, 3), 0)

    #     print(str(g.board))

    def test_can_undo(self):
        g = Game()

        g.move(2)
        self.assertEqual(g.getPiece(g.ROWS - 1, 2), 1)
        g.undo()
        self.assertEqual(g.getPiece(g.ROWS - 1, 2), 0)

    # def test_can_redo(self):
    #     g = Game()

    #     g.move(1)
    #     g.undo()
    #     g.move(2)

    #     self.assertEqual(g.getPiece(g.ROWS - 1, 2), 1)

    def test_nobody_won_yet(self):
        g = Game()

        for t in range(3):
            g.move(2)
            g.move(3)
            self.assertEqual(g.whoWon(), 0)

    def test_p1_won(self):
        g = Game()

        g.move(1)
        g.move(2)

        g.move(1)
        g.move(4)

        g.move(1)
        g.move(4)

        g.move(1)

        self.assertEqual(g.whoWon(), 1)

    # def test_p1_won_again(self):
    #     g = Game()

    #     g.move(3)
    #     g.move(3)

    #     g.move(4)
    #     g.move(4)

    #     g.move(1)
    #     g.move(1)

    #     g.move(2)

    #     self.assertEqual(g.whoWon(), 1)













    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()
