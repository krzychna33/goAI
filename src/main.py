import os
import random
import time
import threading

import pygame

FPS = 60

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280
PADDING = 64

DEFAULT_ASSET_SIZE = 128

TRASHES_COUNT = 4

WHITE_COLOR = (255, 255, 255)

TRASH_BOTTLE = "TRASH_BOTTLE"
TRASH_CAN = "TRASH_CAN"


class Trash:
    def __init__(self):
        self.generate_random_trash()
        self.get_random_coordinates()

    def generate_random_trash(self):
        random_index = random.randint(1, 2)

        if random_index == 1:
            self.type = TRASH_BOTTLE
            asset_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'trashes', 'plastic-bottle.png')
        else:
            self.type = TRASH_CAN
            asset_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'trashes', 'can.png')

        self.asset = pygame.image.load(asset_path)
        coordinates = self.get_random_coordinates()
        self.object = pygame.Rect(coordinates["x"], coordinates["y"], DEFAULT_ASSET_SIZE, DEFAULT_ASSET_SIZE)

    def get_random_coordinates(self):
        return {
            "x": random.randint(PADDING, WINDOW_WIDTH - PADDING),
            "y": random.randint(PADDING, WINDOW_HEIGHT - PADDING)
        }


class Truck:
    def __init__(self):
        asset_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'garbage-truck.png')
        self.asset = pygame.image.load(asset_path)
        self.object = pygame.Rect(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, DEFAULT_ASSET_SIZE, DEFAULT_ASSET_SIZE)
        self.velocity = 5

    def move_up(self):
        self.object.y -= self.velocity

    def move_down(self):
        self.object.y += self.velocity

    def move_right(self):
        self.object.x += self.velocity

    def move_left(self):
        self.object.x -= self.velocity


class Environment:
    def __init__(self):
        self.truck = Truck()
        self.run = True
        self.clock = pygame.time.Clock()
        self.WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.trashes_list = []
        self.generate_trashes(TRASHES_COUNT)
        self.trashes_collected = []

        while self.run:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            self.keys_pressed = pygame.key.get_pressed()
            self.draw_objects()
            self.handle_keyboard()
            self.handle_collisions()

    def draw_objects(self):
        self.WINDOW.fill(WHITE_COLOR)
        self.draw_trashes()
        self.WINDOW.blit(self.truck.asset, (self.truck.object.x, self.truck.object.y))
        pygame.display.update()

    def draw_trashes(self):
        for trash in self.trashes_list:
            self.WINDOW.blit(trash.asset, (trash.object.x, trash.object.y))

    def handle_keyboard(self):
        if self.keys_pressed[pygame.K_w]:
            self.truck.move_up()
        if self.keys_pressed[pygame.K_s]:
            self.truck.move_down()
        if self.keys_pressed[pygame.K_d]:
            self.truck.move_right()
        if self.keys_pressed[pygame.K_a]:
            self.truck.move_left()

    def generate_trashes(self, count):
        for i in range(count):
            trash = Trash()
            self.WINDOW.blit(trash.asset, (trash.object.x, trash.object.y))
            self.trashes_list.append(trash)

    def add_trashes(self):
        time.sleep(1)
        trash = Trash()
        self.WINDOW.blit(trash.asset, (trash.object.x, trash.object.y))
        self.trashes_list.append(trash)

    def handle_collisions(self):
        for trash in self.trashes_list:
            if self.truck.object.colliderect(trash.object):
                self.trashes_collected.append(trash)
                self.trashes_list.remove(trash)
                timer = threading.Thread(target=self.add_trashes)
                timer.daemon = True
                timer.start()


environment = Environment()
