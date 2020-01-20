import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_event(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def check_keyup_event(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """check the mouse and key"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event,ai_settings,screen,ship,bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_event(event,ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    """update the image in screen and turn to the new screen"""
    #Redraw screen on each cycle
    screen.fill(ai_settings.bg_color)

    #Redraw bullets at the back of ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    #display score
    sb.show_score()

    #if game_active == False draw play_button
    if not stats.game_active:
        play_button.draw_button()

    # Make the recently drawn screen visible
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """update bullets's location and delete disappearded bullets"""
    #update bullets's location
    bullets.update()

    #Delete disappearded bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(ai_settings,screen,stats,sb,ship,aliens,bullets)


def check_bullet_alien_collision(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """check if there bullets hit aliens"""
    #delete bullet and alien if it's
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings,screen,ship,aliens)

def fire_bullet(ai_settings,screen,ship,bullets):
    """fire bullet if there are bullets surplus"""
    # build new bullet and add it in bullets
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def create_fleet(ai_settings,screen,ship,aliens):
    """creat fleet of aliens"""
    #build an alien and
    #the interval between two aliens is an alien's width
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    #create aliens of the first row
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(ai_settings,alien_width):
    #calculate how many aliens a row can hold
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    """calculate how many rows can be hold"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """create an alien and place it at current row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """update all aliens' locations """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #check aliens hit ship
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    #check aliens arrive the bottom of screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_fleet_edges(ai_settings,aliens):
    """check is there alien at the edges of screen"""
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    """move fleet down and change fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """response aliens hit ship"""
    if stats.ships_left > 0:
        stats.ships_left -= 1

        #update scoreboard
        sb.prep_ships()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    # empty aliens and bullets
    aliens.empty()
    bullets.empty()

    # creat fleet of aliens and ship
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # pause
    sleep(1)

def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """check aliens arrive the bottom of screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom :
            ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
            break

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    """begin the game when player click play_button"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #initialize speed settings
        ai_settings.initialize_dynamic_settings()

        #hide mouse when game beginning
        pygame.mouse.set_visible(False)

        #reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        #reset the score and level
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()

        #empty bullets and aliens
        aliens.empty()
        bullets.empty()

        #build a new fleet of aliens and place ship at the center of the bottom of screen
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
def check_high_score(stats,sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
