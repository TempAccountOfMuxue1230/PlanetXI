"""
File: sense/gui.py
File Version: 1.3
"""
import sys

import pyautogui
import pygame

from helper.image import resize_image_to_height
from .gui_componts import ButtonComponent, TextComponent, ImageComponent
from .senses import Sense


class GUISense(Sense):
    """
    A class to handle GUI interactions
    """

    def __init__(self, manager, bg_img_path, bg_uv=(0, 0)):
        super().__init__(manager)
        self.background_image = resize_image_to_height(bg_img_path, pyautogui.size().height).convert()
        self.background_uv = bg_uv

        self.components = []
        self.next_sense = None

    @staticmethod
    def get_name():
        return "GUISence"

    def update(self):
        for component in self.components:
            component.update()

    def draw(self, screen):
        screen.blit(self.background_image, self.background_uv)
        for component in self.components:
            component.draw(screen)

    def close(self, next_sense):
        self.next_sense = next_sense

    def open(self):
        self.manager.selet(self.get_name())

    def event(self, event):
        for component in self.components:
            component.event(event)


class MainMenuSense(GUISense):
    """
    A class of game sense that test gui sense
    """

    def __init__(self, manager):
        super().__init__(manager, "assets/background.png")

        self.components.append(
            ImageComponent(
                "assets/title.png",
                (pyautogui.size()[0] * 0.05, pyautogui.size()[1] * 0.05),
                (int(600*1.2), int(281*1.2))))

        self.components.append(
            ButtonComponent(
                self.manager.translator.translate("gui.test_menu.button.continue"),
                (pyautogui.size()[0] * 0.1, pyautogui.size()[1] * 0.30),
                (500, 100), self.exit_game, size=40, disabled=True))

        self.components.append(
            ButtonComponent(
                self.manager.translator.translate("gui.test_menu.button.new"),
                (pyautogui.size()[0] * 0.1, pyautogui.size()[1] * 0.40),
                (500, 100), self.exit_game, size=40))

        self.components.append(
            ButtonComponent(
                self.manager.translator.translate("gui.test_menu.button.saves"),
                (pyautogui.size()[0] * 0.1, pyautogui.size()[1] * 0.50),
                (500, 100), self.exit_game, size=40))

        self.components.append(
            ButtonComponent(
                self.manager.translator.translate("gui.test_menu.button.settings"),
                (pyautogui.size()[0] * 0.1, pyautogui.size()[1] * 0.60),
                (500, 100), self.exit_game, size=40))

        self.components.append(
            ButtonComponent(
                self.manager.translator.translate("gui.test_menu.button.exit"),
                (pyautogui.size()[0] * 0.1, pyautogui.size()[1] * 0.70),
                (500, 100), self.exit_game, size=40))

        self.black_front = pygame.Surface(pyautogui.size()).convert_alpha()
        self.black_front.fill((0, 0, 0))
        self.black_front.set_alpha(255)

        self.is_fade_in = False
        self.is_fade_out = False
        self.fade_in = 255
        self.fade_out = 0

    @staticmethod
    def get_name():
        return "MainMenuSense"

    @staticmethod
    def exit_game():
        pygame.quit()
        sys.exit()

    def update(self):
        if self.fade_in <= 0:
            self.is_fade_in = False
        if self.is_fade_in:
            self.fade_in -= 6
            self.black_front.set_alpha(self.fade_in)
        if not self.is_fade_in or not self.is_fade_out:
            super().update()

    def close(self, next_sense):
        super().close(next_sense)
        self.is_fade_in = False
        self.is_fade_out = True

    def open(self):
        super().open()
        self.is_fade_in = True
        self.is_fade_out = False

    def draw(self, screen):
        super().draw(screen)

        if self.is_fade_in or self.is_fade_out:
            screen.blit(self.black_front, (0, 0))
