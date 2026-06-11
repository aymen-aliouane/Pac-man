from components import State, Game
from displaying.ui_components import Title, Button
import pygame



class LostState(State):
    """Class that handle the user events in the menue"""
    def __init__(self):
        self.button_save_score = None

    def handle_input(self, events: list[pygame.Event], game: Game) -> bool:
        """Handle the events when lost,
        return True if the user want to quit the game"""
        for event in events:
            if self.button_save_score is not None and self.button_save_score.is_clicked(event):
                from states.save_score_state import SaveScoreState
                game.state = SaveScoreState()
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return True

        return False

    def update(self, game, dt):
        """Update the game state when lost,
        execute the actions of the user choice"""
        # print("You lost")
        pass

    def render(self, game: Game, screen: pygame.Surface):
        """Render the lost screen"""
        screen.fill((0, 0, 0))
        title = Title(
            text="You Lost",
            color=(255, 0, 0),
            width=game.display.width,
            height=300,
            type_="Arial",
            screen=screen,
            size=208
            )
        title.render()
        score_text = Title(
            text=f"Your score is {game.score}",
            color=(255, 255, 255),
            width=game.display.width,
            height=500,
            type_="Arial",
            screen=screen,
            size=80
            )
        score_text.render()
        self.button_save_score = Button(
            screen=screen,
            text="Do you Want to Save Your Score ?",
            font_type="Arial",
            font_size=50,
            color=(255, 0, 0),
            hover_color=(200, 0, 0),
            text_color=(255, 255, 255),
            x=game.display.width // 2,
            y=700,
            width=200,
            height=150,
            game=game
        )
        self.button_save_score.render()
