"""
File: sense/sense.py
File Version: 1.5
"""
import threading
import time

import pyautogui
import requests
from bs4 import BeautifulSoup
from pygame.locals import *

from helper.image import *
from helper.utils import Version
from sense.gui_componts import ProgressBarComponent


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

    def async_handler(self):
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
                self.manager.select("GetReadySense")
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


class GetReadySense(Sense):
    """
    A class of game sense
    """

    def __init__(self, manager):
        Sense.__init__(self, manager)

        self.background = resize_image_to_height("assets/background.png", pyautogui.size()[1])

        self.black_front = pygame.Surface(pyautogui.size()).convert_alpha()
        self.black_front.fill((0, 0, 0))
        self.black_front.set_alpha(255)

        self.is_fade_in = True
        self.fade_in = 255

        self.front_screen = pygame.Surface(pyautogui.size()).convert_alpha()
        self.front_screen.fill((0, 0, 0, 0))
        self.prograss = ProgressBarComponent((pyautogui.size()[0] * 0.02, pyautogui.size()[1] * 0.9),
                                             (pyautogui.size()[0] * 0.96, 10),
                                             10, (100, 100, 255), (120, 120, 120),
                                             title="Checking Update...", title_pos='nw', title_bold=True,
                                             title_size=24)

        threading.Thread(target=self.async_handler).start()

    def event(self, event):
        super().event(event)

    @staticmethod
    def get_name():
        return "GetReadySense"

    def update(self):
        super().update()

        if self.fade_in <= 0:
            self.is_fade_in = False
        if self.is_fade_in:
            self.fade_in -= 6
            self.black_front.set_alpha(self.fade_in)

    def draw(self, screen):
        super().draw(screen)

        screen.blit(self.background, (0, 0))
        screen.blit(self.front_screen, (0, 0))

        if self.is_fade_in:
            screen.blit(self.black_front, (0, 0))

    def get_latest_release_name(self):
        url = 'https://github.com/TempAccountOfMuxue1230/PlanetXI/releases'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://github.com/ ",
            "DNT": "1",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找所有 h2 标签，提取以 "X1 V" 开头的版本标题
        for h2 in soup.find_all('h2'):
            title = h2.get_text(strip=True)
            if title.startswith('X1 V'):
                return title

        return None

    def async_handler(self):
        while self.is_fade_in:
            time.sleep(0.5)

        self.prograss.draw(self.front_screen)

        latest_version = Version(self.get_latest_release_name())
        version = Version("X1 V1.0.6 Alpha")

        if latest_version > version:
            pass
        else:
            self.prograss.set_progress(100)
            self.prograss.draw(self.front_screen)
            time.sleep(0.1)
            self.front_screen.fill((0, 0, 0, 0))
            time.sleep(0.5)
            self.manager.select("MainMenuSense")
