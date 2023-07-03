import pygame
import sys
import math


# Class for a visual talking indicator using Pygame.
class TalkingIndicator:
    def __init__(self, system):
        self.init_pygame()
        self.system = system
        # Variables for the beating sphere
        self.max_radius = 50
        self.min_radius = 30
        self.radius = self.min_radius
        self.speed = 3 

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
                self.max_radius = 100
                self.min_radius = 90
                self.speed = 10
                self.color = (255, 140, 0)  # nice orange
                self.width = 5
            else:
                self.min_radius = 80
                self.max_radius = 60
                self.speed = 5
                self.color = (0, 255, 255)  # cyan
                self.width = 15

            # Calculate the new radius using a sine wave for smooth transitions
            radius = self.min_radius + (self.max_radius - self.min_radius) * (math.sin(pygame.time.get_ticks() * self.speed / 1000) + 1) / 2

            # Clear the screen
            self.screen.fill((0, 0, 0))

            # Draw the beating sphere
            pygame.draw.circle(self.screen, self.color, (200,200), int(radius),self.width)

            # Draw a circle at the bottom, color depends on self.talking
            color = (0,255,0) if self.talking else (255,0,0)
            pygame.draw.circle(self.screen, self.color, (200, 350), 25)

            pygame.display.flip()
            self.clock.tick(60)