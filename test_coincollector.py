import pytest
from random import randint
import pygame  # Import Pygame
import os  # Import os to set environment variables

# Attempt to use Pygame Zero's Actor.
# This requires:
# 1. Pygame Zero (pgzrun) installed.
# 2. Image files: An 'images' folder in the same directory as this test file, containing 'fox.png' and 'coin.png'.

try:
    from pgzero.actor import Actor
except ImportError:
    # If pgzrun is not installed, skip these tests at the module level.
    pytest.skip("Pygame Zero (pgzrun) not installed or Actor not found, skipping all tests in this file.",
                allow_module_level=True)

# --- Test Constants ---
WIDTH_TEST = 400
HEIGHT_TEST = 400

# Contains game state and logic for testing.
class GameTestContext:
    def __init__(self, width, height):
        self.score = 0
        self.width = width
        self.height = height
        self.time_left = 10
        self.game_over = False

        # Actor initialization can fail if images are missing or Pygame isn't set up.
        # The fixture calling this constructor will handle exceptions.
        self.fox = Actor("fox")
        self.fox.pos = 100, 100

        self.coin = Actor("coin")
        self.coin.pos = 200, 200

    def update(self, dt):
        # A method to simulate the game's main update loop
        if not self.game_over:
            self.time_left -= dt
            if self.time_left <= 0:
                self.game_over = True
                self.time_left = 0

            # You could also call your score logic from here
            self.update_score_logic()

    def place_coin(self):
        # Simulates placing the coin within test boundaries.
        self.coin.x = randint(20, (self.width - 20))
        self.coin.y = randint(20, (self.height - 20))

    def update_score_logic(self):
        # Simulates the core score update logic from the game.
        coin_collected = self.fox.colliderect(self.coin)
        if coin_collected:
            self.score += 10
            self.place_coin()

# Pytest fixture to set up and tear down the Pygame environment and provide a GameTestContext instance.
@pytest.fixture

def game_context():
    # Set the SDL_VIDEODRIVER to dummy BEFORE pygame.init()
    os.environ['SDL_VIDEODRIVER'] = 'dummy'

    try:
        pygame.init()
        pygame.display.set_mode((WIDTH_TEST, HEIGHT_TEST))  # Or (1,1)
    except pygame.error as e:
        pytest.skip(f"Pygame initialization or display setup failed: {e}. "
                    "Ensure Pygame and its dependencies are correctly installed.")
        return  # Exit fixture if Pygame setup fails

    try:
        context = GameTestContext(WIDTH_TEST, HEIGHT_TEST)
    except Exception as e:  # Catch errors during Actor initialization
        pygame.quit()  # Clean up Pygame if context creation fails
        pytest.skip(f"Could not initialize GameTestContext (Actors likely failed). "
                    f"Ensure 'images/fox.png' and 'images/coin.png' exist "
                    f"in an 'images' subdirectory. Error: {e}")
        return  # Exit fixture

    yield context  # Provide the context to the test

    # Teardown: Quit Pygame after each test
    pygame.quit()


# --- Initialization and Setup Tests ---

def test_initial_score_is_zero(game_context):
    # Test that the score is 0 when the game context is initialized.
    assert game_context.score == 0, "Initial score should be 0."

def test_place_coin_within_bounds(game_context):
    # Test that place_coin() places the coin within the specified boundaries.
    min_coord = 20
    max_x = game_context.width - 20
    max_y = game_context.height - 20

    for _ in range(100):  # Run multiple times to check the random placement
        game_context.place_coin()
        assert min_coord <= game_context.coin.x <= max_x, "Coin x-position is out of bounds."
        assert min_coord <= game_context.coin.y <= max_y, "Coin y-position is out of bounds."


