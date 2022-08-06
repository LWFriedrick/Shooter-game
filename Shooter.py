from pygame import*
from random import randint
WIN_WIDTH = 900
WIN_HEIGHT = 700
player_speed = 10
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png' 
score = 0
#----------------------------------
class GameSprite(sprite.Sprite):
    def __init__(self, image_file, x , y, size_x, size_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(image_file), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
#----------------------------------
class TextSprite(sprite.Sprite):
    def __init__(self, text, color, pos, font_size):
        self.font = font.SysFont(None, font_size)
        self.color = color
        self.pos = pos
        self.update_text(text)
        self.rect = self.image.get_rect()
    def update_text(self, new_text):
        self.image = self.font.render(new_text,True, self.color)
    def draw(self, surface):
        surface.blit(self.image, self.pos)
#----------------------------------
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0 or self.rect.top > WIN_HEIGHT:
            self.kill()
#----------------------------------
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5 :
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < WIN_WIDTH - (self.rect.width + 5):
            self.rect.x += self.speed
        if keys[K_DOWN] and self.rect.bottom < WIN_HEIGHT-5 :
            self.rect.y += self.speed 
        if keys[K_UP] and self.rect.top > WIN_HEIGHT - 200:
            self.rect.y -= self.speed
        self.speed = player_speed
    def fire(self):
        b = Bullet("bullet.png", ship.rect.centerx -8, ship.rect.centery, 16,32,15)
        bullets.add(b)
        mixer.Sound.play(fire_sound)
        self.speed = 0
#--------------------------------------
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > WIN_HEIGHT:
            self.rect.bottom = 0
            self.rect.x = (randint(0,16))*50
#----------------------------------
class Reflecting(GameSprite):
    def __init__(self, image_file, x , y, size_x, size_y, speed):
        super().__init__(image_file, x , y, size_x, size_y, speed)
        self.Health = 0 
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom > WIN_HEIGHT - 5 or self.rect.top < 5:
            self.speed *= -1
            self.Health +=1
        if self.Health == 5: 
            self.kill()
#----------------------------------
class Boss(GameSprite):
    def __init__(self, image_file, x , y, size_x, size_y, speed):
        super().__init__(image_file, x , y, size_x, size_y, speed)
        self.Hp = 0 
        self.x_speed = self.speed
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > WIN_HEIGHT:
            self.rect.bottom = 0
            self.rect.x = (randint(0, 2))*300
            self.x_speed *= -1
        if 0 < self.rect.y < 600:
            self.rect.x += self.x_speed
    def shoot(self):
        e_b = Bullet("bullet.png", self.rect.centerx -20, self.rect.centery, 40,30,-12)
        enemy_bullets.add(e_b)
        mixer.Sound.play(fire_sound)
#----------------------------------
def GamePhaseOne():
    x = randint(1,100)
    if x >= 99 - int(score/10):
        x = 1
    else:
        x = 0
    for _ in range(x):
        e = Enemy(img_enemy, randint(0,16)*50, -70 , 100, 70, randint(5,8))
        enemys.add(e)
def GamePhaseTwo():
    for _ in range(5):
        r = Reflecting(img_enemy, randint(0,17)*50, 5 , 50, 35, randint(6,10))
        reflectings.add(r)
font.init()
display.set_caption('Space Shooting')
window = display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = time.Clock()
bullets = sprite.Group()
enemys = sprite.Group()
enemy_bullets = sprite.Group()
reflectings = sprite.Group()
bosses = sprite.Group()
background = transform.scale(image.load(img_back),(WIN_WIDTH,WIN_HEIGHT))
ship = Player(img_hero, WIN_WIDTH/2 - 25, WIN_HEIGHT - 40, 50, 80, player_speed)
boss = Boss(img_enemy, WIN_WIDTH/2 - 110, -200, 300, 120, 5)
bosses.add(boss)
scoretext = TextSprite(text = "Score: 0", color = "white" , pos = (20,20), font_size = 40)
pausetext = TextSprite(text = "Pause", color = "white" , pos = (830,20), font_size = 20)
over_screen = TextSprite(text = "Game Over!", color = "white" , pos = (260,340), font_size = 100)
game_over = False
finish = False
#----------------------------------
while not game_over:
    for ev in event.get():
        if ev.type == QUIT:
            game_over = True    
        if ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                ship.fire()
                misspoint = randint(1,20)
                if misspoint >= 19:
                    score -= 1
        #if ev.type == MOUSEBUTTONUP:
            #mouse_pos = mouse.get_pos()
            #if pausetext.rect.collidepoint(mouse_pos):   
    if finish != True:
        window.blit(background, (0,0))
        if score > 80:
            if 0 <= (time.get_ticks() % 240) <= 6:
                boss.shoot()
            if 0 <= (time.get_ticks() % 600) <= 1:
                GamePhaseTwo()
            enemy_bullets.update()
            boss.update()
            boss.draw(window)
            enemy_bullets.draw(window)
        else:    
            GamePhaseOne()
            if score >= 40:
                if 0 <= (time.get_ticks() % 800) <= 1:
                    GamePhaseTwo() 
        if boss.Hp == 30:
            boss.kill()
            score += 30
        ship.update()
        enemys.update()
        bullets.update()
        reflectings.update()
        enemys.draw(window)
        bullets.draw(window)
        ship.draw(window)
        reflectings.draw(window)
        scoretext.draw(window)
        pausetext.draw(window)
        if sprite.groupcollide(bullets, enemys,True, True, collided = None):
            score += 1
            scoretext.update_text("Score: " + str(score))
        if sprite.groupcollide(bullets, bosses,True, False, collided = None):
            boss.Hp += 1
            print(boss.Hp)
        if sprite.spritecollide(ship,enemys, True) or sprite.spritecollide(ship,reflectings, True) or sprite.spritecollide(ship,enemy_bullets, True) or sprite.spritecollide(ship,bosses, True):
            finish = True
        if score >= 120:
            over_screen.update_text("Hail you the Victorious!")
            over_screen.pos = (100,340)
            over_screen.draw(window)
            finish = True
    else:
        window.fill('lightblue')
        over_screen.draw(window)
#----------------------------------
    display.update()
    clock.tick(60)