import sys

import pygame
from pygame.sprite import  Group

from settings import Settings
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from ship import Ship
from alien import Alien
import game_functions as gf

def run_game():
    #Initialization pygame and settings and screen
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width , ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #store statistics
    stats = GameStats(ai_settings)

    #build a scoreboard
    sb = Scoreboard(ai_settings,screen,stats)

    #Build a ship
    ship = Ship(ai_settings,screen)

    #Build a group to store aliens
    aliens = Group()
    gf.create_fleet(ai_settings,screen,ship,aliens)

    #Build a group to store bullets
    bullets = Group()

    #build "Play" button
    play_button = Button(ai_settings,screen,"Play")

    #Begin main cycle of game
    while True:

        #Monitoring events
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active :
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)

        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)

run_game()