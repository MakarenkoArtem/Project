import sys
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
    import pygame_gui
try:
    import pygame
except ModuleNotFoundError:
    import pip

    pip.main(['install', "pygame"])
    import pygame

"""--------------------------------------------------------------------------"""


class GameStates(Enum):
    START_SCREEN = 1
    GAME_SCREEN = 2
    GAME_ON_PAUSE_SCREEN = 3
    STOP_SCREEN = 4


WIDTH, HEIGHT = 1200, 900
tile_width = tile_height = 50
FPS = 30
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
data = Base_date('elements.sqlite3')


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
    if n == 0:
        lamp = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        try:
            import work_with_bd
            sprite.image = load_image("On.png", colorkey=-1)
        except ModuleNotFoundError:
            text = 'Нет модуля работы с базой данных'
            sprite.image = load_image("Off.png", colorkey=-1)
        finally:
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = 100
            sprite.rect.y = 200
            lamp.add(sprite)
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
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()
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
                if n:
                    return GameStates.GAME_SCREEN
        if mistake:
            mistake_rendered = font.render(message, 1, pygame.Color('red'))
            mistake_rect = mistake_rendered.get_rect()
            mistake_rect.top = 250
            mistake_rect.x = 200
            screen.blit(mistake_rendered, mistake_rect)

        if time.time() - start > random.randrange(1, 5) or push:
            start = time.time()
            message = loading(n)
            print(1)
            if message is not None:
                mistake = True

            n += 1
        pygame.display.flip()
        clock.tick(FPS)


buttons = []


def change_group(elements, manage):
    global buttons
    for _ in range(len(buttons)):
        buttons.pop(0).kill()
    buttons = []
    for i in range(len(elements)):
        buttons.append(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, i * 40 + 40), (150, 35)),
            text=elements[i],
            manager=manage))


def draw(background):
    background.fill((0, 0, 0))
    pygame.draw.rect(background, (50, 150, 50),
                     (200, 0, WIDTH - 200, HEIGHT), width=0)
    for i in range(29):
        for y in range(26):
            pygame.draw.rect(background, (150, 150, 150),
                             (200 + i * 35, y * 35, 35, 35), width=1)


def game_screen():
    global state
    pygame.display.set_caption("Start")
    window_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    background = pygame.Surface((WIDTH, HEIGHT))
    draw(background)
    manage = pygame_gui.UIManager((WIDTH, HEIGHT), 'data/theme.json')
    res = data.select(['Type'], 'Groups')
    group = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=res, starting_option=res[0],
        relative_rect=pygame.Rect((10, 10), (150, 25)), manager=manage
    )
    change_group(data.select(['title'], 'Elements', 'and', ["type", res[0]]),
                 manage)
    pygame.draw.rect(background, (50, 150, 50),
                     (200, 0, WIDTH - 200, HEIGHT), width=0)
    entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((350, 100), (100, 25)), manager=manage)
    """======================Кнопка с картинкой============================"""
    b = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((100, 5 * 40 + 40), (150, 150)),
            text='', manager=manage, object_id="#my_button")
    """======================Кнопка с картинкой============================"""
    clock = pygame.time.Clock()
    run = True
    element_sprites = pygame.sprite.Group()
    while run:
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
                elif event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED:
                    '''if event.ui_element == green:
                        color = (0, 255, 0)
                    elif event.ui_element == red:
                        color = (255, 0, 0)
                    elif event.ui_element == blue:
                        color = (0, 0, 255)'''
                elif event.user_type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
                    color = (0, 0, 0)
                elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    print(event.text)
                    change_group(data.select(['title'], 'Elements', 'and',
                                             ["type", event.text]), manage)
                draw(background)
            manage.process_events(event)
        manage.update(time_delta)
        window_surface.blit(background, (0, 0))
        manage.draw_ui(window_surface)
        pygame.display.flip()


if __name__ == "__main__":
    state = GameStates.START_SCREEN

    screen_funcs = {GameStates.START_SCREEN: start_screen,
                    GameStates.GAME_SCREEN: game_screen}
    while True:
        state = screen_funcs[state]()
pygame.quit()
