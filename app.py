import pygame

import CONSTANTS
import utils
from level import Level

current_level = None


def main():
    global current_level

    pygame.init()
    screen = pygame.display.set_mode((CONSTANTS.CONST_WINDOW_WIDTH, CONSTANTS.CONST_WINDOW_HEIGHT))
    pygame.display.set_caption("UNTITLED CUBE GAME")

    bg = pygame.image.load(utils.get_image_path("background.jpg")).convert()
    bg = pygame.transform.scale(bg, (CONSTANTS.CONST_WINDOW_WIDTH, CONSTANTS.CONST_WINDOW_HEIGHT))

    current_level = Level(1)
    current_level.load_tiles()

    last_update_date = utils.get_current_time_millis()

    run = True
    while run:
        time_diff = utils.get_current_time_millis() - last_update_date
        if time_diff >= 1000 / 30:
            last_update_date = utils.get_current_time_millis()

            current_level.update(time_diff)

            screen.blit(bg, (0, 0))
            current_level.render(screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


if __name__ == "__main__":
    main()
