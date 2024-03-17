import pygame

from pygame_gui import UIManager, UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton, UILabel

from app_state_interface import IAppState


class Customisations(IAppState):
    # state which displays the character and weapon customisations
    def __init__(self, window_surface: pygame.Surface, ui_manager: UIManager):
        self.window_surface = window_surface
        self.ui_manager = ui_manager

        self.to_menu_button = None
        self.customisations_title = None  # set to null so it doesn't display on the main menu

        self.is_time_to_transition = False
        self.transition_target = "None"

        self.background_surface = None

        self.soldier_image = None  # a frame of soldier sprite sheet
        self.soldier_rect = None  # surrounding rectangle
        self.boy_image = None  # a frame of boy sprite sheet
        self.boy_rect = None

        self.char_choices = None  # list
        self.char_choice = 0  # initial choice

    def start(self):
        self.is_time_to_transition = False
        self.transition_target = "None"

        self.background_surface = pygame.Surface(self.window_surface.get_size())
        self.background_surface.convert(self.window_surface)
        self.background_surface.fill(pygame.Color('#2f0909'))  # background set to dark red

        start_game_button_pos_rect = pygame.Rect(0, 0, 150, 40)
        start_game_button_pos_rect.right = self.window_surface.get_rect().right - 50
        start_game_button_pos_rect.bottom = self.window_surface.get_rect().bottom - 50
        self.to_menu_button = UIButton(relative_rect=start_game_button_pos_rect,
                                       text="To Menu",
                                       manager=self.ui_manager)

        self.customisations_title = UILabel(relative_rect=pygame.Rect(0, 15,
                                                                      self.window_surface.get_width(),
                                                                      70),
                                            text='Character Customisations',
                                            manager=self.ui_manager,
                                            object_id='#customisations_title')  # main heading
        # soldier image, scale, rectangle, coordinate attributes
        self.soldier_image = pygame.image.load('images/player_img.png').convert_alpha()
        self.soldier_image = pygame.transform.scale(self.soldier_image, (250, 354))  # enlarge scale
        self.soldier_rect = self.soldier_image.get_rect()
        self.soldier_rect.topleft = (100, 100)  # top left position
        # boy image, scale, rectangle, coordinate attributes
        self.boy_image = pygame.image.load('images/player_2_img.png').convert_alpha()
        self.boy_image = pygame.transform.scale(self.boy_image, (250, 354))
        self.boy_rect = self.boy_image.get_rect()
        self.boy_rect.topleft = (600, 100)

        self.char_choices = [self.soldier_image, self.boy_image]  # list of choices

    def stop(self):
        self.to_menu_button.kill()  # remove buttons from screen
        self.to_menu_button = None

        self.customisations_title.kill()
        self.customisations_title = None

        self.background_surface = None

        self.to_menu_button = None

    def time_to_transition(self) -> bool:
        return self.is_time_to_transition

    def get_transition_target(self) -> str:
        return self.transition_target

    def update(self, time_delta: float):
        self.ui_manager.update(time_delta=time_delta)

        with open('character_selection.txt', 'w') as character_selection:  # open character selection text file
            if self.char_choice == 0:  # if soldier selected
                character_selection.write(str(self.char_choice))  # write selection to text file
            elif self.char_choice == 1:  # if boy selected
                character_selection.write(str(self.char_choice))  # write 1 if boy selected

    def process_event(self, event: pygame.event.Event):
        self.ui_manager.process_events(event)

        if (event.type == pygame.USEREVENT
                and event.user_type == UI_BUTTON_PRESSED
                and event.ui_element == self.to_menu_button):
            self.is_time_to_transition = True
            self.transition_target = 'main_menu'  # redirects to menu

        if event.type == pygame.MOUSEBUTTONDOWN:  # checks for mouse presses
            if self.soldier_rect.collidepoint(event.pos) and pygame.mouse.get_pressed()[0]:
                print("Soldier selected")  # print this if soldier image clicked
                pygame.draw.rect(self.soldier_image, (0, 255, 0), self.soldier_image.get_rect(), 4)
                # highlight soldier image, de-highlight boy image
                pygame.draw.rect(self.boy_image, (47, 9, 9), self.boy_image.get_rect(), 4)
                self.char_choice = 0  # set choice to 0
            elif self.boy_rect.collidepoint(event.pos) and pygame.mouse.get_pressed()[0]:
                print("Boy selected")
                pygame.draw.rect(self.boy_image, (0, 255, 0), self.boy_image.get_rect(), 4)
                # highlight boy image, de-highlight soldier image
                pygame.draw.rect(self.soldier_image, (47, 9, 9), self.soldier_image.get_rect(), 4)
                self.char_choice = 1  # set choice to 1

    def draw(self):
        self.window_surface.blit(self.background_surface, (0, 0))  # display background
        self.window_surface.blit(self.char_choices[0], self.soldier_rect)  # draw soldier
        self.window_surface.blit(self.char_choices[1], self.boy_rect)  # draw boy
        self.ui_manager.draw_ui(self.window_surface)  # draw ui
