from components import State, Game
from .game_state import GameState
from displaying.ui_components import Title, Button
import pygame

class MenuState(State):
    """Class that handle the user events in the menu"""
    def __init__(self):
        self.play_button = None

    def handle_input(self, events: list[pygame.Event], game: Game) -> bool:
        # Handle the events
        for event in events:
            if self.play_button is not None and self.play_button.is_clicked(event):
                game.state = GameState()
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                # if the user press escape, it will pause the game
                if event.key == pygame.K_ESCAPE:
                    from .pause_state import PauseState
                    game.state = PauseState()


                if event.key == pygame.K_SPACE:
                    game.state = GameState()
        
                if event.key == pygame.K_q:
                    return True

    def update(self, game: Game, dt: float):
        """Update the game state"""
        pass


    def render(self, game: Game, screen: pygame.Surface):
        """Render the menu state"""
        screen.fill((255, 223, 0))

        title = Title(
            text="PAC-MAN",
            color=(255, 255, 255),
            width=game.display.width,
            height=300,
            type_="Arial",
            screen=screen,
            size=208
            )
        title.render()
        press_space = Title(
            text="press Space to Play",
            color=(255, 255, 255),
            width=game.display.width,
            height=800,
            type_="Arial",
            screen=screen,
            size=80
            )
        press_space.render()
        self.play_button = Button(
            screen=screen,
            text="PLAY",
            font_type="Arial",
            font_size=40,
            color=(50, 120, 255),
            hover_color=(30, 80, 200),
            text_color=(255, 255, 255),
            width=300,
            height=180,
            x=game.display.width - 400,
            y=game.display.height - 280,
            game=game
        )
        self.play_button.render()


