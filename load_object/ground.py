import assets
import pygame.sprite
from layer import Layer

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        self._layer = Layer.GROUND
        self.image = assets.get_sprite("ground")
        if self.image is None:
            raise ValueError("Không tìm thấy sprite cho 'ground'")
        self.rect = self.image.get_rect(topleft=(x, y))
        super().__init__(*groups)