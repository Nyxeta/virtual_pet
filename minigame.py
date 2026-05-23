import pygame
import random
from settings import *

class CatchGame:
    def __init__(self, screen, basket_sprite, food_sprite):
        self.screen = screen
        self.basket_sprite = basket_sprite
        self.food_sprite = food_sprite

        # Basket
        self.basket_x = SCREEN_WIDTH // 2
        self.basket_y = SCREEN_HEIGHT - 25    # was += instead of =
        self.basket_speed = 120

        # Food
        self.food_x = random.randint(10, SCREEN_WIDTH - 26)
        self.food_y = 20
        self.food_speed = 60

        # Score
        self.score = 0
        self.misses = 0
        self.max_misses = 3
        self.running = True

        self.font = pygame.font.SysFont(None, 14)

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.basket_x = max(0, self.basket_x - self.basket_speed * dt)
        if keys[pygame.K_RIGHT]:
            self.basket_x = min(SCREEN_WIDTH - 16, self.basket_x + self.basket_speed * dt)

    def update(self, dt):
        # Move food down
        self.food_y += self.food_speed * dt

        # Check if basket caught food
        if (self.food_y + 16 >= self.basket_y and
                self.basket_x < self.food_x + 16 and
                self.basket_x + 16 > self.food_x):    # was . instead of >
            self.score += 1
            self.food_speed += 5
            self.reset_food()

        # Food missed
        if self.food_y > SCREEN_HEIGHT:
            self.misses += 1
            self.reset_food()

        # Game over condition
        if self.misses >= self.max_misses:
            self.running = False

    def reset_food(self):
        self.food_x = random.randint(10, SCREEN_WIDTH - 26)
        self.food_y = 20

    def draw(self):
        self.screen.fill(LIGHT_PINK)

        # Draw basket and food
        self.screen.blit(self.food_sprite, (int(self.food_x), int(self.food_y)))
        self.screen.blit(self.basket_sprite, (int(self.basket_x), int(self.basket_y)))

        # Draw score and misses
        score_text = self.font.render(f"Score: {self.score}", True, DARK_PINK)
        misses_text = self.font.render(f"Misses: {self.misses}/{self.max_misses}", True, DARK_PINK)
        self.screen.blit(score_text, (5, 5))
        self.screen.blit(misses_text, (SCREEN_WIDTH - 70, 5))

    def get_result(self):
        if self.score >= 5:
            return 30
        elif self.score >= 3:
            return 20
        else:
            return 10