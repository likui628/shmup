# Pygame template - skeleton for a new pygame project
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

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

text_font = pygame.font.match_font('arial')

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(text_font, size)
    text_surface = font.render(text, True, WHITE)
    rect = text_surface.get_rect()
    rect.midtop = (x, y)
    surface.blit(text_surface, rect)


def draw_shield_bar(surface, x, y, pec):
    if pec < 0:
        pec = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, BAR_LENGTH * (pec / 100), BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)


def draw_lives(surface, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x - 30 * i
        img_rect.y = y
        surface.blit(img, img_rect)


def add_mob():
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)


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

        self.lives = 3
        self.shield = 100
        self.hidden = False
        self.hidden_timer = pygame.time.get_ticks()

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hidden_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

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

    def hide(self):
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
        self.hidden_timer = pygame.time.get_ticks()
        self.hidden = True

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        pew_sound.play()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_origin = random.choice(mob_img_list)
        self.image_origin.set_colorkey(BLACK)

        self.image = self.image_origin.copy()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.radius = int(self.rect.width / 2 * 0.85)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-140, -100)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 8)

        self.rot = 0
        self.rot_speed = random.randrange(-10, 10)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_origin, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = new_image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right <= 0 or self.rect.left >= WIDTH or self.rect.top > HEIGHT:
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


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_dict[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_dict[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = expl_dict[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# load all game graphics
background = pygame.image.load(path.join(img_dir, 'starfield-1.jpg')).convert()
background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

bullet_img = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()
mob_img_list = []
image_list = [
    'meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png',
    'meteorBrown_big4.png', 'meteorBrown_med1.png', 'meteorBrown_med3.png',
    'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png',
    'meteorBrown_tiny2.png']
for img in image_list:
    mob_img_list.append(pygame.image.load(path.join(img_dir, img)).convert())

# load explosion graphics
expl_dict = {'lg': [], 'sm': [], 'player': []}
for i in range(9):
    img = pygame.image.load(path.join(img_dir, 'regularExplosion0{}.png'.format(i))).convert()
    img.set_colorkey(BLACK)
    expl_dict['lg'].append(pygame.transform.scale(img, (75, 75)))
    expl_dict['sm'].append(pygame.transform.scale(img, (35, 35)))

    img = pygame.image.load(path.join(img_dir, 'sonicExplosion0{}.png'.format(i))).convert()
    img.set_colorkey(BLACK)
    expl_dict['player'].append(pygame.transform.scale(img, (75, 75)))

# load all sounds
pew_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(0, 8):
    add_mob()

# Game loop
score = 0
pygame.mixer.music.play()
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
        score += (55 - hit.radius)
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        add_mob()

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        add_mob()
        if player.shield <= 0:
            player_die_sound.play()
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # Name 'death_expl' can be undefined, how to fix it?
    if player.lives == 0 and not death_expl.alive():
        running = False

    # Draw / render
    screen.fill(WHITE)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, 'score: ' + str(score), 20, WIDTH / 2, 10)
    draw_shield_bar(screen, 10, 15, player.shield)
    draw_lives(screen, WIDTH - 35, 10, player.lives, player_mini_img)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
