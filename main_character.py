import pygame
import json
import os
import spritesheet
from bullet import Bullet

# global variable for distance
dist = 15
speed = [0, 1]
gravity = 0.3


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_group, enemy_group, spike_group, char_choice):
        # initialise surface, display, player, clock and colour attributes
        pygame.sprite.Sprite.__init__(self)
        self.canvas = pygame.Surface((1000, 600))
        self.window = pygame.display.set_mode((1000, 600))
        self.platform = pygame.Rect(0, 515, 1000, 600)
        # player, enemy group retrieved from game state to check for collisions
        self.sprite_group = sprite_group
        self.enemy_group = enemy_group
        self.spike_group = spike_group

        if char_choice == 0:  # use soldier sprite sheet if choice = 0
            self.sprite_sheet_image = pygame.image.load('images/spritesheet_player.png').convert_alpha()
        elif char_choice == 1:  # use boy sprite sheet if choice = 1
            self.sprite_sheet_image = pygame.image.load('images/spritesheet_player_2.png').convert_alpha()
        else:  # in any case of error use the soldier sprite sheet
            self.sprite_sheet_image = pygame.image.load('images/spritesheet_player.png').convert_alpha()
        # sprite sheet loading and selecting rectangle from spritesheet
        self.sprite_sheet = spritesheet.Spritesheet(self.sprite_sheet_image)
        self.flicker = False  # to flicker a damage effect
        self.collision = False  # changed to true later when collision detected

        self.animation_list = []  # creating an animation list
        self.animation_steps = [6, 6, 6]  # list of frames for each action
        self.action = 0  # holds index of animation steps, changed according to player actions
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 120  # delay between frames
        self.frame = 0  # initial frame
        self.step_counter = 0
        for animation in self.animation_steps:
            self.temp_img_list = []  # create temporary list
            for _ in range(animation):  # cycles through animation frames without tracking value
                # get rectangle on the spritesheet by calling spritesheet class
                self.temp_img_list.append(self.sprite_sheet.get_image(self.step_counter, 125, 177, 2))
                self.step_counter += 1  # increment counter
            self.animation_list.append(self.temp_img_list)  # add temporary list to the animation list
        self.change_frame = False
        self.flip = False  # flip the direction the player is facing
        self.moving = False  # check if player is moving to play animation

        self.image = self.animation_list[self.action][self.frame]  # sprite attributes
        self.rect = self.image.get_rect()
        self.rect.center = (100, 300)
        self.dir = 1  # direction player is facing

        self.lives = 5  # lives counter
        self.shooting = False  # check if player is shooting
        self.shoot_cooldown = 0  # delay between shots
        self.bullet_group = pygame.sprite.Group()  # creating a bullet group
        self.score = 0  # score count

        # Initialising the controller
        self.joysticks = []  # initialised as a list
        for i in range(pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))  # append each joystick value
        for self.joystick in self.joysticks:
            self.joystick.init()

        # opens the json file to retrieve the values of each button
        with open(os.path.join("ps4_keys.json"), 'r+') as file:
            self.button_keys = json.load(file)
        # 0: Left analog horizontal, 1: Left Analog Vertical, 2: Right Analog Horizontal
        # 3: Right Analog Vertical 4: Left Trigger, 5: Right Trigger
        self.analog_keys = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1}

        self.background_scroll = 0  # changed when player reaches certain width
        self.scrolling = False  # check if screen is scrolling or not

    def update(self, points_amount, boss):  # receive points, boss parameters
        self.run()  # calls controls method
        self.collide()  # calls collide method
        self.switch_frames()  # calls animation method
        self.image = pygame.transform.flip(self.animation_list[self.action][self.frame],
                                           self.flip, False)  # flip direction/ set the animation frame
        # gravity drawing player downwards,
        speed[1] += gravity  # gravity added to the speed
        self.rect = self.rect.move(speed)  # stopping when hitting the platform
        if self.rect.top < 0 or self.rect.bottom >= self.platform.top:
            speed[1] = 1

        if self.shooting:
            self.shoot()  # calls shoot method

        # increase points when enemy hit
        for enemy in self.enemy_group:
            if enemy.hit:
                self.score += points_amount
        # check if boss is alive
        if boss is not None:
            if boss.hit:  # increase points by 50 if hit
                self.score += boss.points_amount

    def run(self):
        # handles keyboard key presses
        key = pygame.key.get_pressed()
        self.moving = False  # reset 'moving' value
        if key[pygame.K_DOWN] or key[pygame.K_s]:  # down key
            self.rect.y += dist  # move down
        elif key[pygame.K_UP] or key[pygame.K_w]:  # up key
            self.rect.y -= 10  # jump
            self.moving = True  # 'moving' set to true when jumping
        if key[pygame.K_RIGHT] or key[pygame.K_d]:  # right key
            self.change_frame = True  # change frame
            self.action = 1
            self.flip = False
            self.dir = 1
            self.background_scroll -= 2
            self.scrolling = True
            self.moving = True  # 'moving' set to true when running
        elif key[pygame.K_LEFT] or key[pygame.K_a]:  # left key
            self.flip = True
            self.dir = -1
            self.scrolling = False
        else:
            self.scrolling = False
        if key[pygame.K_j]:  # j key
            self.shooting = True
            self.action = 2  # play shoot animation
            self.moving = True  # 'moving' also set to true when shooting
        else:
            self.shooting = False
            self.action = 1  # switch back to run animation

        # controller optimised controls
        if len(self.joysticks) > 0:
            joystick = self.joysticks[0]  # receive input from controller if buttons pressed

            if joystick.get_button(self.button_keys['R1']):
                self.shooting = True  # triggers shoot method
                self.action = 2  # shoot animation
                self.moving = True  # moving value
            if joystick.get_button(self.button_keys['x']):
                self.rect.y -= 10  # jump
                self.moving = True
            else:
                self.rect.y += 0  # no vertical movement

            if joystick.get_axis(0) > .7:  # analog sticks
                self.change_frame = True  # switch frames
                self.flip = False  # facing towards right
                self.background_scroll -= 2  # scroll background
                self.scrolling = True
                self.moving = True
                self.dir = 1  # reset direction to facing right
            elif joystick.get_axis(0) < -.7:
                self.action = 1  # run action
                self.flip = True  # flip direction
                self.dir = -1  # facing towards left
            else:
                self.rect.x += 0  # prevent horizontal movement

    def collide(self):
        self.flicker = False  # damage effect off
        # detects collision between player and platform
        if self.rect.colliderect(self.platform):
            self.collision = True
            # calculates overlap and resets player position by that amount
            if self.rect.bottom > self.platform.top:
                overlap = self.rect.bottom - self.platform.top
                self.rect.bottom -= overlap
            if self.action == 0:
                self.action += 1  # switch to run animation
        else:
            self.collision = False
            self.action = 0  # play jump animation when in the air

        # collide with enemy
        for enemy in self.enemy_group:
            if enemy.alive:
                if pygame.sprite.collide_mask(self, enemy):
                    self.flicker = True  # damage effect on
                    self.lives -= 1
                    enemy.kill()  # destroy enemy object
        # collide with spikes
        for spike in self.spike_group:
            if pygame.sprite.collide_mask(self, spike):
                self.flicker = True
                self.lives -= 1
                spike.kill()  # destroy spike object

        # keep player on screen
        if self.rect.right >= 1050:
            self.rect.right = 1050
        elif self.rect.left <= 50:
            self.rect.left = 50

        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1  # decrement cooldown value

    def switch_frames(self):
        current_time = pygame.time.get_ticks()
        if (self.change_frame == True) and (current_time - self.last_update >= self.animation_cooldown):
            if self.moving:  # check if the player is moving
                self.frame += 1  # increment frames if it's time to switch
                self.last_update = current_time
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0  # reset frame index to 0

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20  # reset cooldown if it reaches 0
            bullet = Bullet(self.rect.centerx + (0.4 * self.rect.size[0] * self.dir), self.rect.centery + 10,
                            self.dir, self.bullet_group)
            self.bullet_group.add(bullet)  # create bullet instance then add to group

    def draw(self, window_surface):
        window_surface.blit(self.image, self.rect)  # draw player at position
