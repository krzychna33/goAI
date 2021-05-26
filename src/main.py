import random

import pygame

from config import *
from src.entitie.Obs import Obs
from src.entitie.Space import Space
from src.entitie.Trash import Trash
from src.entitie.Truck import Truck


class EnvMap:
    def generate_map_field(self, x, y):
        random_index = random.randint(0, 100)
        if random_index < 5:
            return Trash(x, y)
        elif random_index < 80:
            return Space(x, y)
        else:
            return Obs(x, y)

    def generate_map(self):
        temp_map = []
        for x in range(DEFAULT_MAP_SIZE):
            temp_map.append([self.generate_map_field(x, y) for y in range(16)])

        self.map = temp_map

    def import_map(self, map):
        self.map = map

    def set_truck(self):
        self.truck = Truck()
        self.map[0][0] = self.truck

    def get_map_copy(self):
        newMap = []
        newEnvMap = EnvMap()
        for x in range(DEFAULT_MAP_SIZE):
            newMap.append([None for y in range(16)])
        for x in range(DEFAULT_MAP_SIZE):
            for y in range(DEFAULT_MAP_SIZE):
                o = self.map[x][y]
                no = None
                if o.__class__.__name__ == 'Truck':
                    no = Truck(x, y)
                    no.direction = o.direction
                    newEnvMap.truck = no

                if o.__class__.__name__ == 'Trash':
                    no = Trash(x, y)

                if o.__class__.__name__ == 'Obs':
                    no = Obs(x, y)

                if o.__class__.__name__ == 'Space':
                    no = Space(x, y)

                newMap[x][y] = no

        newEnvMap.import_map(newMap)
        return newEnvMap


class Node():
    def __init__(self, state):
        self.state = state
        self.parent = None
        self.action = None


class PathFinder():
    def __init__(self, envMap):
        self.envMap = envMap

    def graphsearch(self, istate):
        fringe = []
        explored = []

        fringe.append(Node(istate))

        while True:
            if len(fringe) == 0:
                return False

            elem = fringe.pop()

            if self.goal_test(elem.state):
                actions_pack = []
                while (elem.parent):
                    print(elem.action)
                    actions_pack.append(elem.action)
                    elem = elem.parent

                return actions_pack

            explored.append(elem)

            for [action, state] in self.succ(elem.state):
                if not self.is_state_belongs(fringe, explored, state):
                    x = Node(state)
                    x.parent = elem
                    x.action = action
                    fringe.append(x)

    def goal_test(self, state):
        for x in range(DEFAULT_MAP_SIZE):
            for y in range(DEFAULT_MAP_SIZE):
                if isinstance(state.map[x][y], Trash):
                    return False
        return True

    def succ(self, state):
        pack = []
        truck = state.truck

        altState1 = state.get_map_copy()
        t1 = altState1.map[truck.abstractX][truck.abstractY]
        t1.rotate_up()
        t1.move(altState1.map)

        altState2 = state.get_map_copy()
        t2 = altState2.map[truck.abstractX][truck.abstractY]
        t2.rotate_down()
        t2.move(altState2.map)

        altState3 = state.get_map_copy()
        t3 = altState3.map[truck.abstractX][truck.abstractY]
        t3.move(altState3.map)

        pack.append([R_UP, altState1])
        pack.append([R_DOWN, altState2])
        pack.append([NOTHING, altState3])

        return pack

    def are_states_the_same(self, s1, s2):
        for x in range(DEFAULT_MAP_SIZE):
            for y in range(DEFAULT_MAP_SIZE):
                a = s1.map[x][y]
                b = s2.map[x][y]
                if a.__class__.__name__ == 'Truck' and b.__class__.__name__ == 'Truck':
                    if a.direction != b.direction:
                        return False
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


class Environment:
    def __init__(self):
        self.envMap = EnvMap()
        self.envMap.generate_map()
        self.envMap.set_truck()
        self.run = True
        self.clock = pygame.time.Clock()
        self.WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.trashes_list = []
        self.trashes_collected = []
        self.pathFinder = PathFinder(self.envMap)

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
            self.envMap.truck.move(self.envMap.map)
        if key == pygame.K_w:
            self.envMap.truck.rotate_up()
        if key == pygame.K_s:
            self.envMap.truck.rotate_down()
        if key == pygame.K_o:
            actions = self.pathFinder.graphsearch(self.envMap.get_map_copy())
            self.navigate(actions)

    def navigate(self, actions):
        next = pygame.time.get_ticks() + 300
        while len(actions) > 0:
            if next <= pygame.time.get_ticks():
                action = actions.pop()
                next = pygame.time.get_ticks() + 300
                self.update()
                ev=None
                if action == R_UP:
                    ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_w})
                if action == R_DOWN:
                    ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_s})

                if ev:
                    pygame.event.post(ev)

                ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
                pygame.event.post(ev)


environment = Environment()
