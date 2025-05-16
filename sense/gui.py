"""
File: sense/gui.py
File Version: 1.2
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

    def close(self):
        pass

    def open(self):
        pass

    def event(self, event):
        for component in self.components:
            component.event(event)


class MainMenuSense(GUISense):
    """
    A class of game sense that test gui sense
    """

    def __init__(self, manager):
        super().__init__(manager, "assets/background.png")

        # self.components.append(
        #     TextComponent(
        #         self.manager.translator.translate("gui.test_menu.title"),
        #         (100, 100), size=165))

        self.components.append(
            ImageComponent(
                "assets/title.png", (100, 100)))

        self.components.append(
            ButtonComponent(
                self.manager.translator.translate("gui.test_menu.button.continue"),
                (100, 500), (500, 100), self.exit_game, size=40, disabled=True))

        self.components.append(
            ButtonComponent(
                self.manager.translator.translate("gui.test_menu.button.new"),
                (100, 650), (500, 100), self.exit_game, size=40))

        self.components.append(
            ButtonComponent(
                self.manager.translator.translate("gui.test_menu.button.saves"),
                (100, 800), (500, 100), self.exit_game, size=40))

        self.components.append(
            ButtonComponent(
                self.manager.translator.translate("gui.test_menu.button.settings"),
                (100, 950), (500, 100), self.exit_game, size=40))

        self.components.append(
            ButtonComponent(
                self.manager.translator.translate("gui.test_menu.button.exit"),
                (100, 1100), (500, 100), self.exit_game, size=40))

    @staticmethod
    def get_name():
        return "MainMenuSense"

    @staticmethod
    def exit_game():
        pygame.quit()
        sys.exit()
