import os
import random
import pygame

from src.config import *


class Trash:
    def __init__(self, x, y):
        self.abstractX = x
        self.abstractY = y
        self.generate_random_trash(x, y)

    def generate_random_trash(self, x, y):
        random_index = random.randint(1, 2)

        if random_index == 1:
            self.type = TRASH_BOTTLE
            asset_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'trashes', 'plastic-bottle.png')
        else:
            self.type = TRASH_CAN
            asset_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'trashes', 'can.png')

        self.asset = pygame.transform.scale(pygame.image.load(asset_path), (DEFAULT_ASSET_SIZE, DEFAULT_ASSET_SIZE))
        self.object = pygame.Rect(self.abstractX * DEFAULT_ASSET_SIZE, self.abstractY * DEFAULT_ASSET_SIZE,
                                  DEFAULT_ASSET_SIZE, DEFAULT_ASSET_SIZE)
