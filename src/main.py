import os
import os
import random

import pygame

FPS = 2

DEFAULT_ASSET_SIZE = 64
DEFAULT_MAP_SIZE = 16

WINDOW_HEIGHT = DEFAULT_ASSET_SIZE * DEFAULT_MAP_SIZE
WINDOW_WIDTH = DEFAULT_ASSET_SIZE * DEFAULT_MAP_SIZE
PADDING = 64

TRASHES_COUNT = 4

WHITE_COLOR = (255, 255, 255)

TRASH_BOTTLE = "TRASH_BOTTLE"
TRASH_CAN = "TRASH_CAN"

FREE_SPACE = 0
OBSTACLE = 1

D_RIGHT = "D_RIGHT"
D_LEFT = "D_LEFT"
D_UP = "D_UP"
D_DOWN = "D_DOWN"

R_RIGHT = "R_RIGHT"
R_LEFT = "R_LEFT"
R_UP = "R_UP"
R_DOWN = "R_DOWN"

NAVIAGTION_EVENT = pygame.USEREVENT + 1


class Space:
    def __init__(self, x, y):
        self.abstractX = x
        self.abstractY = y
        self.object = pygame.Rect(self.abstractX * DEFAULT_ASSET_SIZE, self.abstractY * DEFAULT_ASSET_SIZE,
                                  DEFAULT_ASSET_SIZE, DEFAULT_ASSET_SIZE)
        self.asset = pygame.Surface((64, 64))
        self.asset.fill((21, 30, 40))


class Obs:
    def __init__(self, x, y):
        self.abstractX = x
        self.abstractY = y
        self.object = pygame.Rect(self.abstractX * DEFAULT_ASSET_SIZE, self.abstractY * DEFAULT_ASSET_SIZE,
                                  DEFAULT_ASSET_SIZE, DEFAULT_ASSET_SIZE)
        self.asset = pygame.Surface((64, 64))
        self.asset.fill((171, 48, 74))


class Trash:
    def __init__(self, x, y):
        self.abstractX = x
        self.abstractY = y
        self.generate_random_trash(x, y)

    def generate_random_trash(self, x, y):
        random_index = random.randint(1, 2)

        if random_index == 1:
            self.type = TRASH_BOTTLE
            asset_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'trashes', 'plastic-bottle.png')
        else:
            self.type = TRASH_CAN
            asset_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'trashes', 'can.png')

        self.asset = pygame.transform.scale(pygame.image.load(asset_path), (DEFAULT_ASSET_SIZE, DEFAULT_ASSET_SIZE))
        self.object = pygame.Rect(self.abstractX * DEFAULT_ASSET_SIZE, self.abstractY * DEFAULT_ASSET_SIZE,
                                  DEFAULT_ASSET_SIZE, DEFAULT_ASSET_SIZE)


class Truck:
    def __init__(self, x=0, y=0):
        self.abstractX = x
        self.abstractY = y
        self.direction = D_RIGHT
        asset_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'garbage-truck.png')
        self.backAsset = pygame.transform.scale(pygame.image.load(asset_path), (DEFAULT_ASSET_SIZE, DEFAULT_ASSET_SIZE))
        self.asset = pygame.transform.scale(pygame.image.load(asset_path), (DEFAULT_ASSET_SIZE, DEFAULT_ASSET_SIZE))
        self.object = pygame.Rect(self.abstractX * DEFAULT_ASSET_SIZE, self.abstractY * DEFAULT_ASSET_SIZE,
                                  DEFAULT_ASSET_SIZE, DEFAULT_ASSET_SIZE)
        self.velocity = DEFAULT_ASSET_SIZE

    def rotate_up(self):
        self.asset = self.backAsset
        self.asset = pygame.transform.rotate(self.asset, 90)
        self.direction = D_UP

    def rotate_down(self):
        self.asset = self.backAsset
        self.asset = pygame.transform.rotate(self.asset, -90)
        self.direction = D_DOWN

    def rotate_right(self):
        self.asset = self.backAsset
        self.direction = D_RIGHT

    def rotate_left(self):
        self.asset = self.backAsset
        self.asset = pygame.transform.rotate(self.asset, 180)
        self.asset = pygame.transform.flip(self.asset, False, True)
        self.direction = D_LEFT

    def move(self, map):
        if self.direction == D_UP:
            self.move_up(map)
        if self.direction == D_DOWN:
            self.move_down(map)
        if self.direction == D_RIGHT:
            self.move_right(map)
        if self.direction == D_LEFT:
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


class EnvMap:
    def __init__(self):
        self.map = self.generate_map()

    def generate_map_field(self, x, y):
        random_index = random.randint(0, 100)
        if random_index == -1:
            return Trash(x, y)
        elif random_index < 80:
            return Space(x, y)
        else:
            return Obs(x, y)

    def generate_map(self):
        temp_map = []
        for x in range(DEFAULT_MAP_SIZE):
            temp_map.append([self.generate_map_field(x, y) for y in range(16)])

        temp_map[12][14] = Trash(12, 14)
        return temp_map


class Node():
    def __init__(self, state):
        self.state = state
        self.parent = None
        self.action = None


