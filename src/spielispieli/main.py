import sys
from pathlib import Path
from typing import Dict, List, Optional
import logging
import time

import numpy as np
import pygame

from spielispieli.maths.vectors import Vec2
from spielispieli.utils import improved_sleep

log = logging.getLogger(__name__)



def SPIELISPIELI_LOOP():

    pygame.init()
    pygame.display.set_caption("DasRender keyboard input")
    icon = pygame.image.load(Path(__file__).parent / "resources/polyggle.png")
    pygame.display.set_icon(icon)

    size = (256, 256)
    screen = pygame.display.set_mode(size)
    background = pygame.image.load(Path(__file__).parent / "resources/polyggle.png")
    background.set_alpha(int(0.2*256))

    font_size = 20
    font = pygame.font.Font('freesansbold.ttf', font_size)
    dbg_font = pygame.font.Font('freesansbold.ttf', 10)
    font_instructions = pygame.font.Font('freesansbold.ttf', 9)

    _held_keys = []
    _held_inputs = {}
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

        inputs = {}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                _held_keys.append(key_name)
                _held_inputs[f"{key_name}_held"] = 1.0
            if event.type == pygame.KEYUP:
                key_name = pygame.key.name(event.key)
                _held_keys.remove(key_name)
                inputs[f"{key_name}_up"] = 1.0

                held_key_name = f"{key_name}_held"
                if held_key_name in _held_inputs:
                    del _held_inputs[held_key_name]

        delta = time_passed * velocity
        if "w" in _held_keys:
            player_pos.y += delta
        if "s" in _held_keys:
            player_pos.y -= delta
        if "d" in _held_keys:
            player_pos.x += delta
        if "a" in _held_keys:
            player_pos.x -= delta

        screen.fill((44, 44, 44))
        screen.blit(background, (64, 64))

        text = font.render(", ".join(_held_keys), True, (255, 255, 255))
        screen.blit(text, (5, 5))

        text = font.render("+", True, (255, 255, 255))
        aaaaarg = 2*np.pi * blink_velocity * time_since_start_of_program
        alpha = (np.sin(aaaaarg)*0.5+0.5) * 256
        text.set_alpha(int(alpha))
        screen.blit(text, ((player_pos.x), size[1] - font_size - int(player_pos.y)))

        text = dbg_font.render(f"{time_since_start_of_program:.2f}", True, (255, 255, 255))
        screen.blit(text, (size[0] - text.get_width()-5, 5))

        pygame.display.update()

        improved_sleep(1/FPS)


if __name__ == "__main__":
    SPIELISPIELI_LOOP()
