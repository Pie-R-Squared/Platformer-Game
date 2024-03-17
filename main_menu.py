import pygame

from pygame_gui import UIManager, UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton

from app_state_interface import IAppState
import spritesheet


class MainMenu(IAppState):

    def __init__(self, window_surface: pygame.Surface, ui_manager: UIManager):
        # initialise main menu attributes
        self.window_surface = window_surface
        self.ui_manager = ui_manager

        self.start_game_button = None
        self.customisations_button = None
        self.controls_button = None
        self.quit_button = None

        self.player_image = pygame.image.load('images/spritesheet_player.png').convert_alpha()
        self.sprite_sheet_player = spritesheet.Spritesheet(self.player_image)
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 120  # delay between animation frames
        self.player_frame = 0  # initial animation frame
        self.player_animation_list = []  # holds all animation frames
        self.player_animation_steps = 12  # number of steps in sprite-sheet
        for x in range(self.player_animation_steps):  # append frames to animation list
            self.player_animation_list.append(self.sprite_sheet_player.get_image(x, 125, 177, 2))

        self.enemy_image = pygame.image.load('images/zombie_sheet.png').convert_alpha()
        self.sprite_sheet_enemy = spritesheet.Spritesheet(self.enemy_image)
        self.enemy_frame = 0
        self.enemy_animation_list = []
        self.enemy_animation_steps = 6
        for x in range(self.enemy_animation_steps):  # append frames to animation list
            self.enemy_animation_list.append(self.sprite_sheet_enemy.get_image(x+8, 200, 250, 2))

        self.is_time_to_transition = False
        self.transition_target = "None"

        self.background_surface = None
        self.game_title = None

        self.font = pygame.font.SysFont('Rage', 100)  # font set to 'rage', size 100

    def start(self):
        # transition time originally set to false
        self.is_time_to_transition = False
        self.transition_target = "None"

        # sets the background image and converts to proper format
        self.background_surface = pygame.image.load('images/dark_cave_entrance.png').convert_alpha()

        self.game_title = self.font.render('Zombie Onslaught', False, (220, 0, 0))

        # draws the 'start game' rectangle
        start_game_button_pos_rect = pygame.Rect(0, 0, 200, 40)
        start_game_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        start_game_button_pos_rect.top = self.window_surface.get_height() * 0.4
        self.start_game_button = UIButton(relative_rect=start_game_button_pos_rect,
                                          text="Start Game",
                                          manager=self.ui_manager)

        # draws the 'customisations' rectangle
        customisations_button_pos_rect = pygame.Rect(0, 0, 200, 40)
        customisations_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        customisations_button_pos_rect.top = start_game_button_pos_rect.bottom + 25
        self.customisations_button = UIButton(relative_rect=customisations_button_pos_rect,
                                              text="Customisations",
                                              manager=self.ui_manager)

        # draws the 'controls' rectangle
        controls_button_pos_rect = pygame.Rect(0, 0, 200, 40)
        controls_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        controls_button_pos_rect.top = customisations_button_pos_rect.bottom + 25
        self.controls_button = UIButton(relative_rect=controls_button_pos_rect,
                                        text="Controls",
                                        manager=self.ui_manager)

        # draws the 'quit' rectangle
        quit_button_pos_rect = pygame.Rect(0, 0, 200, 40)
        quit_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        quit_button_pos_rect.top = controls_button_pos_rect.bottom + 25
        self.quit_button = UIButton(relative_rect=quit_button_pos_rect,
                                    text="Quit",
                                    manager=self.ui_manager)

    def stop(self):
        # removes buttons when function called
        self.start_game_button.kill()
        self.customisations_button.kill()
        self.controls_button.kill()
        self.quit_button.kill()

        self.background_surface = None
        self.game_title = None

        self.start_game_button = None
        self.customisations_button = None
        self.controls_button = None
        self.quit_button = None

    # handles the transition changes and their data types
    def time_to_transition(self) -> bool:
        return self.is_time_to_transition

    def get_transition_target(self) -> str:
        return self.transition_target

    def update(self, time_delta: float):
        self.ui_manager.update(time_delta=time_delta)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.player_frame += 1  # increment frame after cooldown
            self.enemy_frame += 1
            self.last_update = current_time  # reset timer
            if self.player_frame >= len(self.player_animation_list):
                self.player_frame = 0  # loop back to first frame when last frame reached
            if self.enemy_frame >= len(self.enemy_animation_list):
                self.enemy_frame = 0

    def process_event(self, event: pygame.event.Event):
        self.ui_manager.process_events(event)

        # checks if each button is pressed then moves onto the selected screen
        if event.type == pygame.USEREVENT and event.user_type == UI_BUTTON_PRESSED:
            if event.ui_element == self.start_game_button:
                self.is_time_to_transition = True
                self.transition_target = 'game_state'
            elif event.ui_element == self.customisations_button:
                self.is_time_to_transition = True
                self.transition_target = 'customisations_state'
            elif event.ui_element == self.controls_button:
                self.is_time_to_transition = True
                self.transition_target = 'controls_screen'
            elif event.ui_element == self.quit_button:
                self.is_time_to_transition = True
                self.transition_target = 'quit_app'

    def draw(self):
        self.window_surface.blit(self.background_surface, (0, 0))
        self.ui_manager.draw_ui(self.window_surface)
        self.window_surface.blit(self.game_title, (200, 20))
        self.window_surface.blit(self.player_animation_list[self.player_frame], (50, 150))  # draw player animation
        self.window_surface.blit(self.enemy_animation_list[self.enemy_frame], (600, 50))  # draw enemy animation
