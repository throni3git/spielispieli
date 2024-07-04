from pathlib import Path
import logging
import time

import numpy as np
import pygame

from spielispieli.maths.vectors import Vec2
from spielispieli.utils import improved_sleep

log = logging.getLogger(__name__)


def init_game() -> None:
    pygame.init()
    pygame.display.set_caption("DasRender keyboard input")
    icon = pygame.image.load(Path(__file__).parent / "resources/polyggle.png")
    pygame.display.set_icon(icon)

def init_screen(size: tuple[int, int]) -> tuple[pygame.Surface, pygame.Surface]:

    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    background = pygame.image.load(Path(__file__).parent / "resources/polyggle.png")
    background.set_alpha(int(0.2*256))
    return screen, background

def run_loop(surface_screen: pygame.Surface, 
                assets: dict[str, pygame.Surface], 
                fonts: dict[str, pygame.font.Font]) -> None:

    held_keys = []
    held_inputs = {}
    player_pos = Vec2(0, 0)
    velocity = 100
    FPS = 60
    blink_velocity = 2
    old = time.time_ns()
    time_since_start_of_program = 0
    running = True
    while running:

        now = time.time_ns()
        time_passed = (now - old) / 1e9
        old = now
        time_since_start_of_program += time_passed

        size_screen = surface_screen.get_size()
        
        surface_screen.fill((44, 44, 44))

        inputs = {}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                # surface_screen.blit(pygame.transform.scale(assets["background"], event.dict["size"]), (0,0))
                # pygame.display.update()
                pass
            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                held_keys.append(key_name)
                held_inputs[f"{key_name}_held"] = 1.0
            if event.type == pygame.KEYUP:
                key_name = pygame.key.name(event.key)
                held_keys.remove(key_name)
                inputs[f"{key_name}_up"] = 1.0

                held_key_name = f"{key_name}_held"
                if held_key_name in held_inputs:
                    del held_inputs[held_key_name]

        delta = time_passed * velocity
        if "w" in held_keys:
            player_pos.y += delta
        if "s" in held_keys:
            player_pos.y -= delta
        if "d" in held_keys:
            player_pos.x += delta
        if "a" in held_keys:
            player_pos.x -= delta

        pos_background = (
            size_screen[0]//2-assets["background"].get_size()[0]//2,
            size_screen[1]//2-assets["background"].get_size()[1]//2
        )
        surface_screen.blit(assets["background"], pos_background)

        text = fonts["big"].render(", ".join(held_keys), True, (255, 255, 255))
        surface_screen.blit(text, (5, 5))

        text = fonts["big"].render("+", True, (255, 255, 255))
        aaaaarg = 2*np.pi * blink_velocity * time_since_start_of_program
        alpha = (np.sin(aaaaarg)*0.5+0.5) * 256
        text.set_alpha(int(alpha))
        pos = (player_pos.x+3, surface_screen.get_size()[1] - fonts["big"].get_linesize() - int(player_pos.y))
        surface_screen.blit(text, pos)

        text = fonts["default"].render(f"{time_since_start_of_program:.2f}", True, (255, 255, 255))
        surface_screen.blit(text, (surface_screen.get_size()[0] - text.get_width()-5, 5))

        pygame.display.update()

        improved_sleep(1/FPS)

def main():
    init_game()

    screen_size = (256, 256)
    surface_screen, surface_background = init_screen(screen_size)
    
    assets = {
        "background": surface_background,
    }
    fonts= {
        "big" : pygame.font.Font('freesansbold.ttf', 20),
        "default" : pygame.font.Font('freesansbold.ttf', 10)
    }

    run_loop(surface_screen, assets, fonts)



if __name__ == "__main__":
    main()
