# coding=utf-8
"""
Shilang Hunter
A GUI program.
- Functionality: Shoot and defeat Shilang.
- Developers: Cheple_Bob.
- Special Thanks: Gavin - Give some advice to improve Shilang_Hunter.
- Dependencies: pygame >= 2.5.2.
- Usage Instructions: How to run or use the program.
    Example Usage:
    python3 main.py
- Note: Please ensure that the Python interpreter is installed before running this program.
Also, Please ensure that requirements.txt packs is already installed before running this program.
- Warning: Don't open this program on April 1st and May 13th!(Just For Fun!)
(Except for these two days, no code will torture the user.)
"""
import json
from datetime import datetime
from decimal import Decimal
from math import ceil, radians
from os import chdir, path
from typing import Union
import pygame
from pygame import *

chdir(path.dirname("../"))
# 现在当前工作目录就是项目根目录了,可以进行文件操作
pygame.init()
# 初始化音频
pygame.mixer.init()
clock: any = pygame.time.Clock()
tick_frequency: int = 60
date: str = datetime.now().strftime("%m-%d")
# date: str = "04-01"
with open("data/Idea.json") as b:
    json_str11: any = json.load(b)
if date == "04-01" or date == "05-13":  # 常用的一些图片
    load_number: int = 0
else:
    load_number: int = 1
game_version: str = json_str11["Game_version"]
image_usually_use: list = json_str11["Images"][load_number]
waiting_time: list = json_str11["Waiting_time"][load_number]
sound: list = json_str11["Sound"][load_number]
game_text: list = json_str11["Text"][load_number]
game_title: str = json_str11["Game_title"][load_number]
game_icon: any = pygame.image.load(image_usually_use[22])  # 游戏标题和图标初始化
if (json_str11["Default_setting"]["width"] == 1280 and json_str11["Default_setting"]["height"] == 720 and
        json_str11["Default_setting"]["balance_width"] == 1280 and
        json_str11["Default_setting"]["balance_height"] == 720):
    game_caption: str = f"{game_title} {game_version} 未修改"
else:
    game_caption: str = f"{game_title} {game_version} !已修改!"
pygame.display.set_icon(game_icon)
pygame.display.set_caption(game_caption)
full_width: int = pygame.display.Info().current_w  # 全屏情况下的长和宽
full_height: int = pygame.display.Info().current_h
volume: float = json_str11["Default_setting"]["volume"]
width: int = json_str11["Default_setting"]["width"]
height: int = json_str11["Default_setting"]["height"]
screen: any = pygame.display.set_mode((width, height), pygame.SRCALPHA)


class Music:
    """播放音频文件"""

    def __init__(self) -> None:
        pass

    @staticmethod
    def music_play(mode: int, music: str, is_music: bool) -> None:
        """加载并播放背景音乐"""
        # 加载背景音乐
        if is_music:
            pygame.mixer.music.load(music)
            pygame.mixer.music.set_volume(volume)
            # 开始播放背景音乐,-1表示无限循环
            pygame.mixer.music.play(mode)
        else:
            play_sound = pygame.mixer.Sound(music)
            play_sound.set_volume(volume)
            play_sound.play()


soundtrack: any = Music()


class Mouse:
    """点击后产生反馈的功能"""

    def __init__(self, frequency: int) -> None:
        self.frequency: int = frequency
        self.x: int = 0
        self.activate: bool = False
        self.pos: any = None

    def click(self) -> None:
        """单击后产生反馈"""
        mouse_pos: tuple = pygame.mouse.get_pos()
        if self.x < self.frequency and self.activate:
            self.x += 1
            # 创建一个带有 Alpha 通道的新 Surface 对象
            circle_surface: any = pygame.Surface((width, height), pygame.SRCALPHA)
            # 在 Surface 上绘制一个透明的圆形
            pygame.draw.circle(circle_surface, (53, 220, 217, 255 - 255 // self.frequency * self.x),
                               self.pos, 2 + self.x * 2, width=4)
            screen.blit(circle_surface, (0, 0))
        else:
            self.activate: bool = False
        mouse1: any = pygame.image.load(image_usually_use[10])
        mouse1: any = pygame.transform.scale(mouse1, (30, 30))  # 绘制鼠标和点击特效
        screen.blit(mouse1, mouse_pos)

    def click_activate(self) -> None:
        """激活上方的click方法"""
        self.pos: any = pygame.mouse.get_pos()
        self.x: int = 0
        self.activate: bool = True


class PopupMessage:
    """设置弹窗"""

    def __init__(self, popup_width: int, popup_height: int, img_path: str, visible_time: int,
                 popup_text: str, text_color: tuple, text_fonts: str, text_size: int, text_x: int, text_y: int,
                 lateral_display: bool, popup_x: int, popup_y: int, input_image: Union[str, None], input_scale: tuple,
                 input_x: int, input_y: int, queue: list, pop_id: int, auto_fit: Union[tuple, None],
                 text_center: tuple[bool, bool], input_center: tuple[bool, bool]) -> None:
        self.popup_rect: any = None
        self.lateral_display: bool = lateral_display
        self.input_scale: tuple = input_scale
        self.pop_id: int = pop_id
        self.popup_x: int = popup_x
        self.popup_y: int = popup_y
        self.text_x: int = text_x
        self.text_y: int = text_y
        self.popup_text: str = popup_text
        self.visible: bool = False
        self.text_color: tuple = text_color
        self.text_size: int = text_size
        self.text_fonts: str = text_fonts
        self.input_x: int = input_x
        self.count: int = 0
        self.input_y: int = input_y
        self.enable_change: bool = True
        self.x: int = 0
        self.img_path: str = img_path
        self.visible_time: int = visible_time
        self.text_center: tuple[bool, bool] = text_center
        self.input_center: tuple[bool, bool] = input_center
        self.input_image: Union[str, None] = input_image
        self.font: any = pygame.font.Font(self.text_fonts, self.text_size)
        self.txt_surface: any = self.font.render(self.popup_text, True, self.text_color)
        if isinstance(auto_fit, tuple):
            self.popup_width: int = max(popup_width, max(input_x + input_scale[0], text_x +
                                                         self.txt_surface.get_size()[0]) + auto_fit[0])
            self.popup_height: int = max(popup_height, max(input_y + input_scale[1], text_y +
                                                           self.txt_surface.get_size()[1]) + auto_fit[1])
        else:
            self.popup_width: int = popup_width
            self.popup_height: int = popup_height
        if isinstance(self.input_image, str):
            self.input_image2: any = pygame.image.load(input_image)
            self.input_image2: any = pygame.transform.scale(self.input_image2, input_scale)
        self.img_origin: any = pygame.image.load(self.img_path).convert_alpha()
        self.img_new: any = pygame.transform.scale(self.img_origin, (self.popup_width, self.popup_height))
        self.direction: int = 0
        self.queue: list = queue
        self.last_visible: bool = False
        self.queue_id: int = 0

    def draw(self) -> None:
        """绘制弹窗"""
        if self.text_center[0]:
            self.text_x: int = self.popup_width // 2 - self.txt_surface.get_width() // 2
        if self.text_center[1]:
            self.text_y: int = self.popup_height // 2 - self.txt_surface.get_height() // 2
        if self.input_center[0]:
            self.input_x: int = self.popup_width // 2 - self.input_scale[0] // 2
        if self.input_center[1]:
            self.input_y: int = self.popup_height // 2 - self.input_scale[1] // 2
        if self.x != 20 and self.visible is True:  # 在游戏中循环，每次往左移
            if self.enable_change:
                self.x += 1
            if self.x <= 10 and self.enable_change:  # 初始
                if self.x == 10:
                    self.enable_change: bool = False
                    self.count: int = pygame.time.get_ticks()
                if self.lateral_display:
                    self.img_new.set_alpha(255 // 10 * self.x)
                    direction = self.img_new.get_rect(center=(self.popup_x, self.popup_y))
                    screen.blit(self.img_new, direction)
                    if isinstance(self.input_image, str):
                        self.input_image2.set_alpha(255 // 10 * self.x)
                        screen.blit(self.input_image2, (direction[0] + self.input_x, direction[1] + self.input_y))
                    self.txt_surface.set_alpha(255 // 10 * self.x)
                    screen.blit(self.txt_surface, (direction[0] + self.text_x, direction[1] + self.text_y))
                else:
                    self.direction: int = width - self.x * (self.popup_width // 10)
                    screen.blit(self.img_new, (self.direction, self.popup_y + (self.queue_id * self.popup_height)))
                    screen.blit(self.txt_surface, (self.direction + self.text_x, self.popup_y + self.text_y +
                                                   (self.queue_id * self.popup_height)))
                    if isinstance(self.input_image, str):
                        screen.blit(self.input_image2, (self.direction + self.input_x, self.popup_y + self.input_y
                                                        + (self.queue_id * self.popup_height)))
            elif not self.enable_change:  # 中间状态
                if pygame.time.get_ticks() - self.count >= self.visible_time:
                    self.enable_change: bool = True
                if self.lateral_display:
                    direction = self.img_new.get_rect(center=(self.popup_x, self.popup_y))
                    screen.blit(self.img_new, direction)
                    screen.blit(self.txt_surface, (direction[0] + self.text_x, direction[1] + self.text_y))
                    if isinstance(self.input_image, str):
                        screen.blit(self.input_image2, (direction[0] + self.input_x, direction[1] + self.input_y))
                    screen.blit(self.txt_surface, (direction[0] + self.text_x, direction[1] + self.text_y))
                else:
                    self.direction: int = width - self.popup_width
                    screen.blit(self.img_new, (self.direction, self.popup_y + (self.queue_id * self.popup_height)))
                    screen.blit(self.txt_surface, (self.direction + self.text_x, self.popup_y + self.text_y +
                                                   (self.queue_id * self.popup_height)))
                    if isinstance(self.input_image, str):
                        screen.blit(self.input_image2, (self.direction + self.input_x, self.popup_y + self.input_y
                                                        + (self.queue_id * self.popup_height)))
            else:  # 结束状态
                if self.lateral_display:
                    self.img_new.set_alpha(255 - 255 // 10 * (self.x - 10))
                    direction = self.img_new.get_rect(center=(self.popup_x, self.popup_y))
                    screen.blit(self.img_new, direction)
                    if isinstance(self.input_image, str):
                        self.input_image2.set_alpha(255 - 255 // 10 * (self.x - 10))
                        screen.blit(self.input_image2, (direction[0] + self.input_x, direction[1] + self.input_y))
                    self.txt_surface.set_alpha(255 - 255 // 10 * (self.x - 10))
                    screen.blit(self.txt_surface, (direction[0] + self.text_x, direction[1] + self.text_y))
                else:
                    self.direction: int = (width - (20 - self.x) *
                                           (self.popup_width // 10))
                    screen.blit(self.img_new, (self.direction, self.popup_y + (self.queue_id * self.popup_height)))
                    screen.blit(self.txt_surface, (self.direction + self.text_x, self.popup_y + self.text_y +
                                                   (self.queue_id * self.popup_height)))
                    if isinstance(self.input_image, str):
                        screen.blit(self.input_image2, (self.direction + self.input_x, self.popup_y + self.input_y
                                                        + (self.queue_id * self.popup_height)))
        else:
            self.visible: bool = False  # 其他情况隐藏弹窗
            if self.visible != self.last_visible:
                del self.queue[0]
        self.last_visible: bool = self.visible

    def activate(self) -> None:
        """弹窗激活方法"""
        if self.pop_id not in self.queue:
            self.queue.append(self.pop_id)
            self.queue_id: int = len(self.queue) - 1
            self.visible: bool = True
            self.x: int = 0


class DynamicBackground:
    """动态背景"""

    def __init__(self, image_path: str, speed: int, img_width: int, img_height: int, scroll_forward: bool,
                 scroll_upward: bool, link_up_x: bool, link_up_y: bool, alpha: int) -> None:
        self.background_image: any = pygame.image.load(image_path).convert_alpha()
        self.alpha: int = alpha
        if self.alpha != 255:
            self.background_image.set_alpha(self.alpha)
        self.background_new_image: any = None
        self.link_up_x: bool = link_up_x
        self.link_up_y: bool = link_up_y
        self.scroll_upward: bool = scroll_upward
        self.scroll_forward: bool = scroll_forward
        self.background_speed: int = speed
        self.img_width: int = img_width
        self.img_height: int = img_height
        self.background_image: any = pygame.transform.scale(self.background_image, (self.img_width, self.img_height))
        self.background_rect: any = self.background_image.get_rect()
        self.background_x: int = 0
        self.background_y: int = 0
        self.background_x2: int = 0
        self.background_y2: int = 0
        if self.scroll_upward:
            if self.scroll_forward:
                self.background_y2: int = -self.background_rect.height
            else:
                self.background_y2: int = self.background_rect.height
        else:
            if self.scroll_forward:
                self.background_x2: int = -self.background_rect.width
            else:
                self.background_x2: int = self.background_rect.width

    def update(self) -> None:
        """更新信息"""
        # 更新背景位置，如果超出屏幕就修改位置
        if self.scroll_upward:
            if self.scroll_forward:
                self.background_y += self.background_speed
                self.background_y2 += self.background_speed
                if self.background_y >= self.background_rect.height:
                    self.background_y: int = -self.background_rect.height
                if self.background_y2 >= self.background_rect.height:
                    self.background_y2: int = -self.background_rect.height
            else:
                self.background_y -= self.background_speed
                self.background_y2 -= self.background_speed
                if self.background_y <= -self.background_rect.height:
                    self.background_y: int = self.background_rect.height
                if self.background_y2 <= -self.background_rect.height:
                    self.background_y2: int = self.background_rect.height
        else:
            if self.scroll_forward:
                self.background_x += self.background_speed
                self.background_x2 += self.background_speed
                if self.background_x >= self.background_rect.width:
                    self.background_x: int = -self.background_rect.width
                if self.background_x2 >= self.background_rect.width:
                    self.background_x2: int = -self.background_rect.width
            else:
                self.background_x -= self.background_speed
                self.background_x2 -= self.background_speed
                if self.background_x <= -self.background_rect.width:
                    self.background_x: int = self.background_rect.width
                if self.background_x2 <= -self.background_rect.width:
                    self.background_x2: int = self.background_rect.width

    def draw(self) -> None:
        """绘制背景"""
        # 绘制两个背景图像
        self.background_new_image: any = pygame.transform.flip(self.background_image, self.link_up_x, self.link_up_y)
        if self.scroll_upward:
            if self.scroll_forward:
                screen.blit(self.background_image, (0, self.background_y))
                screen.blit(self.background_new_image, (0, self.background_y2))
            else:
                screen.blit(self.background_image, (0, self.background_y))
                screen.blit(self.background_new_image, (0, self.background_y2))
        else:
            if self.scroll_forward:
                screen.blit(self.background_image, (self.background_x, 0))
                screen.blit(self.background_new_image, (self.background_x2, 0))
            else:
                screen.blit(self.background_image, (self.background_x, 0))
                screen.blit(self.background_new_image, (self.background_x2, 0))


class LinkUp:
    """转场衔接效果"""

    def __init__(self, frequency: int, img1: str, img2: str) -> None:
        self.background_image: any = pygame.image.load(img1).convert_alpha()
        self.background_image: any = pygame.transform.scale(self.background_image, (width, height))
        self.background_image2: any = pygame.image.load(img2).convert_alpha()
        self.background_image2: any = pygame.transform.scale(self.background_image2, (width, 100))
        self.background_image3: any = pygame.transform.flip(self.background_image2, False, True)
        self.x: int = 0
        self.y: int = 0
        self.frequency: int = frequency
        self.active: bool = False
        self.can_exit: bool = False

    def access(self, wait_time: int) -> None:
        """进入背景"""
        if self.active:
            pygame.mixer_music.stop()
            if self.x < self.frequency:  # 移动板块位置
                self.x += 1
            elif self.y < self.frequency:
                self.y += 1
            screen.blit(self.background_image, (width - width // self.frequency * self.x, 0))  # 加载不同的板块
            screen.blit(self.background_image2, (0, height - 100 // self.frequency * self.y))
            screen.blit(self.background_image3, (0, -100 + 100 // self.frequency * self.y))
            if self.x == self.frequency and self.y == self.frequency:
                now_time: int = pygame.time.get_ticks()
                while True:
                    timer: int = pygame.time.get_ticks()  # 计时，时间到后完成转场特效
                    if timer - now_time >= wait_time:
                        break
                soundtrack.music_play(0, sound[0], False)
                self.can_exit: bool = True
                self.x: int = 0
                self.y: int = 0

    def activate(self) -> None:
        """激活"""
        self.x: int = 0
        self.y: int = 0
        self.background_image: any = pygame.transform.scale(self.background_image, (width, height))
        self.background_image2: any = pygame.transform.scale(self.background_image2, (width, 100))
        self.background_image3: any = pygame.transform.flip(self.background_image2, False, True)
        self.active: bool = True
        self.can_exit: bool = False
        soundtrack.music_play(0, sound[1], False)

    def exit(self) -> None:
        """离开背景"""
        if self.active:  # 移出画面
            if self.y < self.frequency:
                self.y += 1
            elif self.x < self.frequency:
                self.x += 1
            else:
                self.active: bool = False
                self.can_exit: bool = False
            screen.blit(self.background_image, (0 - width // self.frequency * self.x, 0))
            screen.blit(self.background_image2, (0, (height - 100) + 100 // self.frequency * self.y))
            screen.blit(self.background_image3, (0, 0 - 100 // self.frequency * self.y))
        else:
            self.can_exit: bool = False


class Switch:
    """点按可切换状态的按钮"""

    def __init__(self, switch_width: int, switch_height: int, x: int, y: int, inactive: str, active: str,
                 default: bool, is_level: bool, center: int, x_grid: tuple, y_grid: tuple, alpha: int) -> None:
        self.background_image: any = None
        self.switch_width: int = switch_width
        self.switch_height: int = switch_height
        self.is_level: bool = is_level
        self.touch: bool = False
        self.x: int = x
        self.y: int = y
        self.alpha: int = alpha
        self.temp: int = 0
        self.center: int = center
        self.x_grid: tuple = x_grid
        self.y_grid: tuple = y_grid
        self.inactive: str = inactive
        self.active: str = active
        self.rect: any = pygame.Rect(x, y, self.switch_width, self.switch_height)
        self.rect.center = (x, y)
        self.clicked = False
        if self.is_level:
            self.activate: bool = False
        else:
            self.activate: bool = default

    def reset(self) -> None:
        """重置部分参数"""
        self.temp: int = 0

    def draw(self, can_active: Union[bool, list]) -> bool:
        """绘制按钮"""
        if self.center != 3:  # 定位
            if self.center != 2:
                self.x: int = width // self.x_grid[1] * self.x_grid[0]
            if self.center != 1:
                self.y: int = height // self.y_grid[1] * self.y_grid[0]
        self.rect = pygame.Rect(self.x, self.y, self.switch_width, self.switch_height)
        self.rect.center = (self.x, self.y)
        mouse_pos: tuple = pygame.mouse.get_pos()  # 获取鼠标位置
        if self.rect.collidepoint(mouse_pos):
            self.touch: bool = True
        else:
            self.touch: bool = False
        if isinstance(can_active, list):
            active_can: bool = can_active[0]
        else:
            active_can: bool = can_active
        if not self.is_level:
            if can_active:
                if self.rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:  # 鼠标按下开关则切换状态
                        if not self.clicked:
                            soundtrack.music_play(0, sound[2], False)
                            self.clicked: bool = True
                            self.activate: bool = not self.activate
                    else:
                        self.clicked: bool = False
        else:
            if pygame.mouse.get_pressed()[0]:
                if not self.clicked:
                    if self.rect.collidepoint(mouse_pos) and not self.activate and active_can:  # 鼠标点击关卡后触发
                        soundtrack.music_play(0, sound[2], False)
                        self.clicked: bool = True
                        self.activate: bool = True
                        if isinstance(can_active, list):
                            can_active[0] = False
                        self.reset()
                    if (not self.rect.collidepoint(mouse_pos) and self.activate and
                            mouse_pos[1] <= height - 20 * self.temp):  # 鼠标不在关卡上和关卡信息上点击时，关闭
                        self.clicked: bool = True
                        self.activate: bool = False
                        if isinstance(can_active, list):
                            can_active[0] = True
                        self.reset()
            else:
                self.clicked: bool = False
        if self.activate:  # 激活时输出图片
            self.background_image: any = pygame.image.load(self.active).convert_alpha()
        else:
            self.background_image: any = pygame.image.load(self.inactive).convert_alpha()
        self.background_image: any = pygame.transform.scale(self.background_image,
                                                            (self.switch_width, self.switch_height))
        self.background_image.set_alpha(self.alpha)
        screen.blit(self.background_image, self.rect)
        return self.activate

    def level_draw(self, level_id: int, level: int, account: int, can_active: bool) -> int:
        """当作为关卡时，绘制关卡信息"""
        if self.is_level and can_active:
            with open(f"data/User.json", encoding="UTF-8") as f:
                json_str: any = json.load(f)
                f.close()
            with open(f"data/Level.json", encoding="UTF-8") as f:
                json_str2: any = json.load(f)
                f.close()
            with open(f"data/Build.json", encoding="UTF-8") as f:
                json_str3: any = json.load(f)
                f.close()
            with open(f"data/Charm.json", encoding="UTF-8") as f:
                json_str4: any = json.load(f)
                f.close()
            if self.temp < 10:
                self.temp += 1
            button: any = ""
            button2: any = ""
            if (json_str["progress"][account][json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]
                [
                    "Level_id"
                ]
            ] != -1  # 确定关卡解锁状态
            ):
                if json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]["Type"] == 0:
                    button: any = Button("开始作战", 0, (height + 50) - 20 * self.temp, 300, 90,
                                         image_usually_use[0], image_usually_use[1], image_usually_use[2], 1,
                                         1, (6, 8), (1, 2))
                    if (json_str["progress"][account][json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]
                        [
                            "Level_id"
                        ]
                    ] > 1
                    ):
                        button2: any = Button("开始闪击", 0, (height + 150) - 20 * self.temp, 300, 90,
                                              image_usually_use[0], image_usually_use[1], image_usually_use[2],
                                              1, 1, (6, 8), (1, 2))
                elif json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]["Type"] == 1:
                    button2: any = Button("开始闪击", 0, (height + 100) - 20 * self.temp, 300, 90,
                                          image_usually_use[0], image_usually_use[1], image_usually_use[2],
                                          1, 1, (6, 8), (1, 2))
                else:
                    button: any = Button("进入", 0, (height + 100) - 20 * self.temp, 300, 90,
                                         image_usually_use[0], image_usually_use[1], image_usually_use[2], 1,
                                         1, (6, 8), (1, 2))
            background_image: any = pygame.image.load(image_usually_use[11]).convert_alpha()
            background_image: any = pygame.transform.scale(background_image,
                                                           (width, 200))
            screen.blit(background_image, (0, height - 20 * self.temp))
            if (json_str["progress"][account][json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]
                [
                    "Level_id"
                ]
            ] == -1
            ):
                render_main: str = "未解锁"
                render_text: str = json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]["Lock_Description"]
                render_type: str = "未知"
                render_reward: str = ""
            else:
                render_main: str = json_str2[f"Level{level}"][f"{level_id}"]["Title"]
                render_text: str = json_str2[f"Level{level}"][f"{level_id}"]["Description"]
                if json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]["Type"] == 0:
                    render_type: str = "主线关卡"
                elif json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]["Type"] == 1:
                    render_type: str = "支线关卡"
                else:
                    render_type: str = "前进节点"
                render_reward: str = "首次通关解锁 "
                if json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]["Unlock_equipments"] is not None:
                    for x in range(len(json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]
                                       ["Unlock_equipments"])):
                        if render_reward != "首次通关解锁 ":
                            render_reward += "、"
                        render_reward += f"建造物：{json_str3[f"{json_str2[f"Level{json_str["level"][account]}"]
                                                                         [f"{level_id}"]["Unlock_equipments"][x]}"]
                                                                         ["Chinese_name"]}"
                if json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]["Unlock_charms"] is not None:
                    for x in range(len(json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]
                                       ["Unlock_charms"])):
                        if render_reward != "首次通关解锁 ":
                            render_reward += "、"
                        render_reward += f"护符：{json_str4[f"{json_str2[f"Level{json_str["level"][account]}"]
                                                                       [f"{level_id}"]["Unlock_charms"][x]}"]
                                                                       ["Chinese_name"]}"
            screen.blit(pygame.font.Font('assets/fonts/Text.TTF', 50)
                        .render(render_main, True, (255, 255, 255)),
                        (180, (height + 10) - 20 * self.temp))
            screen.blit(pygame.font.Font('assets/fonts/Text.TTF', 32)
                        .render(render_text, True, (255, 255, 255)),
                        (180, (height + 70) - 20 * self.temp))
            if json_str["progress"][account][json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]
                                                      [
                "Level_id"
            ]
            ] != -1:
                screen.blit(pygame.font.Font('assets/fonts/Text.TTF', 26)
                            .render(render_type, True, (255, 255, 255)),
                            (60, (height + 25) - 20 * self.temp))
            if (json_str["progress"][account][json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]
                                                       [
                "Level_id"
            ]
            ] == 0 and render_reward != "首次通关解锁 "):
                screen.blit(pygame.font.Font('assets/fonts/Text.TTF', 30)
                            .render(render_reward, True, (255, 255, 0)),
                            (180, (height + 110) - 20 * self.temp))
            if (json_str["progress"][account][json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]
                [
                    "Level_id"
                ]
            ] != -1
            ):
                if (json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]["Type"] == 0 or
                        json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]["Type"] == 2):
                    if button.draw(50, (180, 180, 180), (255, 255, 255),
                                   (180, 180, 180), can_active):
                        if json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]["Type"] == 0:
                            return 0
                        else:
                            return 2
                if (json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]["Type"] == 0 and
                    json_str["progress"][account][json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]
                    [
                        "Level_id"
                    ]
                ] > 1
                ):
                    if button2.draw(50, (180, 180, 180), (222, 8, 2),
                                    (0, 0, 0), can_active):
                        return 1
                if json_str2[f"Level{json_str["level"][account]}"][f"{level_id}"]["Type"] == 1:
                    if button2.draw(50, (180, 180, 180), (222, 8, 2),
                                    (0, 0, 0), can_active):
                        return 1


