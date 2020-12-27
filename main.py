import sys
import os
import random
from enum import Enum
from work_with_bd import *

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
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return GameStates.GAME_SCREEN
        pygame.display.flip()
        clock.tick(FPS)

def change_group(elements, manage):
    for i in range(len(elements)):
        pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((5, i*45 + 35), (100, 40)), text=elements[i],
            manager=manage)
def game_screen():
    global state
    pygame.display.set_caption("Start")
    window_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    background = pygame.Surface((WIDTH, HEIGHT))
    color = (0, 0, 0)
    background.fill(color)
    manage = pygame_gui.UIManager((WIDTH, HEIGHT))
    '''green = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0, 150), (100, 50)), text='green',
        manager=manage)
    red = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0, 250), (100, 50)), text='red',
        manager=manage)
    blue = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0, 350), (100, 50)), text='fon22.jpg',
        manager=manage)'''
    res = data.select(['Type'], 'Groups')
    group = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=res, starting_option=res[0],
        relative_rect=pygame.Rect((10, 10), (150, 25)), manager=manage
    )
    change_group(data.select(['title'], 'Elements', 'and', ["type", res[0]]), manage)
    entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((350, 100), (100, 25)), manager=manage)
    clock = pygame.time.Clock()
    run = True
    while run:
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                conf_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((250, 200), (300, 200)), manager=manage,
                    window_title="Подтверждение",
                    action_long_desc='Вы уверены?', action_short_name='OK',
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
                    change_group(data.select(['title'], 'Elements', 'and', ["type", event.text]), manage)
                background.fill(color)
            manage.process_events(event)
        manage.update(time_delta)
        window_surface.blit(background, (0, 0))
        manage.draw_ui(window_surface)
        pygame.display.update()


if __name__ == "__main__":
    state = GameStates.START_SCREEN

    screen_funcs = {GameStates.START_SCREEN: start_screen,
                    GameStates.GAME_SCREEN: game_screen}
    while True:
        state = screen_funcs[state]()
pygame.quit()
