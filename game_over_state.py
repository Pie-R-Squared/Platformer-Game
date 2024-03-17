import pygame

from pygame_gui import UIManager, UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton

from app_state_interface import IAppState
import spritesheet


class GameOver(IAppState):
    # state for game over screen
    def __init__(self, window_surface: pygame.Surface, ui_manager: UIManager):
        self.window_surface = window_surface
        self.ui_manager = ui_manager

        self.menu_button = None  # button for redirecting to menu
        self.is_time_to_transition = False
        self.transition_target = "None"

        self.score_font = pygame.font.SysFont('Book Antiqua', 40)  # choose custom font
        self.text_surface = None  # no text shown until game over
        self.text_rect = None  # score text rectangle
        self.high_score_font = pygame.font.SysFont('Book Antiqua', 30)  # custom high scores font
        self.high_scores_text = None  # shown alongside the score
        self.high_scores_text_rect = None  # high score rectangle
        self.score = None  # score will later be read from a file

        self.background_surface = None  # no background initially
        self.death_animation_sheet = None  # sprite sheet image
        self.death_animation = None  # sprite sheet attribute
        self.animation_steps = 6  # number of frames
        self.animation_list = []
        self.change_frame = True  # frame changes as soon as it's game over
        self.frame = 0  # initial frame
        self.last_update = pygame.time.get_ticks()  # last updated time
        self.animation_cooldown = 200  # animation delay

    def start(self):
        # transition time originally set to false
        self.is_time_to_transition = False
        self.transition_target = "None"

        # sets the background image and converts to proper format
        self.background_surface = pygame.image.load('images/dark_cavern2.jpg').convert_alpha()
        self.death_animation_sheet = pygame.image.load('images/character_death_animation.png').convert_alpha()
        self.death_animation = spritesheet.Spritesheet(self.death_animation_sheet)  # initialise sprite sheet
        for x in range(self.animation_steps):  # loop through each frame
            self.animation_list.append(self.death_animation.get_image(x, 188, 177, 2))  # add to the animation list

        # draws the 'back to menu' rectangle
        menu_button_pos_rect = pygame.Rect(0, 0, 250, 40)
        menu_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        menu_button_pos_rect.top = self.window_surface.get_height() * 0.6
        self.menu_button = UIButton(relative_rect=menu_button_pos_rect,
                                    text="Back to Menu",
                                    manager=self.ui_manager)
        with open('score.txt', 'r') as scoring:
            self.score = scoring.read()  # read score from text file, display game over, score
        self.text_surface = self.score_font.render('You died. Score: ' + self.score, False, (220, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=(500, 200))  # align text to centre

    def stop(self):
        # removes buttons when function called
        self.menu_button.kill()
        self.background_surface = None
        self.menu_button = None

    # handles the transition changes and their data types
    def time_to_transition(self) -> bool:
        return self.is_time_to_transition

    def get_transition_target(self) -> str:
        return self.transition_target

    def update(self, time_delta: float):
        self.ui_manager.update(time_delta=time_delta)
        with open('high-scores.txt', 'r+') as high_scores:
            high_score = high_scores.read()  # read previous high score
            high_scores.seek(0)  # checks item at the first index
            if int(self.score) >= int(high_score):  # compare score and high score as integers
                high_scores.write(self.score)  # write new high score at the end of the file
                high_scores.truncate()  # clear old data
                self.high_scores_text = self.high_score_font.render('New High Score: ' + self.score + "!", False,
                                                                    (150, 0, 0))  # render high score text
            else:
                self.high_scores_text = self.high_score_font.render('High Score: ' + high_score, False, (150, 0, 0))
            self.high_scores_text_rect = self.text_surface.get_rect(center=(550, 300))  # set high score text centre

        current_time = pygame.time.get_ticks()  # checks the time
        if self.frame != len(self.animation_list)-1 and (current_time - self.last_update >= self.animation_cooldown):
            self.frame += 1  # update animation frames
            self.last_update = current_time  # set last timer update to the current time

    def process_event(self, event: pygame.event.Event):
        self.ui_manager.process_events(event)

        # checks if menu button is pressed then moves onto the main menu screen
        if event.type == pygame.USEREVENT and event.user_type == UI_BUTTON_PRESSED:
            if event.ui_element == self.menu_button:
                self.is_time_to_transition = True
                self.transition_target = 'main_menu'

    def draw(self):
        self.window_surface.blit(self.background_surface, (0, 0))
        self.ui_manager.draw_ui(self.window_surface)
        self.window_surface.blit(self.text_surface, self.text_rect)  # display text at centre
        self.window_surface.blit(self.high_scores_text, self.high_scores_text_rect)  # display high score
        self.window_surface.blit(self.animation_list[self.frame], (0, 100))  # draw death animation
