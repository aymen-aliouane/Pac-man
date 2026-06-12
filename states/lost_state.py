from components import State, Game
from displaying.ui_components import Title, Button, ExitButton, PlayButton
import pygame



class LostState(State):
    """Class that handle the user events in the menue"""
    def __init__(self):
        self.button_save_score = None
        self.play_button = None
        self.exit_button = None

    def handle_input(self, events: list[pygame.Event], game: Game) -> bool:
        """Handle the events when lost,
        return True if the user want to quit the game"""
        for event in events:
            if self.button_save_score is not None and self.button_save_score.is_clicked(event):
                from states.save_score_state import SaveScoreState
                game.state = SaveScoreState()
            if event.type == pygame.QUIT or (self.exit_button is not None and self.exit_button.is_clicked(event)):
                return True
            if self.play_button is not None and self.play_button.is_clicked(event):
                from states.menu_state import MenuState
                game.engine.restart()
                game.state = MenuState()
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
            width=800,
            height=100,
            border_radius=0
        )
        self.button_save_score.render()

        self.exit_button = ExitButton(screen, game, 200, 100)
        self.exit_button.color = (255, 0, 0)
        self.exit_button.draw()


        self.play_button = PlayButton(screen, game, 200, 100)
        self.play_button.text = "Play Again"
        self.play_button.color = self.play_button.hover_color
        self.play_button.draw()
