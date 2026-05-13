import pygame
from enum import Enum


class Controls(Enum):
    """Different command available for the user"""
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


class Cheat(Enum):
    """Available cheats"""

    INVICIBLE = "invincible"
    NO_COLLISIONS = "no_collision"
    SKIP_LEVEL = "skip_level"
    INCREASE_SPEED = "increase_speed"

