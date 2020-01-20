import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self,ai_settings,screen):
        """initialization the ship and set the space of ship"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #load image of ship and get the rect of the image
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Place the new ship in the center at the bottom of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #change the property of ship's center to float
        self.center = float(self.rect.centerx)

        #the enabling of move
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Adjust the location of the ship according to the enabling position"""
        if self.moving_right and self.center < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.center > self.screen_rect.left:
            self.center -= self.ai_settings.ship_speed_factor

        #change float back
        self.rect.centerx = self.center

    def blitme(self):
        """Place the ship in the designated location"""
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        """place ship at the middle of the bottom of screen"""
        self.center = self.screen_rect.centerx