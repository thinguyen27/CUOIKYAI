import assets
import pygame.sprite
from layer import Layer

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self._layer = Layer.PLAYER
        self.x = x
        self.y = y
        self.direction = "down"
        self.sprites = {
            "up": assets.get_sprite("player_up"),
            "down": assets.get_sprite("player_down"),
            "left": assets.get_sprite("player_left"),
            "right": assets.get_sprite("player_right")
        }
        self.image = self.sprites[self.direction]
        self.rect = self.image.get_rect(topleft=(x, y))

    def set_direction(self, direction):
        if direction in self.sprites:
            self.direction = direction
            self.image = self.sprites[direction]