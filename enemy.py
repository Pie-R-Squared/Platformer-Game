import pygame
import spritesheet


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # load spritesheet for enemy and pass it to the spritesheet class
        self.zombie_sheet = pygame.image.load('images/zombie_sheet.png').convert_alpha()
        self.sprite_sheet = spritesheet.Spritesheet(self.zombie_sheet)

        self.animation_list = []  # create list for frames
        self.animation_steps = [8, 6]  # number of frames
        self.last_update = pygame.time.get_ticks()  # checks time
        self.animation_cooldown = 100  # time between frames
        self.action = 1
        self.frame = 0  # initialised at index 0
        self.step_counter = 0
        for animation in self.animation_steps:
            self.temp_img_list = []  # create temporary list
            for _ in range(animation):  # cycles through animation frames without tracking value
                self.temp_img_list.append(self.sprite_sheet.get_image(self.step_counter, 200, 250, 2))
                self.step_counter += 1  # increment counter
            self.animation_list.append(self.temp_img_list)  # add temporary list to the animation list

        self.image = self.animation_list[self.action][self.frame]  # image attribute for sprite
        self.rect = self.image.get_rect()  # sprite rectangle
        self.x = 1200  # changed to spawn off-screen # randomly generates an x-coordinate
        self.y = 300  # constant y coordinate to stay on platform
        self.rect.center = (self.x, self.y)  # assigns rectangle centre
        self.pos = self.rect.center
        self.speed = 2.5  # pixels moved
        self.health = 100  # enemy health
        self.max_health = self.health  # to display in health bar
        self.alive = True  # enemy is alive
        self.flip = False  # when to flip the image
        self.mask = pygame.mask.from_surface(self.image)  # creates mask for collision

        self.points_amount = 20  # points given when killed
        self.hit = False  # to check when bullets hit

    def update(self, player, enemy_group, scrolling):
        # calls all the methods (move, animate, scrolling..)
        self.move(player)
        self.check_alive(enemy_group)
        self.animate()
        self.image = pygame.transform.flip(self.animation_list[self.action][self.frame], self.flip, False)
        if scrolling:
            self.rect.x -= 3  # scroll past dead enemies

    def move(self, player):
        if self.alive:  # only move when alive
            if self.x < player.rect.centerx:
                self.x += self.speed  # move towards player on the left
                self.rect.center = (self.x, self.y)  # centre coordinates
                self.flip = True  # flips direction

            elif self.x > player.rect.centerx:
                self.x -= self.speed  # move towards player on right
                self.rect.center = (self.x, self.y)
                self.flip = False  # resets direction

    def animate(self):
        current_time = pygame.time.get_ticks()  # gets current time
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1  # increments frame if it's time to switch
            self.last_update = current_time  # to get time for next frame
            if self.frame >= len(self.animation_list[self.action]):
                if self.action == 0:  # stay on last frame if death animation is playing
                    self.frame = len(self.animation_list[self.action]) - 1
                else:
                    self.frame = 0  # resets to 0 if all frames displayed

    def update_action(self, new_action):
        # check if new action different to previous
        if new_action != self.action:
            self.action = new_action  # swap old for new animation
            self.frame = 0  # reset frames
            self.last_update = pygame.time.get_ticks()  # clock tick

    def check_alive(self, enemy_group):
        self.hit = False  # resets hits to prevent rapidly earning points
        if self.health <= 0:
            self.health = 0  # health set to 0
            self.speed = 0  # enemy stops moving
            self.alive = False  # set alive attribute to False
            self.update_action(0)  # play death animation
        if self.rect.x < 10:
            enemy_group.remove(self)  # remove enemy from group

    def draw(self, screen):
        # draws enemies at position with animation
        screen.blit(self.image, self.rect)


class Spikes(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/spikes.png')  # load image
        self.image = pygame.transform.scale(self.image, (128, 128))  # scaled down
        self.rect = self.image.get_rect()  # sprite rectangle
        self.rect.center = (1100, 440)  # assigns rectangle centre

    def update(self, scrolling, spike_group):
        if scrolling:
            self.rect.x -= 4  # scroll spikes
            if self.rect.x < 10:
                spike_group.remove(self)  # remove when out of bounds

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # draw at randomised position


class Fire(Spikes):  # inherit from Spikes class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/fire_obstacle2.png')  # load image
        self.image = pygame.transform.scale(self.image, (120, 59))  # scaled down
        self.rect = self.image.get_rect()  # sprite rectangle
        self.rect.center = (1500, 480)  # assigns rectangle centre


class Boss(Enemy):  # boss class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.boss_spritesheet = pygame.image.load('images/boss_sheet.png').convert_alpha()
        self.sprite_sheet = spritesheet.Spritesheet(self.boss_spritesheet)

        self.animation_list = []  # create list for frames
        self.animation_steps = [8, 6]  # number of frames
        self.last_update = pygame.time.get_ticks()  # checks time
        self.animation_cooldown = 100  # time between frames
        self.action = 1
        self.frame = 0  # initialised at index 0
        self.step_counter = 0
        for animation in self.animation_steps:
            self.temp_img_list = []  # create temporary list
            for _ in range(animation):  # cycles through animation frames without tracking value
                self.temp_img_list.append(self.sprite_sheet.get_image(self.step_counter, 200, 250, 2))
                self.step_counter += 1  # increment counter
            self.animation_list.append(self.temp_img_list)  # add temporary list to the animation list

        self.image = self.animation_list[self.action][self.frame]  # image attribute for sprite
        self.rect = self.image.get_rect()  # sprite rectangle
        self.x = 1000  # constant x coordinate of 800
        self.y = 300  # constant y coordinate to stay on platform
        self.rect.center = (self.x, self.y)  # assigns rectangle centre
        self.pos = self.rect.center
        self.speed = 1.5  # pixels moved
        self.health = 500  # enemy health
        self.max_health = self.health  # to display in health bar
        self.alive = True  # enemy is alive
        self.flip = False  # when to flip the image
        self.mask = pygame.mask.from_surface(self.image)  # creates mask for collision

        self.points_amount = 50  # points given when killed
        self.hit = False  # to check when bullets hit
