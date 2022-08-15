# Pygame template - skeleton for a new pygame project
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 360
HEIGHT = 480
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 37))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.radius = 19
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5

        self.rect.x += self.speedx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = mob_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.radius = int(self.rect.width / 2 * 0.85)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left < 0 or self.rect.right > WIDTH or self.rect.top > HEIGHT:
            self.rect.x = random.randrange(0, WIDTH - self.image.get_width())
            self.rect.bottom = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


# load all game graphics
background = pygame.image.load(path.join(img_dir, 'starfield-1.jpg')).convert()
background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
mob_img = pygame.image.load(path.join(img_dir, 'meteorBrown_med1.png')).convert()
bullet_img = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(0, 8):
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # collide detection
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        mob = Mob()
        all_sprites.add(mob)
        mobs.add(mob)

    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if hits:
        running = False

    # Draw / render
    screen.fill(WHITE)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
