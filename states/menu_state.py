from components import State, Game
from .game_state import GameState
from displaying.ui_components import Title, Button, ExitButton
import pygame
import json
import copy

class MenuState(State):
    """Class that handle the user events in the menu"""
    def __init__(self):
        self.play_button = None
        self.exit_button = None

    def handle_input(self, events: list[pygame.Event], game: Game) -> bool:
        # Handle the events
        for event in events:
            if self.play_button is not None and self.play_button.is_clicked(event):
                game.state = GameState()

            if event.type == pygame.QUIT or (self.exit_button is not None and self.exit_button.is_clicked(event)):
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
        # press_space.render()
        font = pygame.font.SysFont("Impact", 50)
        font_surface = font.render("Scores:", True, (255, 255, 255))
        screen.blit(font_surface, (game.display.width // 3 + 50, game.display.height // 2 - 80))
        try:
            with open(game.settings.high_scores_file, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        sorted_scores = sorted(data.items(), key=lambda x: x[1], reverse=True)
        for i, (name, score) in enumerate(sorted_scores[:10]):
            score_surface = font.render(f"{i+1}. {name}: {score} points", True, (255, 255, 255))
            screen.blit(score_surface, (game.display.width // 3 + 50, game.display.height // 2 - 80 + (i + 1) * 50))

        button_width = 200
        button_height = 100
        self.play_button = Button(
            screen=screen,
            text="PLAY",
            font_type="Impact",
            font_size=40,
            color=(255, 255, 255),
            hover_color=(255, 255, 255),
            text_color=(255, 255, 255),
            width=button_width,
            height=button_height,
            x=game.display.width - button_width // 2 - 50,
            y=game.display.height - button_height - 50,
            border_radius=0
        )

        self.play_button.render()
        self.play_button.x += 100
        self.play_button.y += 10
        self.play_button.width -= 20
        self.play_button.height -=  20
        self.play_button.color = (0, 0, 128)
        self.play_button.hover_color = (0, 0, 255)
        self.play_button.render()
        

        self.exit_button = ExitButton(screen, game, button_width, button_height)
        self.exit_button.draw()
