import pygame
from front_package import GameFront
from front_package import Button
from strategy import Strategy
from strategy import MCTSStrategy
from strategy import MCTSStrategyDawcio

COLOR_BOARD = (255, 180, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)


class Frontend:
    def __init__(self):
        pygame.init()
        self.game_width = 675
        self.screen = pygame.display.set_mode((self.game_width + 600, self.game_width + 45))
        pygame.display.set_caption("Gomoku Swap")
        self.game_front = None
        self.pvp_button = Button((self.game_width + 200) / 2 - 200, 300, 200, 100, "Player vs Player",
                                 pygame.font.Font(None, 36),
                                 COLOR_WHITE, COLOR_GREEN, self.handle_pvp_button)
        self.pve_button = Button((self.game_width + 200) / 2 + 200, 300, 200, 100, "Player vs AI",
                                 pygame.font.Font(None, 36),
                                 COLOR_WHITE, COLOR_GREEN, self.handle_pve_button)

    def handle_pvp_button(self):
        print("START")
        self.game_front = GameFront(self.screen, player_1_strategy="human", player_2_strategy="human", board_size=5)

        self.game_front.start_app()

    def handle_pve_button(self):
        print("START")
        self.game_front = GameFront(self.screen, player_1_strategy="human", player_2_strategy=MCTSStrategyDawcio(2, False), board_size=15)
        self.game_front.start_app()

    def start_app(self):
        while True:
            for event in pygame.event.get():
                self.pvp_button.handle_event(event)
                self.pve_button.handle_event(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.render()

    def render(self):
        self.screen.fill(COLOR_BOARD)
        self.pvp_button.draw(self.screen)
        self.pve_button.draw(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    f = Frontend()
    f.start_app()
