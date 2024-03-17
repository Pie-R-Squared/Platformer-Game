from typing import Tuple

import pygame


class LivesCounter(pygame.sprite.Sprite):
    def __init__(self,
                 position: Tuple[int, int],  # receives position
                 font: pygame.font.Font,  # font
                 counters: pygame.sprite.Group):
        super().__init__(counters)  # added to 'counters' sprite group

        self.num_lives = 5

        self.heart = pygame.image.load('images/heart.png').convert_alpha()  # pixel format
        self.heart = pygame.transform.scale(self.heart, (50, 50))  # reduces size
        self.text_surface = font.render('Lives: ', False, pygame.Color('#ADD8E6'))  # light blue

        # calculate the space needed for the counters and 'lives:' text
        self.life_spacing = 10  # space between each heart
        width = self.text_surface.get_width() + (5 * (self.heart.get_width() + self.life_spacing))
        height = max(self.text_surface.get_height(), self.heart.get_height())
        self.rect = pygame.Rect(position, (width, height))  # sets lives' position

        # calculates the position to place 'lives:'
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.centery = int(self.rect.height / 2)

        # lay out the positions of the hearts
        life_rect_1 = self.heart.get_rect()  # gets rectangle
        life_rect_1.left = self.text_rect.right  # placed to the right of 'lives:'
        life_rect_1.centery = int(self.rect.height / 2)  # centre is halfway

        life_rect_2 = self.heart.get_rect()
        life_rect_2.left = life_rect_1.right + self.life_spacing
        life_rect_2.centery = int(self.rect.height / 2)

        life_rect_3 = self.heart.get_rect()
        life_rect_3.left = life_rect_2.right + self.life_spacing
        life_rect_3.centery = int(self.rect.height / 2)

        life_rect_4 = self.heart.get_rect()
        life_rect_4.left = life_rect_3.right + self.life_spacing
        life_rect_4.centery = int(self.rect.height / 2)

        life_rect_5 = self.heart.get_rect()
        life_rect_5.left = life_rect_4.right + self.life_spacing
        life_rect_5.centery = int(self.rect.height / 2)

        self.life_hearts = [life_rect_1, life_rect_2, life_rect_3, life_rect_4, life_rect_5]

        self._redraw()  # calls the draw function

    def _redraw(self):
        # create an empty, transparent surface to start filling in
        self.image = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
        self.image.fill(pygame.Color('#00000000'))

        # blit the text on to the heart sprite's image
        self.image.blit(self.text_surface, self.text_rect)

        # blit the hearts on to the display
        for i in range(self.num_lives):
            self.image.blit(self.heart, self.life_hearts[i])

    def set_num_lives(self, number_of_lives: int):
        self.num_lives = max(0, min(number_of_lives, 5))
        self._redraw()  # calls draw method to update lives
