"""
File: sense/gui_components.py
File Version: 2.0
"""
import ctypes
import threading
import time
import uuid

import cv2
import numpy as np
import pygame
import webview
from pygame.locals import *
from PIL import Image, ImageSequence

from helper.image import resize_image_to_size, resize_surface_to_size, resize_surface_to_height, resize_image_to_height


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
            if isinstance(size, tuple):
                self.original_image = resize_surface_to_size(self.original_image, size)
            else:
                self.original_image = resize_surface_to_height(self.original_image, size)

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

    def __init__(self, text, position, btn_size, function, font='SimSun', size=20, bold=False, italic=False,
                 disabled=False,
                 nor_img='assets/btn/normal.png', hov_img='assets/btn/hover.png', cli_img='assets/btn/click.png'):
        super().__init__(text, position, font, size, bold, italic)

        if isinstance(btn_size, tuple):
            self.btn_normal = resize_image_to_size(nor_img, btn_size)
            self.btn_hover = resize_image_to_size(hov_img, btn_size)
            self.btn_click = resize_image_to_size(cli_img, btn_size)
        else:
            self.btn_normal = resize_image_to_height(nor_img, btn_size)
            self.btn_hover = resize_image_to_height(hov_img, btn_size)
            self.btn_click = resize_image_to_height(cli_img, btn_size)

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


class ProgressBarComponent(Component):
    """
    A class that represents a horizontal progress bar component with an optional title.
    """

    def __init__(self, position, size,
                 progress=0,
                 fg_color=(0, 200, 255),
                 bg_color=(50, 50, 50),
                 border_color=None,
                 border_width=0,
                 radius=0,
                 title="",
                 title_pos="n",
                 title_font='SimSun',
                 title_size=20,
                 title_bold=False,
                 title_italic=False,
                 title_color=(255, 255, 255)):
        """
        :param position: 进度条在屏幕上的位置 (x, y)
        :param size: 进度条尺寸 (width, height)
        :param progress: 初始进度值 (0-100)
        :param fg_color: 前景色 (填充部分)
        :param bg_color: 背景色 (背景部分)
        :param border_color: 边框颜色
        :param border_width: 边框宽度
        :param radius: 圆角半径 (0-50)
        :param title: 标题文本
        :param title_pos: 标题显示位置，可选值：n, s, e, w, m, nw, ne, se, sw
        :param title_font: 标题字体
        :param title_size: 标题字号
        :param title_bold: 是否加粗
        :param title_italic: 是否斜体
        :param title_color: 标题颜色
        """
        self.size = size
        self.progress = progress
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.radius = radius

        # 标题相关
        self.title = title
        self.title_pos = title_pos
        self.title_color = title_color
        self.title_font = pygame.font.SysFont(title_font, title_size, title_bold, title_italic)
        self.title_surface = pygame.Surface((0, 0)).convert_alpha()
        self._render_title()

        # 创建进度条图像
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self._render()

        super().__init__(self.image, position)

    def _render_title(self):
        """渲染标题文本"""
        if self.title:
            self.title_surface = self.title_font.render(self.title, True, self.title_color)
        else:
            self.title_surface = None

    def _render(self):
        """重新绘制进度条"""
        self.image.fill((0, 0, 0, 0))  # 完全透明

        # 绘制背景
        pygame.draw.rect(self.image, self.bg_color,
                         (0, 0, self.size[0], self.size[1]),
                         border_radius=self._calc_radius())

        # 计算填充区域
        fill_width = int(self.size[0] * (self.progress / 100))

        # 绘制前景
        pygame.draw.rect(self.image, self.fg_color,
                         (0, 0, fill_width, self.size[1]),
                         border_top_left_radius=self._calc_radius() if fill_width == self.size[0] else 0,
                         border_bottom_left_radius=self._calc_radius() if fill_width == self.size[0] else 0)

        # 绘制边框
        if self.border_width > 0 and self.border_color:
            pygame.draw.rect(self.image, self.border_color,
                             (0, 0, self.size[0], self.size[1]),
                             width=self.border_width,
                             border_radius=self._calc_radius())

    def _calc_radius(self):
        """计算圆角半径（像素）"""
        return int(min(self.size) * self.radius / 100)

    def set_progress(self, progress):
        """设置进度值（0-100）"""
        if 0 <= progress <= 100 and progress != self.progress:
            self.progress = progress
            self._render()

    def set_title(self, new_title):
        """更新标题文本"""
        if self.title != new_title:
            self.title = new_title
            self._render_title()

    def update(self):
        """用于保持组件接口一致性"""
        pass

    def draw(self, screen):
        """绘制组件及标题"""
        # 绘制进度条
        screen.blit(self.image, (self.position[0], self.position[1] + self.title_surface.get_height()))

        # 绘制标题
        if self.title_surface:
            pb_rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
            title_width, title_height = self.title_surface.get_size()
            title_rect = pygame.Rect(0, 0, title_width, title_height)

            # 根据 title_pos 设置标题位置
            if self.title_pos == 'n':
                title_rect.centerx = pb_rect.centerx
                title_rect.bottom = pb_rect.top
            elif self.title_pos == 's':
                title_rect.centerx = pb_rect.centerx
                title_rect.top = pb_rect.bottom
            elif self.title_pos == 'e':
                title_rect.centery = pb_rect.centery
                title_rect.left = pb_rect.right
            elif self.title_pos == 'w':
                title_rect.centery = pb_rect.centery
                title_rect.right = pb_rect.left
            elif self.title_pos == 'm':
                title_rect.center = pb_rect.center
            elif self.title_pos == 'nw':
                title_rect.topleft = pb_rect.topleft
            elif self.title_pos == 'ne':
                title_rect.topright = pb_rect.topright
            elif self.title_pos == 'se':
                title_rect.bottomright = pb_rect.bottomright
            elif self.title_pos == 'sw':
                title_rect.bottomleft = pb_rect.bottomleft
            else:
                # 默认 'n'
                title_rect.centerx = pb_rect.centerx
                title_rect.bottom = pb_rect.top

            # 绘制标题
            screen.blit(self.title_surface, title_rect.topleft)


