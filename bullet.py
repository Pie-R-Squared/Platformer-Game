import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet_group):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.image.load('images/bullet_img.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = direction
        self.bullet_group = bullet_group

    def update(self, enemy_group, boss):
        # move bullet
        self.rect.x += (self.direction * self.speed)
        # check if bullet has gone off the screen
        if self.rect.right < 0 or self.rect.left > 1000:
            self.kill()
        # check collision with enemy, and whether to delete them from the groups, pixel perfect collision
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, self.bullet_group, False, pygame.sprite.collide_mask):
                if enemy.alive:  # verifies enemy is not dead
                    enemy.health -= 50  # reduce enemy health by 50
                    enemy.hit = True  # earn points on every hit
                    self.kill()  # destroy bullet
        if boss is not None:  # check if boss instance exists
            if pygame.sprite.collide_mask(self, boss):
                if boss.alive:
                    boss.health -= 50  # reduce health by 50
                    boss.hit = True  # hit marker
                    self.kill()  # destroy bullet
