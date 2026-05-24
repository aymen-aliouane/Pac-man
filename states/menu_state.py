from components import State
import pygame

class MenuState(State):
    """Class that handle the user events in the menu"""
    def handle_input(self, events: list[pygame.Event], game: Game) -> bool:
        # Handle the events
        for event in events:
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                # if the user press escape, it will pause the game
                if event.key == pygame.K_ESCAPE:
                    from .pause_state import PauseState
                    game.state = PauseState()


                if event.key == pygame.K_SPACE:
                    game.state = MenuState()

    def update(self, game: Game, dt: float):
        """Update the game state"""
        pass


    def render(self, game: Game, screen: pygame.Surface):
        """Render the menu state"""
        screen.fill((255, 223, 0))

        # Render the title
        font = pygame.font.SysFont("Arial", 208)
        text = font.render("PAC-MAN", True, (255, 255, 255))
        text_rect = text.get_rect(center=(game.display.width // 2, 300))
        screen.blit(text, text_rect)

