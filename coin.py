import pgzrun
from random import randint

WIDTH = 400
HEIGHT = 400

# Global game state variables
score = 0
game_over = False

# Actors
fox = Actor("fox")
coin = Actor("coin")

def init_game_state():
    """Initializes or resets the game state."""
    global score, game_over
    score = 0
    game_over = False
    fox.pos = 100, 100
    coin.pos = 200, 200
    # place_coin() # Called separately in main or after init


def draw():
    screen.fill("chartreuse4")
    fox.draw()
    coin.draw()
    screen.draw.text("Score: " + str(score), color="black", topleft=(10, 10))

    if game_over:
        screen.fill("orange")  # changed from pink to orange
        screen.draw.text("Final Score: " + str(score), topleft=(10, 10), fontsize=60)


def place_coin():
    coin.x = randint(20, (WIDTH - 20))
    coin.y = randint(20, (HEIGHT - 20))


def time_up():
    global game_over
    game_over = True


def update():
    global score

    # Corrected movement logic:
    # 'a' or left arrow to move left
    if keyboard.a or keyboard.left:
        fox.x = fox.x - 5
    # 'd' or right arrow to move right
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


# Main game execution block
if __name__ == "__main__":
    init_game_state()
    place_coin()  # Initial coin placement
    clock.schedule(time_up, 10.0)  # Schedule the game timer

pgzrun.go()