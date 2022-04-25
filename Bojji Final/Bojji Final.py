#Michael Pagano final project
import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 70

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Bojji Platformer')


tile_size = 50
donezo = 0
mm = True
level = 1

sun = pygame.image.load('img/sun1.png')
rock = pygame.image.load('img/rock.png')
bg = pygame.image.load('img/sky2.png')
restimg = pygame.image.load('img/rest.png')
hokuro = pygame.image.load('img/hokuro.png')
vap = pygame.image.load('img/vlap.png')
opon = pygame.image.load('img/open.png')
lev = pygame.image.load('img/lev.png')
endtx = pygame.image.load('img/endmsg.png')
bojjiop = pygame.image.load('img/opboj.jpg')
bojjiop = pygame.transform.scale(bojjiop, (1000, 1000))
opon = pygame.transform.scale(opon, (160, 80))
lev = pygame.transform.scale(lev, (160, 80))


class restart():
    def __init__(bojji, x, y, image):
        bojji.image = image
        bojji.rect = bojji.image.get_rect()
        bojji.rect.x = x
        bojji.rect.y = y
        bojji.clicked = False

    def draw(bojji):
        
        mos = pygame.mouse.get_pos()
        doob = False
        if bojji.rect.collidepoint(mos):
            if pygame.mouse.get_pressed()[0] == 1 and bojji.clicked == False:
                bojji.clicked = True
                doob = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            bojji.clicked = False
                
        
        screen.blit(bojji.image, bojji.rect)
        
        return doob

