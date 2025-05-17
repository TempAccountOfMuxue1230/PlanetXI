"""
File: helper/image.py
File Version: 1.1
"""
from PIL import Image
import pygame


def resize_surface_to_size(surface: pygame.Surface, size: tuple[int, int]) -> pygame.Surface:
    pil_image = Image.frombytes('RGBA', surface.get_size(), pygame.image.tostring(surface, 'RGBA'))

    resized_pil = pil_image.resize(size, resample=Image.Resampling.LANCZOS)

    resized_data = resized_pil.tobytes()

    # 创建 Pygame Surface
    return pygame.image.fromstring(resized_data, size, 'RGBA').convert_alpha()


def resize_image_to_size(image_path: str, target_size: [int, int]) -> pygame.Surface:
    pil_image = Image.open(image_path).convert('RGBA')

    original_width, original_height = pil_image.size
    if original_width == 0:
        raise ValueError("原始图像宽度为 0，无法进行缩放。")

    resized_pil = pil_image.resize(target_size, resample=Image.Resampling.LANCZOS)

    resized_data = resized_pil.tobytes()

    # 创建 Pygame Surface
    return pygame.image.fromstring(resized_data, target_size, 'RGBA').convert_alpha()


def resize_surface_to_height(surface: pygame.Surface, target_height: int) -> pygame.Surface:
    """
    将传入的 Pygame Surface 等比例放大到指定高度，并返回新的 Surface。

    参数:
        surface (pygame.Surface): 要缩放的图像 Surface
        target_height (int): 目标高度（像素）

    返回:
        pygame.Surface: 缩放后的图像 Surface
    """
    # 获取原始尺寸
    original_width, original_height = surface.get_size()

    if original_height == 0:
        raise ValueError("原始 Surface 高度为 0，无法进行缩放。")

    # 计算缩放比例
    scale = target_height / original_height
    new_width = int(original_width * scale)

    # 将 Surface 转换为 RGBA 格式以保留透明通道
    surface_rgba = surface.convert_alpha()

    # 获取像素数据（格式为 RGBA）
    image_data = pygame.image.tostring(surface_rgba, 'RGBA')

    # 使用 Pillow 创建图像
    pil_image = Image.frombytes('RGBA', (original_width, original_height), image_data)

    # 缩放图像
    resized_image = pil_image.resize(
        (new_width, target_height),
        resample=Image.Resampling.LANCZOS
    )

    # 转换为字节数据
    resized_data = resized_image.tobytes()

    # 创建新的 Pygame Surface
    new_surface = pygame.image.fromstring(resized_data, (new_width, target_height), 'RGBA').convert_alpha()

    return new_surface


def resize_image_to_height(image_path: str, target_height: int) -> pygame.Surface:
    """
    等比例放大图片到指定高度，并返回对应的 Pygame Surface。

    参数:
        image_path (str): 图像文件路径
        target_height (int): 目标高度（像素）

    返回:
        pygame.Surface: 调整尺寸后的图像 Surface
    """
    pil_image = Image.open(image_path).convert('RGBA')

    return resize_surface_to_height(pygame.image.frombytes(pil_image.tobytes(), pil_image.size, 'RGBA'), target_height)


def split_image_into_grid(image_path: str, height_present: float) -> list[list[pygame.Surface]]:
    """
    将指定路径的 1024x1024 图片分割为 4x4 的网格，返回包含每个子图的二维列表。

    参数:
        image_path (str): 图像文件路径

    返回:
        list[list[PIL.Image]]: 4x4 的二维列表，每个元素为一个子图的 PIL.Image 对象

    注意:
        - 假设输入图片尺寸为 1024x1024，若尺寸不符可能导致结果异常。
    """
    # 加载图像
    image = Image.open(image_path)

    # 获取图像尺寸
    width, height = image.size

    # 计算每个子图的尺寸
    tile_width = width // 4
    tile_height = height // 4

    # 初始化二维列表用于存储子图
    grid = []

    # 遍历每一行和每一列，裁剪子图
    for i in range(4):
        row = []
        for j in range(4):
            left = j * tile_width
            upper = i * tile_height
            right = left + tile_width
            lower = upper + tile_height

            # 裁剪子图
            tile = image.crop((left, upper, right, lower)).convert('RGBA')
            img = pygame.image.fromstring(tile.tobytes(), tile.size, 'RGBA')
            row.append(resize_surface_to_height(img, round(height_present * img.get_height())).convert_alpha())
        grid.append(row)

    return grid