class Image:
    """加载图片"""

    def __init__(self, image_path: str, image_width: int, image_height: int, image_x: int, image_y: int,
                 mode: int, alpha: int, x_flip: bool, y_flip: bool, x_grid: tuple, y_grid: tuple) -> None:
        self.image_path: str = image_path
        self.image_width: int = image_width
        self.x_flip: bool = x_flip
        self.y_flip: bool = y_flip
        self.image_height: int = image_height
        self.image_x: int = image_x
        self.image_y: int = image_y
        self.type: int = mode
        self.alpha: int = alpha
        self.x_grid: tuple = x_grid
        self.y_grid: tuple = y_grid

    def draw(self) -> None:
        """加载并输出图片"""
        # mode: 0 - 全部功能 1 - 不进行图片尺寸修改 2 - 不进行位置校准 21 - 不进行x坐标校准 22 - 不进行y坐标校准 3 - 不进行任何额外操作
        # 4 - 不进行位置校准和图片尺寸修改 41 - 不进行x坐标校准和图片尺寸修改 42 - 不进行y坐标校准和图片尺寸修改
        image_origin: any = pygame.image.load(self.image_path).convert_alpha()
        if self.type != 1 and self.type != 3 and self.type != 4 and self.type != 41 and self.type != 42:
            image_new: any = pygame.transform.scale(image_origin, (self.image_width, self.image_height))
        else:
            image_new: any = image_origin
        image_new: any = pygame.transform.flip(image_new, self.x_flip, self.y_flip)
        image_new.set_alpha(self.alpha)
        if self.type != 2 and self.type != 3 and self.type != 4:
            if self.type != 21 and self.type != 41:
                image_x: float = width // self.x_grid[1] * self.x_grid[0]
            else:
                image_x: int = self.image_x
            if self.type != 22 and self.type != 42:
                image_y: float = height // self.y_grid[1] * self.y_grid[0]
            else:
                image_y: int = self.image_y
        else:
            image_x: int = self.image_x
            image_y: int = self.image_y
        image_rect: any = image_new.get_rect(center=(image_x, image_y))
        screen.blit(image_new, image_rect)


class Button:
    """可交互的按钮"""

    def __init__(self, text: str, x: int, y: int, button_width: int, button_height: int, inactive: any, active: any,
                 click: any, mode: int, type2: int, x_grid: tuple, y_grid: tuple) -> None:
        # type2:0 - 全部定位 1 - 仅定x 2 - 仅定y 3 -不定
        self.text: str = text
        self.x: int = x
        self.y: int = y
        self.button_width: int = button_width
        self.button_height: int = button_height
        self.inactive: any = inactive
        self.active: any = active
        self.click: any = click
        self.type: int = mode
        self.type2: int = type2
        self.x_grid: tuple = x_grid
        self.y_grid: tuple = y_grid
        if self.type2 == 0 or self.type2 == 1:
            self.x: float = width // self.x_grid[1] * self.x_grid[0]
        if self.type2 == 0 or self.type2 == 2:
            self.y: float = height // self.y_grid[1] * self.y_grid[0]
        self.rect: any = pygame.Rect(x, y, button_width, button_height)
        self.rect.center = (x, y)
        self.clicked: bool = False

    def draw(self, font_size: int, font_color: tuple, font_color_hover: tuple, font_color_click: tuple,
             can_active: bool) -> bool:
        """绘制按钮"""
        if self.type2 == 0 or self.type2 == 1:
            self.x: float = width // self.x_grid[1] * self.x_grid[0]
        if self.type2 == 0 or self.type2 == 2:
            self.y: float = height // self.y_grid[1] * self.y_grid[0]
        self.rect.center = (self.x, self.y)
        action: bool = False
        # 获取鼠标位置
        mouse_pos: tuple = pygame.mouse.get_pos()
        # 检查鼠标是否悬停在按钮上
        if self.rect.collidepoint(mouse_pos) and can_active:
            if self.type == 0:
                pygame.draw.rect(screen, self.active, self.rect)
            else:
                origin_image: any = pygame.image.load(self.active)
                image_new: any = pygame.transform.scale(origin_image, (self.button_width, self.button_height))
                screen.blit(image_new, self.rect)
            if pygame.mouse.get_pressed()[0]:  # 左键按下
                if not self.clicked:
                    soundtrack.music_play(0, sound[2], False)
                    if self.type == 0:
                        pygame.draw.rect(screen, self.click, self.rect)
                    else:
                        origin_image: any = pygame.image.load(self.click)
                        image_new: any = pygame.transform.scale(origin_image, (self.button_width, self.button_height))
                        screen.blit(image_new, self.rect)
                    action: bool = True
                    self.clicked: bool = True  # 记录已点击
            else:
                self.clicked: bool = False
        else:
            if self.type == 0:
                pygame.draw.rect(screen, self.inactive, self.rect)
            else:
                origin_image: any = pygame.image.load(self.inactive)
                image_new: any = pygame.transform.scale(origin_image, (self.button_width, self.button_height))
                screen.blit(image_new, self.rect)
        # 添加文字
        fonts = pygame.font.Font("assets/fonts/Text.TTF", font_size)
        if self.rect.collidepoint(mouse_pos) and can_active:
            if pygame.mouse.get_pressed()[0] and not self.clicked:  # 左键按下
                text_surface: any = fonts.render(self.text, True, font_color_click)
            else:
                text_surface: any = fonts.render(self.text, True, font_color_hover)
        else:
            text_surface: any = fonts.render(self.text, True, font_color)
        text_rect: any = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        return action


class CustomText:
    """输出文本"""

    def __init__(self, text: str, font_path: str, font_size: int, font_color: tuple, pos: list, alpha: int,
                 center: int, x_grid: tuple, y_grid: tuple, center2: bool, center3: bool, max_text: Union[int, None])\
            -> None:
        """初始化自定义文本对象"""
        self.font_color: any = font_color
        self.font_path: str = font_path
        self.font_size: int = font_size
        self.text: str = text
        self.pos: list = pos
        self.alpha: int = alpha
        self.center: int = center
        self.center2: bool = center2
        self.center3: bool = center3
        self.x_grid: tuple = x_grid
        self.y_grid: tuple = y_grid
        self.max_text: Union[int, None] = max_text

    def draw(self) -> None:
        """在屏幕上绘制文本"""
        if self.center != 3:  # 居中定位
            if self.center != 2:
                self.pos[0] = width // self.x_grid[1] * self.x_grid[0]
            if self.center != 1:
                self.pos[1] = height // self.y_grid[1] * self.y_grid[0]
        fonts: any = pygame.font.Font(self.font_path, self.font_size)
        if isinstance(self.max_text, int) and self.max_text > 0:
            for x in range(ceil(len(self.text) / self.max_text)):
                text_surface: any = fonts.render(self.text[0 + self.max_text * x:self.max_text + self.max_text * x],
                                                 True, self.font_color)
                text_surface.set_alpha(self.alpha)
                transparent_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
                transparent_surface.blit(text_surface, (0, 0))
                text_rect: any = transparent_surface.get_rect(center=self.pos)
                text_rect.bottom += x * (text_surface.get_size()[1] - ceil(self.font_size / 6))
                if not self.center2:
                    if self.center3:
                        text_rect.right = self.pos[0]
                    else:
                        text_rect.left = self.pos[0]
                screen.blit(transparent_surface, text_rect)
        else:
            text_surface: any = fonts.render(self.text, True, self.font_color)
            text_surface.set_alpha(self.alpha)
            transparent_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
            transparent_surface.blit(text_surface, (0, 0))
            text_rect: any = transparent_surface.get_rect(center=self.pos)
            if not self.center2:
                if self.center3:
                    text_rect.right = self.pos[0]
                else:
                    text_rect.left = self.pos[0]
            screen.blit(transparent_surface, text_rect)


class CustomInputBox:
    """带光标的输入框"""

    def __init__(self, default_text: str, center: int, color_inactive: any, color_active: any, text_color: tuple,
                 text_color_active: tuple, fonts: str, img_path: str, img_path_active: str, box_width: int,
                 box_height: int, font_size: int, x: int, y: int, max_text: int, cursor_color: tuple, cursor_width: int,
                 cursor_blink_interval: int, can_enter: bool, can_active: bool, x_grid: tuple, y_grid: tuple) -> None:
        """初始化输入框"""
        self.txt_rect: any = None
        self.can_active: bool = can_active
        self.text: str = ""
        self.default_text: str = default_text
        self.can_enter: bool = can_enter
        self.index: int = 0
        self.list_type: list = []
        self.max_text: int = max_text
        self.width: int = box_width
        self.height: int = box_height
        self.x_grid: tuple = x_grid
        self.y_grid: tuple = y_grid
        self.x: int = x
        self.y: int = y
        self.color_inactive: any = color_inactive
        self.color_active: any = color_active
        self.color: any = self.color_inactive
        self.txt_surface: any = None
        self.active: bool = False
        self.font_size: int = font_size
        self.rect: any = pygame.Rect(x, y, width, height)
        self.center: int = center
        self.img_path: str = img_path
        self.cursor_position: int = 0  # 光标初始位置
        self.cursor_visible: bool = True  # 初始时光标可见
        self.cursor_color: tuple = cursor_color  # 光标颜色
        self.cursor_width: int = cursor_width  # 光标宽度
        self.cursor_blink_timer: int = pygame.time.get_ticks()  # 光标闪烁计时器
        self.cursor_blink_interval: int = cursor_blink_interval  # 光标闪烁间隔时间（毫秒）
        self.font: any = pygame.font.Font(fonts, font_size)
        if img_path:
            origin_image: any = pygame.image.load(img_path)
            origin_image: any = pygame.transform.scale(origin_image, (width, height))
            self.background: any = origin_image
            self.img_path_active: str = img_path_active
        else:
            self.background: any = pygame.Surface((width, height))
            self.background.fill(color_inactive)
        self.text_color: tuple = text_color
        self.text_color_active: tuple = text_color_active
        self.txt_surface: any = self.font.render(self.text, True, self.text_color)
        self.update_rect()

    def cursor_update(self) -> None:
        """控制光标的闪烁"""
        current_time: int = pygame.time.get_ticks()
        if current_time - self.cursor_blink_timer > self.cursor_blink_interval:
            self.cursor_visible: bool = not self.cursor_visible
            self.cursor_blink_timer: int = current_time

    def draw_cursor(self) -> None:
        """绘制光标"""
        if self.cursor_visible:
            cursor_x: int = self.txt_rect.x + self.cursor_position  # 计算光标x坐标
            temp: int = max(0, len(self.text) - 1)
            # noinspection PyUnusedLocal
            for x in range(len(self.text) - self.index):
                if temp >= 0:  # 确保temp是非负数
                    cursor_x -= self.list_type[temp]
                temp -= 1
            pygame.draw.line(screen, self.cursor_color, (cursor_x, self.rect.top),
                             (cursor_x, self.rect.bottom), self.cursor_width)

    def handle_event(self, events: any, can_active: bool) -> None:
        """处理事件"""
        self.can_active: bool = can_active
        if events.type == pygame.MOUSEBUTTONDOWN and events.button == 1 and self.can_active:
            # 如果点击输入框,则激活或取消激活
            if self.rect.collidepoint(events.pos):
                soundtrack.music_play(0, sound[2], False)
                self.active: bool = not self.active
            else:
                self.active: bool = False
        if events.type == pygame.KEYDOWN:
            if self.active:
                if events.key == pygame.K_RETURN and self.can_enter:
                    self.text: str = ""
                    self.list_type: list = []
                    self.index: int = 0
                elif events.key == pygame.K_LEFT:
                    if self.index > 0:
                        self.index -= 1
                elif events.key == pygame.K_RIGHT:
                    if self.index < len(self.text):
                        self.index += 1
                elif events.key == pygame.K_UP:
                    self.index: int = 0
                elif events.key == pygame.K_DOWN:  # 控制上下左右点击后的光标及索引
                    self.index: int = len(self.text)
                elif events.key == pygame.K_BACKSPACE:  # 按下退格时改变索引和文本内容
                    if len(self.text) > 0:
                        if 0 < self.index < len(self.text):
                            temp1: str = self.text[0:self.index - 1]
                            temp2: str = self.text[self.index:len(self.text)]
                            self.text: str = temp1 + temp2
                            self.index -= 1
                            del self.list_type[self.index]
                        else:
                            if self.index == len(self.text):
                                self.text: str = self.text[:-1]
                                self.index -= 1
                                del self.list_type[self.index]
                elif 32 <= events.key <= 126:  # 确保输入内容正常
                    if len(self.text) < self.max_text:
                        temp1: str = self.text[0:self.index]
                        temp2: str = self.text[self.index:len(self.text)]
                        temp1 += events.unicode
                        self.index += 1
                        old_txt_surface: int = self.font.render(self.text, True, self.text_color_active).get_width()
                        self.text: str = temp1 + temp2
                        self.list_type.insert(self.index - 1,
                                              self.font.render(self.text, True, self.text_color_active).
                                              get_width() - old_txt_surface)
                # 重新渲染文本
                if self.active:
                    self.txt_surface: any = self.font.render(self.text, True, self.text_color_active)
                else:
                    self.txt_surface: any = self.font.render(self.text, True, self.text_color)
                # 更新输入框大小
        self.update_rect()

    def update_rect(self) -> None:
        """更新状态"""
        # 更新输入框的位置和大小
        new_width: int = max(self.width, self.txt_surface.get_width() + 10)
        # 保持高度不变
        if self.center != 3:
            if self.center != 2:
                self.x: int = width // self.x_grid[1] * self.x_grid[0]
            if self.center != 1:
                self.y: int = height // self.y_grid[1] * self.y_grid[0]
        self.rect = pygame.Rect(self.x, self.y, new_width, self.height)
        self.rect.center = (self.x, self.y)
        if self.active:
            self.txt_surface: any = self.font.render(self.text, True, self.text_color_active)
            if not self.img_path:
                self.background.fill(self.color_active)
            else:
                img_active: any = pygame.image.load(self.img_path_active)
                img_active: any = pygame.transform.scale(img_active, (new_width, self.height))
                self.background: any = img_active
        else:
            self.txt_surface: any = self.font.render(self.text, True, self.text_color)
            if not self.img_path:
                self.background.fill(self.color_inactive)
            else:
                img_inactive: any = pygame.image.load(self.img_path)
                img_inactive: any = pygame.transform.scale(img_inactive, (new_width, self.height))
                self.background: any = img_inactive
        self.txt_rect = self.txt_surface.get_rect(center=self.rect.center)
        self.cursor_position: int = self.txt_surface.get_width()

    def draw(self) -> None:
        """绘制输入框"""
        # 如果没有文本，显示默认文本
        if len(self.list_type) < 1:
            if self.active:
                self.txt_surface: any = self.font.render(self.default_text, True, self.text_color_active)
            else:
                self.txt_surface: any = self.font.render(self.default_text, True, self.text_color)
        else:
            if self.active:
                self.txt_surface: any = self.font.render(self.text, True, self.text_color_active)
            else:
                self.txt_surface: any = self.font.render(self.text, True, self.text_color)
        # 绘制输入框
        # 背景
        screen.blit(self.background, self.rect)
        # 文字
        screen.blit(self.txt_surface, self.txt_rect.topleft)
        self.draw_cursor()  # 绘制光标

    def delete(self) -> None:
        """清除文本内容"""
        self.text: str = ""
        self.list_type: list = []
        self.index: int = 0