class Environment:
    def __init__(self):
        self.truck = Truck()
        self.envMap = EnvMap()
        self.envMap.map[0][0] = self.truck
        self.run = True
        self.clock = pygame.time.Clock()
        self.WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.trashes_list = []
        self.trashes_collected = []

        while self.run:
            self.update()

    def update(self):
        self.clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                self.handle_keyboard(event.key)

        self.draw_objects()

    def draw_objects(self):
        self.WINDOW.fill(WHITE_COLOR)
        self.draw_map()
        pygame.display.update()

    def draw_map(self):
        for x in range(DEFAULT_MAP_SIZE):
            for y in range(DEFAULT_MAP_SIZE):
                obj = self.envMap.map[x][y]
                self.WINDOW.blit(obj.asset, (obj.object.x, obj.object.y))

    def handle_keyboard(self, key):
        if key == pygame.K_SPACE:
            self.truck.move(self.envMap.map)
        if key == pygame.K_w:
            self.truck.rotate_up()
        if key == pygame.K_s:
            self.truck.rotate_down()
        if key == pygame.K_d:
            self.truck.rotate_right()
        if key == pygame.K_a:
            self.truck.rotate_left()
        if key == pygame.K_o:
            cpy = self.get_map_copy(self.envMap.map)
            actions = self.graphsearch([], [], cpy, self.succ, self.goal_test)
            self.navigate(actions)


    def get_map_copy(self, map):
        newMap = []
        for x in range(DEFAULT_MAP_SIZE):
            newMap.append([None for y in range(16)])
        for x in range(DEFAULT_MAP_SIZE):
            for y in range(DEFAULT_MAP_SIZE):
                o = map[x][y]
                no = None
                if o.__class__.__name__ == 'Truck':
                    no = Truck(x, y)

                if o.__class__.__name__ == 'Trash':
                    no = Trash(x, y)

                if o.__class__.__name__ == 'Obs':
                    no = Obs(x, y)

                if o.__class__.__name__ == 'Space':
                    no = Space(x, y)

                newMap[x][y] = no

        return newMap

    def goal_test(self, state):
        for x in range(DEFAULT_MAP_SIZE):
            for y in range(DEFAULT_MAP_SIZE):
                if isinstance(state[x][y], Trash):
                    return False
        return True

    def succ(self, state):
        pack = []
        truck = None
        for x in range(DEFAULT_MAP_SIZE):
            for y in range(DEFAULT_MAP_SIZE):
                if isinstance(state[x][y], Truck):
                    truck = state[x][y]

        print("x: {} y: {}".format(truck.abstractX, truck.abstractY))

        altState1 = self.get_map_copy(state)
        t1 = altState1[truck.abstractX][truck.abstractY]
        t1.rotate_up()
        t1.move(altState1)

        altState2 = self.get_map_copy(state)
        t2 = altState2[truck.abstractX][truck.abstractY]
        t2.rotate_down()
        t2.move(altState2)

        altState3 = self.get_map_copy(state)
        t3 = altState3[truck.abstractX][truck.abstractY]
        t3.rotate_right()
        t3.move(altState3)

        altState4 = self.get_map_copy(state)
        t4 = altState4[truck.abstractX][truck.abstractY]
        t4.rotate_left()
        t4.move(altState4)

        pack.append([R_UP, altState1])
        pack.append([R_DOWN, altState2])
        pack.append([R_RIGHT, altState3])
        pack.append([R_LEFT, altState4])

        return pack

    def are_states_the_same(self, s1, s2):
        for x in range(DEFAULT_MAP_SIZE):
            for y in range(DEFAULT_MAP_SIZE):
                a = s1[x][y]
                b = s2[x][y]
                if a.__class__.__name__ != b.__class__.__name__:
                    return False
        return True

    def is_state_belongs(self, fringe, explored, state):
        for elem in fringe:
            if self.are_states_the_same(elem.state, state):
                return True
        for elem in explored:
            if self.are_states_the_same(elem.state, state):
                return True
        return False

    def navigate(self, actions):
        print('actions:')
        print(actions)
        next = pygame.time.get_ticks() + 300
        while len(actions) > 0:
            if next <= pygame.time.get_ticks():
                action = actions.pop()
                next = pygame.time.get_ticks() + 300
                self.update()
                if action == R_UP:
                    ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_w})
                if action == R_DOWN:
                    ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_s})

                if action == R_RIGHT:
                    ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_d})

                if action == R_LEFT:
                    ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a})

                pygame.event.post(ev)

                ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
                pygame.event.post(ev)

    def graphsearch(self, fringe, explored, istate, succ, goaltest):
        fringe.append(Node(istate))

        while True:
            if len(fringe) == 0:
                return False

            elem = fringe.pop()

            if goaltest(elem.state):
                actions_pack = []
                while (elem.parent):
                    print(elem.action)
                    actions_pack.append(elem.action)
                    elem = elem.parent

                return actions_pack

            explored.append(elem)

            for [action, state] in succ(elem.state):
                if not self.is_state_belongs(fringe, explored, state):
                    x = Node(state)
                    x.parent = elem
                    x.action = action
                    fringe.append(x)


environment = Environment()
