"""
File: sense/sense.py
File Version: 1.3
"""
import pyautogui
from pygame.locals import *

from helper.image import *


class Sense:
    """
    A class of game sences
    """

    def __init__(self, manager):
        self.manager = manager

    @staticmethod
    def get_name():
        return "Sence"

    def update(self):
        pass

    def draw(self, screen):
        pass

    def event(self, event):
        pass


class LoadSense(Sense):
    """
    A class of game sense
    """

    def __init__(self, manager):
        Sense.__init__(self, manager)

        self.wasgame = resize_image_to_height("assets/wasgame.png", int(pyautogui.size()[0] * 0.2))
        self.wasgame_text = resize_image_to_height("assets/wasgame_text.png", int(pyautogui.size()[0] * 0.1))

        self.game_title = resize_image_to_height("assets/title.png", int(pyautogui.size()[0] * 0.2))
        self.game_title.set_alpha(0)

        self.animation = 0
        self.animation_p = 1
        self.animation_k = 0

    @staticmethod
    def get_name():
        return "LoadSense"

    def update(self):
        self.animation += 2 * self.animation_p

        if self.animation == 400:
            self.animation_p = -1
        elif self.animation == 0:
            if self.animation_k:
                pygame.mixer.music.load('assets/bg_music.mp3')
                pygame.mixer.music.play(-1)
                self.manager.get("MainMenuSense").open()
            self.animation_p = 1
            self.animation_k = 1

        if self.animation_k == 0:
            self.wasgame.set_alpha(self.animation)
            self.wasgame_text.set_alpha(self.animation)
        else:
            self.game_title.set_alpha(self.animation)

    def draw(self, screen):
        screen.fill((0, 0, 0))

        screen.blit(self.wasgame, (pyautogui.size()[0] * 0.5 - self.wasgame.get_size()[0] * 0.5
                                   - self.wasgame_text.get_size()[0] * 0.5,
                                   pyautogui.size()[1] * 0.5 - self.wasgame.get_size()[1] * 0.5))
        screen.blit(self.wasgame_text, (pyautogui.size()[0] * 0.5 - self.wasgame_text.get_size()[0] * 0.1,
                                        pyautogui.size()[1] * 0.5 - self.wasgame_text.get_size()[1] * 0.5))

        screen.blit(self.game_title, (pyautogui.size()[0] * 0.5 - self.game_title.get_size()[0] * 0.5,
                                      pyautogui.size()[1] * 0.5 - self.game_title.get_size()[1] * 0.5))

    def event(self, event):
        pass


class TestSense(Sense):
    """
    A class of game sense
    """

    def __init__(self, manager, bg_img_path, actor_img_path):
        super().__init__(manager)

        self.background_image = resize_image_to_height(bg_img_path, pyautogui.size().height).convert()
        self.actor = split_image_into_grid(actor_img_path, 5)

        self.x = 0
        self.t = 0
        self.actor_animation = [True, 0]

    @staticmethod
    def get_name():
        return "TestSence"

    def update(self):
        if pygame.key.get_pressed()[K_a]:
            self.x += 5
            self.t += 1
            self.actor_animation[0] = False
            if self.x >= self.background_image.get_width():
                self.x = 0
        elif pygame.key.get_pressed()[K_d]:
            self.x -= 5
            self.t += 1
            self.actor_animation[0] = True
            if self.x <= -self.background_image.get_width():
                self.x = 0
        else:
            self.t = 0
            self.actor_animation[1] = 0

        if self.t % 25 == 0:
            self.actor_animation[1] = (self.actor_animation[1] + 1) % 4

    def draw(self, screen):
        screen.blit(self.background_image, (self.x, 0))
        screen.blit(self.background_image, (self.background_image.get_width() + self.x, 0))
        screen.blit(self.background_image, (self.background_image.get_width() * 2 + self.x, 0))
        screen.blit(self.background_image, (-self.background_image.get_width() + self.x, 0))
        screen.blit(
            self.actor[1 + self.actor_animation[0]][self.actor_animation[1]],
            (
                self.background_image.get_width() // 2 - self.actor[1 + self.actor_animation[0]][
                    self.actor_animation[1]].get_width(),
                round(self.background_image.get_height() * 0.9) - self.actor[1 + self.actor_animation[0]][
                    self.actor_animation[1]].get_height()
            )
        )
