# Screen
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 135
FPS = 30
TITLE = "Virtual Pet"

# Colours (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (232, 160, 191)
DARK_PINK = (199, 95, 160)
LIGHT_PINK = (253, 240, 246)
GREEN = (100, 200, 100)
RED = (220, 80, 80)
YELLOW = (255, 220, 80)
GREY = (150, 150, 150)
DARK = (45,45,45)

# Stat settings
MAX_STAT = 100
MIN_STAT = 0
STARTING_STAT = 80      # All stats begin at 80 (not full, not empty)

# How much each stat drops per second
HUNGER_DECAY = 2
HAPPINESS_DECAY = 1.5
CLEANLINESS_DECAY = 1
ENERGY_DECAY = 1
HEALTH_DECAY = 0.5      # Only drops when other stats are critically low

# Stat threshold for "critical" (below this = danger zone)
CRITICAL_THRESHOLD = 20

# Animation
ANIMATION_SPEED = 0.15  # Seconds per frame

# menu
MENU_ITEMS = ["Feed", "Play", "Clean", "Sleep", "Medicine"]
MENU_Y = 8

# Poop
POOP_INTERVAL = 15       # Seconds between poops appearing
MAX_POOPS = 3            # Maximum poops on screen at once
POOP_CLEANLINESS = 5     # How much each poop drains cleanliness per second

# Food options
FOODS = [
    {"name": "Egg",     "sprite": "egg.png",     "hunger": 25, "happiness": 10, "weight": 1},
    {"name": "Cupcake", "sprite": "cupcake.png",  "hunger": 20, "happiness": 30, "weight": 3},
]