import pygame
import random

from pygame_gui import UIManager, UI_CONFIRMATION_DIALOG_CONFIRMED
from pygame_gui.windows import UIConfirmationDialog

from app_state_interface import IAppState
from main_character import Player
from enemy import Enemy, Spikes, Fire, Boss
from lives_counter import LivesCounter
from score_counter import ScoreCounter


class GameState(IAppState):
    # Game state for interactivity of program
    def __init__(self, window_surface: pygame.Surface, ui_manager: UIManager):
        # initialising the window attributes
        self.window_surface = window_surface
        self.ui_manager = ui_manager
        self.ui_manager.preload_fonts([{'name': 'fira_code', 'point_size': 14, 'style': 'bold'}])

        self.canvas = pygame.Surface((1000, 600))  # surface dimensions
        self.clock = pygame.time.Clock()  # gets time

        self.is_time_to_transition = False  # transition attributes
        self.transition_target = "None"

        self.background_surface = None  # background attributes
        self.gravel_img = None
        self.sprites = None  # sprite groups
        self.counters = None
        self.zombies = None
        self.zombie = None
        self.max_enemies = 5  # maximum number of enemies on-screen
        self.spikes = None
        self.spike = None
        self.fire = None
        self.boss = None

        # initialise character attributes
        self.main_character = None
        self.lives_counter = None
        self.score_counter = None
        self.time = pygame.time.get_ticks()  # start timer
        self.game_over = False  # determines when the game is over
        self.quit_confirmation = None  # check if user really wants to quit

        # custom events
        self.ticks = random.randint(3, 15)  # randomise number of seconds between spawns
        self.enemy_spawn_event = pygame.USEREVENT + 1  # enemy spawning event
        pygame.time.set_timer(self.enemy_spawn_event, (self.ticks * 100))  # 1000 milliseconds = 1 second
        self.spike_spawn_event = pygame.USEREVENT + 2  # new event for spawning spikes
        pygame.time.set_timer(self.spike_spawn_event, ((self.ticks + 10) * 1000))  # set timer
        self.boss_spawn_event = pygame.USEREVENT + 4  # new event for spawning boss
        pygame.time.set_timer(self.boss_spawn_event, 30000)  # set timer

        self.scroll_event = pygame.USEREVENT + 3  # event for handling speed/ time
        pygame.time.set_timer(self.scroll_event, 500)  # increase scroll speed every .5 seconds

        self.vignette = pygame.image.load('images/BloodOverlay.png').convert_alpha()  # blood vignette effect
        self.damage_effect = False  # verifies effect activation
        self.char_choice = None

    def start(self):
        # receive selected character from file
        with open('character_selection.txt', 'r') as character_selection:
            self.char_choice = int(character_selection.read())  # integer value

        self.background_surface = pygame.image.load('images/dark_cavern3.png').convert()
        self.gravel_img = pygame.image.load('images/gravel2.png').convert_alpha()
        # make cursor invisible
        pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
        self.is_time_to_transition = False
        self.transition_target = "None"

        self.sprites = pygame.sprite.Group()  # character group
        self.counters = pygame.sprite.Group()  # score and lives counter group
        self.zombies = pygame.sprite.Group()  # enemy group
        self.spikes = pygame.sprite.Group()  # create spikes group

        # create main character sprite
        self.main_character = Player(self.sprites, self.zombies, self.spikes, self.char_choice)
        self.sprites.add(self.main_character)  # add to sprites group

        self.zombie = Enemy()  # create instance of zombie
        self.zombies.add(self.zombie)  # add to zombies group

        # create the counters
        font = pygame.font.Font(None, 32)
        lives_counter_position = (self.window_surface.get_rect().right - 365,
                                  5)
        self.lives_counter = LivesCounter(position=lives_counter_position,
                                          font=font,
                                          counters=self.counters)  # lives counter

        self.score_counter = ScoreCounter(position=(10, 5),
                                          font=font,
                                          counters=self.counters)  # score counter

    def stop(self):
        pygame.mouse.set_cursor(pygame.cursors.broken_x)
        self.background_surface = None

        # character removed when program terminates
        if self.main_character is not None:
            self.main_character.kill()
            self.main_character = None

        if self.lives_counter is not None:
            self.lives_counter.kill()  # remove counter when terminating
            self.lives_counter = None

        if self.score_counter is not None:
            self.score_counter.kill()
            self.score_counter = None

        if self.boss is not None:
            self.boss = None

        if self.quit_confirmation is not None:
            self.quit_confirmation = None

    def time_to_transition(self) -> bool:
        return self.is_time_to_transition

    def get_transition_target(self) -> str:
        return self.transition_target

    def update(self, time_delta: float):
        # Keep the counters up to date
        if (self.main_character is not None and
                self.main_character.lives != self.lives_counter.num_lives):
            self.lives_counter.set_num_lives(self.main_character.lives)  # update lives

        if (self.main_character is not None and
                self.main_character.score != self.score_counter.score):
            self.score_counter.set_score(self.main_character.score)  # update score

        # check if the game is over
        if self.main_character is not None and self.main_character.lives <= 0:
            self.game_over = True
            with open('score.txt', 'w') as scoring:
                scoring.write(str(self.score_counter.score))  # write score to text file

        # updates the screen, character and enemies
        self.main_character.update(self.zombie.points_amount, self.boss)  # update player, pass boss instance
        self.zombies.update(self.main_character, self.zombies, self.main_character.scrolling)
        if self.boss is not None:  # update boss if not None
            self.boss.update(self.main_character, self.zombies, self.main_character.scrolling)
            if pygame.sprite.collide_mask(self.main_character, self.boss) and self.boss.alive:  # boss collision
                self.main_character.flicker = True  # damage effect active
                self.main_character.lives -= 2  # deduct 2 lives
                self.boss = None  # destroy boss object
            else:
                self.main_character.flicker = False  # damage effect deactivated
        self.spikes.update(self.main_character.scrolling, self.spikes)  # update spikes group
        self.main_character.bullet_group.update(self.zombies, self.boss)  # pass boss to bullet class via player
        self.ui_manager.update(time_delta=time_delta)
        self.counters.update(time_delta)  # update lives and score

        # flicker red vignette effect if damaged
        if self.main_character.flicker:
            self.damage_effect = True  # activate blood effect
        else:
            self.damage_effect = False  # deactivate effect

    def process_event(self, event: pygame.event.Event):
        # updates event
        self.ui_manager.process_events(event)

        # When escape is pressed, a confirmation box pops up
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.mouse.set_cursor(pygame.cursors.broken_x)  # make cursor visible
            quit_confirmation_rect = pygame.Rect(0, 0, 280, 200)  # rectangle dimensions
            quit_confirmation_rect.center = self.window_surface.get_rect().center  # centre
            self.quit_confirmation = UIConfirmationDialog(rect=quit_confirmation_rect,
                                                          manager=self.ui_manager,
                                                          action_long_desc='<b>Are you sure you want to quit?</b>',
                                                          window_title='Go back to main menu',
                                                          action_short_name='Menu',
                                                          object_id='#quit_confirmation')  # text
        if (event.type == pygame.USEREVENT and
                event.user_type == UI_CONFIRMATION_DIALOG_CONFIRMED):
            self.is_time_to_transition = True  # needs to transition to next state
            self.transition_target = 'main_menu'  # Exit to menu when menu pressed on box

        if not self.main_character.lives <= 0:  # check character is alive
            if event.type == self.enemy_spawn_event:
                if len(self.zombies.sprites()) < self.max_enemies:  # spawn enemies if less than maximum
                    self.zombie = Enemy()  # create new instance of enemy
                    self.zombies.add(self.zombie)  # added to enemy group
            if event.type == self.spike_spawn_event:  # spawn spikes
                if len(self.spikes.sprites()) < 2:
                    self.spike = Spikes()  # create new instance if less than 2 spikes
                    self.spikes.add(self.spike)  # add to spikes group
                    self.fire = Fire()  # create fire instance
                    self.spikes.add(self.fire)  # add to spikes group
            if event.type == self.boss_spawn_event:  # spawn boss
                if self.boss is None:
                    self.boss = Boss()  # create new boss instance
                    pygame.time.set_timer(self.enemy_spawn_event, 5000)  # delay mob spawn for 5 seconds
                if not self.boss.alive:  # reset regular spawn rate of mobs
                    pygame.time.set_timer(self.enemy_spawn_event, (self.ticks * 100))
                    time = pygame.time.get_ticks()
                    if time >= 1000:
                        self.boss = None  # allow enough time for death animation

        if self.game_over:
            self.game_over = False
            self.main_character.lives = 5  # reset lives
            self.is_time_to_transition = True  # transition set to True
            self.transition_target = 'game_over_state'  # switches to game over state

        if event.type == self.scroll_event:
            if self.main_character.scrolling:
                self.main_character.background_scroll -= 2  # scroll amount increases by 2 px

    def draw(self):
        # draws the background and updated player position - draw scrolling background:
        self.window_surface.blit(self.background_surface, (self.main_character.background_scroll, 0))
        self.window_surface.blit(self.background_surface, (2000 + self.main_character.background_scroll, 0))
        if self.main_character.background_scroll == -2000:
            self.window_surface.blit(self.background_surface, (2000 + self.main_character.background_scroll, 0))
            self.main_character.background_scroll = 0

        # draws scrolling platform tiles
        i = 0
        while i < 2000:
            self.window_surface.blit(self.gravel_img, (i + self.main_character.background_scroll, 500))
            self.window_surface.blit(self.gravel_img, (i + 2000 + self.main_character.background_scroll, 500))
            if self.main_character.background_scroll == -2000:
                self.window_surface.blit(self.gravel_img, (i + 2000 + self.main_character.background_scroll, 0))
            i += 100

        self.ui_manager.draw_ui(self.window_surface)  # draw user interface
        self.main_character.draw(self.window_surface)  # draw player
        self.zombies.draw(self.window_surface)  # draws all enemies
        if self.boss is not None:
            self.boss.draw(self.window_surface)  # draw boss
        self.main_character.bullet_group.draw(self.window_surface)  # draw bullets
        self.counters.draw(self.window_surface)  # draw counters
        self.spikes.draw(self.window_surface)  # draw spikes/ fire

        if self.damage_effect:
            # self.vignette = pygame.image.load('images/BloodOverlay.png').convert_alpha()  # reset visibility
            self.window_surface.blit(self.vignette, (0, 0))  # draw damage effect
        else:
            self.vignette.fill((0, 0, 0, 0))  # fill vignette image with transparency

        # clock tick, updating the display
        self.clock.tick(60)
        pygame.display.update()  # updates the display
