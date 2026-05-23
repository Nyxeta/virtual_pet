import os
import pygame
from settings import *

## load sprite
def load_sprite(filename):
    path = os.path.join("sprites",filename)
    image = pygame.image.load(path).convert_alpha()
    return image

## drawing stats
def draw_stats(surface,pet):
    bar_width = 30
    bar_height = 6
    spacing = 44
    start_x = 10
    y = 120

    stats = [
        ("HUN", pet.hunger, RED),
        ("HAP", pet.happiness, YELLOW),
        ("CLN", pet.cleanliness, GREEN),
        ("ENE", pet.energy, PINK),
        ("HLT", pet.health, DARK_PINK),
    ]

    for i, (label, value, colour) in enumerate(stats):
        x = start_x + i * spacing

        ## draw label
        font = pygame.font.SysFont(None, 12)
        text = font.render(label, True, GREY)
        surface.blit(text, (x, y - 10))

        ## draw background (empty)
        pygame.draw.rect(surface, GREY, (x, y, bar_width, bar_height))

     ## draw filled portion
        fill_width = int((value / MAX_STAT) * bar_width)
        pygame.draw.rect(surface, colour, (x, y, fill_width, bar_height))

def draw_pet(surface, sprite):
    sprite_x = (SCREEN_WIDTH - sprite.get_width()) // 2 ## draw sprite in center
    sprite_y = (SCREEN_HEIGHT - sprite.get_height()) // 2 ##draw sprite in center
    surface.blit(sprite, (sprite_x, sprite_y)) ## draw sprite in center

# menu display
def draw_menu(surface, selected_index):
    font = pygame.font.SysFont(None, 14)
    spacing = 46
    start_x = 8

    for i, item in enumerate(MENU_ITEMS):
        x = start_x + i * spacing

        if i == selected_index: ## highlight selected item
            pygame.draw.rect(surface, DARK_PINK, (x - 2, MENU_Y - 2, 40, 14), border_radius = 3)
            text = font.render(item, True, WHITE)
        else:
            text = font.render(item, True, DARK)

        surface.blit(text, (x, MENU_Y))
def get_current_sprite(pet, sprites):
    if not pet.is_alive:
        return sprites["dead"]
    elif pet.is_sick:
        return sprites["sick"]
    elif pet.energy < CRITICAL_THRESHOLD:
        return sprites["sleeping"]
    elif pet.hunger < CRITICAL_THRESHOLD or pet.health < CRITICAL_THRESHOLD:
        return sprites["sad"]
    elif pet.happiness > 80:
        return sprites["happy"]
    else:
        return sprites["idle"]

# poops on screen
def draw_poops(surface, pet, poop_sprite):

    pet_x = (SCREEN_WIDTH - 48) // 2
    pet_y = (SCREEN_HEIGHT - 48) // 2

    poop_positions =[
        (pet_x - 20, pet_y + 16),
        (pet_x +52, pet_y +16),
        (pet_x + 16, pet_y + 52),
    ]

    for i in range(pet.poops):
        surface.blit(poop_sprite, poop_positions[i])

def draw_food_menu(surface, selected_food, sprites):
    font_title = pygame.font.SysFont(None, 14)
    font_label = pygame.font.SysFont(None, 12)

    # Title
    title = font_title.render("What to feed?", True, DARK_PINK)
    surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 15))

    # Two food options side by side
    positions = [80, 145]
    food_keys = ["egg", "cupcake"]

    for i, (x, key) in enumerate(zip(positions, food_keys)):
        # Highlight selected
        if i == selected_food:
            pygame.draw.rect(surface, DARK_PINK, (x - 4, 45, 36, 50), border_radius=4)

        # Draw sprite
        surface.blit(sprites[key], (x, 50))

        # Draw name
        name = font_label.render(FOODS[i]["name"], True, WHITE if i == selected_food else DARK_PINK)
        surface.blit(name, (x - 2, 72))

def draw_death_screen(surface, sprites):
    font_title = pygame.font.SysFont(None, 20)
    font_sub = pygame.font.SysFont(None, 14)

    surface.fill(LIGHT_PINK)

    # draw sprite in center
    sprite = sprites["dead"]
    x = (SCREEN_WIDTH - sprite.get_width()) // 2
    y =30
    surface.blit(sprite, (x, y))

    #text for game over
    title = font_title.render("It died :(", True, DARK_PINK)
    sub = font_sub.render("Press R to restart", True, GREY)

    surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 90))
    surface.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, 110))


# pet movement
def draw_pet_offset(surface, sprite, x_offset):
    x = (SCREEN_WIDTH - sprite.get_width()) // 2 + x_offset
    y = (SCREEN_HEIGHT - sprite.get_height()) // 2
    surface.blit(sprite, (x, y))