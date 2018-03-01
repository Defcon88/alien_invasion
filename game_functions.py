import sys
from time import sleep

import pygame

from bullet import Bullet
from bullet import RightBullet
from explosion import Explosion

from alien import Alien

def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, blaster, sb):
    '''respond to keypresses and mouse events'''
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event, ai_settings, screen, stats, 
                    ship, aliens, bullets, blaster, sb)
            
            elif event.type == pygame.KEYUP:
                check_keyup_events(event, ship)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats, play_button, 
                    ship, aliens, bullets, mouse_x, mouse_y, sb)

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, 
    bullets, mouse_x, mouse_y, sb):
    '''Start a new game when the player clicks play'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        start_game(ai_settings, screen, stats, ship, aliens, bullets, sb)
        
def start_game(ai_settings, screen, stats, ship, aliens, 
    bullets, sb):
    
    if not stats.game_active:
        '''start a new game'''
        #hide mouse cursor
        pygame.mouse.set_visible(False)
        
        #reset stats and game settings
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        stats.game_active = True
        
        
        #empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        
        #create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_keydown_events(event, ai_settings, screen, stats, ship, aliens, 
    bullets, blaster, sb):
    '''respond to presses'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets, blaster)
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, ship, aliens, bullets, sb)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets, blaster):
    #fire a bullet if length not reached
    if len(bullets) < ai_settings.bullets_allowed:
        #create a new bullet and add to a bullets group
        new_bullet_left = Bullet(ai_settings, screen, ship)
        new_bullet_right = RightBullet(ai_settings, screen, ship)
        bullets.add(new_bullet_left)
        bullets.add(new_bullet_right)
        blaster.blast.play()


def check_keyup_events(event, ship):
    '''respond to key releasees'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, 
    explosions, sb):
    '''update images on the screen and flip to the new screen'''
    #redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    #redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    explosions.draw(screen)
    
    #draw the score information
    sb.show_score()
    
    #draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()
    
    #make the most recently drawn screen visible.
    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets, blaster, 
    explosions, sb, stats):
    bullets.update()
    for bullet in bullets.copy():
            if bullet.rect.bottom <=0:
                bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, 
        bullets, blaster, explosions, sb, stats)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, 
    bullets, blaster, explosions, sb, stats):
    # check for any bullets that have hit aliens
    # if so, get rid of the bullet and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    for collision in collisions:
        expl = Explosion(collision.rect.center)
        explosions.add(expl)
    if collisions:
        sound = blaster.get_explosion()
        sound.play()
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        #destroy existing bullets, speed up game and create a new fleet
        bullets.empty()
        ai_settings.increase_speed()
        
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)
        
        
def get_number_aliens_x(ai_settings, alien_width):
    '''determine the number of aliens that fit into a row'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '''determine the number of rows of aliens that fit on screen'''
    available_space_y = (ai_settings.screen_height - 
        (3*alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''create an alein and place it in the row'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    '''create a fleet full of aliens'''
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, 
        alien.rect.height)
    
    #create first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                row_number)


def check_fleet_edges(ai_settings, aliens):
    '''respond appropriately of any aliens have reached an edge'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    '''drop the entire fleet and change the fleet's direction'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    '''Respond to ship being hit by alien'''
    if stats.ships_left > 1:
        # decrement ships_left
        stats.ships_left -= 1
        sb.prep_ships()
    
        #Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
    
        #create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
    
        #pause
        sleep(0.5)
    
    else: 
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
    '''check if the fleet is at an edge and then
        update the postions of all the aliens in the fleet'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    #look for alien/ship collisions/
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
    
    #look for aliens that make it to the bottom of the screen
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    '''check if any aliens have made it to the bottom of the screen'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #treat this the same as if a ship got hit
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break

def check_high_score(stats, sb):
    '''check to see if there is a new high score'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
