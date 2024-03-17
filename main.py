# import relevant modules
import pygame

from pygame_gui import UIManager
# imports the main menu state
from main_menu import MainMenu
from game_state import GameState
from customisations_state import Customisations
from controls_screen import ControlsState
from game_over_state import GameOver


class Game:
    def __init__(self):
        pygame.init()  # initialise pygame module

        # opens pygame window with set dimensions
        self.window_surface = pygame.display.set_mode((1000, 600))
        self.ui_manager = UIManager(window_resolution=self.window_surface.get_size(),
                                    theme_path='theme.json')  # load font and colours
        pygame.display.set_caption("game window")  # sets caption of pygame window

        # initialises the main menu state and all the connected states in a dictionary
        self.states = {'main_menu': MainMenu(self.window_surface, self.ui_manager),
                       'game_state': GameState(self.window_surface, self.ui_manager),
                       'controls_screen': ControlsState(self.window_surface, self.ui_manager),
                       'customisations_state': Customisations(self.window_surface, self.ui_manager),
                       'game_over_state': GameOver(self.window_surface, self.ui_manager)}
        self.active_state = self.states['main_menu']  # sets main menu state as current state
        self.active_state.start()  # launches current state
        pygame.mouse.set_cursor(pygame.cursors.broken_x)  # change cursor design

        self.clock = pygame.time.Clock()  # starts timer
        self.is_running = True  # to check if the game is running

    def run(self):
        # loops until it's time to quit
        while self.is_running:
            time_delta = self.clock.tick() / 1000.0
            # checks if it's time to switch states
            self.check_transition()

            for event in pygame.event.get():  # event handler
                if event.type == pygame.QUIT:
                    self.is_running = False  # sets running to false
                # passes event from queue to current state
                self.active_state.process_event(event)
            # updates current state and passes time_delta parameter
            self.active_state.update(time_delta=time_delta)
            # draws current state
            self.active_state.draw()

            pygame.display.update()  # updates the display
        # quits the current state
        self.active_state.stop()

    def check_transition(self):
        # Checks the active state to see if it's time to switch to a different state
        if self.active_state.time_to_transition():
            if self.active_state.get_transition_target() == "quit_app":
                self.is_running = False  # terminate if exit button clicked
            else:
                self.active_state.stop()  # quit current state
                new_state = self.states[self.active_state.get_transition_target()]
                new_state.start()  # start next state
                self.active_state = new_state  # set new state as the current state


# terminates program
if __name__ == "__main__":
    app = Game()
    app.run()  # runs program
