# Original project from the DK book, "Coding Games in Python."

import pgzrun
from random import randint

WIDTH = 400
HEIGHT = 400
score = 0
game_over = False
time_left = 10

fox = Actor("fox")
fox. pos = 100, 100

coin = Actor("coin")
coin.pos = 200, 200

def draw():
    screen.fill("chartreuse4")
    fox.draw()
    coin.draw()
    screen.draw.text("Score: " + str(score), color="black", topleft=(10, 10))
    screen.draw.text("Time: " + str(int(time_left)), color="black", topright=(WIDTH - 10, 10))

    if game_over:
        screen.fill("orange") #changed from pink to orange
        screen.draw.text("Final Score: " + str(score), topleft=(10, 10), fontsize = 60)

def place_coin():
    coin.x = randint(20, (WIDTH - 20))
    coin.y = randint(20, (HEIGHT - 20))

def time_up():
    global game_over
    game_over = True

def update(dt):
# dt = delta time
    global score, game_over, time_left

    if not game_over:
        if keyboard.a:
            fox.x = fox.x - 5
        elif keyboard.d:
            fox.x = fox.x + 5
        elif keyboard.w:
            fox.y = fox.y - 5
        elif keyboard.s:
            fox.y = fox.y + 5

    coin_collected = fox.colliderect(coin)
    if coin_collected:
        score = score + 10
        place_coin()

    time_left = time_left - dt
    if time_left <= 0:
        game_over = True
        time_left = 0

place_coin()

pgzrun.go()