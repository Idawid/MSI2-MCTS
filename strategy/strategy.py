class Strategy:
    def get_next_move(self, board, enemy_move: (int, int)) -> (int, int):
        pass

    def get_start_swap_position(self, board):
        pass

    # If returns true if wants to play white
    def choose_starting_color(self, board) -> bool:
        pass
