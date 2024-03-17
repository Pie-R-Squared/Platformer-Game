import pygame

from pygame_gui import UIManager, UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton, UILabel

from app_state_interface import IAppState


class ControlsState(IAppState):
    # state which displays the controller/ keyboard controls
    def __init__(self, window_surface: pygame.Surface, ui_manager: UIManager):
        self.window_surface = window_surface
        self.ui_manager = ui_manager

        self.to_menu_button = None
        self.controls_state_title = None  # set to null so it doesn't display on the main menu

        self.keyboard_subtitle = None  # subtitles for each set of controls
        self.ds4_subtitle = None

        self.keyboard_keys = None  # images of keyboard
        self.ds4_controls = None  # and controller

        self.is_time_to_transition = False
        self.transition_target = "None"

        self.background_surface = None

    def start(self):
        self.is_time_to_transition = False
        self.transition_target = "None"

        self.background_surface = pygame.Surface(self.window_surface.get_size())
        self.background_surface.convert(self.window_surface)
        self.background_surface.fill(pygame.Color('#2f0909'))  # background set to dark red

        self.keyboard_keys = pygame.image.load('images/keyboard_keys2.png').convert_alpha()  # load keyboard image
        self.keyboard_keys = pygame.transform.scale(self.keyboard_keys, (520, 479))  # increase scale
        self.ds4_controls = pygame.image.load('images/ds4_controls.png').convert_alpha()  # load ds4 image
        self.ds4_controls = pygame.transform.scale(self.ds4_controls, (500, 363)) # decrease scale

        start_game_button_pos_rect = pygame.Rect(0, 0, 150, 40)
        start_game_button_pos_rect.right = self.window_surface.get_rect().right - 50
        start_game_button_pos_rect.bottom = self.window_surface.get_rect().bottom - 50
        self.to_menu_button = UIButton(relative_rect=start_game_button_pos_rect,
                                       text="To Menu",
                                       manager=self.ui_manager)

        self.controls_state_title = UILabel(relative_rect=pygame.Rect(0, 15,
                                                                      self.window_surface.get_width(),
                                                                      70),
                                            text='Controls',
                                            manager=self.ui_manager,
                                            object_id='#controls_state_title')  # main heading

        self.keyboard_subtitle = UILabel(relative_rect=pygame.Rect(150, 100, 200, 50),
                                         text='Keyboard Controls',
                                         manager=self.ui_manager,
                                         object_id='#keyboard_subtitle')  # keyboard subtitle

        self.ds4_subtitle = UILabel(relative_rect=pygame.Rect(640, 100, 200, 50),
                                    text='DualShock 4 Controls',
                                    manager=self.ui_manager,
                                    object_id='#ds4_subtitle')  # controller subtitle

    def stop(self):
        self.to_menu_button.kill()  # remove buttons from screen
        self.to_menu_button = None

        self.controls_state_title.kill()
        self.controls_state_title = None
        self.keyboard_subtitle.kill()
        self.keyboard_subtitle = None
        self.ds4_subtitle.kill()
        self.ds4_subtitle = None

        self.background_surface = None

        self.to_menu_button = None

    def time_to_transition(self) -> bool:
        return self.is_time_to_transition

    def get_transition_target(self) -> str:
        return self.transition_target

    def update(self, time_delta: float):
        self.ui_manager.update(time_delta=time_delta)

    def process_event(self, event: pygame.event.Event):
        self.ui_manager.process_events(event)

        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_PRESSED
                and event.ui_element == self.to_menu_button):
            self.is_time_to_transition = True
            self.transition_target = 'main_menu'  # redirects to menu

    def draw(self):
        self.window_surface.blit(self.background_surface, (0, 0))  # display background
        self.window_surface.blit(self.keyboard_keys, (0, 100))  # display kb image
        self.window_surface.blit(self.ds4_controls, (480, 145))  # display controller image
        self.ui_manager.draw_ui(self.window_surface)  # draw ui
