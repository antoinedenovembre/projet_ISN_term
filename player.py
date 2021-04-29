import pygame

import CONSTANTS
import utils


class Player:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

        self.img = pygame.image.load(utils.get_image_path("square.png")).convert_alpha()
        self.transformed_image = None

        self.velocity_x = 0
        self.velocity_y = 0

        self.can_move = False
        self.is_on_ground = False
        self.is_dead = False
        self.has_win = False

        self.speed_multiplier = 0

    def render(self, screen, camera):
        self.compute_transformed_image()

        screen.blit(self.transformed_image, (camera.get_render_x(self.x), camera.get_render_y(self.y)))

    def update(self, time_diff, camera, tiles):
        camera.set_x(self.x + 275)

        if not self.can_move:
            return

        self.speed_multiplier = time_diff / 10

        """ Collision sur l'axe X """

        self.velocity_x = CONSTANTS.CONST_SPEED

        while utils.get_tile_value(tiles, self.x + CONSTANTS.CONST_PLAYER_SIZE + self.velocity_x * self.speed_multiplier, self.y) == 1 or utils.get_tile_value(tiles, self.x + CONSTANTS.CONST_PLAYER_SIZE + self.velocity_x * self.speed_multiplier, self.y + CONSTANTS.CONST_PLAYER_SIZE - 1) == 1:
            self.velocity_x -= 0.1
            if 0.1 > self.velocity_x > 0:
                self.velocity_x = 0
                self.kill()  # collision droite block

        while utils.get_tile_value(tiles, self.x + CONSTANTS.CONST_PLAYER_SIZE - (CONSTANTS.CONST_BLOCK_SIZE - CONSTANTS.CONST_SPIKE_SIZE ) / 2 + self.velocity_x * self.speed_multiplier, self.y + CONSTANTS.CONST_PLAYER_SIZE - 1) == 2:
            self.velocity_x -= 0.1
            if 0.1 > self.velocity_x > 0:
                self.velocity_x = 0
                self.kill()
                # collision droite pour les piques

        while utils.get_tile_value(tiles, self.x + CONSTANTS.CONST_PLAYER_SIZE + self.velocity_x * self.speed_multiplier, self.y) is None:
            self.velocity_x -= 0.1
            if 0.1 > self.velocity_x > 0:
                self.velocity_x = 0
                self.has_win = True

        self.x += self.velocity_x * self.speed_multiplier  # avancer

        """ Fin collision de l'axe X """

        """ Collision sur l'axe Y / Détection de si le joueur est sur le sol / Activation du saut"""

        self.velocity_y += CONSTANTS.CONST_GRAVITY

        """ Collision avec le block en dessous """

        while utils.get_tile_value(tiles, self.x, self.y + CONSTANTS.CONST_PLAYER_SIZE + self.velocity_y * self.speed_multiplier) == 1 or utils.get_tile_value(tiles, self.x + CONSTANTS.CONST_PLAYER_SIZE, self.y + CONSTANTS.CONST_PLAYER_SIZE + self.velocity_y * self.speed_multiplier) == 1:
            self.velocity_y -= 0.1
            if 0.1 > self.velocity_y > 0:
                self.velocity_y = 0
                self.is_on_ground = True # Si le joueur est en collision avec le block du dessous, cela veut dire qu'il est sur le sol
                break

        while utils.get_tile_value(tiles, self.x, self.y + CONSTANTS.CONST_PLAYER_SIZE - (CONSTANTS.CONST_BLOCK_SIZE - CONSTANTS.CONST_SPIKE_SIZE) + self.velocity_y * self.speed_multiplier) == 2:
            self.velocity_y -= 0.1
            if 0.1 > self.velocity_y > 0:
                self.velocity_y = 0
                self.kill()  # collision bas pour les piques

        """ Collision avec le block du haut """

        while utils.get_tile_value(tiles, self.x, self.y + self.velocity_y * self.speed_multiplier) == 1 or utils.get_tile_value(tiles, self.x + CONSTANTS.CONST_PLAYER_SIZE, self.y + self.velocity_y * self.speed_multiplier) == 1:
            self.velocity_y += 0.1
            if 0 > self.velocity_y > -0.1:
                self.velocity_y = 0  # collision haut block

        if self.velocity_y != 0:
            self.is_on_ground = False

        if self.is_on_ground and pygame.key.get_pressed()[pygame.K_SPACE]:
            self.velocity_y = CONSTANTS.CONST_JUMP_FORCE  # saut

        self.y += self.velocity_y * self.speed_multiplier

        """ Fin collision de l'axe Y """

    def kill(self):
        self.can_move = False
        self.is_dead = True
        self.velocity_y = 0
        self.velocity_x = 0

    def compute_transformed_image(self):
        self.transformed_image = pygame.transform.scale(self.img, (CONSTANTS.CONST_PLAYER_SIZE, CONSTANTS.CONST_PLAYER_SIZE))

    def get_x(self):
        return self.x

    def set_x(self, new_x):
        self.x = new_x

    def get_y(self):
        return self.y

    def set_y(self, new_y):
        self.y = new_y

    def get_velocity_y(self):
        return self.velocity_y

    def set_velocity_y(self, new_velocity_y):
        self.velocity_y = new_velocity_y

    def canMove(self):
        return self.can_move

    def set_can_move(self, new_can_move_value):
        self.can_move = new_can_move_value

    def isOnGround(self):
        return self.is_on_ground

    def set_dead(self, new_dead_value):
        self.is_dead = new_dead_value

    def isDead(self):
        return self.is_dead
