import os

import pygame

from src.config import *
from src.entitie.Obs import Obs
from src.entitie.Space import Space


class Truck:
    def __init__(self, x=0, y=0):
        self.abstractX = x
        self.abstractY = y
        self.direction = R_RIGHT
        asset_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'garbage-truck.png')
        self.backAsset = pygame.transform.scale(pygame.image.load(asset_path), (DEFAULT_ASSET_SIZE, DEFAULT_ASSET_SIZE))
        self.asset = pygame.transform.scale(pygame.image.load(asset_path), (DEFAULT_ASSET_SIZE, DEFAULT_ASSET_SIZE))
        self.object = pygame.Rect(self.abstractX * DEFAULT_ASSET_SIZE, self.abstractY * DEFAULT_ASSET_SIZE,
                                  DEFAULT_ASSET_SIZE, DEFAULT_ASSET_SIZE)
        self.velocity = DEFAULT_ASSET_SIZE

    def rotate_up(self):
        self.asset = self.backAsset
        self.asset = pygame.transform.rotate(self.asset, 90)
        self.direction = R_UP

    def rotate_down(self):
        self.asset = self.backAsset
        self.asset = pygame.transform.rotate(self.asset, -90)
        self.direction = R_DOWN

    def rotate_right(self):
        self.asset = self.backAsset
        self.direction = R_RIGHT

    def rotate_left(self):
        self.asset = self.backAsset
        self.asset = pygame.transform.rotate(self.asset, 180)
        self.asset = pygame.transform.flip(self.asset, False, True)
        self.direction = R_LEFT

    def move(self, map):
        if self.direction == R_UP:
            self.move_up(map)
        if self.direction == R_DOWN:
            self.move_down(map)
        if self.direction == R_RIGHT:
            self.move_right(map)
        if self.direction == R_LEFT:
            self.move_left(map)

    def replace(self, map, oldX, oldY):
        map[oldX][oldY] = Space(oldX, oldY)
        map[self.abstractX][self.abstractY] = self

    def move_up(self, map):
        if self.abstractY == 0:
            return
        oldX = self.abstractX
        oldY = self.abstractY
        if isinstance(map[self.abstractX][self.abstractY - 1], Obs):
            return
        self.abstractY -= 1
        self.object.y -= self.velocity
        self.replace(map, oldX, oldY)

    def move_down(self, map):
        if self.abstractY == DEFAULT_MAP_SIZE - 1:
            return
        oldX = self.abstractX
        oldY = self.abstractY
        if isinstance(map[self.abstractX][self.abstractY + 1], Obs):
            return
        self.abstractY += 1
        self.object.y += self.velocity
        self.replace(map, oldX, oldY)

    def move_right(self, map):
        if self.abstractX == DEFAULT_MAP_SIZE - 1:
            return
        oldX = self.abstractX
        oldY = self.abstractY
        if isinstance(map[self.abstractX + 1][self.abstractY], Obs):
            return
        self.abstractX += 1
        self.object.x += self.velocity
        self.replace(map, oldX, oldY)

    def move_left(self, map):
        if self.abstractX == 0:
            return
        oldX = self.abstractX
        oldY = self.abstractY
        if isinstance(map[self.abstractX - 1][self.abstractY], Obs):
            return
        self.abstractX -= 1
        self.object.x -= self.velocity
        self.replace(map, oldX, oldY)
