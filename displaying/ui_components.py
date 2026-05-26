from typing import Tuple
import pygame
from abc import ABC
from states.game_state import GameState


class Component(ABC):
    def render(self):
        pass


class Title(Component):
    def __init__(self, screen: pygame.Surface, text: str, type_: str, color: Tuple[int, int, int], width: int, height: int, size: int):
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
        game
    ):
        self.screen = screen

        self.text = text

        self.font_type = font_type
        self.font_size = font_size

        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

        self.rect = pygame.Rect(x, y, width, height)
        self.game = game

    def render(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.color

        pygame.draw.rect(
            self.screen,
            current_color,
            self.rect,
            border_radius=12
        )

        font = pygame.font.SysFont(
            self.font_type,
            self.font_size
        )

        text_surface = font.render(
            self.text,
            True,
            self.text_color
        )

        text_rect = text_surface.get_rect(
            center=self.rect.center
        )

        self.screen.blit(text_surface, text_rect)




    def is_clicked(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)

        return False
    
