"""
File: sense/gui_components.py
File Version: 1.2
"""
import cv2
import numpy as np
import pygame
from pygame.locals import *
from PIL import Image, ImageSequence

from helper.image import resize_image_to_size, resize_surface_to_size


class Component:
    """
    A class that represents a component in the sense
    """

    def __init__(self, image, position):
        self.image = image
        self.position = position

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def event(self, event):
        pass


class TextComponent(Component):
    """
    A class that represents a text component in the sense
    """

    def __init__(self, text, position, font='SimSun', size=20, bold=False, italic=False):
        self.font = pygame.font.SysFont(font, size, bold, italic)
        self.text = text
        self.color = (255, 255, 255)

        self.text_surface = self.font.render(self.text, True, self.color)

        super().__init__(self.text_surface, position)

    def set_text(self, new_text):
        self.text = new_text
        self.text_surface = self.font.render(self.text, True, self.color)
        self.image = self.text_surface


class ImageComponent(Component):
    def __init__(self, image_source, position, size=None):
        """
        :param image_source: 图片路径（str） 或 已有的 pygame.Surface 对象
        :param position: 图片在屏幕上的位置 (x, y)
        :param size: 缩放尺寸 (width, height)，可选
        """
        # 加载图片
        if isinstance(image_source, str):
            # 从文件路径加载
            self.original_image = pygame.image.load(image_source).convert_alpha()
        elif isinstance(image_source, pygame.Surface):
            # 使用已有的 Surface
            self.original_image = image_source.convert_alpha()
        else:
            raise ValueError("image_source 必须是文件路径或 pygame.Surface")

        # 缩放图片
        if size:
            self.original_image = resize_surface_to_size(self.original_image, size)

        # 调用父类 Component 初始化
        super().__init__(self.original_image, position)

    def set_image(self, new_image_source, new_size=None):
        """
        动态更换图片
        :param new_image_source: 新图片路径或 Surface
        :param new_size: 新尺寸，可选
        """
        if isinstance(new_image_source, str):
            new_image = pygame.image.load(new_image_source).convert_alpha()
        elif isinstance(new_image_source, pygame.Surface):
            new_image = new_image_source.convert_alpha()
        else:
            raise ValueError("new_image_source 必须是文件路径或 pygame.Surface")

        if new_size:
            new_image = pygame.transform.smoothscale(new_image, new_size)

        self.image = new_image
        self.original_image = new_image


class ButtonComponent(TextComponent):
    """
    A class that represents a button component in the sense
    """

    def __init__(self, text, position, btn_size, function, font='SimSun', size=20, bold=False, italic=False, disabled=False,
                 nor_img='assets/btn/normal.png', hov_img='assets/btn/hover.png', cli_img='assets/btn/click.png'):
        super().__init__(text, position, font, size, bold, italic)

        self.btn_normal = resize_image_to_size(nor_img, btn_size)
        self.btn_hover = resize_image_to_size(hov_img, btn_size)
        self.btn_click = resize_image_to_size(cli_img, btn_size)

        self.present_img = self.btn_normal
        self.present_rect = self.present_img.get_rect(topleft=self.position)

        self.function = function
        self.disabled = disabled
        self.is_pressed = False

    def event(self, event):
        if self.disabled:
            return
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.present_rect.collidepoint(event.pos):
                    self.present_img = self.btn_click
                    self.is_pressed = True

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if self.present_rect.collidepoint(event.pos) and self.is_pressed:
                    self.function()  # Execute the callback
                    self.present_img = self.btn_hover
                self.is_pressed = False

        elif event.type == MOUSEMOTION:
            if self.present_rect.collidepoint(event.pos):
                if not self.is_pressed:
                    self.present_img = self.btn_hover
            else:
                if not self.is_pressed:
                    self.present_img = self.btn_normal

    def draw(self, screen):
        screen.blit(self.present_img, self.present_rect.topleft)

        if self.is_pressed or self.disabled:
            dimmed_color = tuple(int(c * 0.5) for c in self.color)
            text_surface = self.font.render(self.text, True, dimmed_color)
        else:
            text_surface = self.font.render(self.text, True, self.color)

        text_rect = text_surface.get_rect(center=self.present_rect.center)
        screen.blit(text_surface, text_rect)


class GIFComponent:
    """
    A class that represents a GIF component in the sense
    """

    def __init__(self, gif_path, position, scale=None):
        self.gif = Image.open(gif_path)
        self.frames = []
        self.position = position
        self.current_frame = 0
        self.last_time = pygame.time.get_ticks()

        for frame in ImageSequence.Iterator(self.gif):
            frame = frame.convert("RGBA")
            data = frame.tobytes("raw", "RGBA")
            size = frame.size
            surface = pygame.image.fromstring(data, size, "RGBA").convert_alpha()
            if scale:
                surface = pygame.transform.smoothscale(surface, scale)
            self.frames.append(surface)

        self.total_frames = len(self.frames)

    def update(self):
        now = pygame.time.get_ticks()
        delay = 100
        if now - self.last_time > delay:
            self.current_frame = (self.current_frame + 1) % self.total_frames
            self.last_time = now

    def draw(self, screen):
        screen.blit(self.frames[self.current_frame], self.position)


class VideoComponent(Component):
    """
    A class that represents a video component in the sense
    """
    def __init__(self, video_path, position, size=None, loop=False):
        super().__init__(None, position)  # image 由 update 更新

        self.video_path = video_path
        self.size = size
        self.loop = loop
        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():
            raise FileNotFoundError(f"无法打开视频文件: {video_path}")

        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS)) or 30

        self.current_frame = None
        self.is_playing = True
        self.last_update_time = pygame.time.get_ticks()

    def update(self):
        if not self.is_playing:
            return

        now = pygame.time.get_ticks()
        frame_duration = 1000 // self.fps

        if now - self.last_update_time > frame_duration:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if self.size:
                    frame = cv2.resize(frame, self.size)
                frame = np.rot90(frame)
                self.image = pygame.surfarray.make_surface(frame)
                self.last_update_time = now
            else:
                if self.loop:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                else:
                    self.is_playing = False

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.position)

    def pause(self):
        self.is_playing = False

    def resume(self):
        self.is_playing = True

    def set_loop(self, loop):
        self.loop = loop

    def stop(self):
        self.is_playing = False
        self.cap.release()