class Player():
    def __init__(bojji, x, y):
        bojji.stagain(x, y)

        
    def update(bojji, donezo, world):
        dx = 0
        dy = 0
        walk_cooldown = 7

        if donezo == 0:
        
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                dx -= 5
                bojji.counter += 1
                bojji.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                bojji.counter += 1
                bojji.direction = 1
            if key[pygame.K_SPACE] and bojji.jumped == False and bojji.vel_y==0 and bojji.o == False:
                bojji.vel_y = -15
                bojji.jumped = True
            if key[pygame.K_SPACE] == False:
                bojji.jumped = False
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                bojji.counter = 0
                bojji.index = 0
                if bojji.direction == 1:
                    bojji.image = bojji.images_right[bojji.index]
                if bojji.direction == -1:
                    bojji.image = bojji.images_left[bojji.index]

            if bojji.counter > walk_cooldown:
                bojji.counter = 0
                bojji.index +=1
                if bojji.index >= len(bojji.images_right):
                    bojji.index = 0
                if bojji.direction == 1:
                    bojji.image = bojji.images_right[bojji.index]
                if bojji.direction == -1:
                    bojji.image = bojji.images_left[bojji.index]
            bojji.vel_y += 1
            if bojji.vel_y >= 10:
                bojji.vel_y = 10
            dy += bojji.vel_y

    #Collision
            bojji.o = True
            for tile in world.tile_list:

                if tile[1].colliderect(bojji.rect.x + dx, bojji.rect.y, bojji.width, bojji.height):
                    dx = 0
                if tile[1].colliderect(bojji.rect.x, bojji.rect.y + dy, bojji.width, bojji.height):
                    if bojji.vel_y < 0:
                        dy = tile[1].bottom - bojji.rect.top
                        bojji.vel_y = 0
                    elif bojji.vel_y >= 0:
                        dy = tile[1].top - bojji.rect.bottom
                        bojji.vel_y = 0
                        bojji.o = False

            #enemy ded
            if pygame.sprite.spritecollide(bojji, kage_group, False):
                donezo = -1
            if pygame.sprite.spritecollide(bojji, spikeg, False):
                donezo = -1
            if pygame.sprite.spritecollide(bojji, portalg, False):
                donezo = 1
            if pygame.sprite.spritecollide(bojji, deidag, False):
                donezo = -1
            if pygame.sprite.spritecollide(bojji, lavag, False):
                if level == 3:
                    donezo = 1
                else:
                    donezo = -1
            if pygame.sprite.spritecollide(bojji, domasg, False):
                dx+=30
                dy-=50
            if pygame.sprite.spritecollide(bojji, oguardg, False):
                donezo = -1
                
            bojji.rect.x+=dx
            bojji.rect.y+=dy
            
        elif donezo == -1:
            bojji.image = bojji.ded
                
        screen.blit(bojji.image, bojji.rect)
        
        return donezo

    def stagain(bojji, x, y):
        bojji.images_right = []
        bojji.images_left = []
        bojji.index = 0
        bojji.counter = 0
        for i in range(1, 5):
            img_right = pygame.image.load(f'img/bojji{i}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            bojji.images_right.append(img_right)
            bojji.images_left.append(img_left)

        bojji.ded = pygame.image.load('img/grave.png')
        bojji.image = bojji.images_right[bojji.index]
        bojji.rect = bojji.image.get_rect()
        bojji.rect.x = x
        bojji.rect.y = y
        bojji.width = bojji.image.get_width()
        bojji.height = bojji.image.get_height()
        bojji.vel_y = 0
        bojji.jumped = False
        bojji.direction = 0
        bojji.o = True
    
        
class World():
    def __init__(bojji, data):
        bojji.tile_list = []

        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass1.png')
        spike = pygame.image.load('img/spike.png')
        portal = pygame.image.load('img/portal.png')
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    bojji.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    bojji.tile_list.append(tile)
                if tile == 3:
                    kage = kages(col_count * tile_size, row_count * tile_size)
                    kage_group.add(kage)
                if tile == 4:
                    spike = spikes(col_count * tile_size, row_count * tile_size)
                    spikeg.add(spike)
                if tile == 5:
                    portal = portals(col_count * tile_size, row_count * tile_size)
                    portalg.add(portal)
                if tile == 6:
                    deida = deidas(col_count * tile_size, row_count * tile_size)
                    deidag.add(deida)
                if tile == 7:
                    img = pygame.transform.scale(rock, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    bojji.tile_list.append(tile)
                if tile == 8:
                    hokuro = hokuros(col_count * tile_size, (row_count * tile_size)-27.5)
                    hokurog.add(hokuro)
                if tile == 9:
                    lava = lavas(col_count * tile_size, row_count * tile_size)
                    lavag.add(lava)
                if tile == 10:
                    domas = domass(col_count * tile_size, (row_count * tile_size)-27.5)
                    domasg.add(domas)
                if tile == 11:
                    oguard = oguards(col_count * tile_size, (row_count * tile_size)-70)
                    oguardg.add(oguard)
                    

                col_count += 1
            row_count += 1



    def draw(bojji):
        for tile in bojji.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

class kages(pygame.sprite.Sprite):
    def __init__(bojji, x, y):
        pygame.sprite.Sprite.__init__(bojji)
        bojji.image = pygame.image.load('img/kage.png')
        bojji.image = pygame.transform.scale(bojji.image, (50, 50))
        bojji.rect = bojji.image.get_rect()
        bojji.rect.x = x
        bojji.rect.y = y
        bojji.movedirection = 2
        bojji.move_counter = 0

    def update(bojji):
        bojji.rect.x += bojji.movedirection
        bojji.move_counter += 1
        if bojji.move_counter > 50:
            bojji.movedirection *= -1
            bojji.move_counter *= -1
class oguards(pygame.sprite.Sprite):
    def __init__(bojji, x, y):
        pygame.sprite.Sprite.__init__(bojji)
        bojji.image = pygame.image.load('img/oguard.png')
        bojji.image = pygame.transform.scale(bojji.image, (120, 120))
        bojji.rect = bojji.image.get_rect()
        bojji.rect.x = x
        bojji.rect.y = y
        bojji.movedirection = 2
        bojji.move_counter = 0

    def update(bojji):
        bojji.rect.x += bojji.movedirection
        bojji.move_counter += 1
        if bojji.move_counter > 42:
            bojji.movedirection *= -1
            bojji.move_counter *= -1
class spikes(pygame.sprite.Sprite):
    def __init__(bojji, x, y):
        pygame.sprite.Sprite.__init__(bojji)
        img = pygame.image.load('img/spike.png')
        bojji.image = pygame.transform.scale(img, (tile_size, tile_size))
        bojji.rect = bojji.image.get_rect()
        bojji.rect.x = x
        bojji.rect.y = y
class portals(pygame.sprite.Sprite):
    def __init__(bojji, x, y):
        pygame.sprite.Sprite.__init__(bojji)
        img = pygame.image.load('img/portal.png')
        bojji.image = pygame.transform.scale(img, (tile_size, tile_size))
        bojji.rect = bojji.image.get_rect()
        bojji.rect.x = x
        bojji.rect.y = y
class hokuros(pygame.sprite.Sprite):
    def __init__(bojji, x, y):
        pygame.sprite.Sprite.__init__(bojji)
        img = pygame.image.load('img/hokuro.png')
        bojji.image = pygame.transform.scale(img, (125, 125))
        bojji.rect = bojji.image.get_rect()
        bojji.rect.x = x
        bojji.rect.y = y
class domass(pygame.sprite.Sprite):
    def __init__(bojji, x, y):
        pygame.sprite.Sprite.__init__(bojji)
        img = pygame.image.load('img/domas.png')
        bojji.image = pygame.transform.scale(img, (125, 125))
        bojji.rect = bojji.image.get_rect()
        bojji.rect.x = x
        bojji.rect.y = y
class lavas(pygame.sprite.Sprite):
    def __init__(bojji, x, y):
        pygame.sprite.Sprite.__init__(bojji)
        img = pygame.image.load('img/lava.png')
        bojji.image = pygame.transform.scale(img, (tile_size, tile_size))
        bojji.rect = bojji.image.get_rect()
        bojji.rect.x = x
        bojji.rect.y = y
ind = 1
class deidas(pygame.sprite.Sprite):
    def __init__(bojji, x, y):
        pygame.sprite.Sprite.__init__(bojji)
        ind = 1
        
        bojji.image = pygame.image.load(f'img/deida{ind}.png')
        bojji.image = pygame.transform.scale(bojji.image, (100, 100))
        bojji.rect = bojji.image.get_rect()
        bojji.rect.x = x
        bojji.rect.y = y
        bojji.movedirection = 15
        bojji.move_counter = 0
        bojji.mc = 0
    def update(bojji, ind):
        
        bojji.rect.x += bojji.movedirection
        bojji.move_counter += 1
        bojji.mc += 1
        if bojji.mc >= 2:
            ind += 1
            
            if ind >3:
                ind = 0
            bojji.mc = 0
        if bojji.move_counter > 22:
            bojji.movedirection *= -1
            bojji.move_counter *= -1
            if bojji.movedirection>=1:
                bojji.image = pygame.image.load(f'img/deida{ind}.png')
                bojji.image = pygame.transform.scale(bojji.image, (100, 100))
            elif bojji.movedirection<=1:
                bojji.image = pygame.image.load(f'img/deida{ind}.png')
                bojji.image = pygame.transform.scale(bojji.image, (100, 100))
                bojji.image = pygame.transform.flip(bojji.image, True, False)
        
    
worlddata1 = [
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 3, 0, 0, 1, 1, 1, 1, 1, 1], 
[1, 4, 0, 0, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

worlddata2 = [
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 2, 6, 0, 0, 2, 0, 0, 0, 0, 5, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1], 
[1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]
]
worlddata3 = [
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 8, 0, 0, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 7, 7, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 7, 0, 0, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 7, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 10, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9, 9, 9, 1]
]
worlddata4 = [
[7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
[7, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
[7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
[7, 0, 7, 0, 0, 11, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
[7, 0, 7, 7, 7, 7, 7, 7, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
[7, 0, 7, 0, 0, 0, 0, 0, 7, 7, 0, 0, 7, 0, 0, 0, 11, 0, 0, 7], 
[7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7], 
[7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
[7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 7], 
[7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 7, 7, 7, 7, 7], 
[7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 11, 0, 7, 0, 7, 0, 0, 0, 0, 7], 
[7, 0, 7, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 7], 
[7, 0, 7, 0, 0, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
[7, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
[7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
[7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 7], 
[7, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
[7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 7], 
[7, 0, 7, 0, 7, 0, 0, 7, 0, 0, 7, 0, 0, 0, 7, 0, 0, 0, 5, 7], 
[7, 9, 7, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 7, 7]
]
worlddata5 = [
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 3, 0, 6, 8, 10, 0, 0, 0, 11, 0, 0, 0, 1], 
[1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]]


player = Player(100, screen_height - 130)
kage_group = pygame.sprite.Group()
spikeg = pygame.sprite.Group()
portalg = pygame.sprite.Group()
deidag = pygame.sprite.Group()
hokurog = pygame.sprite.Group()
lavag = pygame.sprite.Group()
domasg = pygame.sprite.Group()
oguardg = pygame.sprite.Group()

#butt
ress = restart(screen_width // 2, screen_height //2, restimg)

oponb = restart(screen_width // 2 - 350, screen_height //2, opon)
levb = restart(screen_width // 2 + 250, screen_height //2, lev)
endthx = restart(screen_width // 5, screen_height // 4, endtx)
vlap = restart(screen_width // 2 - 25, screen_height//2+50, vap)
run = True
while run:
    clock.tick(fps)
    
    screen.blit(bg, (0, 0))
    if level == 1 or level == 2:
        screen.blit(sun, (330, 90))
    if level == 3:
        screen.blit(sun, (50, 100))
    if level == 5:
        screen.blit(sun, (290, 100))
        vlap.draw()

    if mm == True:
        screen.blit(bojjiop, (0, 0))
        if oponb.draw():
            world = World(worlddata1)
            mm = False
        if levb.draw():
            run = False

    else:
            
        world.draw()

        if donezo == 0:

            kage_group.update()
            deidag.update(ind)
            oguardg.update()
            
        kage_group.draw(screen)
        spikeg.draw(screen)
        portalg.draw(screen)
        deidag.draw(screen)
        hokurog.draw(screen)
        lavag.draw(screen)
        domasg.draw(screen)
        oguardg.draw(screen)
        
        donezo = player.update(donezo, world)

        if donezo == -1:
            if ress.draw():
                player.stagain(100, screen_height - 130)
                donezo = 0

        if donezo == 1:
            level += 1
            if level <= 5:
                if level == 2:
                    kage_group.empty()
                    spikeg.empty()
                    portalg.empty()
                    worlddata1 = []
                    world = World(worlddata1)
                    player.stagain(100, screen_height - 130)
                    world = World(worlddata2)
                    world.draw()
                    donezo = 0
                    bg = pygame.image.load('img/castlebg.png')
                if level == 3:
                    deidag.empty()
                    worlddata2 = []
                    portalg.empty()
                    world = World(worlddata2)
                    player.stagain(100, screen_height - 130)
                    world = World(worlddata3)
                    world.draw()
                    donezo = 0
                    bg = pygame.image.load('img/barrenbg.png')
                if level == 4:
                    lavag.empty()
                    hokurog.empty()
                    domasg.empty()
                    worlddata3 = []
                    portalg.empty()
                    world = World(worlddata3)
                    player.stagain(100, screen_height-20)
                    world = World(worlddata4)
                    world.draw()
                    donezo = 0
                    bg = pygame.image.load('img/spiralbg.png')
                if level == 5:
                    lavag.empty()
                    oguardg.empty()
                    portalg.empty()
                    worlddata4 = []
                    player.stagain(100, screen_height - 130)
                    world = World(worlddata5)
                    world.draw()
                    donezo = 0
                    
                    bg = pygame.image.load('img/finallev.png')
                    vlap.draw()
                    
            elif level > 5:
                
                    
                
                    
                    
                
                
            
                endthx.draw()
                if levb.draw():
                    run = False
        


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
