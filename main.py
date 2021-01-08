import sys
import json
import os
import time
from work_with_bd import *
import random
from enum import Enum
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog

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
try:
    from screeninfo import get_monitors
except ModuleNotFoundError:
    import pip

    pip.main(['install', "screeninfo"])
    from screeninfo import get_monitors


class GameStates(Enum):
    START_SCREEN = 1
    GAME_SCREEN = 2
    GAME_ON_PAUSE_SCREEN = 3
    STOP_SCREEN = 4


size = get_monitors()[0]
size = WIDTH, HEIGHT = size.width - 50, size.height - 100
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
        z = []
        lamp = pygame.sprite.Group()
        for i in range(CHECKS):
            sprite = pygame.sprite.Sprite()
            sprite.image = load_image("data/Off.png", colorkey=None)
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = WIDTH // (CHECKS + 1) * (i + 1)
            sprite.rect.y = HEIGHT * 0.8
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
    elif text is not None:
        text = text.rjust(int(WIDTH * 0.0645), " ")

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
    text_coord = WIDTH * 0.1
    for line in intro_text:
        string_rendered = font.render(line, 1, (50, 50, 150))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = HEIGHT * 0.08
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
                # if mistake:
                #    terminate()
                push = True
                if n >= CHECKS:
                    return GameStates.GAME_SCREEN
        if mistake:
            mistake_rendered = font.render(message, 1, pygame.Color('red'))
            mistake_rect = mistake_rendered.get_rect()
            mistake_rect.y = HEIGHT * 0.95
            mistake_rect.x = 0
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


'''
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
'''


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, all_sprites, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(x, y)
        self.n = 0
        self.down = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.n += 1
        if self.n // 35 and self.down:
            self.n = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if self.n // 35:
            self.n = 0
        if not self.down:
            self.cur_frame = 1
            self.image = self.frames[self.cur_frame]


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
            relative_rect=pygame.Rect((15 + (i + 1) // 2 * 75, i // 2 * 100 + 40), (65, 95)),
            text='',
            manager=manage, object_id=group + "_" + str(i))] = elements[i]

    print(buttons)


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(372, 341)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(6, 212, 111, 16))
        self.label.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(120, 210, 221, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(6, 242, 111, 16))
        self.label_2.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(350, 240, 16, 16))
        self.label_3.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(6, 272, 111, 16))
        self.label_4.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(350, 270, 16, 16))
        self.label_5.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_5.setObjectName("label_5")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.doubleSpinBox.setGeometry(QtCore.QRect(120, 240, 221, 21))
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(120, 270, 221, 21))
        self.spinBox.setMaximum(100)
        self.spinBox.setProperty("value", 100)
        self.spinBox.setObjectName("spinBox")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(264, 310, 101, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Название:"))
        self.label_2.setText(_translate("Dialog", "Напряжение:"))
        self.label_3.setText(_translate("Dialog", "В"))
        self.label_4.setText(_translate("Dialog", "Целостность:"))
        self.label_5.setText(_translate("Dialog", "%"))
        self.pushButton.setText(_translate("Dialog", "Редактировать"))


class Info(QDialog, Ui_Dialog):  # Класс виджета информации о программе
    def __init__(self, title, voltage, health):
        super(Info, self).__init__()
        super().__init__()
        self.setupUi(self)
        self.lineEdit.setText(title)
        self.doubleSpinBox.setValue(voltage)
        self.spinBox.setValue(health)


class Element(pygame.sprite.Sprite):  # Надо работать здесь
    def __init__(self, group, buttons, args):
        super().__init__(group)
        self.title, self.voltage, self.image_off, self.image_on, self.health = args[1:]
        self.voltage = float(".".join(self.voltage.split(",")))
        if self.health is None:
            self.health = 100
        self.image_on = load_image("data/images/" + self.image_on)
        self.image = self.image_off = load_image("data/images/" + self.image_off)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.y, self.rect.x = 300, 300
        self.down = False
        self.dx, self.dy = 0, 0

    def show(self):
        app = QApplication(sys.argv)
        Info(self.title, self.voltage, self.health).exec_()  # Вызов класс виджета информации о программе
        app.exit()

    def down_event(self, pos, sprite):
        if self.rect[0] <= pos[0] <= self.rect[0] + self.rect[2] and self.rect[1] <= pos[1] <= self.rect[1] + self.rect[
            3]:
            self.down = True
            self.dx = pos[0] - self.rect[0]
            self.dy = pos[1] - self.rect[1]
            self.sprite = sprite
        return self.down

    def move(self, pos):
        if self.down:
            self.rect.x, self.rect.y = pos[0] - self.dx, pos[1] - self.dy


class Elementsprites(pygame.sprite.Group):
    def down(self, pos):
        for sprite in self.sprites():
            if isinstance(sprite, Element):
                if sprite.down_event(pos, sprite):
                    print(sprite)
                    return sprite

    def killed(self, trash):
        for sprite in self.sprites():
            if pygame.sprite.collide_mask(sprite, trash):
                sprite.kill()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, group, x1, y1, x2, y2):
        super().__init__(group)
        self.image = pygame.Surface([x2, y2])
        self.rect = pygame.Rect(x1, y1, x2, y2)
        pygame.draw.rect(self.image, (150, 250, 150), (0, 0, x2, y2), 1)


