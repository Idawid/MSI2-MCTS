from engine import GomokuEngine
from strategy import HumanStrategy
import pygame

COLOR_BOARD = (255, 180, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)


class Frontend:
    def __init__(self, board_size = 11):
        self.board_size = board_size
        self.engine = GomokuEngine(board_size)
        self.game_width = 675
        self.line_distance = self.game_width / self.board_size
        self.current_player = 1
        self.winner_text = ""
        self.instruction_text = "Loasdasd sad asd asdasdasd"

        start_board = [["" for _ in range(board_size)] for _ in range(board_size)]
        start_board[3][4] = "white"
        start_board[3][3] = "black"
        start_board[4][4] = "white"
        self.engine.apply_strategy(HumanStrategy(None, start_board, False), 1)
        self.current_player = self.engine.apply_strategy(HumanStrategy(None, start_board, False), 2)
        self.engine.print_board()

        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((self.game_width + 600, self.game_width + 45))
        pygame.display.set_caption("Gomoku Swap")
        self.font = pygame.font.Font(None, 36)

    def start_app(self):
        while True:
            for event in pygame.event.get():
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
        if (self.line_distance/2 <= x_mouse <= self.game_width + self.line_distance / 2
                and self.line_distance/2 <= y_mouse <= self.game_width + self.line_distance / 2):
            self.handle_add_circle(x_mouse, y_mouse)

    def handle_add_circle(self, x_pos, y_pos):
        # Handle add circle
        board_x = round((x_pos - self.line_distance) / self.line_distance)
        board_y = round((y_pos - self.line_distance) / self.line_distance)
        human_move = HumanStrategy((board_x, board_y), None, None)
        try:
            self.current_player = self.engine.apply_strategy(human_move, self.current_player)
        except ValueError as ve:
            print(ve)
        potential_winner = self.engine.has_game_ended()
        if potential_winner != 0:
            print(f"Player {potential_winner} won!")
            self.winner_text = f"Player {potential_winner} won!"
            self.running = False

    def render(self):
        self.screen.fill(COLOR_BOARD)

        winner_text_obj = self.font.render(self.winner_text, True, COLOR_BLACK)
        winner_rect = winner_text_obj.get_rect()
        winner_rect.center = (self.game_width + 300, 100)
        self.screen.blit(winner_text_obj, winner_rect)

        instruction_text_obj = self.font.render(self.instruction_text, True, COLOR_BLACK)
        instruction_rect = instruction_text_obj.get_rect()
        instruction_rect.center = (self.game_width + 300, 300)
        self.screen.blit(instruction_text_obj, instruction_rect)
        self.draw_board()
        pygame.display.update()

    def draw_board(self):
        current_board = self.engine.get_current_board()
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
    screen = pygame.display.set_mode((900, 725))
    pygame.display.set_caption("XDD")
    front = Frontend()
    front.start_app()
