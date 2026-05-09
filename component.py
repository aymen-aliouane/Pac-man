from dataclasses import dataclass
from enum import Enum
import pygame


class Controls(Enum):
    WASD = {
        "UP": pygame.K_w,
        "DOWN": pygame.K_s,
        "LEFT": pygame.K_a,
        "RIGHT": pygame.K_d
    }
    ZQSD = {
        "UP": pygame.K_z,
        "DOWN": pygame.K_s,
        "LEFT": pygame.K_q,
        "RIGHT": pygame.K_d
    }
    ARROWS = {
        "UP": pygame.K_UP,
        "DOWN": pygame.K_DOWN,
        "LEFT": pygame.K_LEFT,
        "RIGHT": pygame.K_RIGHT
    }


class Game:
    settings: Settings

@dataclass
class Settings:
    width: int
    height: int
    max_time: int
    controls: Controls
