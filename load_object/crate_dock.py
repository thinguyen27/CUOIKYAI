import assets
import pygame.sprite
from layer import Layer

class CrateDock(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        self._layer = Layer.CRATE_DOCK
        self.image = assets.get_sprite("crate_docked")
        if self.image is None:
            raise ValueError("Không tìm thấy sprite cho 'crate_docked'")
        self.rect = self.image.get_rect(topleft=(x, y))
        super().__init__(*groups)