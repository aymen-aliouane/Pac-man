from typing import Tuple
import pygame
from abc import ABC
# from states.game_state import GameState


class Component(ABC):
    def render(self):
        pass


class Title(Component):
    def __init__(
        self,
        screen: pygame.Surface,
        text: str,
        type_: str,
        color: Tuple[int, int, int],
        width: int,
        height: int,
        size: int
        ):
        self.text = text
        self.type = type_
        self.color = color
        self.width = width
        self.screen = screen
        self.size = size
        self.height= height

    def render(self):
        font = pygame.font.SysFont(self.type, self.size)
        text = font.render(self.text, True, self.color)
        text_rect = text.get_rect(center=(self.width // 2, self.height))
        self.screen.blit(text, text_rect)


class Button(Component):
    def __init__(
        self,
        screen: pygame.Surface,
        text: str,
        font_type: str,
        font_size: int,
        color: Tuple[int, int, int],
        hover_color: Tuple[int, int, int],
        text_color: Tuple[int, int, int],
        x: int,
        y: int,
        width: int,
        height: int,
        border_radius: int = 10

    ):
        self.screen = screen
        self.border_radius = border_radius
        self.text = text

        self.font_type = font_type
        self.font_size = font_size

        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def render(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.color

        font = pygame.font.SysFont(
            self.font_type,
            self.font_size
        )

        text_surface = font.render(
            self.text,
            True,
            self.text_color
        )

        padding_x = 20
        padding_y = 10

        self.x = self.x - self.width // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        text_rect = text_surface.get_rect(
            center=self.rect.center
        )

        pygame.draw.rect(
            self.screen,
            current_color,
            self.rect,
            border_radius=self.border_radius
        )

        self.screen.blit(text_surface, text_rect)




    def is_clicked(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)

        return False


class InputBox(Button):
    def __init__(
        self,
        screen: pygame.Surface,
        type_: str,
        color: Tuple[int, int, int],
        x: int,
        y: int,
        width: int,
        height: int,
        size: int,
    ):
        self.name = ""
        self.type = type_
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size = size
        self.screen = screen
        self.active = True
        self.error = ""


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]

            elif event.key == pygame.K_RETURN:
                print("Submitted:", self.name)

            elif len(self.name) < 14:
                self.name += event.unicode
            if len(self.name) > 10:
                self.color = (255, 0, 0)
                self.error = "Name must be at most 10 characters"
                self.active = False
            elif not all(c.isalnum() or c.isspace() for c in self.name):
                self.color = (255, 0, 0)
                self.error = "Name must contain only alphanumeric characters and spaces"
                self.active = False
            else:
                self.error = ""
                self.color = (0, 0, 0)
                self.active = True

    def render(self):
        rect = pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.color, rect, 3)
        font = pygame.font.SysFont(self.type, self.size)

        text_surface = font.render(
            self.name,
            True,
            self.color
        )

        self.screen.blit(
            text_surface,
            (self.x - self.width // 2 + 20,
            self.y + self.height // 2 - text_surface.get_height() // 2
            ))

        font_error = pygame.font.SysFont(self.type, self.size - 10)
        error_surface = font_error.render(
            self.error,
            True,
            (255, 0, 0)
        )
        error_rect = error_surface.get_rect(
            center=(self.x, self.y + self.height + 20)
        )
        self.screen.blit(
            error_surface,
            error_rect
        )


class ExitButton(Button):
    def __init__(self, screen, game, button_width, button_height):
        super().__init__(
            screen=screen,
            text="EXIT",
            font_type="Impact",
            font_size=40,
            color=(255, 255, 255),
            hover_color=(0, 0, 0),
            text_color=(255, 255, 255),
            width=button_width,
            height=button_height,
            x=button_width - 50,
            y=game.display.height - button_height - 50,
            border_radius=0
        )
        self.render()
        self.x += 100
        self.y += 10
        self.width -= 20
        self.height -= 20
        self.color = (128, 0, 0)
        self.hover_color = (255, 0, 0)

    def draw(self):
        self.render()



class PlayButton(Button):
    def __init__(self, screen, game, button_width, button_height):
        super().__init__(
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

        self.render()

        self.x += 100
        self.y += 10
        self.width -= 20
        self.height -= 20
        self.color = (0, 0, 128)
        self.hover_color = (0, 0, 255)

    def draw(self):
        self.render()