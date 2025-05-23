"""
Project: X1
Version: 1.0.7
Author: MUXUE1230

File: main.py
File Version: 1.7
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
pygame.mixer.init()

config = config.Config()
screen = pygame.display.set_mode(pyautogui.size(), DOUBLEBUF | FULLSCREEN | HWSURFACE, 32, 0, 1)
pygame.display.set_caption("PlanetXI")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))
font = pygame.font.SysFont("comicsans", 30)

translator = Translator()
translator.use_lang('zh_cn')

sense_manager = SenseManager(translator)
sense_manager.add(LoadSense)
sense_manager.add(GetReadySense)
sense_manager.add(MainMenuSense)
sense_manager.select("LoadSense")

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        sense_manager.get().event(event)
        if sense_manager.osg_is_opened():
            sense_manager.get_osg().event(event)

    sense_manager.get().update()
    if sense_manager.osg_is_opened():
        sense_manager.get_osg().update()

    sense_manager.get().draw(screen)
    if sense_manager.osg_is_opened():
        sense_manager.get_osg().draw(screen)

    screen.blit(font.render(f"FPS:{round(clock.get_fps())}", True, (255, 255, 255)), (10, 10))
    pygame.display.flip()
    clock.tick(60)
