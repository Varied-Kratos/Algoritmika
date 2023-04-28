from pygame import * 
from random import randint
from time import time as timer
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound=mixer.Sound('fire.ogg')

font.init()
font1=font.Font(None,80)
font2=font.Font(None,36)
win=font1.render('ПОБЕДА',True,(255,255,255))
lose=font1.render('Проигрыш',True,(180,0,0))

img_back='galaxy.jpg'
img_hero='rocket.png'
img_enemy='ufo.png'
img_bullet='bullet.png'
img_asteroid='asteroid.png'
score= 0
goal=20
lost=0
max_lost=10
num_fire=0 #для перезарядки
lifes=3
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image=transform.scale(image.load(player_image),(size_x,size_y))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x-=self.speed
        if keys[K_RIGHT] and self.rect.x<700-80:
            self.rect.x+=self.speed
        if keys[K_UP] and self.rect.y>5:
            self.rect.y-=self.speed
        if keys[K_DOWN] and self.rect.y<500-80:
            self.rect.y+=self.speed
    def fire(self):
        bullet=Bullet(img_bullet,self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        global lost
        if self.rect.y>win_height:
            self.rect.x=randint(80,win_width-80)
            self.rect.y=0
            lost+=1
class Bullet(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y<0:
            self.kill()

win_width=700
win_height=500
window=display.set_mode((win_width,win_height))
background=transform.scale(image.load(img_back),(win_width,win_height))

ship=Player(img_hero,5,win_height-100,80,100,10)
monsters=sprite.Group()#создаем группу спрайтов
for i in range(1,7):
    monster = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
    monsters.add(monster)
asteroids=sprite.Group()
for i in range(3):
    asteroid = Enemy(img_asteroid,randint(30,win_width-30),-40,80,50,randint(1,5))
    asteroids.add(asteroid)
bullets=sprite.Group()
finish=False
run=True
rel_time=False

while run:
    for e in event.get():
        if e.type==QUIT:
            run=False
        if e.type==KEYDOWN:
            if e.key==K_ESCAPE:
                run=False
        if e.type==KEYDOWN:
            if e.key==K_SPACE:
                if num_fire<5 and rel_time==False:
                    num_fire+=1
                fire_sound.play()
                ship.fire()

                if num_fire>=5 and rel_time==False:
                    last_time=timer()
                    rel_time=True
    

    if not finish:
        window.blit(background,(0,0))
        text=font2.render('Счёт:'+str(score),1,(255,255,255))
        window.blit(text,(10,20))
        text_lose=font2.render('Пропущено:' + str(lost),1,(255,255,255))
        ship.update()
        bullets.update()
        monsters.update()
        asteroids.update()

        if rel_time==True:
            now_time=timer()

            if now_time - last_time<3:
                reload=font2.render('Подожди. Перезарядка...',1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire=0
                rel_time=False

        ship.reset()
        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)
        collides=sprite.groupcollide(monsters,bullets,True, True)
        for c in collides:
            score+=1
            monster=Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
            monsters.add(monster)
        
        if sprite.spritecollide(ship,monsters,False) or sprite.spritecollide(ship,asteroids,False):
            sprite.spritecollide(ship,monsters,True)
            sprite.spritecollide(ship,asteroids,True)
            finish=True
            window.blit(lose,(200,200)) 
        if lifes==0 or lost>=max_lost:
            finish=Truewindow.blit(lose,(200,200))


        if score>=goal:
            finish=True
            window.blit(win,(200,200))
        if lifes==3:
            color_lifes=(0,255,0)
        elif lifes==2:
            color_lifes=(150,150,0)
        else:
            color_lifes=(255,0,0)

        text_lifes=font1.render(str(lifes),1,(color_lifes))
        window.blit(text_lifes,(649,10))
        display.update()
    else:
        finish=False
        score=0
        lost=0
        time.delay(3000)

        for m in monsters:
            m.kill()

        for b in bullets:
            b.kill()

        for a in asteroids:
            a.kill()

        for i in range(1,7):
            monster = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
            monsters.add(monster)


        for i in range(3):
            asteroid = Enemy(img_enemy,randint(30,win_width-30),-40,80,50,randint(1,5))
            asteroids.add(asteroid)  



    time.delay(120)