class HTML5Component(Component):
    """
    支持 JS 交互与自动定位的 HTML5 组件
    特点：无边框、不可移动、不可缩放、始终置顶 Pygame 窗口之上
    """

    def __init__(self, position, size, url=None, html=None, parent_window=None):
        """
        :param position: 在 Pygame 中的坐标 (x, y)
        :param size: 尺寸 (width, height)
        :param url: 要加载的网页 URL
        :param html: 要加载的 HTML 字符串内容（优先于 url）
        :param parent_window: Pygame 主窗口标题（用于自动定位）
        """
        self.url = url
        self.html = html
        self.position = position
        self.size = size
        self.parent_window = self._find_window_by_title(parent_window)
        self.webview_window = None
        self.running = False
        self.hwnd = None  # 网页窗口句柄
        self.js_api = None  # JS API 对象
        self.position_monitor_thread = None  # 自动定位线程
        self.uuid = uuid.uuid4()

        # 创建透明占位图像
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # 完全透明

        super().__init__(self.image, position)

    def start(self):
        """启动网页窗口"""
        if self.running:
            return

        self.running = True
        self.js_api = self._create_js_api()
        threading.Thread(target=self._run_webview, daemon=True).start()

    def _create_js_api(self):
        """创建 JS API 对象，供网页调用"""

        class JSAPI:
            def __init__(self, component):
                self.component = component

            def send_message_to_pygame(self, message):
                """网页调用此方法发送消息到 Pygame"""
                print("收到网页消息:", message)
                # 可以在这里触发 Pygame 自定义事件
                event = pygame.event.Event(pygame.USEREVENT, {"source": "webview", "message": message})
                pygame.event.post(event)

            def get_pygame_position(self):
                """网页查询 Pygame 窗口位置"""
                if self.component.parent_window:
                    rect = self.component.parent_window.get_rect()
                    return {'x': rect.x, 'y': rect.y}
                return {'x': 0, 'y': 0}

        return JSAPI(self)

    def _run_webview(self):
        """在子线程中启动 webview 窗口"""
        try:
            # 创建无标题栏窗口
            kwargs = {
                'title': self.uuid,
                'width': self.size[0],
                'height': self.size[1],
                'resizable': False,
                'frameless': True,
                'on_top': True,
                'js_api': self.js_api
            }

            if self.html:
                self.webview_window = webview.create_window(html=self.html, **kwargs)
            elif self.url:
                self.webview_window = webview.create_window(url=self.url, **kwargs)
            else:
                self.webview_window = webview.create_window(html="<h1>Empty</h1>", **kwargs)

            webview.start(gui='edgechromium')  # 强制使用 Edge Chromium 内核

            # 获取窗口句柄并设置样式
            self.hwnd = self._find_window_by_title(self.uuid)
            if self.hwnd:
                self._set_window_style()
                self._set_window_position()
                self._start_position_monitor()

        except Exception as e:
            print("Webview 启动失败:", e)
            self.running = False

    def _find_window_by_title(self, title):
        """通过标题查找窗口句柄"""
        hwnd = ctypes.windll.user32.FindWindowW(None, title)
        if hwnd == 0:
            time.sleep(0.5)  # 等待窗口创建完成
            hwnd = ctypes.windll.user32.FindWindowW(None, title)
        return hwnd

    def _set_window_style(self):
        """设置无边框、不可移动、不可缩放"""
        GWL_STYLE = -16
        WS_CAPTION = 0xC00000
        WS_THICKFRAME = 0x40000

        style = ctypes.windll.user32.GetWindowLongW(self.hwnd, GWL_STYLE)
        style &= ~WS_CAPTION  # 去掉标题栏
        style &= ~WS_THICKFRAME  # 去掉调整边框
        ctypes.windll.user32.SetWindowLongW(self.hwnd, GWL_STYLE, style)

    def _set_window_position(self):
        """设置窗口位置，覆盖在 Pygame 指定位置"""
        if not self.parent_window:
            x, y = self.position
        else:
            rect = self.parent_window.get_rect()
            x, y = rect.x + self.position[0], rect.y + self.position[1]

        w, h = self.size
        HWND_TOPMOST = -1
        SWP_NOOWNERZORDER = 0x0200

        ctypes.windll.user32.SetWindowPos(
            self.hwnd, HWND_TOPMOST,
            x, y, w, h,
            SWP_NOOWNERZORDER
        )

    def _start_position_monitor(self):
        """启动自动定位线程"""
        if self.parent_window is None:
            return

        self.position_monitor_thread = threading.Thread(target=self._monitor_position, daemon=True)
        self.position_monitor_thread.start()

    def _monitor_position(self):
        """监控主窗口位置变化，自动更新网页窗口位置"""
        last_pos = self.parent_window.get_rect().topleft
        while self.running:
            current_pos = self.parent_window.get_rect().topleft
            if current_pos != last_pos:
                self._set_window_position()
                last_pos = current_pos
            time.sleep(0.1)

    def update(self):
        """用于保持组件接口一致性"""
        pass

    def draw(self, screen):
        """绘制组件（仅占位）"""
        screen.blit(self.image, self.position)

    def close(self):
        """关闭网页窗口"""
        if self.webview_window:
            try:
                self.webview_window.destroy()
            except:
                pass
            self.running = False

    def execute_js(self, script):
        """从 Python 调用 JavaScript 脚本"""
        if self.webview_window:
            self.webview_window.evaluate_js(script)
