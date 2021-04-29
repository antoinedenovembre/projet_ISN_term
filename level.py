import pygame
import utils
import CONSTANTS
from camera import Camera
from player import Player


class Level:

    def __init__(self, id):
        self.tiles = []
        self.id = id

        self.spike = pygame.transform.scale(pygame.image.load(utils.get_image_path("spike.png")).convert_alpha(), (CONSTANTS.CONST_SPIKE_SIZE, CONSTANTS.CONST_SPIKE_SIZE))
        self.ground = pygame.image.load(utils.get_image_path("ground.png")).convert_alpha()
        self.gradient = pygame.image.load(utils.get_image_path("gradient.png")).convert_alpha()
        self.timer_three = pygame.image.load(utils.get_image_path("3.png")).convert_alpha()
        self.timer_two = pygame.image.load(utils.get_image_path("2.png")).convert_alpha()
        self.timer_one = pygame.image.load(utils.get_image_path("1.png")).convert_alpha()
        self.timer_go = pygame.image.load(utils.get_image_path("go.png")).convert_alpha()
        self.win = pygame.image.load(utils.get_image_path("win.png")).convert_alpha()

        self.spawn_x = 0
        self.spawn_y = 0

        self.player = Player()
        self.camera = Camera(camera_y=CONSTANTS.CONST_WINDOW_HEIGHT / 2)

        self.start_date = utils.get_current_time_millis()

    def render(self, screen):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if self.tiles[y][x] == 1:
                    screen.blit(self.ground, (self.camera.get_render_x(x * CONSTANTS.CONST_BLOCK_SIZE), self.camera.get_render_y(y * CONSTANTS.CONST_BLOCK_SIZE)))
                if self.tiles[y][x] == 2:
                    screen.blit(self.spike, (self.camera.get_render_x(x * CONSTANTS.CONST_BLOCK_SIZE + (CONSTANTS.CONST_BLOCK_SIZE - CONSTANTS.CONST_SPIKE_SIZE) / 2), self.camera.get_render_y(y * CONSTANTS.CONST_BLOCK_SIZE + CONSTANTS.CONST_BLOCK_SIZE - CONSTANTS.CONST_SPIKE_SIZE)))

        self.player.render(screen, self.camera)

        screen.blit(self.gradient, (0, 0))

        elapsed_time = utils.get_current_time_millis() - self.start_date
        if elapsed_time > 200:
            if elapsed_time > 400:
                if elapsed_time > 600:
                    if elapsed_time > 800:
                        pass
                    else:
                        screen.blit(self.timer_go, (0, 0))
                        self.player.set_can_move(True)
                else:
                    screen.blit(self.timer_one, (0, 0))
            else:
                screen.blit(self.timer_two, (0, 0))
        else:
            screen.blit(self.timer_three, (0, 0))

        if self.player.has_win:
            screen.blit(self.win, (0, 0))

    def update(self, time_diff):
        self.player.update(time_diff, self.camera, self.tiles)

        if self.player.get_y() + CONSTANTS.CONST_PLAYER_SIZE > CONSTANTS.CONST_WINDOW_HEIGHT or utils.restart(self.player.has_win):
            self.player.kill()
            self.player.has_win = False

        if self.player.isDead():
            self.player.set_x(self.spawn_x)
            self.player.set_y(self.spawn_y)
            self.player.set_dead(False)
            self.start_date = utils.get_current_time_millis()

    def load_tiles(self):
        file = open("ressources/levels/level" + str(self.id) + ".lvl", "r")
        for line in file:
            x_tiles = []
            for char in line:
                if char == "3":
                    self.spawn_x = CONSTANTS.CONST_BLOCK_SIZE * len(x_tiles)
                    self.spawn_y = CONSTANTS.CONST_BLOCK_SIZE * len(self.tiles) + CONSTANTS.CONST_BLOCK_SIZE - CONSTANTS.CONST_PLAYER_SIZE
                    self.player.set_x(self.spawn_x)
                    self.player.set_y(self.spawn_y)
                if char != "\n":
                    x_tiles.append(int(char))
            self.tiles.append(x_tiles)

    def get_tiles(self):
        return self.tiles

    def get_id(self):
        return self.id
