from engine import GomokuEngine
from strategy import HumanStrategy
from front_package.button import Button

import pygame

COLOR_BOARD = (255, 180, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)


class GameFront:
    def __init__(self, screen, player_1_strategy, player_2_strategy, board_size=11, game_width=675):
        self.board_size = board_size
        self.engine = GomokuEngine(board_size)
        self.game_width = game_width
        self.player_1_strategy = player_1_strategy
        self.player_2_strategy = player_2_strategy

        self.line_distance = self.game_width / self.board_size
        self.current_player = 1
        self.winner_text = ""
        self.instruction1_text = "Choose starting position by"
        self.instruction2_text = "placing 2 white and 1 black stones (alternating)"
        self.current_board = [["" for _ in range(board_size)] for _ in range(board_size)]

        self.engine.print_board()
        self.has_swap_finished = False
        self.swap_stones_placed = 0
        self.show_swap_button = False

        self.screen = screen
        self.running = True

        self.font = pygame.font.Font(None, 36)
        self.swap_button = Button(self.game_width + 200, 500, 200, 100, "Swap", pygame.font.Font(None, 36),
                                  COLOR_WHITE, COLOR_GREEN, self.handle_swap_button)
        self.no_swap_button = Button(self.game_width + 200, 610, 200, 100, "No Swap", pygame.font.Font(None, 36),
                                     COLOR_WHITE, COLOR_GREEN, self.handle_no_swap_button)

    def handle_swap_button(self):
        if not self.show_swap_button:
            return
        if self.current_player == 1 and self.player_1_strategy == "human":
            self.current_player = self.engine.apply_strategy(HumanStrategy(None, None, True), self.current_player)
        elif self.current_player == 2 and self.player_2_strategy == "human":
            self.current_player = self.engine.apply_strategy(HumanStrategy(None, None, True), self.current_player)
        else:
            self.current_player = self.engine.apply_strategy(
                self.player_1_strategy if self.current_player == 1 else self.player_2_strategy,
                self.current_player)
        print("SWAP CLICKeD")
        self.show_swap_button = False

    def handle_no_swap_button(self):
        if not self.show_swap_button:
            return
        self.current_player = self.engine.apply_strategy(HumanStrategy(None, None, False), self.current_player)
        print("No SWAP CLICKeD")
        self.show_swap_button = False

    def start_app(self):
        while True:
            for event in pygame.event.get():
                self.swap_button.handle_event(event)
                self.no_swap_button.handle_event(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.running:
                        self.handle_mouse_click()
                    else:
                        print("Game ended, please close app")

            self.render()

    def handle_mouse_click(self):
        x_mouse, y_mouse = pygame.mouse.get_pos()
        if (self.line_distance / 2 <= x_mouse <= self.game_width + self.line_distance / 2
                and self.line_distance / 2 <= y_mouse <= self.game_width + self.line_distance / 2):
            if not self.has_swap_finished:
                self.handle_add_swap_circle(x_mouse, y_mouse)
            if self.has_swap_finished and self.swap_stones_placed >= 3:
                self.swap_stones_placed = -1
            elif self.has_swap_finished and self.swap_stones_placed == -1:
                self.handle_add_circle(x_mouse, y_mouse)

    def handle_add_swap_circle(self, x_pos, y_pos):
        board_x = round((x_pos - self.line_distance) / self.line_distance)
        board_y = round((y_pos - self.line_distance) / self.line_distance)
        self.current_board[board_y][board_x] = "white" if self.swap_stones_placed % 2 == 0 else "black"
        self.swap_stones_placed += 1
        if self.swap_stones_placed >= 3:
            print("Setting has swap to true")
            self.has_swap_finished = True
            self.current_player = self.engine.apply_strategy(
                HumanStrategy(None, self.current_board, None), self.current_player)
            self.instruction1_text = ""
            self.instruction2_text = ""
            if self.current_player == 1 and self.player_1_strategy != "human":
                cp = self.current_player
                self.current_player = self.engine.apply_strategy(self.player_1_strategy, self.current_player)
                if self.current_player == cp:
                    self.current_player = self.engine.apply_strategy(self.player_1_strategy, self.current_player)
            elif self.current_player == 2 and self.player_2_strategy != "human":
                cp = self.current_player
                self.current_player = self.engine.apply_strategy(self.player_2_strategy, self.current_player)
                if self.current_player == cp:
                    self.current_player = self.engine.apply_strategy(self.player_2_strategy, self.current_player)
            else:
                self.show_swap_button = True

    def handle_add_circle(self, x_pos, y_pos):
        # Handle add circle
        board_x = round((x_pos - self.line_distance) / self.line_distance)
        board_y = round((y_pos - self.line_distance) / self.line_distance)
        human_move = HumanStrategy((board_x, board_y), None, None)
        try:
            self.current_player = self.engine.apply_strategy(human_move, self.current_player)
        except ValueError as ve:
            print(ve)
        self.current_board = self.engine.get_current_board()
        potential_winner = self.engine.has_game_ended()
        if potential_winner != 0:
            print(f"Player {potential_winner} won!")
            self.winner_text = f"Player {potential_winner} won!"
            self.instruction1_text = "Game finished, close the application"
            self.instruction2_text = ""
            self.running = False
            return
        if self.current_player == 1 and self.player_1_strategy != "human":
            self.current_player = self.engine.apply_strategy(self.player_1_strategy, self.current_player)
        if self.current_player == 2 and self.player_2_strategy != "human":
            self.current_player = self.engine.apply_strategy(self.player_2_strategy, self.current_player)
        self.current_board = self.engine.get_current_board()
        potential_winner = self.engine.has_game_ended()
        if potential_winner != 0:
            print(f"Player {potential_winner} won!")
            self.winner_text = f"Player {potential_winner} won!"
            self.instruction1_text = "Game finished, close the application"
            self.instruction2_text = ""
            self.running = False

    def render(self):
        self.screen.fill(COLOR_BOARD)

        winner_text_obj = self.font.render(self.winner_text, True, COLOR_BLACK)
        winner_rect = winner_text_obj.get_rect()
        winner_rect.center = (self.game_width + 300, 100)
        self.screen.blit(winner_text_obj, winner_rect)

        instruction1_text_obj = self.font.render(self.instruction1_text, True, COLOR_BLACK)
        instruction1_rect = instruction1_text_obj.get_rect()
        instruction1_rect.center = (self.game_width + 300, 300)
        self.screen.blit(instruction1_text_obj, instruction1_rect)

        instruction2_text_obj = self.font.render(self.instruction2_text, True, COLOR_BLACK)
        instruction2_rect = instruction2_text_obj.get_rect()
        instruction2_rect.center = (self.game_width + 300, 350)
        self.screen.blit(instruction2_text_obj, instruction2_rect)

        curr_player_text = self.font.render(f"Current Player: {self.current_player}", True, COLOR_BLACK)
        curr_player_rect = curr_player_text.get_rect()
        curr_player_rect.center = (self.game_width + 300, 50)
        self.screen.blit(curr_player_text, curr_player_rect)

        if self.show_swap_button:
            self.swap_button.draw(self.screen)
            self.no_swap_button.draw(self.screen)
        self.draw_board()
        pygame.display.update()

    def draw_board(self):
        current_board = self.current_board
        # Draw grid
        for i in range(1, self.board_size + 1):
            pygame.draw.line(self.screen, COLOR_BLACK, [self.line_distance * i, self.line_distance],
                             [self.line_distance * i, self.game_width], 2)
            pygame.draw.line(self.screen, COLOR_BLACK, [self.line_distance, self.line_distance * i],
                             [self.game_width, self.line_distance * i], 2)

        # Draw circles
        for rowIndex, row in enumerate(current_board):
            for columnIndex, cell in enumerate(row):
                if cell == "white":
                    pygame.draw.circle(self.screen, COLOR_WHITE,
                                       [self.line_distance * (columnIndex + 1), self.line_distance * (rowIndex + 1)],
                                       self.line_distance / 2.1)
                elif cell == "black":
                    pygame.draw.circle(self.screen, COLOR_BLACK,
                                       [self.line_distance * (columnIndex + 1), self.line_distance * (rowIndex + 1)],
                                       self.line_distance / 2.1)


if __name__ == "__main__":
    pygame.init()
    running = True
    screeny = pygame.display.set_mode((900, 725))
    pygame.display.set_caption("XDD")
    front = GameFront(screeny, "human", "human")
    front.start_app()
