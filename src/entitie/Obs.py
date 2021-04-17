import pygame
from src.config import DEFAULT_ASSET_SIZE

class Obs:
    def __init__(self, x, y):
        self.abstractX = x
        self.abstractY = y
        self.object = pygame.Rect(self.abstractX * DEFAULT_ASSET_SIZE, self.abstractY * DEFAULT_ASSET_SIZE,
                                  DEFAULT_ASSET_SIZE, DEFAULT_ASSET_SIZE)
        self.asset = pygame.Surface((64, 64))
        self.asset.fill((171, 48, 74))