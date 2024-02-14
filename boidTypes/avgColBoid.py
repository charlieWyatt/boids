import pygame
import sys
import random
import math
from boidTypes.boid import Boid

def limit(vector, max_force):
    if vector.length() > max_force:
        vector = vector.normalize() * max_force
    return vector

class AvgColBoid(Boid):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)
        self.colour = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255)) # more likely to be lighter colours

    def update(self):
        super().update()
        total_nearby = len(self.neighbours)
        if total_nearby > 0:
            colour_sum = pygame.Vector3(self.colour)
            for other_boid in self.neighbours:
                colour_sum += pygame.Vector3(other_boid.colour)
            average_colour = colour_sum / (total_nearby + 1)
            self.colour = [int(self.colour[i] + (average_colour[i] - self.colour[i]) * 0.1) for i in range(3)]
            self.colour = tuple(min(max(c, 0), 255) for c in self.colour)