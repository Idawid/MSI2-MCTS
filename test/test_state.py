import unittest
from engine import GomokuEngine
from mcts.mcts_node import State


class TestState(unittest.TestCase):
    def setUp(self):
        # Create a GomokuEngine instance for testing
        self.engine = GomokuEngine()
        # 2 moves for 1P, 1 move for 2P
        self.engine.board = [['', '', '', '', ''],
                             ['', '', '', '', ''],
                             ['', 'white', 'black', 'white', ''],
                             ['', '', '', '', ''],
                             ['', '', '', '', '']]
        self.engine.board_size = 5
        self.engine.player_1_color = 'white'
        self.engine.player_2_color = 'black'

        # Create a State instance for testing
        self.state = State(self.engine.board)

    def test_get_legal_actions(self):
        # Test that the legal actions are correct
        expected_legal_actions = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                                  (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
                                  (2, 0),                         (2, 4),
                                  (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
                                  (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
        self.assertEqual(self.state.get_legal_actions(), expected_legal_actions)

    def test_is_game_over(self):
        # Test that the game is not over initially
        self.assertFalse(self.state.is_game_over())

        # Test that the game is over when there is a winner
        self.engine.board[2][0] = 'white'
        self.engine.board[2][1] = 'white'
        self.engine.board[2][2] = 'white'
        self.engine.board[2][3] = 'white'
        self.engine.board[2][4] = 'white'
        self.assertTrue(self.state.is_game_over())

    def test_game_result(self):
        # Test that the game result is 0 initially
        self.assertEqual(self.state.game_result(), 0)

        # Test that the game result is 1 when player 1 wins
        self.engine.board[2][0] = 'white'
        self.engine.board[2][1] = 'white'
        self.engine.board[2][2] = 'white'
        self.engine.board[2][3] = 'white'
        self.engine.board[2][4] = 'white'
        self.assertEqual(self.state.game_result(), 1)

        # Test that the game result is -1 when player 2 wins
        self.engine.board[2][0] = 'black'
        self.engine.board[2][1] = 'black'
        self.engine.board[2][2] = 'black'
        self.engine.board[2][3] = 'black'
        self.engine.board[2][4] = 'black'
        self.assertEqual(self.state.game_result(), -1)

    def test_move(self):
        action = (0, 0)
        new_state = self.state.move(action)
        self.assertEqual(new_state.board[0][0], 'black')

        # Check that it's player 1's turn after player 2 made a move
        self.assertEqual(new_state.board, [['black', '', '', '', ''],
                                            ['', '', '', '', ''],
                                            ['', 'white', 'black', 'white', ''],
                                            ['', '', '', '', ''],
                                            ['', '', '', '', '']])


if __name__ == '__main__':
    unittest.main()
