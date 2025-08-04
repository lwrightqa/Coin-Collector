# Original project from the DK book, "Coding Games in Python."

import pgzrun
from random import randint

WIDTH = 400
HEIGHT = 400

score = 0
game_over = False
game_started = False
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
        screen.draw.text("Final Score: " + str(score), center=(WIDTH/2, HEIGHT/2), fontsize = 60, color="black")

def place_coin():
    coin.x = randint(20, (WIDTH - 20))
    coin.y = randint(20, (HEIGHT - 20))

def time_up():
    global game_over
    game_over = True

def update(dt):
# dt = delta time
    global score, game_over, time_left, game_started

    if not game_over:
        if keyboard.w or keyboard.a or keyboard.s or keyboard.d or keyboard.up or keyboard.down or keyboard.left or keyboard.right:
            game_started = True

        if keyboard.a or keyboard.left:
            fox.x = fox.x - 5
        elif keyboard.d or keyboard.right:
            fox.x = fox.x + 5
        elif keyboard.w or keyboard.up:
            fox.y = fox.y - 5
        elif keyboard.s or keyboard.down:
            fox.y = fox.y + 5

    coin_collected = fox.colliderect(coin)
    if coin_collected:
        score = score + 10
        place_coin()

    if game_started and not game_over:
        time_left = time_left - dt
        if time_left <= 0:
            game_over = True
            time_left = 0
place_coin()

pgzrun.go()