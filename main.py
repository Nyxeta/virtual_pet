import pygame
from settings import *
from pet import Pet
from display import load_sprite, draw_stats, draw_pet, draw_menu, get_current_sprite, draw_poops, draw_food_menu, draw_death_screen, draw_pet_offset
from minigame import CatchGame

# Setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Create pet
my_pet = Pet()

# Load sprites
sprites = {
    "idle": load_sprite("idle_1.png"),
    "happy": load_sprite("happy_1.png"),
    "sad": load_sprite("sad_1.png"),
    "sleeping": load_sprite("sleeping_1.png"),
    "sick": load_sprite("sick_1.png"),
    "dead": load_sprite("dead_1.png"),
    "poop": load_sprite("poop.png"),
    "basket": load_sprite("basket.png"),
    "food": load_sprite("food.png"),
    "egg": load_sprite("egg.png"),
    "cupcake": load_sprite("cupcake.png"),
    "eating_1": load_sprite("eating_1.png"),
    "eating_2": load_sprite("eating_2.png"),
    "blink": load_sprite("blink.png"),
}

# Menu
selected_index = 0

# Game state
game_state = "main"
current_minigame = None

# Food
selected_food = 0
eating_timer = 0
eating_frame = 0

# idle movement
pet_x_offset = 80
pet_direction = 1
pet_speed = 60
idle_state = "moving"
idle_timer = 0
blink_timer = 0
blink_count = 0
is_blinking = False

# Game loop
running = True
while running:

    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_state == "main":
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % len(MENU_ITEMS)
                if event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(MENU_ITEMS)
                if event.key == pygame.K_RETURN:
                    if selected_index == 0:
                        game_state = "feeding"
                        selected_food = 0
                    elif selected_index == 1:
                        game_state = "minigame"
                        current_minigame = CatchGame(
                            screen,
                            sprites["basket"],
                            sprites["food"]
                        )
                    elif selected_index == 2:
                        my_pet.clean()
                    elif selected_index == 3:
                        my_pet.sleep()
                    elif selected_index == 4:
                        my_pet.give_medicine()

            elif game_state == "feeding":
                if event.key == pygame.K_LEFT:
                    selected_food = 0
                if event.key == pygame.K_RIGHT:
                    selected_food = 1
                if event.key == pygame.K_RETURN:
                    food = FOODS[selected_food]
                    my_pet.hunger = my_pet.clamp(my_pet.hunger + food["hunger"])
                    my_pet.happiness = my_pet.clamp(my_pet.happiness + food["happiness"])
                    my_pet.weight += food["weight"]
                    game_state = "eating"
                    eating_timer = 0
                    eating_frame = 0

            elif game_state == "dead":
                if event.key == pygame.K_r:
                    my_pet = Pet()
                    game_state = "main"
                    selected_index = 0

    if game_state == "main":
        my_pet.update()
        if not my_pet.is_alive:
            game_state = "dead"

        #movement logic
        if idle_state == "moving":
            pet_x_offset += pet_direction * pet_speed * dt
            idle_timer += dt
            print(f"offset: {pet_x_offset:.2f}, direction: {pet_direction}")  # debug

            #move for amount of seconds, stop, blink
            if idle_timer >= 1.5:
                idle_state = "blink"
                idle_timer = 0
                blink_timer = 0
                blink_count = 0
                is_blinking = False

            #bounce between -30 and 30 pixels from center
            if pet_x_offset > 50:
                pet_x_offset = 50
                pet_direction = -1
            elif pet_x_offset < -50:
                pet_x_offset = -50
                pet_direction = 1

        elif idle_state == "blink":
            blink_timer += dt

            #blink every 0.4 seconds
            if blink_timer >= 0.4:
                blink_timer = 0
                is_blinking = not is_blinking
                if not is_blinking:
                    blink_count += 1
            #move again after 3 blinks
            if blink_count >= 3:
                idle_state = "moving"
                is_blinking = False
                #pick random direction
                import random
                pet_direction = random.choice([-1, 1])
        #pick the right sprite
        if my_pet.is_sick:
            current_sprite = sprites["sick"]
        elif my_pet.energy < CRITICAL_THRESHOLD:
            current_sprite = sprites["sleeping"]
        elif my_pet.hunger <CRITICAL_THRESHOLD or my_pet.health < CRITICAL_THRESHOLD:
            current_sprite = sprites["sad"]
        elif my_pet.happiness > 80:
            current_sprite = sprites["happy"]
        elif idle_state == "blink" and is_blinking:
            current_sprite = sprites["blink"]
        else:
            current_sprite = sprites["idle"]


        screen.fill(LIGHT_PINK)
        draw_menu(screen, selected_index)
        draw_pet_offset(screen, current_sprite, pet_x_offset)
        draw_poops(screen, my_pet, sprites["poop"])
        draw_stats(screen, my_pet)

    elif game_state == "feeding":
        screen.fill(LIGHT_PINK)
        draw_food_menu(screen, selected_food, sprites)

    elif game_state == "eating":
        eating_timer += dt
        if eating_timer < 0.3:
            eating_frame = 0
        elif eating_timer < 0.6:
            eating_frame = 1
        elif eating_timer < 0.9:
            eating_frame = 0
        elif eating_timer < 1.2:
            eating_frame = 1
        else:
            game_state = "main"

        screen.fill(LIGHT_PINK)
        draw_menu(screen, selected_index)
        eating_sprite = sprites["eating_1"] if eating_frame == 0 else sprites["eating_2"]
        draw_pet_offset(screen, eating_sprite, pet_x_offset)
        draw_stats(screen, my_pet)

    elif game_state == "dead":
        draw_death_screen(screen, sprites)

    elif game_state == "minigame" and current_minigame is not None:
        current_minigame.handle_input(dt)
        current_minigame.update(dt)
        current_minigame.draw()

        if not current_minigame.running:
            happiness_boost = current_minigame.get_result()
            my_pet.happiness = my_pet.clamp(my_pet.happiness + happiness_boost)
            game_state = "main"
            current_minigame = None

    pygame.display.flip()

pygame.quit()