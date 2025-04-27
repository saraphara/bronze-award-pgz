import pgzrun
import random
from pgzhelper import *

WIDTH = 480
HEIGHT = 360
music.play('piano.wav')
bg = Actor('bg.png', (235, 65))
bg.scale = 0.5

player = Actor('walk4', (75, 200))
player.walking  = False
player.health = 10
player.scale = 0.15
player.walkframes = ["walk1", "walk2", "walk3", "walk4"]
player.walkframe = 1
player.speed = 6
player.counter = 0
player.side = 1
player.score = 0

orb = Actor('orb', (237, 200))
orb.health = 10
orb.scale = 0.1

enemy = Actor('enemy', (450, 200))  
enemy.side = 1
enemy.cooldown = 1
enemy.scale = 0.05
enemy.killcount = 0

attack = Actor('attack1', (600, 200))
attack.cooldown = False
attack.scale = 0.25
attack.frames = ["attack1","attack2", "attack3", "attack4"]
attack.frame = 0

def update(): 

    player.scale = 0.15
    if enemy.side == 1:
        enemy.x -= 2 + enemy.killcount
    else:
        enemy.x += 2 + enemy.killcount
    if orb.health > 0:
        if keyboard.left:
            player.x -= player.speed
            player.flip_x = True
            player.walking = True
            player.side = 2

        elif keyboard.right:
            player.x += player.speed
            player.flip_x = False
            player.walking = True
            player.side = 1

        else:
            player.walking = False
        if keyboard.f:
            sounds.spell.play()
            if attack.cooldown == False:
                if player.side == 1:
                    attack.pos = (player.x + 50, 200)
                    attack.flip_x = False
                else:
                    attack.pos = (player.x - 50, 200)
                    attack.flip_x = True
                if attack.frame == 4:
                    attack.pos = (600,200)
                    attack.frame = 0
                    attack.cooldown = True
                    clock.schedule_unique(attack_uncool, 0.3)
                else:
                    attack.image = attack.frames[attack.frame]
                    attack.scale = 0.25
                    attack.frame = attack.frame + 1
    if player.walking == True:
        if player.counter == 3:
            if player.walkframe == 3:
                player.walkframe = 0
            else:
                player.image = player.walkframes[player.walkframe]
                player.walkframe = player.walkframe + 1
            player.counter = 0
        else:
            player.counter = player.counter + 1
        "try making it cycle through frames multiple times"
    else:
        player.image = player.walkframes[3]
        player.scale = 0.15
    if enemy.colliderect(orb):
        enemy.side = random.randint(1, 2)
        if enemy.side == 1:
            enemy.pos = 550, 200
        else:
            enemy.pos = -50, 200
        orb.health -= 1
    if enemy.colliderect(attack):
        enemy.side = random.randint(1, 2)
        if enemy.side == 1:
            enemy.pos = 550, 200
        else:
            enemy.pos = -50, 200
        enemy.killcount = enemy.killcount + 0.1
        player.score = player.score + 1
    if orb.health < 1: 
        player.image = 'ded.png'
        player.pos = player.x, 250
        orb.scale = 0.1
        orb.image = 'orb broken.png'
    if keyboard.e:
        print(player.pos)

def draw():
    bg.draw()
    orb.draw()
    player.draw()            
    enemy.draw()
    attack.draw()
    screen.draw.text('Score: ' + str(player.score), (350,25), color=(0,0,0), fontsize=30)


def attack_uncool():
    attack.cooldown = False