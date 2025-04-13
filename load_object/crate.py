import assets
import pygame.sprite
from layer import Layer

class Crate(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        self._layer = Layer.CRATE
        self.image = assets.get_sprite("crate")
        if self.image is None:
            raise ValueError("Không tìm thấy sprite cho 'crate'")
        self.rect = self.image.get_rect(topleft=(x, y))
        super().__init__(*groups)