class EntityCreate:
    """在关卡中生成实体"""

    def __init__(self, game_start_time: int, level: int, stage: int, difficult: int) -> None:
        with open("data/Level_data.json", encoding="UTF-8") as f:
            json_str: any = json.load(f)
            f.close()
        with open("data/Entity.json", encoding="UTF-8") as f:
            json_str2: any = json.load(f)
            f.close()
        with open("data/Idea.json", encoding="UTF-8") as f:
            json_str3: any = json.load(f)
            f.close()
        self.multiple_height: float = height / json_str3["Default_setting"]["balance_height"]
        self.multiple_width: float = width / json_str3["Default_setting"]["balance_width"]
        self.game_start_time: int = game_start_time
        self.approve_damage_text: bool = False
        self.difficult: int = difficult
        self.gun_damage: any = 0
        self.continue_count: int = 0
        self.basic_information: any = None
        self.hit_last_hp: list = []
        self.hp: list = []
        self.location: list = []
        self.blit: list[bool] = []
        self.is_dead: list[bool] = []
        self.last_hp: list = []
        self.dead_temp: list[int] = []
        self.dead_image: list = []
        self.dead_rect: list = []
        self.animation: list[int] = []
        self.is_true_enemy: list[bool] = []
        self.invincible_time: list[int] = []
        self.hp_animation: list = []
        self.can_hit: list[bool] = []
        self.blink: list[bool] = []
        self.path_count: list[int] = []
        self.last_can_hit: list[bool] = []
        self.enable_change_animation: list[bool] = []
        self.can_change_walk_status: list[bool] = []
        self.last_can_change_walk_status: list[bool] = []
        self.walk_status_time: list[int] = []
        self.load_source: list = []
        self.load_tag: list[str] = []
        self.effect: list[list] = []
        self.pop: list = []
        self.enable_pop: list = []
        self.queue: list = []
        for y in range(json_str[f"{level}-{stage}"]["basic"]["popups"][self.difficult]):
            self.pop.append(PopupMessage(json_str[f"{level}-{stage}"][f"entity{difficult}"][f"popups{y}"]["width"] *
                                         self.multiple_width,
                                         json_str[f"{level}-{stage}"][f"entity{difficult}"][f"popups{y}"]["height"] *
                                         self.multiple_height,
                                         image_usually_use[9] if json_str[f"{level}-{stage}"]
                                         [f"entity{difficult}"][f"popups{y}"]["lateral_display"] else
                                         image_usually_use[5], json_str[f"{level}-{stage}"][f"entity{difficult}"]
                                         [f"popups{y}"]["time"], json_str[f"{level}-{stage}"][f"entity{difficult}"]
                                         [f"popups{y}"]["text"], (255, 255, 255),
                                         "assets/fonts/Text.TTF", json_str[f"{level}-{stage}"]
                                         [f"entity{difficult}"][f"popups{y}"]["text_size"], json_str[f"{level}-{stage}"]
                                         [f"entity{difficult}"][f"popups{y}"]["text_x"] * self.multiple_width,
                                         json_str[f"{level}-{stage}"]
                                         [f"entity{difficult}"][f"popups{y}"]["text_y"] * self.multiple_height,
                                         json_str[f"{level}-{stage}"]
                                         [f"entity{difficult}"][f"popups{y}"]["lateral_display"], width //
                                         json_str[f"{level}-{stage}"][f"entity{difficult}"][f"popups{y}"]["x2"] *
                                         json_str[f"{level}-{stage}"][f"entity{difficult}"][f"popups{y}"]["x1"],
                                         height //
                                         json_str[f"{level}-{stage}"][f"entity{difficult}"][f"popups{y}"]["y2"] *
                                         json_str[f"{level}-{stage}"][f"entity{difficult}"][f"popups{y}"]["y1"],
                                         json_str[f"{level}-{stage}"][f"entity{difficult}"][f"popups{y}"]
                                         ["input_image"], (json_str[f"{level}-{stage}"][f"entity{difficult}"]
                                         [f"popups{y}"]["input_width"],
                                         json_str[f"{level}-{stage}"][f"entity{difficult}"]
                                         [f"popups{y}"]["input_height"]), json_str[f"{level}-{stage}"]
                                         [f"entity{difficult}"][f"popups{y}"]["input_x"] * self.multiple_width,
                                         json_str[f"{level}-{stage}"]
                                         [f"entity{difficult}"][f"popups{y}"]["input_y"] * self.multiple_height,
                                         self.queue, 0,
                                         (20, 20), (json_str[f"{level}-{stage}"]
                                         [f"entity{difficult}"][f"popups{y}"]["text_center_x"],
                                                json_str[f"{level}-{stage}"][f"entity{difficult}"][f"popups{y}"][
                                                    "text_center_y"]), (json_str[f"{level}-{stage}"]
                                         [f"entity{difficult}"][f"popups{y}"]["input_center_x"],
                                                                        json_str[f"{level}-{stage}"][
                                                                            f"entity{difficult}"][f"popups{y}"][
                                                                            "input_center_y"])))
            if self.pop[y].lateral_display:
                self.pop[y].img_path = image_usually_use[9]
            self.enable_pop.append(False)
        for x in range(json_str[f"{level}-{stage}"]["basic"]["enemy"][difficult]):
            (self.location.append([Decimal(str(json_str[f"{level}-{stage}"][f"entity{difficult}"][f"{x}"]["pos"][0])) *
                                   Decimal(str(self.multiple_width)),
                                   Decimal(str(json_str[f"{level}-{stage}"][f"entity{difficult}"][f"{x}"]["pos"][1])) *
                                   Decimal(str(self.multiple_height))]))
            self.is_true_enemy.append(True)
            self.effect.append([])
            self.enable_change_animation.append(False)
            self.blit.append(False)
            self.is_dead.append(False)
            self.dead_temp.append(0)
            self.hp_animation.append(0)
            self.dead_image.append("")
            self.dead_rect.append("")
            self.animation.append(1)
            self.hp.append(json_str2[json_str[f"{level}-{stage}"][f"entity{difficult}"][f"{x}"]["id"]]["HP"])
            self.hit_last_hp.append(self.hp[x])
            self.last_hp.append(self.hp[x])
            self.invincible_time.append(0)
            self.can_hit.append(True)
            self.blink.append(False)
            self.last_can_hit.append(True)
            self.path_count.append(0)
            self.can_change_walk_status.append(False)
            self.last_can_change_walk_status.append(True)
            self.walk_status_time.append(0)
        self.level: int = level
        self.game_now_time: int = 0
        self.stage: int = stage
        self.progress: int = 0
        self.pop_progress: int = 0
        self.last_can_active: bool = True
        self.start_frozen_time: int = 0
        self.total_frozen_time: int = 0
        self.temp_save_frozen_time: int = 0
        self.danger_line_y: int = int(Decimal(str(json_str[f"{self.level}-{self.stage}"]["basic"]["danger_line"]
                                                          [difficult])) * Decimal(str(self.multiple_height)))

    def check(self, can_active: bool) -> None:
        """检查是否可以生成实体"""
        self.game_now_time: int = pygame.time.get_ticks()
        with open("data/Level_data.json", encoding="UTF-8") as f:
            json_str: any = json.load(f)
            f.close()
        pygame.draw.line(screen, (255, 52, 40), (0, self.danger_line_y), (width, self.danger_line_y), 5)
        if can_active:
            if self.last_can_active != can_active:  # 计算暂停时间
                self.total_frozen_time += self.temp_save_frozen_time
            if not self.progress == json_str[f"{self.level}-{self.stage}"]["basic"]["enemy"][self.difficult]:
                if (self.game_now_time - self.game_start_time - self.total_frozen_time >=
                        json_str[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{self.progress}"]
                        ["visible_time/ms"]):
                    self.blit[self.progress] = True
                    self.progress += 1
            if not self.pop_progress == json_str[f"{self.level}-{self.stage}"]["basic"]["popups"][self.difficult]:
                if (self.game_now_time - self.game_start_time - self.total_frozen_time >=
                        json_str[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"popups{self.pop_progress}"]
                        ["visible_time/ms"]):
                    self.pop[self.pop_progress].activate()
                    self.enable_pop[self.pop_progress] = True
                    self.pop_progress += 1
        else:
            if self.last_can_active != can_active:  # 开始计算暂停时间
                self.start_frozen_time: int = pygame.time.get_ticks()
            self.temp_save_frozen_time: int = pygame.time.get_ticks() - self.start_frozen_time
        self.last_can_active: bool = can_active

    def create(self, can_active: bool, gun_is_shoot: bool, gun_rect, gun_damage: int, basic_information: list,
               damage_visible: bool, float_damage_visible: bool, build_id: list[int], build_rect: list,
               build_active: list[bool]) -> None:
        """生成实体"""
        self.basic_information: list = basic_information
        self.gun_damage: any = gun_damage
        self.approve_damage_text: bool = False
        temp_hurt_damage: int = 0
        temp_speed: Decimal = Decimal(str(0))
        temp_def: Decimal = Decimal(str(0))
        with open("data/Entity.json", encoding="UTF-8") as f:
            json_str: any = json.load(f)
            f.close()
        with open("data/Level_data.json", encoding="UTF-8") as f:
            json_str2: any = json.load(f)
            f.close()
        with open("data/Path.json", encoding="UTF-8") as f:
            json_str3: any = json.load(f)
            f.close()
        with open("data/Build.json", encoding="UTF-8") as f:
            json_str4: any = json.load(f)
            f.close()
        with open("data/Effect.json", encoding="UTF-8") as f:
            json_str5: any = json.load(f)
            f.close()
        for x in range(json_str2[f"{self.level}-{self.stage}"]["basic"]["enemy"][self.difficult]):  # 对每个敌人进行操作
            if self.blit[x]:  # 如果允许输出就开始操作
                if can_active:
                    temp_hurt_damage: int = 0
                    temp_speed: Decimal = Decimal(str(0))
                    temp_def: Decimal = Decimal(str(0))
                    for y in range(len(self.effect[x])):
                        if 0 in json_str5[f"{self.effect[x][y]}"]["give"]:
                            temp_hurt_damage += json_str5[f"{self.effect[x][y]}"]["give_numerical"][
                                json_str5[f"{self.effect[x][y]}"]["give"].index(0)]
                        if 1 in json_str5[f"{self.effect[x][y]}"]["give"]:
                            temp_def: Decimal = temp_def + Decimal(str(json_str5[f"{self.effect[x][y]}"]
                                                                       ["give_numerical"][
                                                                           json_str5[f"{self.effect[x][y]}"][
                                                                               "give"].index(1)]))
                        if 2 in json_str5[f"{self.effect[x][y]}"]["give"]:
                            temp_speed: Decimal = temp_speed + Decimal(str(json_str5[f"{self.effect[x][y]}"]
                                                                           ["give_numerical"][
                                                                               json_str5[f"{self.effect[x][y]}"][
                                                                                   "give"].index(2)]))
                if (f"assets/images/{json_str2[f"{self.level}-{self.stage}"]
                                              [f"entity{self.difficult}"][f"{x}"]["id"]}{
                    self.animation[x]}{
                    json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["id"]]
                        ["Image_type"]}" in self.load_tag):
                    entity_image: any = self.load_source[self.load_tag.index(f"assets/images/{
                        json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["id"]}{
                        self.animation[x]}{
                        json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["id"]]
                        ["Image_type"]}")]
                else:
                    entity_image: any = pygame.image.load(f"assets/images/{json_str2[f"{self.level}-{self.stage}"]
                                                                                    [f"entity{self.difficult}"]
                                                                                    [f"{x}"]["id"]}{
                        self.animation[x]}{
                        json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["id"]]
                                ["Image_type"]}")  # 控制加载图片
                    entity_image: any = pygame.transform.scale(entity_image, (
                        json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["id"]]
                        ["scale"][0],
                        json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["id"]]
                        ["scale"][1]))  # 修改图片尺寸
                    self.load_source.append(entity_image)
                    self.load_tag.append(f"assets/images/{json_str2[f"{self.level}-{self.stage}"]
                                                                   [f"entity{self.difficult}"][f"{x}"]["id"]}{
                        self.animation[x]}{
                        json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["id"]]
                                ["Image_type"]}")
                if (json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["path"] is None and
                    True in json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["custom_path"]
                        ["Status"][self.path_count[x]]["direction"]):
                    self.enable_change_animation[x] = True
                elif (json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["path"] is not None and
                      True in json_str3[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]
                      ["path"]]["Status"][self.path_count[x]]["direction"]):
                    self.enable_change_animation[x] = True
                else:
                    self.enable_change_animation[x] = False
                if can_active and self.enable_change_animation[x]:
                    if json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]
                                                     ["id"]]["Enemy_type"] < 2:
                        if (self.animation[x] >= json_str[json_str2[f"{self.level}-{self.stage}"]
                                                                   [f"entity{self.difficult}"][f"{x}"]["id"]]
                                                                   ["Animation_count"]):  # 切换图片以实现动画
                            self.animation[x] = 1
                        else:
                            self.animation[x] += 1
                if can_active:  # 移动
                    if (json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["path"] is not None
                            and json_str3[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]
                                                   ["path"]]["Status"][self.path_count[x]]["direction"][0]):
                        self.location[x][1] = (Decimal(str(self.location[x][1])) +
                                               Decimal(
                                                   str((json_str[json_str2[f"{self.level}-{self.stage}"]
                                                                         [f"entity{self.difficult}"][f"{x}"]
                                                                         ["id"]]["Speed"] +
                                                        temp_speed) * Decimal(str(self.multiple_height)))))
                    elif (json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["path"] is None and
                          json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["custom_path"]
                                 ["Status"][self.path_count[x]]["direction"][0]):
                        self.location[x][1] = (Decimal(str(self.location[x][1])) +
                                               Decimal(
                                                   str((json_str[json_str2[f"{self.level}-{self.stage}"]
                                                                         [f"entity{self.difficult}"][f"{x}"]
                                                                         ["id"]]["Speed"] +
                                                        temp_speed) * Decimal(str(self.multiple_height)))))
                    if (json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["path"] is not None
                            and json_str3[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]
                                                   ["path"]]["Status"][self.path_count[x]]["direction"][1]):
                        self.location[x][0] = (Decimal(str(self.location[x][0])) -
                                               Decimal(
                                                   str((json_str[json_str2[f"{self.level}-{self.stage}"]
                                                                         [f"entity{self.difficult}"][f"{x}"]
                                                                         ["id"]]["Speed"] +
                                                        temp_speed) * Decimal(str(self.multiple_width)))))
                    elif (json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["path"] is None and
                          json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["custom_path"]
                                 ["Status"][self.path_count[x]]["direction"][1]):
                        self.location[x][0] = (Decimal(str(self.location[x][0])) -
                                               Decimal(
                                                   str((json_str[json_str2[f"{self.level}-{self.stage}"]
                                                                         [f"entity{self.difficult}"][f"{x}"]
                                                                         ["id"]]["Speed"] +
                                                        temp_speed) * Decimal(str(self.multiple_width)))))
                    if (json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["path"] is not None
                            and json_str3[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]
                                                   ["path"]]["Status"][self.path_count[x]]["direction"][2]):
                        self.location[x][0] = (Decimal(str(self.location[x][0])) +
                                               Decimal(
                                                   str((json_str[json_str2[f"{self.level}-{self.stage}"]
                                                                         [f"entity{self.difficult}"][f"{x}"]
                                                                         ["id"]]["Speed"] +
                                                        temp_speed) * Decimal(str(self.multiple_width)))))
                    elif (json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["path"] is None and
                          json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["custom_path"]
                                 ["Status"][self.path_count[x]]["direction"][2]):
                        self.location[x][0] = (Decimal(str(self.location[x][0])) +
                                               Decimal(
                                                   str((json_str[json_str2[f"{self.level}-{self.stage}"]
                                                                         [f"entity{self.difficult}"][f"{x}"]
                                                                         ["id"]]["Speed"] +
                                                        temp_speed) * Decimal(str(self.multiple_width)))))
                    if (json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["path"] is not None
                            and json_str3[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]
                                                   ["path"]]["Status"][self.path_count[x]]["direction"][3]):
                        self.location[x][1] = (Decimal(str(self.location[x][1])) -
                                               Decimal(
                                                   str((json_str[json_str2[f"{self.level}-{self.stage}"]
                                                                         [f"entity{self.difficult}"][f"{x}"]
                                                                         ["id"]]["Speed"] +
                                                        temp_speed) * Decimal(str(self.multiple_height)))))
                    elif (json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["path"] is None and
                          json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["custom_path"]
                                 ["Status"][self.path_count[x]]["direction"][3]):
                        self.location[x][1] = (Decimal(str(self.location[x][1])) -
                                               Decimal(
                                                   str((json_str[json_str2[f"{self.level}-{self.stage}"]
                                                                         [f"entity{self.difficult}"][f"{x}"]
                                                                         ["id"]]["Speed"] +
                                                        temp_speed) * Decimal(str(self.multiple_height)))))
                    if self.can_change_walk_status[x]:
                        if (json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["path"] is not
                                None and json_str3[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"]
                                                            [f"{x}"]["path"]]["Status_count"]
                                == self.path_count[x] + 1):
                            self.path_count[x] = 0
                        elif (json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["path"] is None
                              and json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]
                              ["custom_path"]["Status_count"]
                                == self.path_count[x] + 1):
                            self.path_count[x] = 0
                        else:
                            self.path_count[x] += 1
                        self.last_can_change_walk_status[x] = self.can_change_walk_status[x]
                        self.can_change_walk_status[x] = False
                    else:
                        if self.last_can_change_walk_status[x] != self.can_change_walk_status[x]:
                            self.walk_status_time[x] = (pygame.time.get_ticks() - self.game_start_time
                                                             - self.total_frozen_time)
                        if (json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["path"] is not
                                None and pygame.time.get_ticks() - self.total_frozen_time -
                                self.game_start_time - self.walk_status_time[x] >=
                                json_str3[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]
                                                   ["path"]]["Status"][self.path_count[x]]["time/ms"]):
                            self.can_change_walk_status[x] = True
                        elif (json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["path"] is None
                                and pygame.time.get_ticks() - self.total_frozen_time -
                                self.game_start_time - self.walk_status_time[x] >=
                              json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["custom_path"]
                              ["Status"][self.path_count[x]]["time/ms"]):
                            self.can_change_walk_status[x] = True
                        self.last_can_change_walk_status[x] = self.can_change_walk_status[x]
                entity_rect = pygame.Rect(
                    0, 0,
                    json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["id"]]["scale"]
                    [0],
                    json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["id"]]["scale"]
                    [1])
                entity_rect.center = (self.location[x][0], self.location[x][1])  # 计算位置
                if can_active:  # 给予和显示状态
                    effect_len: int = 0
                    for y in range(len(self.effect[x])):
                        if (f"assets/images/{json_str5[f"{self.effect[x][y]}"]["name"]}{
                                json_str5[f"{self.effect[x][y]}"]["Image_type"]}" in self.load_tag):
                            effect_image: any = self.load_source[self.load_tag.index(f"assets/images/{
                                json_str5[f"{self.effect[x][y]}"]["name"]}{
                                json_str5[f"{self.effect[x][y]}"]["Image_type"]}")]
                        else:
                            effect_image: any = pygame.image.load(f"assets/images/{json_str5[f"{
                                self.effect[x][y]}"]["name"]}{
                                json_str5[f"{self.effect[x][y]}"]["Image_type"]}")  # 控制加载图片
                            effect_image: any = pygame.transform.scale(effect_image, (40, 40))  # 修改图片尺寸
                            self.load_source.append(effect_image)
                            self.load_tag.append(f"assets/images/{json_str5[f"{self.effect[x][y]}"]["name"]}{
                                json_str5[f"{self.effect[x][y]}"]["Image_type"]}")
                        effect_rect = pygame.Rect(entity_rect.center[0], entity_rect.top - 55, 40, 40)
                        effect_rect.right = entity_rect.center[0] + (40 * len(self.effect[x]) / 2) - effect_len
                        screen.blit(effect_image, effect_rect)
                        effect_len += 40
                    if json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]
                                                     ["id"]]["Enemy_type"] >= 1:
                        for y in range(len(json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"]
                                                             [f"{x}"]["id"]]["cause_effects"])):
                            if (json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]
                                                  ["id"]]["cause_reason"][y] == "global"):
                                for z in range(json_str2[f"{self.level}-{self.stage}"]["basic"]["enemy"]
                                               [self.difficult]):
                                    if self.blit[z]:
                                        if (json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"]
                                                              [f"{z}"]["id"]]["Enemy_type"] in
                                                json_str5[f"{json_str[json_str2[f"{self.level}-{self.stage}"]
                                                                               [f"entity{self.difficult}"][f"{x}"]
                                                                               ["id"]]["cause_effects"][y]}"]
                                                                               ["enemy_type"]):
                                            if (json_str[json_str2[f"{self.level}-{self.stage}"]
                                                                 [f"entity{self.difficult}"][f"{x}"]["id"]]
                                                                 ["cause_effects"][y] not in self.effect[z]):
                                                self.effect[z].append(json_str[json_str2[f"{self.level}-{self.stage}"]
                                                                                        [f"entity{self.difficult}"]
                                                                                        [f"{x}"]["id"]]["cause_effects"]
                                                                      [y])
                if self.blink[x]:
                    entity_image.set_alpha(100)
                else:
                    entity_image.set_alpha(255)  # 无敌时间闪烁
                screen.blit(entity_image, entity_rect)
                if entity_rect.bottom >= self.danger_line_y:
                    basic_information[0] -= (json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"]
                                                              [f"{x}"]["id"]]["minus_HP"] + temp_hurt_damage)
                    if self.is_true_enemy[x]:
                        basic_information[1] += 1
                    soundtrack.music_play(0, sound[3], False)
                    self.blit[x] = False
                    continue
                if can_active:
                    for y in range(len(build_active)):
                        if build_active[y]:
                            if entity_rect.colliderect(build_rect[y]):
                                if json_str4[f"{build_id[y]}"]["type"] == "passive_attack":
                                    soundtrack.music_play(0, sound[4], False)
                                    if json_str4[f"{build_id[y]}"]["damage_type"]:
                                        self.hp[x] = (Decimal(str(self.hp[x])) -
                                                               Decimal(str(json_str4[f"{build_id[y]}"]["damage"])))
                                    else:
                                        damage: any = (Decimal(str(json_str4[f"{build_id[y]}"]["damage"])) -
                                                       Decimal(str(json_str[json_str2[f"{self.level}-{self.stage}"]
                                                                                     [f"entity{self.difficult}"]
                                                                                     [f"{x}"]["id"]]["Def"])) - temp_def
                                                       )
                                        if damage <= 0:
                                            damage: any = 0
                                        self.hp[x] = (Decimal(str(self.hp[x])) -
                                                      Decimal(str(damage)))
                                    self.hp[x] = float(self.hp[x])
                                    build_active[y] = False
                    if entity_rect.colliderect(gun_rect) and gun_is_shoot and self.can_hit[x]:  # 中枪受伤逻辑
                        self.gun_damage: any = (Decimal(str(gun_damage)) -
                                                Decimal(str(json_str[json_str2[f"{self.level}-{self.stage}"]
                                                                              [f"entity{self.difficult}"]
                                                                              [f"{x}"]["id"]]["Def"])) - temp_def)
                        if self.gun_damage < 0:
                            self.gun_damage: any = 0
                        self.hp[x] = Decimal(str(self.hp[x])) - Decimal(str(self.gun_damage))
                        self.hp[x] = float(self.hp[x])
                        if damage_visible:
                            self.approve_damage_text: bool = True
                            if not float_damage_visible:
                                self.gun_damage: int = int(self.gun_damage)
                        self.can_hit[x] = False
                        if self.last_can_hit[x] != self.can_hit[x]:
                            soundtrack.music_play(0, sound[5], False)
                            self.invincible_time[x] = (pygame.time.get_ticks() - self.total_frozen_time
                                                            - self.game_start_time)
                    if self.hp[x] <= 0:  # 血量耗尽时死亡
                        soundtrack.music_play(0, sound[6], False)
                        self.blit[x] = False
                        self.is_dead[x] = True
                        self.dead_image[x] = entity_image
                        self.dead_rect[x] = entity_rect
                        if json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]
                                             ["id"]]["Enemy_type"] >= 1:
                            for y in range(
                                    len(json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"]
                                                          [f"{x}"]["id"]]["cause_effects"])):
                                if (json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]
                                                      ["id"]]["cause_reason"][y] == "global"):
                                    for z in range(json_str2[f"{self.level}-{self.stage}"]["basic"]["enemy"]
                                                   [self.difficult]):
                                        if self.blit[z]:
                                            if (json_str[
                                                json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"]
                                                [f"{z}"]["id"]]["Enemy_type"] in
                                                    json_str5[f"{json_str[json_str2[f"{self.level}-{self.stage}"][
                                                        f"entity{self.difficult}"
                                                    ][f"{x}"]["id"]]["cause_effects"][y]}"]
                                                    ["enemy_type"]):
                                                if (json_str[json_str2[f"{self.level}-{self.stage}"]
                                                                      [f"entity{self.difficult}"][f"{x}"]["id"]]
                                                                      ["cause_effects"][y] in self.effect[z]):
                                                    del self.effect[z][self.effect[z].index(json_str[
                                                                                                json_str2
                                                                                                [f"{self.level}-"
                                                                                                    f"{self.stage}"]
                                                                                                [
                                                                                                    f"entity"
                                                                                                    f"{self.difficult}"]
                                                                                                [f"{x}"]["id"]]
                                                                                            ["cause_effects"][y])]
                        continue
                    if not self.can_hit[x]:  # 无敌时间闪烁效果
                        self.blink[x] = not self.blink[x]
                    if (pygame.time.get_ticks() - self.total_frozen_time - self.invincible_time[x] -
                            self.game_start_time >= json_str[json_str2
                        [f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["id"]]["invincible_time"] and
                            not self.can_hit[x]):  # 无敌时间结束
                        self.can_hit[x] = True
                        self.blink[x] = False
                    self.last_can_hit[x] = self.can_hit[x]
                hp_len: int = (entity_rect.right - 5) - (entity_rect.left + 5)
                if self.last_hp[x] != self.hp[x]:
                    self.hit_last_hp[x] = self.last_hp[x]
                    self.hp_animation[x] = float(Decimal(str(max(self.last_hp[x], self.hp[x]))) -
                                                 Decimal(str(min(self.last_hp[x], self.hp[x]))))
                pygame.draw.line(screen, (0, 0, 0), (entity_rect.left, entity_rect.top - 10),  # 血条加载
                                 (entity_rect.right, entity_rect.top - 10), 12)
                if self.hp_animation[x] > 0:
                    pygame.draw.line(screen, (91, 0, 0), (entity_rect.left + 5 + hp_len * (
                            (self.hit_last_hp[x] - (float(Decimal(str(max(self.hit_last_hp[x], self.hp[x]))) -
                                                    Decimal(str(min(self.hit_last_hp[x], self.hp[x]))))
                                                    - self.hp_animation[x])) / json_str[json_str2[
                                                                                            f"{self.level}-{self.stage}"
                                                                                           ]
                                                                                           [f"entity{self.difficult}"]
                                                                                           [f"{x}"]["id"]]["HP"]),
                                                          entity_rect.top - 10),
                                     (entity_rect.left + 5 + hp_len * (self.hp[x] /
                                                                       json_str[
                                         json_str2[
                                            f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["id"]]
                                        ["HP"]),
                                      entity_rect.top - 10), 8)
                    self.hp_animation[x] -= 1
                if self.hp[x] / json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]
                                                  ["id"]]["HP"] > 0.8:  # 根据剩余血量占比更改血条颜色
                    pygame.draw.line(screen, (94, 203, 118), (entity_rect.left + 5, entity_rect.top - 10),
                                     (entity_rect.left + 5 + hp_len * (self.hp[x] / json_str[json_str2[
                                         f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["id"]]["HP"]),
                                      entity_rect.top - 10), 8)
                elif 0.3 < self.hp[x] / json_str[json_str2[f"{self.level}-{self.stage}"][f"entity{self.difficult}"]
                                                          [f"{x}"]["id"]]["HP"] <= 0.8:
                    pygame.draw.line(screen, (255, 240, 59), (entity_rect.left + 5, entity_rect.top - 10),
                                     (entity_rect.left + 5 + hp_len * (self.hp[x] / json_str[json_str2[
                                         f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["id"]]["HP"]),
                                      entity_rect.top - 10), 8)
                else:
                    pygame.draw.line(screen, (255, 52, 40), (entity_rect.left + 5, entity_rect.top - 10),
                                     (entity_rect.left + 5 + hp_len * (self.hp[x] / json_str[json_str2[
                                         f"{self.level}-{self.stage}"][f"entity{self.difficult}"][f"{x}"]["id"]]["HP"]),
                                      entity_rect.top - 10), 8)
            elif self.dead_temp[x] != 40 and self.is_dead[x] and can_active:
                self.dead(x)
            self.last_hp[x] = self.hp[x]
        for y in range(json_str2[f"{self.level}-{self.stage}"]["basic"]["popups"][self.difficult]):
            if self.enable_pop[y]:
                self.pop[y].draw()

    def dead(self, index: int) -> None:
        """播放死亡动画"""
        self.dead_temp[index] += 1
        if self.dead_temp[index] <= 10:
            images: any = pygame.transform.rotate(self.dead_image[index], -9 * self.dead_temp[index])
        else:
            images: any = pygame.transform.rotate(self.dead_image[index], -90)
            images.set_alpha(255 - 255 // 30 * (self.dead_temp[index] - 10))
        screen.blit(images, self.dead_rect[index])
        if self.dead_temp[index] == 40:
            if self.is_true_enemy[index]:
                self.basic_information[1] += 1


class DamageText:
    """在设置中开启时，命中敌人会在这里显示伤害数值"""

    def __init__(self) -> None:
        self.text_surface: list[any] = []
        self.text_rect: list[any] = []
        self.temp: list[int] = []

    def append_surface(self, text: any) -> None:
        """添加新的文本"""
        fonts: any = pygame.font.Font("assets/fonts/Text.TTF", 40)
        text_surface: any = fonts.render(str(text), True, (255, 255, 255))
        self.text_surface.append(text_surface)
        self.text_rect.append(pygame.mouse.get_pos())
        self.temp.append(0)

    def draw(self) -> None:
        """绘制文本"""
        continue_count: int = 0
        for y in range(len(self.text_surface)):
            x: int = y - continue_count
            if self.temp[x] != 30:
                self.temp[x] += 1
                self.text_surface[x].set_alpha(255 - self.temp[x] * (255 / 30))
                transparent_surface = pygame.Surface(self.text_surface[x].get_size(), pygame.SRCALPHA)
                transparent_surface.blit(self.text_surface[x], (0, 0))
                text_rect: any = transparent_surface.get_rect(center=(self.text_rect[x][0],
                                                                      self.text_rect[x][1] - self.temp[x] * 3))
                screen.blit(transparent_surface, text_rect)
            else:
                continue_count += 1
                del self.temp[x]
                del self.text_rect[x]
                del self.text_surface[x]
                continue


class GameGun:
    """显示游戏枪械"""

    def __init__(self, game_start_time: int, gun_type: int, shoot: list, account: int, basic_information: list,
                 mp_recover_time: int) -> None:
        self.approve_equipments: bool = False
        self.change_equipment: bool = False
        self.now_time: int = 0
        self.accumulation_time: int = 0
        self.last_active: bool = True
        self.total_frozen_time: int = 0
        self.start_frozen_time: int = 0
        self.temp_frozen_time: int = 0
        self.game_start_time: int = game_start_time
        self.indicator: str = ""
        self.account: int = account
        self.damage_multiple: any = None
        self.accumulation_now_time: int = 0
        self.cool_time: int = 0
        self.change_gun_action: bool = False
        self.cool_now_time: int = 0
        self.gun_type: int = gun_type
        self.reload: bool = False
        self.basic_information: list = basic_information
        self.shoot: list = shoot
        self.surplus_bullets: int = 0
        self.action: bool = False
        self.can_action: bool = True
        self.build_id: int = 0
        self.is_accumulation: bool = False
        self.bullets: Union[str, int] = basic_information[2]
        self.mp: int = basic_information[3]
        self.mp_start_recover_time: int = pygame.time.get_ticks() - self.total_frozen_time - self.game_start_time
        self.mp_recover_now_time: int = 0
        self.mp_recover_time: int = mp_recover_time
        self.damage: int = 1
        self.deploy_equipment: bool = False
        self.gun_rect = (0, 0, 0, 0)
        with open(f"data/User.json", encoding="UTF-8") as f:
            self.json_str: any = json.load(f)
            f.close()
        with open(f"data/Gun.json", encoding="UTF-8") as f:
            self.json_str2: any = json.load(f)
            f.close()
        with open(f"data/Build.json", encoding="UTF-8") as f:
            self.json_str3: any = json.load(f)
            f.close()
        self.surplus_bullets: int = 0
        self.audio1: any = pygame.mixer.Sound(sound[7])
        self.audio1.set_volume(volume)

    def draw(self, can_active: bool, deploy_numbers: int, deployment_ceiling: int) -> None:
        """绘制枪械"""
        self.indicator: str = image_usually_use[12]
        mouse_pos: tuple = pygame.mouse.get_pos()
        if self.reload:
            self.indicator: str = image_usually_use[13]
        if can_active:
            self.update(can_active, deploy_numbers, deployment_ceiling)
            if self.shoot[0]:  # 根据是否开枪加载图片
                background_image: any = (
                    pygame.image.load(f"assets/images/gun{self.gun_type}_active.png").convert_alpha())
                self.indicator: str = image_usually_use[14]
            else:
                background_image: any = (
                    pygame.image.load(f"assets/images/gun{self.gun_type}_inactive.png").convert_alpha())
            background_image: any = (
                pygame.transform.scale(background_image, (self.json_str2[f"{self.gun_type}"]["scale"],
                                                          self.json_str2[f"{self.gun_type}"]["scale"])))
            self.gun_rect = background_image.get_rect(center=mouse_pos)
            bullet_image: any = pygame.image.load(image_usually_use[15]).convert_alpha()  # 资源加载
            bullet_image: any = pygame.transform.scale(bullet_image, (30, 30))
            screen.blit(background_image, self.gun_rect)
            indicator_image: any = pygame.image.load(f"assets/images/{self.indicator}")
            indicator_image: any = pygame.transform.scale(indicator_image, (80, 80))
            indicator_image_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 80, 80)
            indicator_image_rect.center = (mouse_pos[0], mouse_pos[1])
            indicator_image_rect.left = mouse_pos[0] + self.json_str2[f"{self.gun_type}"]["scale"] // 2
            screen.blit(indicator_image, indicator_image_rect)  # 输出攻击指示器
            if self.json_str["setting"][self.account]["bullet_visible"]:  # 根据设置调整不同子弹显示方式
                bullets_text: any = (pygame.font.Font('assets/fonts/Text.TTF', 32).render
                                     (f"{self.surplus_bullets}/{self.bullets}", True, (255, 255, 255)))
                text_rect = bullets_text.get_rect()
                screen.blit(bullet_image, (mouse_pos[0] - (40 + text_rect.width) // 2,
                                           mouse_pos[1] + self.json_str2[f"{self.gun_type}"]["scale"] // 2))
                screen.blit(bullets_text, (mouse_pos[0] - (text_rect.width - 20) // 2,
                                           mouse_pos[1] + self.json_str2[f"{self.gun_type}"]["scale"] // 2))
            else:
                for x in range(self.surplus_bullets):
                    bullet_rect = pygame.Rect(0, mouse_pos[1] + 50, 30, 30)
                    bullet_rect.right = mouse_pos[0] + (30 * self.surplus_bullets / 2) - x * 30
                    screen.blit(bullet_image, bullet_rect)
            if self.json_str["equipment_level"][self.account][self.build_id] != -1:
                equipment_image: any = pygame.image.load(f"assets/images/{self.json_str3[f"{self.build_id}"]["name"]}"
                                                         f"{self.json_str3[f"{self.build_id}"]["Image_type"]}")
                cost_text: any = (pygame.font.Font('assets/fonts/Text.TTF', 32).render
                                  (f"费用:{self.basic_information[3]}/{self.json_str3[f"{self.build_id}"]["cost"]}",
                                   True, (255, 255, 255)))
                cost_text_rect = cost_text.get_rect(center=(mouse_pos[0], mouse_pos[1] + 20),
                                                    right=mouse_pos[0] - self.json_str2[f"{self.gun_type}"]
                                                    ["scale"] // 2)
                screen.blit(cost_text, cost_text_rect)
                deploy_text: any = (pygame.font.Font('assets/fonts/Text.TTF', 32).render
                                    (f"部署:{deploy_numbers}/{deployment_ceiling}",
                                     True, (255, 255, 255)))
                deploy_text_rect = deploy_text.get_rect(center=(mouse_pos[0], mouse_pos[1] + 45),
                                                        right=mouse_pos[0] - self.json_str2[f"{self.gun_type}"]
                                                                                           ["scale"] // 2)
                screen.blit(deploy_text, deploy_text_rect)
            else:
                equipment_image: any = pygame.image.load(image_usually_use[16])
            equipment_image: any = pygame.transform.scale(equipment_image, (60, 60))
            equipment_image_rect: any = equipment_image.get_rect(center=(mouse_pos[0], mouse_pos[1] - 20),
                                                                 right=mouse_pos[0] -
                                                                       self.json_str2[f"{self.gun_type}"]
                                                                                     ["scale"] // 2),
            screen.blit(equipment_image, equipment_image_rect)

    def update(self, can_active: bool, deploy_numbers: int, deployment_ceiling: int) -> None:
        """检测是否开枪"""
        if not self.shoot[0]:
            self.damage: int = 1
        else:
            self.damage: Decimal = Decimal(str(self.damage_multiple))
        self.approve_equipments: bool = False
        if can_active:
            self.mp_recover_now_time: int = (pygame.time.get_ticks() - self.game_start_time - self.total_frozen_time -
                                             self.mp_start_recover_time)
            if self.mp_recover_now_time >= self.mp_recover_time:
                self.mp += 1
                self.mp_start_recover_time: int = (pygame.time.get_ticks() - self.game_start_time -
                                                   self.total_frozen_time)
            self.basic_information[2] = self.bullets
            self.basic_information[3] = self.mp
            if self.last_active != can_active:
                self.total_frozen_time += self.temp_frozen_time  # 更新暂停时间
            for events in pygame.event.get():
                if events.type == MOUSEBUTTONDOWN and not self.reload:
                    if events.button == 4 or events.button == 5:
                        soundtrack.music_play(0, sound[8], False)
                        if events.button == 5:
                            if self.build_id + 1 != len(self.json_str3):
                                self.build_id += 1
                            else:
                                self.build_id: int = 0
                        elif events.button == 4:
                            if self.build_id != 0:
                                self.build_id -= 1
                            else:
                                self.build_id: int = len(self.json_str3) - 1
                if events.type == MOUSEBUTTONDOWN:  # 切枪
                    if events.button == 2:
                        soundtrack.music_play(0, sound[8], False)
                        if self.reload and self.surplus_bullets > 0:
                            self.reload: bool = False
                if events.type == pygame.MOUSEWHEEL and self.reload:  # 补充子弹
                    if isinstance(self.bullets, int) and self.bullets > 0:
                        soundtrack.music_play(0, sound[9], False)
                        self.surplus_bullets += 1
                        if isinstance(self.bullets, int):  # 根据是否是无限子弹区分不同处理方法
                            self.bullets -= 1
                        if (self.surplus_bullets == self.json_str2[f"{self.gun_type}"]["initial_bullet_cap"] +
                                self.json_str["gun_level"][self.account][self.gun_type] *
                                self.json_str2[f"{self.gun_type}"]["each_update_bullet_cap"]):
                            self.reload: bool = False
                    elif isinstance(self.bullets, str):
                        soundtrack.music_play(0, sound[9], False)
                        self.surplus_bullets += 1
                        if (self.surplus_bullets == self.json_str2[f"{self.gun_type}"]["initial_bullet_cap"] +
                                self.json_str["gun_level"][self.account][self.gun_type] *
                                self.json_str2[f"{self.gun_type}"]["each_update_bullet_cap"]):
                            self.reload: bool = False
            if (pygame.mouse.get_pressed()[0] and not self.shoot[0] and self.can_action and self.surplus_bullets > 0 and
                    not self.reload):  # 开枪
                self.can_action: bool = False
                if self.json_str2[f"{self.gun_type}"]["accumulation"] == 1:  # 如果是蓄力枪则开始蓄力，否则触发
                    self.audio1.play()
                    self.is_accumulation: bool = True
                    self.accumulation_now_time: int = (pygame.time.get_ticks() - self.game_start_time -
                                                       self.total_frozen_time)
                else:
                    if date == "04-01" or date == "05-13":
                        Music.music_play(0, sound[10], False)
                    else:
                        Music.music_play(0, f"{sound[10]}{self.gun_type}.wav", False)
                    self.surplus_bullets -= 1
                    self.cool_now_time: int = pygame.time.get_ticks() - self.game_start_time - self.total_frozen_time
                    self.now_time: int = pygame.time.get_ticks() - self.game_start_time - self.total_frozen_time
                    self.shoot[0] = True
                    self.action: bool = True
            if (self.is_accumulation and
                    (pygame.time.get_ticks() - self.game_start_time - self.accumulation_now_time -
                     self.total_frozen_time) / 100 >= self.json_str2[f"{self.gun_type}"]["max_accumulation"]):
                self.indicator: str = image_usually_use[17]  # 若伤害倍率满，则更改攻击指示器
            if self.is_accumulation and not pygame.mouse.get_pressed()[0]:  # 结束蓄力
                self.audio1.stop()
                if date == "04-01" or date == "05-13":
                    Music.music_play(0, sound[10], False)
                else:
                    Music.music_play(0, f"{sound[10]}{self.gun_type}.wav", False)
                self.surplus_bullets -= 1
                if ((pygame.time.get_ticks() - self.accumulation_now_time - self.total_frozen_time -
                        self.game_start_time) / 100 >= self.json_str2[f"{self.gun_type}"]["max_accumulation"]):
                    self.damage: float = self.json_str2[f"{self.gun_type}"]["max_accumulation"]
                else:
                    self.damage: Decimal = Decimal(str(pygame.time.get_ticks() - self.accumulation_now_time -
                                                       self.total_frozen_time - self.game_start_time)) / Decimal("100")
                    if self.damage < 1:
                        self.damage: int = 1
                self.now_time: int = pygame.time.get_ticks() - self.game_start_time - self.total_frozen_time
                self.can_action: bool = False
                self.cool_now_time: int = (pygame.time.get_ticks() - self.total_frozen_time - self.game_start_time
                                           + self.json_str2[f"{self.gun_type}"]["time/ms"])
                self.shoot[0] = True
                self.action: bool = True
                self.is_accumulation: bool = False
            if self.surplus_bullets == 0 and not self.shoot[0] and not self.is_accumulation:
                self.reload: bool = True
            if not self.shoot[0] and not self.can_action and not self.is_accumulation:  # 冷却时间
                self.indicator: str = image_usually_use[18]
                self.cool_time: int = pygame.time.get_ticks() - self.total_frozen_time - self.game_start_time
                if self.cool_time - self.cool_now_time >= self.json_str2[f"{self.gun_type}"]["cool_time/ms"]:
                    self.can_action: bool = True
            if self.action:  # 开枪状态
                timer: int = pygame.time.get_ticks() - self.game_start_time - self.total_frozen_time
                if timer - self.now_time >= self.json_str2[f"{self.gun_type}"]["time/ms"]:
                    self.shoot[0] = False
                    self.damage: float = 1
            if pygame.mouse.get_pressed()[2] and not self.deploy_equipment and deploy_numbers < deployment_ceiling:
                self.deploy_equipment: bool = True
                if (self.mp >= self.json_str3[f"{self.build_id}"]["cost"] and
                        self.json_str["equipment_level"][self.account][self.build_id] != -1):
                    self.mp -= self.json_str3[f"{self.build_id}"]["cost"]
                    self.approve_equipments: bool = True
                    Music.music_play(0, sound[11], False)
            elif not pygame.mouse.get_pressed()[2] and self.deploy_equipment:
                self.deploy_equipment: bool = False
            if self.shoot[0]:
                self.damage_multiple: Decimal = Decimal(str(self.damage))
                self.damage: Decimal = (Decimal(str(self.damage)) *
                                        (Decimal(str(self.json_str2[f"{self.gun_type}"]["basic_damage"])) +
                                         Decimal(str(self.json_str["EXP"][self.account] // 500))))
                if 0 in self.json_str["charm_use"][self.account]:
                    self.damage: Decimal = (Decimal(str(self.damage)) * Decimal(str(1.1)))
        else:
            if self.last_active != can_active:  # 控制暂停
                self.temp_frozen_time: int = 0
                self.start_frozen_time: int = pygame.time.get_ticks() - self.total_frozen_time - self.game_start_time
            self.temp_frozen_time: int = pygame.time.get_ticks() - self.start_frozen_time - self.game_start_time
        self.last_active: bool = can_active


class Equipments:
    """显示部署的设备"""

    def __init__(self, build_id: list[int], build_rect: list, build_active: list[bool]) -> None:
        self.build_id: list[int] = build_id
        self.build_rect: list = build_rect
        self.build_surface: list = []
        self.active: list[bool] = build_active

    def build_append(self, build_id: int) -> None:
        """新增设备"""
        with open("data/Build.json", encoding="UTF-8") as f:
            json_str: any = json.load(f)
            f.close()
        equipment_image: any = pygame.image.load(f"assets/images/{json_str[f"{build_id}"]["name"]}"
                                                 f"{json_str[f"{build_id}"]["Image_type"]}")
        equipment_image: any = pygame.transform.scale(equipment_image, (json_str[f"{build_id}"]["scale"][0],
                                                                        json_str[f"{build_id}"]["scale"][1]))
        self.build_id.append(build_id)
        self.build_surface.append(equipment_image)
        self.build_rect.append(self.build_surface[len(self.build_surface) - 1].get_rect(center=pygame.mouse.get_pos()))
        self.active.append(True)

    def draw(self) -> None:
        """绘制设备"""
        continue_count: int = 0
        for y in range(len(self.build_id)):
            x: int = y - continue_count
            if self.active[x]:
                screen.blit(self.build_surface[x], self.build_rect[x])
            else:
                continue_count += 1
                del self.build_id[x]
                del self.build_rect[x]
                del self.build_surface[x]
                del self.active[x]


class ScrollBackground:
    """可滚动的背景"""

    def __init__(self, img_path: str, screen_width: int, screen_height: int, alpha: int
                 ) -> None:
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.scroll_x: int = 0
        self.scroll_y: int = 0
        self.press_shift: bool = False
        self.horizontal_scroll: bool = False
        img: any = pygame.image.load(img_path)
        self.new_img: any = pygame.transform.scale(img, (screen_width, screen_height))
        self.new_img.set_alpha(alpha)

    def draw(self, scroll_speed: int) -> None:
        """绘制背景"""
        for events in pygame.event.get():
            # 检测 Shift 键是否按下
            if pygame.key.get_pressed()[K_LSHIFT] or pygame.key.get_pressed()[K_RSHIFT]:
                if not self.press_shift:
                    self.press_shift: bool = True
                    self.horizontal_scroll: bool = not self.horizontal_scroll
            else:
                self.press_shift: bool = False
            if events.type == MOUSEBUTTONDOWN:
                temp_horizontal_scroll: bool = self.horizontal_scroll
                if events.button == 4:
                    for x in range(scroll_speed):
                        if temp_horizontal_scroll and self.scroll_x > 0:
                            self.scroll_x -= 1
                        elif not temp_horizontal_scroll and self.scroll_y > 0:
                            self.scroll_y -= 1
                elif events.button == 5:
                    for x in range(scroll_speed):
                        if temp_horizontal_scroll and self.scroll_x < self.screen_width - width:
                            self.scroll_x += 1
                        elif not temp_horizontal_scroll and self.scroll_y < self.screen_height - height:
                            self.scroll_y += 1
        screen.blit(self.new_img, (0 - self.scroll_x, 0 - self.scroll_y))

    def scroll_bar(self) -> None:
        """显示滚动条"""
        scroll_len: list = [width // self.screen_width, height // self.screen_height]
        if self.screen_height > height:
            pygame.draw.line(screen, (80, 80, 80), (width, 0), (width, height), 20)
            pygame.draw.line(screen, (150, 150, 150), (width, self.scroll_y / (self.screen_height -
                                                                                height) * height),
                             (width, self.scroll_y / (self.screen_height - height) * height - scroll_len[1]),
                             20)
        if self.screen_width > width:
            pygame.draw.line(screen, (80, 80, 80), (0, height), (width, height), 20)
            pygame.draw.line(screen, (150, 150, 150), (self.scroll_x / (self.screen_width -
                                                                         width) * width, height),
                             (self.scroll_x / (self.screen_width - width) * width - scroll_len[0], height),
                             20)


class Pages:
    """游戏页面"""

    def __init__(self) -> None:
        with open("data/Idea.json", encoding="UTF-8") as f:
            json_str: any = json.load(f)
            f.close()
        self.click: any = Mouse(10)
        self.beginning: bool = True
        self.can_click: bool = False
        self.turn_page: int = 0
        self.account: int = json_str["log_user"]
        self.now_time: int = 0
        self.can_sleep: bool = True
        self.bg: any = DynamicBackground(image_usually_use[19], 40 if date == "04-01" or date == "05-13" else 5,
                                         width, height, False,
                                         False, True, False, 100)
        self.link_up: any = LinkUp(20, image_usually_use[20], image_usually_use[21])
        self.custom_text: any = CustomText(game_title, "assets/fonts/Title.TTF", 232,
                                           (100, 100, 100), [width // 2, 120], 255, 3, (1, 2), (1, 2), True, False,
                                           None)

    def sleep(self, timing: int) -> None:
        """在每次页面切换后停止一段时间各类交互键以避免误触"""
        if self.can_sleep:
            self.can_click: bool = False
            timer: int = pygame.time.get_ticks()
            if timer - self.now_time > timing:
                self.can_click: bool = True
                self.can_sleep: bool = False

    def logo_page(self) -> None:
        """基本信息显示"""
        global screen, volume, width, height
        pygame.mouse.set_visible(False)
        self.can_sleep: bool = True
        self.can_click: bool = False
        self.now_time: int = pygame.time.get_ticks()
        running: bool = True
        logo: any = Image(image_usually_use[23], 400, 400, 0,
                          0, 0, 0, False, False, (1, 4), (1, 2))
        mouse_img: any = Image(image_usually_use[24], 100, 170, 0,
                               0, 0, 0, False, False, (3, 4), (7, 16))
        text1: any = CustomText(game_text[0], "assets/fonts/Text.TTF", 40,
                                (255, 255, 255), [0, 0], 0, 0,
                                (3, 4), (10, 16), True, False, None)
        while running:
            if not self.link_up.can_exit:
                self.sleep(300)
            screen.fill((0, 0, 0))
            logo.draw()
            mouse_img.draw()
            text1.draw()
            if pygame.time.get_ticks() - self.now_time >= waiting_time[0]:
                with open("data/Idea.json", encoding="UTF-8") as c:
                    json_str1: any = json.load(c)
                    c.close()
                with open("data/User.json", encoding="UTF-8") as c:
                    json_str2: any = json.load(c)
                    c.close()
                if json_str1["log_user"] != -1:  # 重新登录上次开启游戏登录的用户
                    volume = json_str2["setting"][json_str1["log_user"]]["sound"]
                    if json_str2["setting"][json_str1["log_user"]]["full_screen"]:
                        width = full_width
                        height = full_height
                        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN, pygame.SRCALPHA)
                    else:
                        width = json_str1["Default_setting"]["width"]
                        height = json_str1["Default_setting"]["height"]
                        screen = pygame.display.set_mode((width, height), pygame.SRCALPHA)
                else:
                    volume = json_str1["Default_setting"]["volume"]
                    width = json_str1["Default_setting"]["width"]
                    height = json_str1["Default_setting"]["height"]
                    screen = pygame.display.set_mode((width, height), pygame.SRCALPHA)
                self.bg: any = DynamicBackground(image_usually_use[19],
                                                 40 if date == "04-01" or date == "05-13" else 5, width, height,
                                                 False,
                                                 False, True, False, 100)
                self.link_up: any = LinkUp(20, image_usually_use[20], image_usually_use[21])
                self.custom_text: any = CustomText(game_title, "assets/fonts/Title.TTF", 232,
                                                   (100, 100, 100), [width // 2, 120], 255, 3, (1, 2), (1, 2), True,
                                                   False,
                                                   None)
                self.home_page()
                return
            else:
                mouse_img.alpha += 10
                logo.alpha += 10
                text1.alpha += 10
            # 事件处理
            for events in pygame.event.get():
                if events.type == pygame.QUIT:  # 检测到窗口关闭事件
                    # 游戏结束,清理工作
                    pygame.quit()
                    exit()
            clock.tick(tick_frequency)
            # 绘图、更新屏幕等操作...
            pygame.display.flip()  # 更新整个待显示的Surface到屏幕上

    def home_page(self) -> None:
        """首页"""
        self.custom_text.pos[1] = 120
        self.now_time: int = pygame.time.get_ticks()
        self.can_sleep: bool = True
        self.can_click: bool = False
        rect_alpha: int = 255
        queue: list = []
        running: bool = True
        pop: any = PopupMessage(350, 100, image_usually_use[5], 800,
                                game_text[1],
                                (255, 255, 255), "assets/fonts/Text.TTF", 40, 100, 30,
                                False, 0, 0, image_usually_use[25], (60, 60), 25,
                                20, queue, 0, None, (False, False), (False, False))
        logo: any = Image(image_usually_use[23], 400, 400, 0,
                          0, 0, 255, False, False, (1, 4), (1, 2))
        mouse_img: any = Image(image_usually_use[24], 100, 170, 0,
                               0, 0, 255, False, False, (3, 4), (7, 16))
        text0: any = CustomText(game_text[0], "assets/fonts/Text.TTF", 40,
                                (255, 255, 255), [0, 0], 255, 0,
                                (3, 4), (10, 16), True, False, None)
        button1: any = Button("开始", 50, 230, 400, 100,
                              image_usually_use[0], image_usually_use[1],
                              image_usually_use[2], 1, 0, (1, 4), (4, 8))
        button2: any = Button("退出", 50, 350, 400, 100,
                              image_usually_use[0], image_usually_use[1],
                              image_usually_use[2], 1, 0, (3, 4), (4, 8))
        button3: any = Button("设置", 50, 590, 400, 100,
                              image_usually_use[0], image_usually_use[1],
                              image_usually_use[2], 1, 0, (3, 4), (6, 8))
        button4: any = Button("账户", 50, 470, 400, 100,
                              image_usually_use[0], image_usually_use[1],
                              image_usually_use[2], 1, 0, (1, 4), (6, 8))
        text1: any = CustomText(f"{datetime.now().strftime("%Y")} Code&Release", "assets/fonts/Text.TTF", 40,
                                (255, 255, 255), [0, height // 40 * 39], 255, 0,
                                (0, 20), (39, 40), False, False, None)
        text2: any = CustomText(f"{game_version}", "assets/fonts/Text.TTF", 40,
                                (255, 255, 255), [width // 20 * 20, height // 40 * 39], 255,
                                0, (20, 20), (39, 40), False, True, None)
        if date == "04-01" or date == "05-13" or self.account != -1:
            pop.activate()
        if self.account == -1:
            button4.x_grid = (2, 4)
        while running:
            if not self.link_up.can_exit:
                self.sleep(300)
            screen.fill((200, 200, 200))
            self.bg.update()
            self.bg.draw()
            if button1.draw(50, (180, 180, 180), (255, 255, 255),
                            (180, 180, 180), self.can_click) and not self.beginning:
                self.turn_page: int = 0
                if self.account == -1:
                    self.choose_account_page()
                else:
                    self.link_up.activate()
                    self.can_click: bool = False
            if button2.draw(50, (180, 180, 180), (255, 255, 255),
                            (180, 180, 180), self.can_click) and not self.beginning:
                # 游戏结束,清理工作
                pygame.quit()
                exit()
            if self.account != -1:
                if button3.draw(50, (180, 180, 180), (255, 255, 255),
                                (180, 180, 180), self.can_click) and not self.beginning:
                    self.setting_page()
                    return
            if button4.draw(50, (180, 180, 180), (255, 255, 255),
                            (180, 180, 180), self.can_click) and not self.beginning:
                self.turn_page: int = -1
                self.choose_account_page()
                return
            self.custom_text.draw()
            text1.draw()
            text2.draw()
            self.click.click()
            if date == "04-01" or date == "05-13" or self.account != -1:
                pop.draw()
            if self.link_up.can_exit:
                if self.turn_page == 0:
                    self.map_page()
                    return
                else:
                    self.link_up.exit()
            else:
                self.link_up.access(100)
            if self.beginning:
                # 在 Surface 上绘制一个透明的矩形
                rect_surface: any = pygame.Surface((width, height), pygame.SRCALPHA)
                pygame.draw.rect(rect_surface, (0, 0, 0, rect_alpha), (0, 0, width, height))
                screen.blit(rect_surface, (0, 0))
                logo.draw()
                mouse_img.draw()
                text0.draw()
                if logo.alpha > 0:
                    logo.alpha -= 26
                    mouse_img.alpha -= 26
                    text0.alpha -= 26
                    rect_alpha -= 26
                    if logo.alpha < 0:
                        logo.alpha = 0
                        mouse_img.alpha = 0
                        text0.alpha = 0
                        rect_alpha: int = 0
                        self.beginning: bool = False
            # 事件处理
            for events in pygame.event.get():
                if events.type == pygame.QUIT:  # 检测到窗口关闭事件
                    # 游戏结束,清理工作
                    pygame.quit()
                    exit()
                elif events.type == pygame.MOUSEBUTTONDOWN:
                    self.click.click_activate()
            clock.tick(tick_frequency)
            # 绘图、更新屏幕等操作...
            pygame.display.flip()  # 更新整个待显示的Surface到屏幕上

    def setting_page(self) -> None:
        """设置部分功能的页面"""
        global screen, width, height, volume
        self.now_time: int = pygame.time.get_ticks()
        self.can_sleep: bool = True
        self.can_click: bool = False
        queue: list = []
        running: bool = True
        with open(f"data/User.json", encoding="UTF-8") as f:
            json_str: any = json.load(f)
            f.close()
        with open(f"data/Idea.json", encoding="UTF-8") as f:
            json_str3: any = json.load(f)
            f.close()
        with open(f"data/Setting.json", encoding="UTF-8") as f:
            json_str4: any = json.load(f)
            f.close()
        scroll: any = ScrollBackground(image_usually_use[19], width, width // 8 * len(json_str4), 0)
        setting: list = []
        setting_text: list = []
        for x in range(len(json_str4)):
            if isinstance(json_str4[f"{x}"]["default"], bool):
                setting.append(Switch(170, 90, width // 4 * 3, height // 8 * (x + 3),
                               image_usually_use[6], image_usually_use[7],
                               json_str["setting"][self.account][json_str4[f"{x}"]["describe"]],
                                      False, 1, (3, 4), ((x + 3), 8), 255))
                setting_text.append(CustomText(json_str4[f"{x}"]["Chinese_describe"], "assets/fonts/Text.TTF", 50,
                                    (255, 255, 255), [width // 6, height // 8 * (x + 3)], 255, 1,
                                               (1, 6), ((x + 3), 8), False, False, 12))
            elif isinstance(json_str4[f"{x}"]["default"], (float, int)):
                setting.append(CustomInputBox(f"{json_str4[f"{x}"]["Chinese_describe"]}"
                                              f"{json_str["setting"][self.account][json_str4[f"{x}"]["describe"]]}"
                                              f"({json_str4[f"{x}"]["lower_limit"]}~"
                                              f"{json_str4[f"{x}"]["upper_limit"]})",
                                              1, None, None, (255, 255, 255),
                                              (100, 100, 100), "assets/fonts/Text.TTF", image_usually_use[3],
                                              image_usually_use[4], 950, 50, 40, 170,
                                              height // 8 * (x + 3), 25, (12, 128, 178), 4,
                                              300, False, self.can_click, (1, 2), ((x + 3), 8)))
                setting_text.append("")
        pop: any = PopupMessage(350, 100, image_usually_use[5], 500,
                                "保存成功", (255, 255, 255), "assets/fonts/Text.TTF", 40, 100, 30,
                                False, 0, 0, image_usually_use[26], (60, 60), 25, 20, queue, 0, None, (False, False),
                                (False, False))
        pop2: any = PopupMessage(350, 100, image_usually_use[5], 500,
                                 "保存出错", (255, 255, 255), "assets/fonts/Text.TTF",
                                 40, 100, 30,
                                 False, 0, 0, image_usually_use[27], (60, 60), 25, 20, queue, 1, None,
                                 (False, False), (False, False))
        button1: any = Button("退出", 200, 590, 400, 100,
                              image_usually_use[0], image_usually_use[1],
                              image_usually_use[2], 1, 0, (2, 8), (30, 32))
        button2: any = Button("保存", 700, 590, 400, 100,
                              image_usually_use[0], image_usually_use[1],
                              image_usually_use[2], 1, 0, (6, 8), (30, 32))
        while running:
            self.sleep(300)
            self.custom_text.pos[1] = 120 - scroll.scroll_y
            for x in range(len(json_str4)):
                setting[x].y = height // 8 * (x + 3) - scroll.scroll_y
                if not isinstance(setting_text[x], str):
                    setting_text[x].pos[1] = height // 8 * (x + 3) - scroll.scroll_y
            screen.fill((200, 200, 200))
            self.bg.update()
            self.bg.draw()
            for x in range(len(json_str4)):
                if isinstance(setting_text[x], str):
                    if setting[x].active:
                        setting[x].cursor_update()
                    else:
                        setting[x].cursor_visible = False
                else:
                    setting_text[x].draw()
                    setting[x].draw(self.can_click)
            self.custom_text.draw()
            # 事件处理
            for events in pygame.event.get():
                if events.type == pygame.QUIT:  # 检测到窗口关闭事件
                    # 游戏结束,清理工作
                    pygame.quit()
                    exit()
                elif events.type == pygame.MOUSEBUTTONDOWN:
                    self.click.click_activate()
                for x in range(len(json_str4)):
                    if isinstance(setting_text[x], str):
                        setting[x].handle_event(events, self.can_click)
            for x in range(len(json_str4)):
                if isinstance(setting_text[x], str):
                    setting[x].draw()  # 绘制输入框
            if button1.draw(50, (180, 180, 180), (255, 255, 255),
                            (180, 180, 180), self.can_click):
                self.home_page()
                return
            if button2.draw(50, (180, 180, 180), (255, 255, 255),
                            (180, 180, 180), self.can_click):
                try:
                    for x in range(len(json_str4)):
                        if isinstance(setting_text[x], str):
                            if setting[x].text != "":
                                if isinstance(json_str4[f"{x}"]["default"], int):
                                    if (json_str4[f"{x}"]["lower_limit"] <= int(setting[x].text) <=
                                            json_str4[f"{x}"]["upper_limit"]):
                                        json_str["setting"][self.account][json_str4[f"{x}"]["describe"]] = (
                                            int(setting[x].text))
                                        setting[x].default_text = (f"{json_str4[f"{x}"]["Chinese_describe"]}"
                                                                   f"{json_str["setting"][self.account][
                                                                       json_str4[f"{x}"]["describe"]]}"
                                                                   f"({json_str4[f"{x}"]["lower_limit"]}~"
                                                                   f"{json_str4[f"{x}"]["upper_limit"]})")
                                else:
                                    if (json_str4[f"{x}"]["lower_limit"] <= float(setting[x].text) <=
                                            json_str4[f"{x}"]["upper_limit"]):
                                        json_str["setting"][self.account][json_str4[f"{x}"]["describe"]] = (
                                            float(setting[x].text))
                                        setting[x].default_text = (f"{json_str4[f"{x}"]["Chinese_describe"]}"
                                                                   f"{json_str["setting"][self.account][
                                                                       json_str4[f"{x}"]["describe"]]}"
                                                                   f"({json_str4[f"{x}"]["lower_limit"]}~"
                                                                   f"{json_str4[f"{x}"]["upper_limit"]})")
                                        if json_str4[f"{x}"]["describe"] == "sound":
                                            volume = float(setting[x].text)
                                setting[x].delete()
                except ValueError:
                    pop2.activate()
                    for x in range(len(json_str4)):
                        if isinstance(setting_text[x], str):
                            setting[x].delete()
                else:
                    for x in range(len(json_str4)):
                        if not isinstance(setting_text[x], str):
                            json_str["setting"][self.account][json_str4[f"{x}"]["describe"]] = setting[x].activate
                    if (json_str["setting"][self.account]["full_screen"] and
                            width == json_str3["Default_setting"]["width"] and
                            height == json_str3["Default_setting"]["height"]):
                        width = full_width
                        height = full_height
                        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN, pygame.SRCALPHA)
                        self.bg: any = DynamicBackground(image_usually_use[19],
                                                         40 if date == "04-01" or date == "05-13" else 5, width, height,
                                                         False,
                                                         False, True, False, 100)
                        self.custom_text: any = CustomText(game_title, "assets/fonts/Title.TTF", 232,
                                                           (100, 100, 100), [width // 2, 120], 255, 3, (1, 2), (1, 2),
                                                           True,
                                                           False,
                                                           None)
                    elif (not json_str["setting"][self.account]["full_screen"] and
                              width != json_str3["Default_setting"]["width"] and
                              height != json_str3["Default_setting"]["height"]):
                        width = json_str3["Default_setting"]["width"]
                        height = json_str3["Default_setting"]["height"]
                        screen = pygame.display.set_mode((width, height), pygame.SRCALPHA)
                        self.bg: any = DynamicBackground(image_usually_use[19],
                                                         40 if date == "04-01" or date == "05-13" else 5, width, height,
                                                         False,
                                                         False, True, False, 100)
                        self.custom_text: any = CustomText(game_title, "assets/fonts/Title.TTF", 232,
                                                           (100, 100, 100), [width // 2, 120], 255, 3, (1, 2), (1, 2),
                                                           True,
                                                           False,
                                                           None)
                    f: any = open(f"data/User.json", "w", encoding="UTF-8")
                    json_str2: str = json.dumps(json_str, ensure_ascii=False, indent=4)
                    f.write(json_str2)
                    f.flush()
                    f.close()
                    pop.activate()
            scroll.draw(json_str["setting"][self.account]["scroll_speed"])
            pop.draw()
            pop2.draw()
            scroll.scroll_bar()
            self.click.click()
            clock.tick(tick_frequency)
            # 绘图、更新屏幕等操作...
            pygame.display.flip()  # 更新整个待显示的Surface到屏幕上

    def choose_account_page(self) -> None:
        """选择一个账户并进入游戏"""
        global width, height, screen, volume
        self.now_time: int = pygame.time.get_ticks()
        self.can_sleep: bool = True
        self.can_click: bool = False
        queue: list = []
        running: bool = True
        with open("data/User.json", encoding="UTF-8") as f:
            json_str: any = json.load(f)
            f.close()
        with open("data/Idea.json", encoding="UTF-8") as f:
            json_str2: any = json.load(f)
            f.close()
        pop: any = PopupMessage(350, 100, image_usually_use[5], 500,
                                "账户不存在", (255, 255, 255), "assets/fonts/Text.TTF", 40, 100, 30,
                                False, 0, 0, image_usually_use[27], (60, 60), 25, 20,
                                queue, 0, None, (False, False), (False, False))
        pop2: any = PopupMessage(350, 100, image_usually_use[5], 500,
                                 "密码错误", (255, 255, 255), "assets/fonts/Text.TTF", 40, 100, 30,
                                 False, 0, 0, image_usually_use[27], (60, 60), 25, 20,
                                 queue, 1, None, (False, False), (False, False))
        button1: any = Button("登录", 150, 380, 400, 100, image_usually_use[0], image_usually_use[1],
                              image_usually_use[2], 1, 0, (2, 8), (5, 8))
        button2: any = Button("注册", 750, 380, 400, 100, image_usually_use[0], image_usually_use[1],
                              image_usually_use[2], 1, 0, (6, 8), (5, 8))
        button3: any = Button("返回", 150, 550, 400, 100, image_usually_use[0], image_usually_use[1],
                              image_usually_use[2], 1, 0, (2, 8), (7, 8))
        if self.turn_page != -1:
            button3.x_grid = (1, 2)
        input_box1: any = CustomInputBox("输入账户名", 0, None, None, (255, 255, 255), (100, 100, 100),
                                         "assets/fonts/Text.TTF", image_usually_use[3],
                                         image_usually_use[4], 950, 50, 40, 170, 250, 25,
                                         (12, 128, 178), 4,
                                         300, False, self.can_click, (1, 2), (3, 8))
        input_box2: any = CustomInputBox("输入账户密码", 0, None, None, (255, 255, 255), (100, 100, 100),
                                         "assets/fonts/Text.TTF", image_usually_use[3],
                                         image_usually_use[4], 950, 50, 40, 170, 320, 25,
                                         (12, 128, 178), 4,
                                         300, False, self.can_click, (1, 2), (4, 8))
        if self.turn_page == -1:
            button4: any = Button("退出登录", 750, 550, 400, 100, image_usually_use[0], image_usually_use[1],
                                  image_usually_use[2], 1, 0, (6, 8), (7, 8))
            pop3: any = PopupMessage(350, 100, image_usually_use[5], 500,
                                     "已退出登录", (255, 255, 255), "assets/fonts/Text.TTF", 40, 100, 30,
                                     False, 0, 0, image_usually_use[26], (60, 60), 25, 20,
                                     queue, 2, None, (False, False), (False, False))
            pop4: any = PopupMessage(350, 100, image_usually_use[5], 500,
                                     "登录成功", (255, 255, 255), "assets/fonts/Text.TTF", 40, 100, 30,
                                     False, 0, 0, image_usually_use[26], (60, 60), 25, 20,
                                     queue, 3, None, (False, False), (False, False))
        else:
            button4: any = ""
            pop3: any = ""
            pop4: any = ""
        while running:
            self.sleep(300)
            screen.fill((200, 200, 200))
            self.bg.update()
            self.bg.draw()
            if input_box1.active:
                input_box1.cursor_update()
            else:
                input_box1.cursor_visible = False
            if input_box2.active:
                input_box2.cursor_update()
            else:
                input_box2.cursor_visible = False
            self.custom_text.draw()
            if (button1.draw(50, (180, 180, 180), (255, 255, 255),
                             (180, 180, 180), self.can_click)
                    and not self.link_up.active):
                try:
                    name_index: int = json_str["name"].index(input_box1.text)
                except ValueError:
                    pop.activate()
                else:
                    if json_str["password"][name_index] == input_box2.text:
                        if (json_str["setting"][name_index]["full_screen"] and
                                width == json_str2["Default_setting"]["width"] and
                                height == json_str2["Default_setting"]["height"]):
                            width = full_width
                            height = full_height
                            screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN, pygame.SRCALPHA)
                            self.bg: any = DynamicBackground(image_usually_use[19],
                                                             40 if date == "04-01" or date == "05-13" else 5, width,
                                                             height,
                                                             False,
                                                             False, True, False, 100)
                            self.custom_text: any = CustomText(game_title, "assets/fonts/Title.TTF", 232,
                                                               (100, 100, 100), [width // 2, 120], 255, 3, (1, 2),
                                                               (1, 2),
                                                               True,
                                                               False,
                                                               None)
                        elif (not json_str["setting"][name_index]["full_screen"] and
                              width != json_str2["Default_setting"]["width"] and
                              height != json_str2["Default_setting"]["height"]):
                            width = json_str2["Default_setting"]["width"]
                            height = json_str2["Default_setting"]["height"]
                            screen = pygame.display.set_mode((width, height), pygame.SRCALPHA)
                            self.bg: any = DynamicBackground(image_usually_use[19],
                                                             40 if date == "04-01" or date == "05-13" else 5, width,
                                                             height,
                                                             False,
                                                             False, True, False, 100)
                            self.custom_text: any = CustomText(game_title, "assets/fonts/Title.TTF", 232,
                                                               (100, 100, 100), [width // 2, 120], 255, 3, (1, 2),
                                                               (1, 2),
                                                               True,
                                                               False,
                                                               None)
                        self.account: int = name_index
                        volume = json_str["setting"][self.account]["sound"]
                        json_str2["log_user"] = name_index
                        f: any = open("data/Idea.json", "w", encoding="UTF-8")
                        json_str3: any = json.dumps(json_str2, ensure_ascii=False, indent=4)
                        f.write(json_str3)
                        f.flush()
                        f.close()
                        if self.turn_page != -1:
                            self.link_up.activate()
                        else:
                            pop4.activate()
                    else:
                        pop2.activate()
            if (button2.draw(50, (180, 180, 180), (255, 255, 255),
                             (180, 180, 180), self.can_click)
                    and not self.link_up.active):
                self.account_page()
                return
            if (button3.draw(50, (180, 180, 180), (255, 255, 255),
                             (180, 180, 180), self.can_click)
                    and not self.link_up.active):
                self.home_page()
                return
            if self.turn_page == -1:
                if (button4.draw(50, (180, 180, 180), (255, 255, 255),
                                 (180, 180, 180), self.can_click)
                        and not self.link_up.active):
                    volume = json_str2["Default_setting"]["volume"]
                    if self.account != -1:
                        if json_str["setting"][self.account]["full_screen"]:
                            width = json_str2["Default_setting"]["width"]
                            height = json_str2["Default_setting"]["height"]
                            screen = pygame.display.set_mode((width, height), pygame.SRCALPHA)
                            self.bg: any = DynamicBackground(image_usually_use[19],
                                                             40 if date == "04-01" or date == "05-13" else 5, width,
                                                             height,
                                                             False,
                                                             False, True, False, 100)
                            self.custom_text: any = CustomText(game_title, "assets/fonts/Title.TTF", 232,
                                                               (100, 100, 100), [width // 2, 120], 255, 3, (1, 2),
                                                               (1, 2),
                                                               True,
                                                               False,
                                                               None)
                    self.account: int = -1
                    json_str2["log_user"] = -1
                    f: any = open("data/Idea.json", "w", encoding="UTF-8")
                    json_str3: any = json.dumps(json_str2, ensure_ascii=False, indent=4)
                    f.write(json_str3)
                    f.flush()
                    f.close()
                    pop3.activate()
            # 事件处理
            for events in pygame.event.get():
                # 判断事件类型是否为QUIT
                if events.type == QUIT:
                    # 游戏结束,清理工作
                    pygame.quit()
                    exit()
                elif events.type == pygame.MOUSEBUTTONDOWN:
                    self.click.click_activate()
                input_box1.handle_event(events, self.can_click)
                input_box2.handle_event(events, self.can_click)
            input_box1.draw()  # 绘制输入框
            input_box2.draw()
            pop.draw()
            pop2.draw()
            if self.turn_page == -1:
                pop3.draw()
                pop4.draw()
            self.click.click()
            if self.link_up.can_exit:
                if self.turn_page == 0:
                    self.map_page()
                    return
                else:
                    self.link_up.exit()
            else:
                self.link_up.access(100)
            # 更新屏幕
            pygame.display.flip()
            clock.tick(tick_frequency)

    def account_page(self) -> None:
        """进行账号注册的界面"""
        self.now_time: int = pygame.time.get_ticks()
        self.can_sleep: bool = True
        self.can_click: bool = False
        queue: list = []
        running: bool = True
        pop: any = PopupMessage(350, 100, image_usually_use[5], 500,
                                "注册成功", (255, 255, 255), "assets/fonts/Text.TTF",
                                40, 100, 30,
                                False, 0, 0, image_usually_use[26], (60, 60), 25, 20, queue, 0, None, (False, False),
                                (False, False))
        pop2: any = PopupMessage(350, 100, image_usually_use[5], 500,
                                 "不能使用这个名称", (255, 255, 255),
                                 "assets/fonts/Text.TTF", 32, 90, 35,
                                 False, 0, 0, image_usually_use[27], (60, 60), 25, 20, queue, 1, None,
                                 (False, False), (False, False))
        button1: any = Button("注册", 50, 460, 400, 100, image_usually_use[0], image_usually_use[1],
                              image_usually_use[2], 1, 0, (1, 4), (7, 8))
        button2: any = Button("返回", 50, 565, 400, 100, image_usually_use[0], image_usually_use[1],
                              image_usually_use[2], 1, 0, (3, 4), (7, 8))
        input_box1: any = CustomInputBox("账户名", 0, None, None, (255, 255, 255), (100, 100, 100),
                                         "assets/fonts/Text.TTF", image_usually_use[3],
                                         image_usually_use[4], 950, 50, 40, 170, 250, 25,
                                         (12, 128, 178), 4,
                                         300, False, self.can_click, (1, 2), (6, 16))
        input_box2: any = CustomInputBox("账户密码", 0, None, None, (255, 255, 255), (100, 100, 100),
                                         "assets/fonts/Text.TTF", image_usually_use[3],
                                         image_usually_use[4], 950, 50, 40, 170, 320, 25,
                                         (12, 128, 178), 4,
                                         300, False, self.can_click, (1, 2), (8, 16))
        while running:
            self.sleep(300)
            screen.fill((200, 200, 200))
            self.bg.update()
            self.bg.draw()
            if input_box1.active:
                input_box1.cursor_update()
            else:
                input_box1.cursor_visible = False
            if input_box2.active:
                input_box2.cursor_update()
            else:
                input_box2.cursor_visible = False
            self.custom_text.draw()
            if button1.draw(50, (180, 180, 180), (255, 255, 255),
                            (180, 180, 180), self.can_click) and pop.x == 0:
                f: any = open("data/User.json", encoding="UTF-8")
                json_str4: any = json.load(f)
                f.close()
                if input_box1.text != "" and input_box1.text not in json_str4["name"]:
                    f: any = open("data/Level.json", encoding="UTF-8")
                    json_str2: any = json.load(f)
                    f.close()
                    f: any = open("data/Gun.json", encoding="UTF-8")
                    json_str3: any = json.load(f)
                    f.close()
                    f: any = open("data/Build.json", encoding="UTF-8")
                    json_str5: any = json.load(f)
                    f.close()
                    f: any = open("data/Charm.json", encoding="UTF-8")
                    json_str6: any = json.load(f)
                    f.close()
                    f: any = open("data/Setting.json", encoding="UTF-8")
                    json_str: any = json.load(f)
                    f.close()
                    json_str4["name"].append(input_box1.text)
                    json_str4["password"].append(input_box2.text)
                    json_str4["level"].append(1)
                    json_str4["EXP"].append(0)
                    json_str4["progress"].append([])
                    json_str4["progress"][len(json_str4["progress"]) - 1].append(0)
                    for x in range(len(json_str2)):
                        for y in range(len(json_str2[f"Level{x + 1}"]) - 1):
                            json_str4["progress"][len(json_str4["progress"]) - 1].append(-1)
                    json_str4["gun_level"].append([])
                    for x in range(len(json_str3)):
                        json_str4["gun_level"][len(json_str4["gun_level"]) - 1].append(0)
                    json_str4["setting"].append({})
                    for x in range(len(json_str)):
                        json_str4["setting"][len(json_str4["setting"]) - 1][f"{json_str[f"{x}"]["describe"]}"] = (
                            json_str[f"{x}"]["default"])
                    json_str4["equipment_level"].append([])
                    for x in range(len(json_str5)):
                        json_str4["equipment_level"][len(json_str4["equipment_level"]) - 1].append(-1)
                    json_str4["charm_slot"].append(1)
                    json_str4["charm"].append([])
                    for x in range(len(json_str6)):
                        json_str4["charm"][len(json_str4["charm"]) - 1].append(-1)
                    json_str4["charm_use"].append([])
                    json_str4: any = json.dumps(json_str4, ensure_ascii=False, indent=4)
                    f: any = open(f"data/User.json", "w", encoding="UTF-8")
                    f.write(json_str4)
                    f.flush()
                    f.close()
                    pop.activate()
                else:
                    pop2.activate()
            if button2.draw(50, (180, 180, 180), (255, 255, 255),
                            (180, 180, 180), self.can_click):
                self.choose_account_page()
                return
            # 事件处理
            for events in pygame.event.get():
                # 判断事件类型是否为QUIT
                if events.type == QUIT:
                    # 游戏结束,清理工作
                    pygame.quit()
                    exit()
                elif events.type == pygame.MOUSEBUTTONDOWN:
                    self.click.click_activate()
                input_box1.handle_event(events, self.can_click)
                input_box2.handle_event(events, self.can_click)
            input_box1.draw()  # 绘制输入框
            input_box2.draw()
            if pop.x == 20:
                self.choose_account_page()
                return
            else:
                pop.draw()
            pop2.draw()
            self.click.click()
            # 更新屏幕
            pygame.display.flip()
            clock.tick(tick_frequency)

    def map_page(self) -> None:
        """加载游戏地图及关卡"""
        with open(f"data/Idea.json", encoding="UTF-8") as f:
            json_str3: any = json.load(f)
            f.close()
        multiple_height: float = height / json_str3["Default_setting"]["balance_height"]
        multiple_width: float = width / json_str3["Default_setting"]["balance_width"]
        self.now_time: int = pygame.time.get_ticks()
        self.can_sleep: bool = True
        self.can_click: bool = False
        draw_rect: bool = False
        change_page: bool = False
        rect_alpha: int = 0
        with open(f"data/User.json", encoding="UTF-8") as f:
            json_str: any = json.load(f)
            f.close()
        with open(f"data/Level.json", encoding="UTF-8") as f:
            json_str2: any = json.load(f)
            f.close()
        running: bool = True
        level: list = []
        for x in range(len(json_str2[f"Level{json_str["level"][self.account]}"])):
            select_icon: str = ""
            if (
                    json_str["progress"][self.account]
                    [
                        json_str2[f"Level{json_str['level'][self.account]}"]
                        [f"{x}"]["Level_id"]
                    ] == -1
            ):
                select_icon: str = "8"
            else:
                if json_str2[f"Level{json_str["level"][self.account]}"][f"{x}"]["Type"] == 0:
                    if (
                            json_str["progress"][self.account]
                            [
                                json_str2[f"Level{json_str["level"][self.account]}"]
                                [f"{x}"]["Level_id"]
                            ] == 0
                    ):
                        select_icon: str = "1"
                    elif (
                            json_str["progress"][self.account]
                            [
                                json_str2[f"Level{json_str["level"][self.account]}"]
                                [f"{x}"]["Level_id"]
                            ] == 1
                    ):
                        select_icon: str = "2"
                    elif (
                            json_str["progress"][self.account]
                            [
                                json_str2[f"Level{json_str["level"][self.account]}"]
                                [f"{x}"]["Level_id"]
                            ] == 2
                    ):
                        select_icon: str = "3"
                    elif (
                            json_str["progress"][self.account]
                            [
                                json_str2[f"Level{json_str["level"][self.account]}"]
                                [f"{x}"]["Level_id"]
                            ] == 3
                    ):
                        select_icon: str = "4"
                elif json_str2[f"Level{json_str["level"][self.account]}"][f"{x}"]["Type"] == 1:
                    if (
                            json_str["progress"][self.account]
                            [
                                json_str2[f"Level{json_str["level"][self.account]}"]
                                [f"{x}"]["Level_id"]
                            ] == 0
                    ):
                        select_icon: str = "5"
                    if (
                            json_str["progress"][self.account]
                            [
                                json_str2[f"Level{json_str["level"][self.account]}"]
                                [f"{x}"]["Level_id"]
                            ] == 3
                    ):
                        select_icon: str = "6"
                elif (json_str2[f"Level{json_str["level"][self.account]}"][f"{x}"]["Type"] == 2 and
                      json_str["progress"][self.account]
                      [
                          json_str2[f"Level{json_str["level"][self.account]}"]
                          [f"{x}"]["Level_id"]
                      ] == 0
                      ):
                    select_icon: str = "7"
            if date == "04-01" or date == "05-13":
                level.append(Switch(80, 80, int(Decimal(str(json_str2[f"Level{json_str["level"]
                                                                                             [self.account]}"][f"{x}"]
                                                                                             ["Position"][0])) *
                                                Decimal(str(multiple_width))),
                                    int(Decimal(str(json_str2[f"Level{json_str["level"][self.account]}"][f"{x}"]
                                                             ["Position"][1])) * Decimal(str(multiple_height))),
                                    image_usually_use[7], image_usually_use[7], False,
                                    True, 3, (1, 2), (1, 2), 255))
            else:
                level.append(Switch(80, 80, int(Decimal(str(json_str2[f"Level{json_str["level"]
                                                                                             [self.account]}"][f"{x}"]
                                                                                             ["Position"][0])) *
                                                Decimal(str(multiple_width))),
                                    int(Decimal(str(json_str2[f"Level{json_str["level"][self.account]}"][f"{x}"]
                                                             ["Position"][1])) * Decimal(str(multiple_height))),
                                    f"assets/images/{select_icon}.png", f"assets/images/{select_icon}.png", False,
                                    True, 3, (1, 2), (1, 2), 255))
        if date == "04-01" or date == "05-13":
            Image(image_usually_use[28], width, height, 0, 0, 0, 255, False, False, (1, 2), (1, 2)).draw()
        else:
            Image(f"{image_usually_use[28]}{json_str["level"][self.account]}.jpg", width, height, 0,
                  0, 0, 255, False, False, (1, 2), (1, 2)).draw()
        button1: any = Button("", 120, 50, 80, 80, image_usually_use[29],
                              image_usually_use[30], image_usually_use[31],
                              1, 1, (2, 8), (1, 2))
        button2: any = Button("", 120, 50, 80, 80, image_usually_use[32],
                              image_usually_use[33], image_usually_use[34],
                              1, 1, (3, 8), (1, 2))
        background_image: any = pygame.image.load(image_usually_use[35]).convert_alpha()
        background_image: any = pygame.transform.scale(background_image,
                                                       (width, 100))
        background_image: any = pygame.transform.flip(background_image, False, True)
        temp_can_click: list = [True]
        choose_level: int = 0
        while running:
            if not self.link_up.can_exit:
                self.sleep(300)
            screen.fill((200, 200, 200))
            if date == "04-01" or date == "05-13":
                image1: any = Image(image_usually_use[28], width, height, 0, 0, 0,
                                    255, False, False, (1, 2), (1, 2))
            else:
                image1: any = Image(f"{image_usually_use[28]}{json_str["level"][self.account]}.jpg",
                                    width, height, 0, 0, 0,
                                    255, False, False, (1, 2), (1, 2))
            image1.draw()
            screen.blit(background_image, (0, 0))
            if button1.draw(50, (180, 180, 180), (255, 255, 255),
                            (180, 180, 180), self.can_click):
                self.turn_page: int = 1
                self.can_click: bool = False
                self.link_up.activate()
            if button2.draw(50, (180, 180, 180), (255, 255, 255),
                            (180, 180, 180), self.can_click):
                self.turn_page: int = 2
                self.can_click: bool = False
                self.link_up.activate()
            have_stage: list = []
            # noinspection PyUnusedLocal
            for x in range(len(json_str2[f"Level{json_str["level"][self.account]}"])):
                have_stage.append(False)
            for x in range(len(json_str2[f"Level{json_str["level"][self.account]}"])):
                if level[x].activate and True not in have_stage:
                    have_stage[x] = True
                elif not level[x].activate:
                    have_stage[x] = False
                level[x].draw(temp_can_click)
                if True in have_stage:
                    information: any = level[have_stage.index(True)].level_draw(have_stage.index(True),
                                                                                json_str["level"][self.account],
                                                                                self.account, self.can_click)
                    if information is not None:
                        information += 2
                        if information == 2 or information == 3 or information == 4:
                            choose_level: int = 0
                            for level_count in range(have_stage.index(True) + 1):
                                if json_str2[f"Level{json_str["level"][self.account]}"][f"{level_count}"]["Type"] <= 1:
                                    choose_level += 1
                            self.turn_page: int = information
                            self.can_click: bool = False
                            draw_rect: bool = True
                            rect_alpha: int = 0
            if draw_rect:
                rect_alpha += 26
                if rect_alpha >= 255:
                    rect_alpha: int = 255
                    if self.turn_page == 2 or self.turn_page == 3:
                        self.game_page(choose_level)
                        return
                # 在 Surface 上绘制一个透明的矩形
                rect_surface: any = pygame.Surface((width, height), pygame.SRCALPHA)
                pygame.draw.rect(rect_surface, (0, 0, 0, rect_alpha), (0, 0, width, height))
                screen.blit(rect_surface, (0, 0))
            # 事件处理
            for events in pygame.event.get():
                # 判断事件类型是否为QUIT
                if events.type == QUIT:
                    # 游戏结束,清理工作
                    pygame.quit()
                    exit()
                elif events.type == pygame.MOUSEBUTTONDOWN:
                    self.click.click_activate()
            self.click.click()
            if self.link_up.can_exit:
                if change_page:
                    if self.turn_page == 4:
                        self.map_page()
                    elif self.turn_page == 1:
                        self.home_page()
                    elif self.turn_page == 2:
                        self.charm_page()
                    return
                self.link_up.exit()
            else:
                change_page: bool = True
                self.link_up.access(0)
            # 更新屏幕
            pygame.display.flip()
            clock.tick(tick_frequency)

    def game_page(self, level: int) -> None:
        """关卡界面"""
        self.now_time: int = pygame.time.get_ticks()
        self.can_sleep: bool = True
        self.can_click: bool = False
        now_time: int = -1
        into_level: bool = True
        change_now_time: bool = False
        rect_alpha: int = 0
        change_block: bool = False
        game_start_time: int = pygame.time.get_ticks()
        start_pause_time: int = 0
        last_click: bool = True
        win_temp_now: int = 0
        pause: bool = False
        settlement: bool = False
        settlement_temp: int = 0
        can_pause: bool = False
        draw_rect: bool = False
        shoot: list = [False]
        change_page: bool = False
        difficult: int = self.turn_page - 2
        with open(f"data/User.json", encoding="UTF-8") as f:
            json_str: any = json.load(f)
            f.close()
        with open(f"data/Level_data.json", encoding="UTF-8") as f:
            json_str2: any = json.load(f)
            f.close()
        with open(f"data/Level.json", encoding="UTF-8") as f:
            json_str3: any = json.load(f)
            f.close()
        create: any = EntityCreate(game_start_time, json_str["level"][self.account], level, difficult)
        hp: int = json_str2[f"{json_str["level"][self.account]}-{level}"]["basic"]["HP"][difficult]
        enemies: int = 0
        bullets: int = json_str2[f"{json_str["level"][self.account]}-{level}"]["basic"]["bullets"][difficult]
        mp: int = 0
        basic_information: list = [hp, enemies, bullets, mp]
        build_rect: list = []
        build_id: list[int] = []
        build_active: list[bool] = []
        running: bool = True
        if date == "04-01" or date == "05-13":
            image1: any = Image(image_usually_use[36], width, height, 0, 0, 0, 0, False, False, (1, 2), (1, 2))
        else:
            image1: any = Image(f"{image_usually_use[36]}{json_str["level"][self.account]}_background.jpg",
                                width, height,
                                0, 0, 0, 0, False, False, (1, 2), (1, 2))
        image2: any = Image(image_usually_use[35], width, 100, 0, 50, 22, 255, False, True, (1, 2), (1, 2))
        image3: any = Image(image_usually_use[37], 80, 80, 200, 50, 22, 255, False, False, (3, 16), (1, 2))
        image4: any = Image(image_usually_use[38], 80, 80, 500, 50, 22, 255, False, False, (6, 16), (1, 2))
        image5: any = Image(image_usually_use[39], 80, 80, 800, 50, 22, 255, False, False, (9, 16), (1, 2))
        image6: any = Image(image_usually_use[40], 80, 80, 800, 50, 22, 255, False, False, (12, 16), (1, 2))
        damage_text: any = DamageText()
        equipments: any = Equipments(build_id, build_rect, build_active)
        dock_rect = pygame.Rect(width // 2, 50, image2.image_width, image2.image_height)
        dock_rect.center = (width // 2, 50)
        gun: any = GameGun(game_start_time, 0, shoot, self.account, basic_information,
                           json_str2[f"{json_str["level"][self.account]}-{level}"]["basic"]["cost_recover_speed"]
                           [difficult])
        mp_len: int = image6.image_width - 10
        text5: any = CustomText(game_text[11 + difficult],
                                "assets/fonts/Text.TTF", 50,
                                (255, 255, 255), [0, 0], 0, 0, (1, 2), (1, 4), True, False, None)
        text6: any = CustomText(f"{json_str3[f"Level{json_str["level"][self.account]}"][f"{level - 1}"]["Title"]}",
                                "assets/fonts/Text.TTF", 100,
                                (255, 255, 255), [0, 0], 0, 0, (1, 2), (2, 4), True, False, None)
        while running:
            if into_level:
                if pygame.time.get_ticks() - self.now_time >= waiting_time[3]:
                    if change_now_time:
                        now_time: int = pygame.time.get_ticks()
                        change_now_time: bool = False
                    if image1.alpha < 255:
                        image1.alpha += 13
                        text5.alpha += 13
                        text6.alpha += 13
                        if image1.alpha >= 255:
                            text5.alpha = 255
                            text6.alpha = 255
                            image1.alpha = 255
                            change_now_time: bool = True
                            change_block: bool = True
                        image1.draw()
                    else:
                        image1.draw()
                        if (pygame.time.get_ticks() - now_time >= waiting_time[4] and not change_now_time
                                and change_block):
                            change_now_time: bool = True
                            change_block: bool = False
                            rect_alpha: int = 255
                            continue
                        if not change_block:
                            # 在 Surface 上绘制一个透明的矩形
                            rect_surface: any = pygame.Surface((width, height), pygame.SRCALPHA)
                            pygame.draw.rect(rect_surface, (0, 0, 0, rect_alpha), (0, 0, width, height))
                            screen.blit(rect_surface, (0, 0))
                        if (rect_alpha > 0 and pygame.time.get_ticks() - now_time >= waiting_time[5] and
                                not change_now_time and not change_block):
                            rect_alpha -= 13
                            text5.alpha -= 13
                            text6.alpha -= 13
                            if rect_alpha <= 0:
                                rect_alpha = 0
                                text5.alpha = 0
                                text6.alpha = 0
                                into_level: bool = False
                                game_start_time: int = pygame.time.get_ticks()
                                create: any = EntityCreate(game_start_time, json_str["level"][self.account], level,
                                                           difficult)
                                gun: any = GameGun(game_start_time, 0, shoot, self.account, basic_information,
                                                   json_str2[f"{json_str["level"][self.account]}-{level}"]["basic"][
                                                       "cost_recover_speed"]
                                                   [difficult])
                                can_pause: bool = True
                                change_page: bool = True
                                self.can_click: bool = True
                    text5.draw()
                    text6.draw()
                else:
                    screen.fill((0, 0, 0))
            else:
                hp: int = basic_information[0]
                enemies: int = basic_information[1]
                bullets: int = basic_information[2]
                mp: int = basic_information[3]
                text1: any = CustomText(f"{hp}/{json_str2[f"{json_str["level"][self.account]}-{level}"]["basic"]["HP"]
                                        [difficult]}",
                                        "assets/fonts/Text.TTF", 50,
                                        (255, 255, 255, 0), [300, 50], 255, 1, (7, 32), (1, 2), False, False, None)
                text2: any = CustomText(f"{enemies}/{json_str2[f"{json_str["level"][self.account]}-{level}"]["basic"]
                                        ["enemy"][difficult]}",
                                        "assets/fonts/Text.TTF", 50,
                                        (255, 255, 255), [600, 50], 255, 1, (13, 32), (1, 2), False, False, None)
                text3: any = CustomText(f"{bullets}",
                                        "assets/fonts/Text.TTF", 50,
                                        (255, 255, 255), [900, 50], 255, 1, (19, 32), (1, 2), False, False, None)
                text4: any = CustomText(f"{mp}",
                                        "assets/fonts/Text.TTF", 50,
                                        (255, 255, 255), [900, 50], 255, 1, (25, 32), (1, 2), False, False, None)
                if self.turn_page != 0:
                    screen.fill((0, 0, 0))
                else:
                    screen.fill((255, 0, 0))
                if json_str["setting"][self.account]["dock_hidden"] and not pause and not settlement:
                    if dock_rect.colliderect(gun.gun_rect):
                        image2.alpha = 150
                        image3.alpha = 150
                        image4.alpha = 150
                        image5.alpha = 150
                        image6.alpha = 150
                        text1.alpha = 150
                        text2.alpha = 150
                        text3.alpha = 150
                        text4.alpha = 150
                    else:
                        image2.alpha = 255
                        image3.alpha = 255
                        image4.alpha = 255
                        image5.alpha = 255
                        image6.alpha = 255
                        text1.alpha = 255
                        text2.alpha = 255
                        text3.alpha = 255
                        text4.alpha = 255
                image1.draw()
                if not settlement:
                    create.check(self.can_click)
                    create.create(self.can_click, shoot[0], gun.gun_rect, gun.damage, basic_information,
                                  json_str["setting"][self.account]["damage_visible"],
                                  json_str["setting"][self.account]["float_damage_visible"], build_id, build_rect,
                                  build_active)
                    if gun.approve_equipments:
                        equipments.build_append(gun.build_id)
                    equipments.draw()
                    if json_str["setting"][self.account]["damage_visible"]:
                        if create.approve_damage_text:
                            damage_text.append_surface(create.gun_damage)
                        damage_text.draw()
                    gun.draw(self.can_click, len(equipments.build_id), json_str2[
                        f"{json_str["level"][self.account]}-{level}"]["basic"]["deployment_ceiling"][difficult])
                    image2.draw()
                    image3.draw()
                    image4.draw()
                    image5.draw()
                    image6.draw()
                    # 创建一个带有 Alpha 通道的新 Surface 对象
                    alpha_surface: any = pygame.Surface((width, height), pygame.SRCALPHA)
                    if json_str["setting"][self.account]["dock_hidden"] and not pause:
                        if dock_rect.colliderect(gun.gun_rect):  # 血条加载
                            pygame.draw.line(alpha_surface, (0, 0, 0, 150), (width // 4 * 3 - image6.image_width // 2,
                                                                             53 + image6.image_width // 2),
                                             (width // 4 * 3 + image6.image_width // 2, 53 + image6.image_width // 2),
                                             12)
                            pygame.draw.line(alpha_surface, (255, 255, 255, 150), (width // 4 * 3 - image6.image_width
                                                                                   // 2
                                                                                   + 5, 53 + image6.image_width // 2),
                                             (width // 4 * 3 - image6.image_width // 2 + 5 + mp_len * (
                                                     gun.mp_recover_now_time / gun.mp_recover_time),
                                              53 + image6.image_width // 2), 8)
                        else:
                            pygame.draw.line(alpha_surface, (0, 0, 0), (width // 4 * 3 - image6.image_width // 2, 53 +
                                                                                       image6.image_width // 2),  # 血条加载
                                             (width // 4 * 3 + image6.image_width // 2, 53 + image6.image_width // 2),
                                             12)
                            pygame.draw.line(alpha_surface, (255, 255, 255), (width // 4 * 3 - image6.image_width // 2
                                                                              + 5,
                                                                                             53 + image6.image_width //
                                                                              2),
                                             (width // 4 * 3 - image6.image_width // 2 + 5 + mp_len * (
                                                     gun.mp_recover_now_time / gun.mp_recover_time),
                                              53 + image6.image_width // 2), 8)
                    else:
                        pygame.draw.line(alpha_surface, (0, 0, 0), (width // 4 * 3 - image6.image_width // 2, 53 +
                                                                                   image6.image_width // 2),  # 血条加载
                                         (width // 4 * 3 + image6.image_width // 2, 53 + image6.image_width // 2), 12)
                        pygame.draw.line(alpha_surface, (255, 255, 255), (width // 4 * 3 - image6.image_width // 2 + 5,
                                                                                         53 + image6.image_width // 2),
                                         (width // 4 * 3 - image6.image_width // 2 + 5 + mp_len *
                                          (gun.mp_recover_now_time /
                                                                                                   gun.mp_recover_time),
                                          53 + image6.image_width // 2), 8)
                    screen.blit(alpha_surface, (0, 0))
                    text1.draw()
                    text2.draw()
                    text3.draw()
                    text4.draw()
                if self.can_click:
                    if hp <= 0:
                        self.can_click: bool = False
                        can_pause: bool = False
                        self.turn_page: int = 0
                        settlement: bool = True
                        settlement_temp: int = 0
                    elif enemies == json_str2[f"{json_str["level"][self.account]}-{level}"]["basic"]["enemy"][
                            difficult]:
                        self.can_click: bool = False
                        can_pause: bool = False
                        if difficult == 1:
                            self.turn_page: int = -3
                        else:
                            if hp == json_str2[f"{json_str["level"][self.account]}-{level}"]["basic"]["HP"][difficult]:
                                self.turn_page: int = -1
                            else:
                                self.turn_page: int = -2
                        settlement: bool = True
                        settlement_temp: int = 0
                    if json_str["setting"][self.account]["mouse_action_visible"]:
                        Image(image_usually_use[48], 40, 70, width - 30, height - 45,
                              2, 255, False, False, (1, 2), (1, 2)).draw()
                        if pygame.mouse.get_pressed()[0]:
                            Image(image_usually_use[49], 40, 70, width - 30, height - 45,
                                  2, 255, False, False, (1, 2), (1, 2)).draw()
                        if pygame.mouse.get_pressed()[1]:
                            Image(image_usually_use[50], 40, 70, width - 30, height - 45,
                                  2, 255, False, False, (1, 2), (1, 2)).draw()
                        if pygame.mouse.get_pressed()[2]:
                            Image(image_usually_use[51], 40, 70, width - 30, height - 45,
                                  2, 255, False, False, (1, 2), (1, 2)).draw()
                if can_pause:
                    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        if pygame.time.get_ticks() - start_pause_time > 200:
                            soundtrack.music_play(0, sound[12], False)
                            pause: bool = not pause
                    if pause:
                        self.can_click: bool = False
                        if last_click != self.can_click:
                            start_pause_time: int = pygame.time.get_ticks()
                        pause_background_image: any = Image(image_usually_use[41], width,
                                                            height, width // 2, height // 2, 3, 100,
                                                            False, False, (1, 2), (1, 2))
                        pause_text: any = CustomText(game_text[2], "assets/fonts/text.TTF", 150,
                                                     (255, 255, 255), [width // 2, height // 4],
                                                     255, 0, (1, 2), (3, 4), True, False, None)
                        button1: any = Button("退出", width // 4, height // 16, 400, 100,
                                              image_usually_use[0], image_usually_use[1], image_usually_use[2], 1,
                                              0, (1, 4), (1, 16))
                        button2: any = Button("重新开始", width // 4 * 3, height // 16, 400,
                                              100, image_usually_use[0], image_usually_use[1],
                                              image_usually_use[2], 1, 0, (3, 4), (1, 16))
                        pause_background_image.draw()
                        pause_text.draw()
                        if button1.draw(50, (180, 180, 180), (255, 255, 255),
                                        (180, 180, 180), can_pause) and not self.link_up.active:
                            self.turn_page: int = 1
                            can_pause: bool = False
                            self.link_up.activate()
                        if button2.draw(50, (180, 180, 180), (255, 255, 255),
                                        (180, 180, 180), can_pause) and not self.link_up.active:
                            self.turn_page: int = difficult + 2
                            can_pause: bool = False
                            draw_rect: bool = True
                        self.click.click()
                    else:
                        if self.turn_page > 0:
                            self.can_click: bool = True
                        if last_click != self.can_click:
                            start_pause_time: int = pygame.time.get_ticks()
                last_click: bool = self.can_click
                if settlement:
                    if settlement_temp < 40:
                        if settlement_temp >= 10 and pygame.time.get_ticks() - win_temp_now >= waiting_time[1]:
                            settlement_temp += 1
                        elif settlement_temp < 10:
                            settlement_temp += 1
                            if settlement_temp == 10:
                                win_temp_now: int = pygame.time.get_ticks()
                    win_rect: any = pygame.Rect(0, 0, width, 250)
                    if settlement_temp <= 10:
                        win_rect.center = (width - (width // 10 * settlement_temp), height // 2)
                        win_rect.left = width - (width // 10 * settlement_temp)
                        text_pos: int = width // 2 * 3 - (width // 10 * settlement_temp)
                    else:
                        win_rect.center = (0 - (width // 10 * (settlement_temp - 10)), height // 2)
                        win_rect.left = 0 - (width // 10 * (settlement_temp - 10))
                        text_pos: int = width // 2 - (width // 10 * (settlement_temp - 10))
                    if settlement_temp <= 20 and self.turn_page != 0:
                        pygame.draw.rect(screen, (0, 0, 0), win_rect)
                        text: str = game_text[3]
                        CustomText(text, "assets/fonts/text.TTF", 150,
                                   (255, 255, 255), [text_pos, 0],
                                   255, 2, (1, 2), (1, 2), True, False, None).draw()
                    if settlement_temp == 40 or self.turn_page == 0:
                        image1.alpha -= 26
                        if image1.alpha <= 0:
                            self.result_page(level)
                            return
                if draw_rect:
                    if rect_alpha != 255:
                        rect_alpha += 13
                        if rect_alpha >= 255:
                            self.game_page(level)
                            return
                        # 在 Surface 上绘制一个透明的矩形
                    rect_surface: any = pygame.Surface((width, height), pygame.SRCALPHA)
                    pygame.draw.rect(rect_surface, (0, 0, 0, rect_alpha), (0, 0, width, height))
                    screen.blit(rect_surface, (0, 0))
                # 事件处理
                for events in pygame.event.get():
                    # 判断事件类型是否为QUIT
                    if events.type == QUIT:
                        # 游戏结束,清理工作
                        pygame.quit()
                        exit()
                    elif events.type == pygame.MOUSEBUTTONDOWN and pause:
                        self.click.click_activate()
                if self.link_up.can_exit:
                    if change_page:
                        if self.turn_page == 1:
                            self.map_page()
                            return
                    self.link_up.exit()
                else:
                    if not can_pause and not pause and self.can_click:
                        can_pause: bool = True
                    change_page: bool = True
                    self.link_up.access(1000)
            # 更新屏幕
            pygame.display.flip()
            clock.tick(tick_frequency)

    def charm_page(self) -> None:
        """选择一个账户并进入游戏"""
        self.now_time: int = pygame.time.get_ticks()
        self.can_sleep: bool = True
        self.can_click: bool = False
        running: bool = True
        with open("data/User.json", encoding="UTF-8") as f:
            json_str: any = json.load(f)
            f.close()
        with open("data/Charm.json", encoding="UTF-8") as f:
            json_str2: any = json.load(f)
            f.close()
        for x in range(json_str["charm_slot"][self.account] - len(json_str["charm_use"][self.account])):
            json_str["charm_use"][self.account].append(-1)
        image2: any = Image(image_usually_use[42], width, 200,
                            0, height - 100, 22, 255, False, False, (1, 2), (1, 2))
        image1: any = Image(image_usually_use[43], width, height,
                            0, 0, 0, 100, False, False, (1, 2), (1, 2))
        button1: any = Button("", 50, 50, 80, 80, image_usually_use[29],
                              image_usually_use[30], image_usually_use[31],
                              1, 3, (1, 2), (1, 2))
        charm: list = []
        charm_equip: list = []
        for x in range(json_str["charm_slot"][self.account]):
            charm_equip.append(Image("", 100, 100,
                                     width // 2 - 100 * json_str["charm_slot"][self.account] // 2 + x * 100 + 50,
                                     height // 8, 21, 255, False, False, (1, 2),
                                     (1, 8)))
            if date == "04-01" or date == "05-13":
                charm_equip[len(charm_equip) - 1].image_path = image_usually_use[44]
            else:
                if json_str["charm_use"][self.account][x] != -1:
                    charm_equip[len(charm_equip) - 1].image_path = (
                        f"{image_usually_use[44]}{json_str2[f"{x}"]["name"]}{json_str2[f"{x}"]["Image_type"]}")
                else:
                    charm_equip[len(charm_equip) - 1].image_path = image_usually_use[45]
        for x in range(len(json_str2)):
            charm.append(Switch(80, 80, 0, 0,
                                "", "", x in json_str["charm_use"][self.account],
                                False, 0, (x % 10 + 1, 11), ((x - x % 10) // 10 + 3, 9),
                                100 if x in json_str["charm_use"][self.account] else 255))
            if date == "04-01" or date == "05-13":
                charm[len(charm) - 1].inactive = image_usually_use[44]
                charm[len(charm) - 1].active = image_usually_use[44]
            else:
                charm[len(charm) - 1].inactive = (f"{image_usually_use[44]}{json_str2[f"{x}"]["name"]}"
                                                  f"{json_str2[f"{x}"]["Image_type"]}")
                charm[len(charm) - 1].active = (f"{image_usually_use[44]}{json_str2[f"{x}"]["name"]}"
                                                f"{json_str2[f"{x}"]["Image_type"]}")
        title_text: any = CustomText("", "assets/fonts/Title.TTF", 60,
                                     (255, 255, 255), [0, 0], 255, 0, (1, 2),
                                     (7, 8), True, False, 8)
        description_text: any = CustomText("", "assets/fonts/Text.TTF", 30,
                                           (255, 255, 255), [0, 0], 255, 0, (1, 2),
                                           (15, 16), True, False, 20)
        state_text: any = CustomText("", "assets/fonts/Text.TTF", 20, (255, 255, 255),
                                     [0, 0], 255, 0, (1, 2),
                                     (13, 16), True, False, 20)
        while running:
            screen.fill((200, 200, 200))
            image1.draw()
            image2.draw()
            title_text.draw()
            description_text.draw()
            state_text.draw()
            title_text.text = ""
            description_text.text = ""
            state_text.text = ""
            for x in range(len(charm_equip)):
                if date == "04-01" or date == "05-13":
                    charm_equip[x].image_path = image_usually_use[44]
                else:
                    if json_str["charm_use"][self.account][x] != -1:
                        charm_equip[x].image_path = (f"{image_usually_use[44]}{json_str2[f"{x}"]["name"]}"
                                                                        f"{json_str2[f"{x}"]["Image_type"]}")
                    else:
                        charm_equip[x].image_path = image_usually_use[45]
                charm_equip[x].draw()
            for x in range(len(charm)):
                if charm[x].touch:
                    if json_str["charm"][self.account][x] != -1:
                        title_text.text = json_str2[f"{x}"]["Chinese_name"]
                        description_text.text = json_str2[f"{x}"]["Description"]
                        if charm[x].activate:
                            state_text.text = game_text[4]
                            state_text.font_color = (0, 0, 255)
                        else:
                            state_text.text = game_text[5]
                            state_text.font_color = (255, 0, 0)
                    else:
                        title_text.text = game_text[6]
                        description_text.text = ""
                        state_text.text = ""
                if json_str["charm"][self.account][x] != -1:
                    if charm[x].activate:
                        if x not in json_str["charm_use"][self.account]:
                            try:
                                json_str["charm_use"][self.account][json_str["charm_use"][self.account].index(-1)] = x
                            except ValueError:
                                charm[x].activate = False
                        charm[x].alpha = 100
                    else:
                        if x in json_str["charm_use"][self.account]:
                            json_str["charm_use"][self.account][json_str["charm_use"][self.account].index(x)] = -1
                        charm[x].alpha = 255
                    charm[x].draw(self.can_click)
                else:
                    pygame.draw.circle(screen, (53, 220, 217),
                                       (width // 11 * (x % 10 + 1), height // 9 * ((x - x % 10) // 10 + 5)),
                                       40, width=10)
            if button1.draw(50, (180, 180, 180), (255, 255, 255),
                            (180, 180, 180), self.can_click):
                json_str3: any = json.dumps(json_str, ensure_ascii=False, indent=4)
                f: any = open(f"data/User.json", "w", encoding="UTF-8")
                f.write(json_str3)
                f.flush()
                f.close()
                self.turn_page: int = 0
                self.can_click: bool = False
                self.link_up.activate()
            # 事件处理
            for events in pygame.event.get():
                # 判断事件类型是否为QUIT
                if events.type == QUIT:
                    # 游戏结束,清理工作
                    pygame.quit()
                    exit()
                elif events.type == pygame.MOUSEBUTTONDOWN:
                    self.click.click_activate()
            self.click.click()
            if self.link_up.can_exit:
                if self.turn_page == 0:
                    self.map_page()
                    return
                else:
                    self.link_up.exit()
            else:
                if not self.link_up.active:
                    self.can_click: bool = True
                self.link_up.access(0)
            # 更新屏幕
            pygame.display.flip()
            clock.tick(tick_frequency)

    def result_page(self, level: int) -> None:
        """结算页面"""
        self.now_time: int = pygame.time.get_ticks()
        self.can_sleep: bool = True
        self.can_click: bool = False
        exp_animation_count: int = 0
        pop: list = []
        queue: list = []
        enable_pop: bool = False
        change_page: bool = False
        running: bool = True
        button1: any = Button("继续", 50, 230, 400, 100,
                              image_usually_use[0], image_usually_use[1],
                              image_usually_use[2], 1, 0, (1, 2), (7, 8))
        with open("data/User.json", encoding="UTF-8") as f:
            json_str: any = json.load(f)
            f.close()
        with open("data/Level.json", encoding="UTF-8") as f:
            json_str2: any = json.load(f)
            f.close()
        with open("data/Build.json", encoding="UTF-8") as f:
            json_str4: any = json.load(f)
            f.close()
        with open("data/Level_data.json", encoding="UTF-8") as f:
            json_str5: any = json.load(f)
            f.close()
        with open("data/Charm.json", encoding="UTF-8") as f:
            json_str6: any = json.load(f)
            f.close()
        give_exp: int = 0
        old_exp: int = json_str["EXP"][self.account]
        if self.turn_page == -2:
            if json_str["progress"][self.account][json_str2[f"Level{json_str["level"][self.account]}"]
                                                           [f"{level - 1}"]["Level_id"]] == 0:
                give_exp += 50
            give_exp += json_str5[f"{json_str["level"][self.account]}-{level}"]["basic"]["enemy"][0]
        elif self.turn_page == -1:
            if json_str["progress"][self.account][json_str2[f"Level{json_str["level"][self.account]}"]
                                                           [f"{level - 1}"]["Level_id"]] < 2:
                give_exp += 100
                if json_str["progress"][self.account][json_str2[f"Level{json_str["level"][self.account]}"]
                                                               [f"{level - 1}"]["Level_id"]] == 0:
                    give_exp += 50
            give_exp += 2 * json_str5[f"{json_str["level"][self.account]}-{level}"]["basic"]["enemy"][0]
        elif self.turn_page == -3:
            if json_str["progress"][self.account][json_str2[f"Level{json_str["level"][self.account]}"]
                                                           [f"{level - 1}"]["Level_id"]] < 3:
                give_exp += 200
            give_exp += 3 * json_str5[f"{json_str["level"][self.account]}-{level}"]["basic"]["enemy"][1]
        elif self.turn_page != 0 and json_str2[f"Level{json_str["level"][self.account]}"][f"{level - 1}"]["Type"] == 1:
            if json_str["progress"][self.account][json_str2[f"Level{json_str["level"][self.account]}"]
                                                           [f"{level - 1}"]["Level_id"]] < 3:
                give_exp += 200
            give_exp += 5 * json_str5[f"{json_str["level"][self.account]}-{level}"]["basic"]["enemy"][1]
        json_str["EXP"][self.account] += give_exp
        text1: any = CustomText(game_text[7], "assets/fonts/Text.TTF", 100, (255, 255, 255),
                                [width // 2, height // 4], 255, 0, (1, 12), (1, 4), False, False, None)
        text2: any = CustomText(f"{json_str2[f"Level{json_str["level"][self.account]}"][f"{level - 1}"]["Title"]}",
                                "assets/fonts/Text.TTF",
                                50, (255, 255, 255),
                                [width // 2, height // 4], 255, 0, (1, 12), (1, 8),
                                False, False, None)
        text3: any = CustomText(f"{int(old_exp / 500) + 1}",
                                "assets/fonts/Text.TTF",
                                100, (255, 255, 255),
                                [0, 0], 255, 0, (1, 8), (24, 32),
                                True, False, None)
        text4: any = CustomText(f"{old_exp % 500}/500",
                                "assets/fonts/Text.TTF",
                                30, (255, 255, 255),
                                [0, 0], 255, 0, (1, 8), (26, 32),
                                True, False, None)
        if date == "04-01" or date == "05-13":
            image1: any = Image(image_usually_use[46], width, height, 0, 0, 0,
                                200, False, False, (1, 2),
                                (1, 2))
        else:
            image1: any = Image(f"{image_usually_use[46]}{json_str["level"][self.account]}_background.jpg",
                                width, height, 0, 0, 0, 200, False, False,
                                (1, 2), (1, 2))
        picture: int = 8
        if self.turn_page != 0:
            if json_str2[f"Level{json_str["level"][self.account]}"][f"{level - 1}"]["Unlock_equipments"] is not None:
                for x in range(len(json_str2[f"Level{json_str["level"][self.account]}"][f"{level - 1}"]
                                   ["Unlock_equipments"])):
                    pop.append(PopupMessage(350, 100, image_usually_use[5], 2000,
                                            f"解锁了{game_text[8]}：{json_str4[f"{json_str2[
                                                f"Level{json_str["level"][self.account]}"
                                            ][f"{level - 1}"]["Unlock_equipments"][x]}"]["Chinese_name"]}",
                                            (255, 255, 255), "assets/fonts/Text.TTF", 40,
                                            100, 30, False, 0, 0,
                                            image_usually_use[26], (60, 60), 25,
                                            20, queue, len(pop), (10, 0), (False, False), (False, False)))
                    if json_str["equipment_level"][self.account][
                        json_str2[f"Level{json_str["level"][self.account]}"][f"{level - 1}"]
                                 ["Unlock_equipments"][x]] == -1:
                        json_str["equipment_level"][self.account][
                            json_str2[f"Level{json_str["level"][self.account]}"][f"{level - 1}"]["Unlock_equipments"]
                            [x]] = 0
            if json_str["progress"][self.account][json_str2[f"Level{json_str["level"][self.account]}"]
                                                               [f"{level - 1}"]["Level_id"]] == 0:
                enable_pop: bool = True
            if json_str2[f"Level{json_str["level"][self.account]}"][f"{level - 1}"]["Type"] == 0:
                complete: int = 0
                if self.turn_page == -1:
                    complete: int = 2
                    picture: int = 3
                elif self.turn_page == -2:
                    complete: int = 1
                    picture: int = 2
                elif self.turn_page == -3:
                    complete: int = 3
                    picture: int = 4
                if json_str["progress"][self.account][json_str2[f"Level{json_str["level"][self.account]}"]
                                                               [f"{level - 1}"]["Level_id"]] < complete:
                    json_str["progress"][self.account][json_str2[f"Level{json_str["level"][self.account]}"]
                                                                [f"{level - 1}"]["Level_id"]] = complete
                if json_str2[f"Level{json_str["level"][self.account]}"][f"{level - 1}"]["Unlock_Level_id"] is not None:
                    for x in range(len(json_str2[f"Level{json_str["level"][self.account]}"][f"{level - 1}"]
                                       ["Unlock_Level_id"])):
                        pop.append(PopupMessage(350, 100, image_usually_use[5], 2000,
                                                f"解锁了{game_text[9]}："
                                                f"{json_str2[f"Level{json_str["level"][self.account]}"][
                                                    f"{json_str2[f"Level{json_str["level"][self.account]}"]
                                                        [f"{level - 1}"]["Unlock_Level_id"][x]}"]["Title"]}",
                                                (255, 255, 255), "assets/fonts/Text.TTF", 40,
                                                100, 30, False, 0, 0,
                                                image_usually_use[26], (60, 60), 25,
                                                20, queue, len(pop), (10, 0), (False, False), (False, False)))
                        if json_str["progress"][self.account][json_str2[f"Level{json_str["level"][self.account]}"]
                                                                       [f"{level - 1}"]["Unlock_Level_id"][x]] == -1:
                            json_str["progress"][self.account][json_str2[f"Level{json_str["level"][self.account]}"]
                                                                        [f"{level - 1}"]["Unlock_Level_id"][x]] = 0
            elif json_str2[f"Level{json_str["level"][self.account]}"][f"{level - 1}"]["Type"] == 1:
                json_str["progress"][self.account][json_str2[f"Level{json_str["level"][self.account]}"][f"{level - 1}"]
                                                            ["Level_id"]] = 3
                picture: int = 6
            if json_str2[f"Level{json_str["level"][self.account]}"][f"{level - 1}"]["Unlock_charms"] is not None:
                for x in range(len(json_str2[f"Level{json_str["level"][self.account]}"][f"{level - 1}"]
                                   ["Unlock_charms"])):
                    pop.append(PopupMessage(350, 100, image_usually_use[5], 2000,
                                            f"解锁了{game_text[10]}：{json_str6[f"{json_str2[
                                                f"Level{json_str["level"][self.account]}"
                                            ][f"{level - 1}"]["Unlock_charms"][x]}"]["Chinese_name"]}",
                                            (255, 255, 255), "assets/fonts/Text.TTF", 40,
                                            100, 30, False, 0, 0,
                                            image_usually_use[26], (60, 60), 25,
                                            20, queue, len(pop), (10, 0), (False, False), (False, False)))
                    if json_str["charm"][self.account][
                        json_str2[f"Level{json_str["level"][self.account]}"][f"{level - 1}"]
                                 ["Unlock_charms"][x]] == -1:
                        json_str["charm"][self.account][
                            json_str2[f"Level{json_str["level"][self.account]}"][f"{level - 1}"]
                            ["Unlock_charms"][x]] = 0
            json_str3: any = json.dumps(json_str, ensure_ascii=False, indent=4)
            with open("data/User.json", "w", encoding="UTF-8") as f:
                f.write(json_str3)
                f.flush()
                f.close()
        if date == "04-01" or date == "05-13":
            image2: any = Image(f"{image_usually_use[47]}", 120, 120, 0,
                                50, 0, 255, False, False, (1, 8), (1, 2))
        else:
            image2: any = Image(f"{image_usually_use[47]}{picture}.png", 120, 120, 0,
                                50, 0, 255, False, False, (1, 8), (1, 2))
        if enable_pop:
            for x in range(len(pop)):
                pop[x].activate()
        rect_alpha: int = 255
        while running:
            screen.fill((255, 255, 255))
            image1.draw()
            text1.draw()
            text2.draw()
            text3.draw()
            text4.draw()
            image2.draw()
            # 定义圆心位置
            arc_center: tuple = (width // 8, height // 4 * 3)
            pygame.draw.circle(screen, (0, 0, 0), (arc_center[0], arc_center[1]), 105, width=25)
            # 定义半径
            radius: int = 100
            exp_animation_count_len: int = json_str["EXP"][self.account] - old_exp
            if exp_animation_count < exp_animation_count_len and rect_alpha == 0:
                old_exp += 1
                text3.text = f"{int(old_exp / 500) + 1}"
                text4.text = f"{old_exp % 500}/500"
            pygame.draw.arc(screen, (94, 203, 118), (arc_center[0] - radius, arc_center[1] - radius, 2 * radius,
                                                                2 * radius), radians(90),
                            radians(90 + old_exp % 500 / 500 * 360), 15)
            if rect_alpha > 0 and pygame.time.get_ticks() - self.now_time >= waiting_time[2]:
                rect_alpha -= 13
                if rect_alpha < 0:
                    rect_alpha: int = 0
                    self.can_click: bool = True
            elif old_exp == json_str["EXP"][self.account]:
                if button1.draw(50, (180, 180, 180), (255, 255, 255),
                                (180, 180, 180), self.can_click):
                    self.turn_page: int = 0
                    self.link_up.activate()
                    self.can_click: bool = False
            # 在 Surface 上绘制一个透明的矩形
            rect_surface: any = pygame.Surface((width, height), pygame.SRCALPHA)
            if picture != 8:
                pygame.draw.rect(rect_surface, (0, 0, 0, rect_alpha), (0, 0, width, height))
            else:
                pygame.draw.rect(rect_surface, (255, 0, 0, rect_alpha), (0, 0, width, height))
            screen.blit(rect_surface, (0, 0))
            if self.can_click:
                for x in range(len(pop)):
                    pop[x].draw()
            if rect_alpha == 0:
                self.click.click()
            if self.link_up.can_exit:
                if change_page:
                    if self.turn_page == 0:
                        self.map_page()
                        return
                self.link_up.exit()
            else:
                change_page: bool = True
                self.link_up.access(0)
            # 事件处理
            for events in pygame.event.get():
                if events.type == pygame.QUIT:  # 检测到窗口关闭事件
                    # 游戏结束,清理工作
                    pygame.quit()
                    exit()
                elif events.type == pygame.MOUSEBUTTONDOWN and rect_alpha == 0:
                    self.click.click_activate()
            clock.tick(tick_frequency)
            # 绘图、更新屏幕等操作...
            pygame.display.flip()  # 更新整个待显示的Surface到屏幕上
