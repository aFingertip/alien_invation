import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """a class to display a single alien"""
    def __init__(self,ai_settings,screen):
        """initialization aliens and setting their initialization location"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #load alien's image and setting it's rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #place it at left_top angle at beginning
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #place it at accurate location
        self.x = float(self.rect.x)

    def blitme(self):
        """draw alien at specified location"""
        self.screen.blit(self.image,self.rect)

    def update(self):
        """move aliens right or left"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return true if the alien is at the edges of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= screen_rect.left :
            return True
