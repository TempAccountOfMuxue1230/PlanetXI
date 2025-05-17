"""
Project: X1
Version: 1.0.2
Author: MUXUE1230

File: main.py
File Version: 1.3
"""
import pyautogui
import config
import pygame
import sys

from pygame.locals import *

from helper.translator import Translator
from sense.sense_manager import SenseManager
from sense.senses import *
from sense.gui import *

pygame.init()

config = config.Config()
screen = pygame.display.set_mode(pyautogui.size(), DOUBLEBUF | HWSURFACE | NOFRAME, 32, 0, 1)
pygame.display.set_caption("PlanetXI")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))
font = pygame.font.SysFont("comicsans", 30)

screen.fill((0, 0, 0))
text = font.render("Loading...", True, (255, 255, 255))
screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2))
pygame.display.flip()

translator = Translator()
translator.use_lang('zh_cn')

sence_manager = SenseManager(translator)
sence_manager.add(TestSense, "assets/background.png", "assets/actor.png")
sence_manager.add(MainMenuSense)
sence_manager.selet("MainMenuSense")

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        sence_manager.get().event(event)

    sence_manager.get().update()

    sence_manager.get().draw(screen)

    screen.blit(font.render(f"FPS:{round(clock.get_fps())}", True, (255, 255, 255)), (10, 10))
    pygame.display.flip()
    clock.tick(120)
