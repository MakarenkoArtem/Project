
import pip
pip.main(['install', 'pygame_gui'])
import pygame
import pygame_gui
pygame.init()
pygame.display.set_caption("Start")
window_surface = pygame.display.set_mode((800, 600))
background = pygame.Surface((800, 600))
color = (0, 0, 0)
background.fill(color)
manage = pygame_gui.UIManager((800, 600))
green = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)), text='green', manager=manage)
red = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 275), (100, 50)), text='red', manager=manage)
blue = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 275), (100, 50)), text='blue', manager=manage)
lis = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=['Easy', 'Medium', 'Hard'], starting_option='Easy', relative_rect=pygame.Rect((350, 150), (100, 25)), manager=manage
)
entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 100), (100, 25)), manager=manage)
clock = pygame.time.Clock()
run = True
while run:
    time_delta = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            conf_dialog = pygame_gui.windows.UIConfirmationDialog(rect=pygame.Rect((250, 200), (300, 200)), manager=manage, window_title="Подтверждение", action_long_desc='Вы уверены?', action_short_name='OK', blocking=False)
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                print(event.text)
            elif event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                run = False
            elif event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED:
                if event.ui_element == green:
                    color = (0, 255, 0)
                elif event.ui_element == red:
                    color = (255, 0, 0)
                elif event.ui_element == blue:
                    color = (0, 0, 255)
            elif event.user_type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
                color = (0, 0, 0)
            elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                print(event.text)
            background.fill(color)
        manage.process_events(event)
    manage.update(time_delta)
    window_surface.blit(background, (0, 0))
    manage.draw_ui(window_surface)
    pygame.display.update()