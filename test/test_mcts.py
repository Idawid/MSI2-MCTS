import unittest

from mcts.mcts_node import State, MonteCarloTreeSearchNode


class TestMonteCarloTreeSearch(unittest.TestCase):
    def setUp(self):
        self.start_board = [['', '', '', '', ''],
                            ['', '', '', '', ''],
                            ['', 'white', 'black', 'white', ''],
                            ['', '', '', '', ''],
                            ['', '', '', '', '']]
        self.player_1_color = 'white'
        self.player_2_color = 'black'

    def test_mcts_best_action(self):
        state = State(self.start_board)
        mcts_root = MonteCarloTreeSearchNode(state)
        selected_node = mcts_root.best_action()
        action = selected_node.parent_action

        # Check that the action is legal
        self.assertIn(action, state.get_legal_actions(), "The action selected is not a legal action.")

        # Check that the new state after the action is correctly updated
        new_state = state.move(action)
        current_player_color = state._get_current_color()
        self.assertEqual(new_state.board[action[0]][action[1]], current_player_color,
                         "The move was not applied correctly to the new state.")

        # Ensure the action leads to a valid game state (not game over immediately)
        self.assertFalse(new_state.is_game_over(), "The selected action should not lead to an immediate game over.")

    def test_mcts_best_action_leads_to_different_state(self):
        state = State(self.start_board)
        mcts_root = MonteCarloTreeSearchNode(state)
        selected_node = mcts_root.best_action()
        action = selected_node.parent_action
        new_state = state.move(action)

        # Ensure that the new state is different from the initial state
        self.assertNotEqual(state.board, new_state.board, "The new state should be different from the initial state after a move.")
        self.assertNotEqual(state._get_current_color(), new_state._get_current_color(),
                            "The current player should switch after a move.")


if __name__ == '__main__':
    unittest.main()