def draw(background):
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
    # draw(background)
    manage = pygame_gui.UIManager((WIDTH, HEIGHT), 'data/theme.json')
    res = data.select(['Type'], 'Groups')
    group = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=res, starting_option=res[0],
        relative_rect=pygame.Rect((15, 10), (150, 25)), manager=manage
    )
    change_group(res[0], manage)
    pygame.draw.rect(background, (50, 150, 50),
                     (200, 0, WIDTH - 200, HEIGHT), width=0)
    '''entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((350, 100), (100, 25)), manager=manage)'''
    clock = pygame.time.Clock()
    run = True
    all_sprites = pygame.sprite.Group()
    trash = AnimatedSprite(all_sprites, load_image("data/basket.png", colorkey=-1), 2, 1, WIDTH - 60, HEIGHT - 65)
    sprite = pygame.sprite.Group()
    for i in range(WIDTH // 50 + 1):
        Border(sprite, 200 + i * 50, 0, 2, HEIGHT)
    for i in range(HEIGHT // 50 + 1):
        Border(sprite, 200, i * 50, WIDTH, 2)
    element_sprites = Elementsprites()
    # camera=Camera()
    mouse_down = False
    elem = None
    while run:
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                conf_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((250, 200), (300, 200)), manager=manage,
                    window_title="Выход",
                    action_long_desc='Вы хотите выйти?', action_short_name='Да',
                    blocking=False)
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    print(event.text)
                elif event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    terminate()
                elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element in buttons.keys():
                        element_sprites.add(Element(element_sprites, buttons, data.select(['*'], 'Elements', 'and',
                                                                                          ['image_on',
                                                                                           buttons[event.ui_element]])[
                            0]))
                elif event.user_type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
                    color = (0, 0, 0)
                elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    print(event.text)
                    change_group(event.text, manage)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                elem = element_sprites.down(event.pos)
                if event.button == 3 and elem is not None:
                    elem.show()
                if elem is not None:
                    trash.down = True
                print(event.button)
            elif event.type == pygame.MOUSEBUTTONUP and elem is not None:
                elem.down = False
                trash.down = False
                elem = None
            elif event.type == pygame.MOUSEMOTION and elem is not None and elem.down:
                elem.move(event.pos)
                '''camera.update(player)
                    for sprite in all_sprites:
                        camera.apply(sprite)'''
            manage.process_events(event)
        manage.update(time_delta)
        window_surface.blit(background, (0, 0))
        sprite.draw(screen)
        element_sprites.killed(trash)
        element_sprites.draw(screen)
        manage.draw_ui(window_surface)
        all_sprites.draw(screen)
        all_sprites.update()
        # screen.fill((0, 150, 50))
        pygame.display.flip()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    sys.excepthook = except_hook
    state = GameStates.START_SCREEN

    screen_funcs = {GameStates.START_SCREEN: start_screen,
                    GameStates.GAME_SCREEN: game_screen}
    while True:
        state = screen_funcs[state]()
pygame.quit()
