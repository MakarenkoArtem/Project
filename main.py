import sys
import json
import os
import time
from work_with_bd import *
import random
from enum import Enum

try:
    import pygame_gui
except ModuleNotFoundError:
    import pip

    pip.main(['install', "pygame_gui"])
try:
    import pygame
except ModuleNotFoundError:
    import pip

    pip.main(['install', "pygame"])
    import pygame




class GameStates(Enum):
    START_SCREEN = 1
    GAME_SCREEN = 2
    GAME_ON_PAUSE_SCREEN = 3
    STOP_SCREEN = 4


size = WIDTH, HEIGHT = 1200, 900
tile_width = tile_height = 50
FPS = 30
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
CHECKS = 4


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def loading(n):
    text = None
    global lamp, z, data
    if n == -1:
        print(n)
        z = []
        lamp = pygame.sprite.Group()
        for i in range(CHECKS):
            sprite = pygame.sprite.Sprite()
            sprite.image = load_image("data/Off.png", colorkey=None)
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = WIDTH // (CHECKS + 1) * (i + 1)
            sprite.rect.y = 750
            lamp.add(sprite)
            z.append(sprite)
    elif n == 0:
        try:
            import pygame_gui
        except ModuleNotFoundError:
            text = 'Нет модуля для работы с виджетами'
    elif n == 1:
        try:
            import work_with_bd
        except ModuleNotFoundError:
            text = 'Нет модуля для работы с базой данных'
    elif n == 2:
        if os.path.isfile('data/elements.sqlite3'):  # Проверка существования бд
            data = Base_date('data/elements.sqlite3')
        else:
            text = "База данных не найдена"
    elif n == 3:
        if os.path.isfile(
                'data/__init__.py'):  # Проверка существования файла для работы с кнопками-картинками
            d = {}
            for y in data.select(['Type'], 'Groups'):
                elements = data.select(['image_on'], 'Elements', 'and',
                                       ["type", y])
                for i in range(len(elements)):
                    if os.path.isfile(f'data/images/{elements[i]}'):
                        d[y + "_" + str(i)] = {
                            "images": {
                                "normal_image": {
                                    "path": f"data/images/{elements[i]}"
                                }
                            }
                        }
            with open("data/theme.json", "w") as write_file:
                json.dump(d, write_file)
        else:
            text = "Нет файла для работы с кнопками-картинками"
    if text is None and n >= 0:
        z[n].image = load_image("data/On.png", colorkey=None)

    lamp.draw(screen)
    return text


def start_screen():
    intro_text = ["  СПРАВКА", "",
                  "Правила работы в приложении:",
                  "  Не перенагружайте цепи!!!", "  Сохраняйте проект"]

    fon = pygame.transform.scale(load_image('fon22.jpg', colorkey=None),
                                 (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, (50, 50, 150))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()
    loading(-1)
    n = 0
    start = time.time()
    mistake = False
    while True:
        push = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if mistake:
                    terminate()
                push = True
                if n >= CHECKS:
                    return GameStates.GAME_SCREEN
        if mistake:
            mistake_rendered = font.render(message, 1, pygame.Color('red'))
            mistake_rect = mistake_rendered.get_rect()
            mistake_rect.y = 850
            mistake_rect.x = WIDTH // 4
            screen.blit(mistake_rendered, mistake_rect)

        if (time.time() - start > random.randrange(1, 5) or push) and n < CHECKS \
                and not mistake:
            start = time.time()
            message = loading(n)
            if message is not None:
                mistake = True

            n += 1
        pygame.display.flip()
        clock.tick(FPS)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = self.x - target.rect.x
        self.dy = self.y - target.rect.y
        self.x, self.y = target.rect.x + self.dx, target.rect.y + self.dy

buttons = {}


def change_group(group, manage):
    global buttons, data
    for i in buttons.keys():
        i.kill()
    buttons = {}
    d = {}
    elements = data.select(['image_on'], 'Elements', 'and', ["type", group])
    for i in range(len(elements)):
        buttons[pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, i * 100 + 40), (60, 95)),
            text='',
            manager=manage, object_id=group + "_" + str(i))] = elements[i]
    print(buttons)
'''class Landing(pygame.sprite.Sprite):
    image = load_image("pt.png")

    def __init__(self, group, pos):
        super().__init__(group)
        self.image = Landing.image
        self.rect = self.image.get_rect()
'''
class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, group, x1, y1, x2, y2):
        super().__init__(group)
        self.image = pygame.Surface([x2, y2])
        print(x1, y1, x2, y2)
        self.rect = pygame.Rect(x1, y1, x2, y2)
        pygame.draw.rect(self.image, (150, 250, 150), (0, 0, x2, y2), 1)
def draw(background):
    print(1)
    background.fill((0, 0, 0))
    pygame.draw.rect(background, (0, 150, 50),
                     (200, 0, WIDTH - 200, HEIGHT), width=0)
    '''for i in range(29):
        for y in range(26):
            pygame.draw.rect(background, (150, 150, 150),
                             (200 + i * 35, y * 35, 35, 35), width=1)'''


def game_screen():
    global state
    pygame.display.set_caption("Start")
    window_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    background = pygame.Surface((WIDTH, HEIGHT))
    #draw(background)
    manage = pygame_gui.UIManager((WIDTH, HEIGHT), 'data/theme.json')
    res = data.select(['Type'], 'Groups')
    group = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=res, starting_option=res[0],
        relative_rect=pygame.Rect((10, 10), (150, 25)), manager=manage
    )
    change_group(res[0], manage)
    pygame.draw.rect(background, (50, 150, 50),
                     (200, 0, WIDTH - 200, HEIGHT), width=0)
    '''entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((350, 100), (100, 25)), manager=manage)'''
    clock = pygame.time.Clock()
    run = True
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Group()
    for i in range(29):
        Border(sprite, 200 + i * 50, 0, 2, HEIGHT)
    for i in range(26):
        Border(sprite, 200, i * 50, WIDTH, 2)
    print(sprite)
    #element_sprites = pygame.sprite.Group()
    #camera=Camera()
    mouse_down = False
    while run:
        #background.fill((0, 150, 50))
        #all_sprites.draw(background)
        #draw(background)
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                conf_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((250, 200), (300, 200)), manager=manage,
                    window_title="Подтверждение",
                    action_long_desc='Вы уверены?', action_short_name='Да',
                    blocking=False)
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    print(event.text)
                elif event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    terminate()
                elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    print(buttons[event.ui_element])
                elif event.user_type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
                    color = (0, 0, 0)
                elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    print(event.text)
                    change_group(event.text, manage)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
            elif event.type == pygame.MOUSEMOTION and mouse_down:
                print(20000)
                '''camera.update(player)
                    for sprite in all_sprites:
                        camera.apply(sprite)'''
            manage.process_events(event)
        manage.update(time_delta)
        window_surface.blit(background, (0, 0))
        sprite.draw(screen)
        manage.draw_ui(window_surface)
        #all_sprites.update()
        #screen.fill((0, 150, 50))
        pygame.display.flip()


if __name__ == "__main__":
    state = GameStates.START_SCREEN

    screen_funcs = {GameStates.START_SCREEN: start_screen,
                    GameStates.GAME_SCREEN: game_screen}
    while True:
        state = screen_funcs[state]()
pygame.quit()