# ---
def test_score_increases_on_collision(game_context):
    # Test that the score increases by 10 when the fox collides with the coin.
    # Position fox and coin to ensure they collide.
    game_context.fox.pos = (150, 150)
    game_context.coin.pos = (150, 150)

    initial_coin_pos_x, initial_coin_pos_y = game_context.coin.pos

    game_context.update_score_logic()  # Run the game logic

    assert game_context.score == 10, "Score should increase to 10 after one collision."

    # Also check if the coin was re-placed (moved)
    assert (game_context.coin.x != initial_coin_pos_x or game_context.coin.y != initial_coin_pos_y), \
        "Coin should have been moved after collection."

def test_score_does_not_increase_if_no_collision(game_context):
    # Test that the score does not change if the fox and coin do not collide.
    # Position fox and coin far from each other
    game_context.fox.pos = (50, 50)
    game_context.coin.pos = (300, 300)

    initial_score = game_context.score  # Should be 0 from fixture reset
    game_context.update_score_logic()  # Run the game logic

    assert game_context.score == initial_score, "Score should remain unchanged if no collision occurs."

def test_score_accumulates_over_multiple_collections(game_context):
    # Test that the score correctly accumulates over several coin collections.
    # --- First collection ---
    game_context.fox.pos = (150, 150)  # Position for collision
    game_context.coin.pos = (150, 150)
    game_context.update_score_logic()
    assert game_context.score == 10, "Score should be 10 after the first collection."

    # --- Second collection ---
    # Simulate the fox moving to the coin's new (random) position.
    game_context.fox.pos = game_context.coin.pos
    game_context.update_score_logic()
    assert game_context.score == 20, "Score should be 20 after the second collection."

    # --- Third collection ---
    game_context.fox.pos = game_context.coin.pos
    game_context.update_score_logic()
    assert game_context.score == 30, "Score should be 30 after the third collection."

def test_game_over_when_time_runs_out(game_context):
    # Test that the game_over flag is set when time_left reaches 0.
    assert not game_context.game_over, "Game should not be over at the start."

    game_context.update(dt=11)  # Simulate 11 seconds passing, more than the initial 10.

    assert game_context.game_over, "Game should be over when time runs out."
    assert game_context.time_left == 0, "Time left should be clamped to 0."

def test_no_score_increase_after_game_over(game_context):
    # Test that score does not increase after the game is over.
    # Position for a collision to happen on the frame the game ends.
    game_context.fox.pos = game_context.coin.pos

    # Run update to end the game. Score will increase on this frame.
    game_context.update(dt=11)
    assert game_context.score == 10, "Score should increase on the final frame."
    assert game_context.game_over is True, "Game should be over."

    # Now that game is over, try to score again.
    # Move fox to the new coin position for another collision.
    game_context.fox.pos = game_context.coin.pos
    game_context.update(dt=1)  # Simulate another second passing

    # The score should not have increased again.
    assert game_context.score == 10, "Score should not increase after game is over."

def test_place_coin_within_bounds(game_context):
    # Test that place_coin() places the coin within the specified boundaries.
    min_coord = 20
    max_x = game_context.width - 20
    max_y = game_context.height - 20

    for _ in range(100):  # Run multiple times to check the random placement
        game_context.place_coin()
        assert min_coord <= game_context.coin.x <= max_x, "Coin x-position is out of bounds."
        assert min_coord <= game_context.coin.y <= max_y, "Coin y-position is out of bounds."

def test_collision_at_edges(game_context):
    # Test that collision is detected correctly at the very edge of the actors.
    game_context.fox.pos = (200, 200)
    touching_x = game_context.fox.x + (game_context.fox.width / 2) + (game_context.coin.width / 2)

    # Position 1: Barely overlapping
    game_context.coin.pos = (touching_x - 1, game_context.fox.y)
    assert game_context.fox.colliderect(game_context.coin), "Collision should be detected when actors are overlapping by one pixel."

    # Position 2: Adjacent, not overlapping
    game_context.coin.pos = (touching_x + 1, game_context.fox.y)
    assert not game_context.fox.colliderect(game_context.coin), "Collision should not be detected when actors are adjacent."