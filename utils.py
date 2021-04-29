import time
import pygame
import CONSTANTS


def get_current_time_millis():
    return int(round(time.time() * 1000))


def get_image_path(image_name):
    return "ressources/images/" + image_name


def get_tile_value(tiles, world_x, world_y):
    try:
        return tiles[get_tile_y(world_y)][get_tile_x(world_x)]
    except IndexError:
        return None


def get_tile_x(world_x):
    return int(world_x // CONSTANTS.CONST_BLOCK_SIZE)


def get_tile_y(world_y):
    return int(world_y // CONSTANTS.CONST_BLOCK_SIZE)


def restart(has_win):
    if pygame.key.get_pressed()[pygame.K_r]:
        if has_win is True:
            return False
        else:
            return True
