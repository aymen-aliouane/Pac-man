from .game_state import GameState
from displaying.ui_components import Title, Button, InputBox
import pygame

class SaveScoreState(GameState):
    """Class that handle the user events in the save score state"""
    def __init__(self):
        self.input_box = None
        self.submit_button = None
    
    def handle_input(self, events: list[pygame.Event], game: Game) -> bool:
        """Handle the events when save score,
        return True if the user want to quit the game"""
        for event in events:
            if self.submit_button is not None and self.submit_button.is_clicked(event):
                with open(game.settings.high_scores_file, "a") as f:
                    f.write(f"{self.input_box.text} {game.score}\n")
                return True
            if self.input_box is not None:
                self.input_box.handle_event(event)

            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return True

        return False
    
    def update(self, game, dt):
        """Update the game state when save score,
        execute the actions of the user choice"""
        pass
    def render(self, game: Game, screen: pygame.Surface):
        """Render the save score screen"""
        screen.fill((0, 0, 0))
        title = Title(
            text="Save Your Score",
            color=(255, 255, 255),
            width=game.display.width,
            height=300,
            type_="Courier New",
            screen=screen,
            size=108
            )
        title.render()
        if self.input_box is None:
            self.input_box = InputBox(
                screen=screen,
                type_="Courier New",
                color=(255, 255, 255),
                x=game.display.width // 2,
                y=game.display.height // 2,
                width=300,
                height=80,
                size=32
            )
        self.input_box.render()
        if self.input_box.active:
            color = (255, 255, 255)
        else:
            color = (200, 200, 200)
        self.submit_button = Button(
            screen=screen,
            font_type="Courier New",
            font_size=24,
            color=color,
            hover_color=(200, 200, 200),
            x=game.display.width // 2,
            y=game.display.height // 2 + 120,
            width=200,
            height=50,
            text="Submit",
            text_color=(0, 0, 0)
        )
        self.submit_button.render()
