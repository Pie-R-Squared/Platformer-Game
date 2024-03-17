from typing import Tuple, Union

import pygame


class ScoreCounter(pygame.sprite.Sprite):
    def __init__(self,
                 position: Tuple[int, int],  # receives position
                 font: pygame.font.Font,  # font
                 counters: pygame.sprite.Group):
        super().__init__(counters)  # added to 'counters' sprite group

        self.position = position  # receive position
        self.score = 0  # initial score
        self.font = font  # apply font

        self.image = None  # type: Union[pygame.Surface, None]
        self.rect = None  # type: Union[pygame.Rect, None]

        self._redraw()  # calls redraw method

    def _redraw(self):
        self.image = self.font.render('Score: ' + str(self.score), False, pygame.Color('#FFFFFF'))
        self.rect = self.image.get_rect()  # gets rectangle from image
        self.rect.topleft = self.position  # set top-left corner position

    def set_score(self, score: int):
        self.score = max(0, score)  # sets score
        self._redraw()  # calls redraw method
