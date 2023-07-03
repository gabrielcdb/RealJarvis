import pygame
import sys
from system import System
import math

# Variables for the beating sphere
max_radius = 50
min_radius = 30
radius = min_radius
speed = 3  # speed of the beating effect
class TalkingIndicator:
    def __init__(self, system):
        self.init_pygame()
        self.system = system
    @property
    def talking(self):
        return self.system.talking
    @property
    def speaking(self):
        return self.system.speaking

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Voice Indicator")
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0,0,0))
             # If speaking, make the sphere beat faster, bigger and change color
            if self.speaking:
                max_radius = 100
                min_radius = 90
                speed = 10
                color = (255, 140, 0)  # nice orange
                width = 5
            else:
                min_radius = 80
                max_radius = 60
                speed = 5
                color = (0, 255, 255)  # cyan
                width = 15

            # Calculate the new radius using a sine wave for smooth transitions
            radius = min_radius + (max_radius - min_radius) * (math.sin(pygame.time.get_ticks() * speed / 1000) + 1) / 2

            # Clear the screen
            self.screen.fill((0, 0, 0))

            # Draw the beating sphere
            pygame.draw.circle(self.screen, color, (200,200), int(radius),width)

            # Draw a circle at the bottom, color depends on self.talking
            color = (0,255,0) if self.talking else (255,0,0)
            pygame.draw.circle(self.screen, color, (200, 350), 25)

            pygame.display.flip()
            self.clock.tick(60)

system = System()
indicator = TalkingIndicator(system)
import threading
system_thread = threading.Thread(target=system.run)
system_thread.start()
indicator.run()