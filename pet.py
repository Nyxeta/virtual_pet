import time
from settings import *

## pet class
class Pet:
    def __init__(self):
        self.hunger = STARTING_STAT
        self.happiness = STARTING_STAT
        self.cleanliness = STARTING_STAT
        self.energy = STARTING_STAT
        self.health = STARTING_STAT
        self.age = 0
        self.weight = 10
        self.is_sick = False
        self.is_alive = True
        self.last_update = time.time()
        self.poops = 0
        self.time_since_last_poop = 0

    def clamp (self, value):
        return max (MIN_STAT, min(MAX_STAT, value))

    def update(self):
        if not self.is_alive:
            return

        now = time.time()
        elapsed = now - self.last_update
        self.last_update = now

        self.hunger = self.clamp(self.hunger - HUNGER_DECAY * elapsed)
        self.happiness = self.clamp(self.happiness - HAPPINESS_DECAY * elapsed)
        self.cleanliness = self.clamp(self.cleanliness - CLEANLINESS_DECAY * elapsed)
        self.energy = self.clamp(self.energy - ENERGY_DECAY * elapsed)

        if self.hunger < CRITICAL_THRESHOLD or \
           self.happiness < CRITICAL_THRESHOLD or \
           self.cleanliness < CRITICAL_THRESHOLD:
            self.health = self.clamp(self.health - HEALTH_DECAY * elapsed)
        # Poop accumulates over time
        self.time_since_last_poop += elapsed
        if self.time_since_last_poop >= POOP_INTERVAL and self.poops < MAX_POOPS:
            self.poops += 1
            self.time_since_last_poop = 0

        # Each poop drains cleanliness
        if self.poops > 0:
            self.cleanliness = self.clamp(
                self.cleanliness - POOP_CLEANLINESS * self.poops * elapsed
                )

        if self.health <=0:
            self.is_alive = False

            # Pet gets sick if health is critically low and not already sick
            if self.health < CRITICAL_THRESHOLD and not self.is_sick:
                self.is_sick = True

    def print_stats(self):
        print(f"Hunger: {self.hunger:.1f} | Happiness: {self.happiness:.1f} | "
              f"Cleanliness: {self.cleanliness:.1f} | Energy: {self.energy:.1f} |"
              f"Health: {self.health:.1f} | Alive: {self.is_alive}")

    # actions
    def feed(self):
        self.hunger = self.clamp(self.hunger + 30)
        self.weight += 1

    def play(self):
        self.happiness = self.clamp(self.happiness +20)
        self.energy = self.clamp(self.energy - 10)
        self.weight = max(1, self.weight - 1)

    def clean(self):
        self.cleanliness = self.clamp(self.cleanliness +30)
        self.poops = 0

    def sleep(self):
        self.energy = self.clamp(self.energy + 40)

    def give_medicine(self):
        self.is_sick = False
        self.happiness = self.clamp(self.happiness - 10)
        self.health = self.clamp(self.health +20)