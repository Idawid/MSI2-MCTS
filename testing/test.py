from engine import GomokuEngine
from strategy import MCTSStrategy
from strategy import MCTSStrategyDawcio
from strategy import MCTSStrategyRAVE

with open("OurVsOur.txt", 'w') as file:
    count_1 = 0
    count_2 = 0
    count_d = 0
    for i in range(10):
        print(i)
        board_size = 15

        engine = GomokuEngine(board_size)
        ai1 = MCTSStrategy(board_size, False, sim_no=10)
        ai2 = MCTSStrategyDawcio(board_size, True)
        active_player = 1
        non_active_player = 2

        start_board = [["" for _ in range(board_size)] for _ in range(board_size)]
        engine.apply_strategy(ai1, active_player)
        active_player = engine.apply_strategy(ai2, non_active_player)
        # engine.print_board()
        # while engine.has_game_ended() == 0:
        #     x, y = map(int, input(f"Enter where Player {active_player} wants to move: ").split())
        #     active_player = engine.apply_strategy(HumanStrategy((x, y), None, None), active_player)
        #     engine.print_board()

        while engine.has_game_ended() == 0:
            if active_player == 1:
                active_player = engine.apply_strategy(ai1, active_player)
            else:
                # Let the MCTS algorithm choose a move
                active_player = engine.apply_strategy(ai2, active_player)

            #engine.print_board()
        res = engine.has_game_ended()
        if res == 1:
            count_1 += 1
        if res == 2:
            count_2 += 1
        if res == -1:
            count_d += 1
    file.write(str(count_1) + "\n")
    file.write(str(count_2) + "\n")
    file.write(str(count_d) + "\n")
