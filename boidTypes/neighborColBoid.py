import pygame
import sys
import random
import math
from boidTypes.boid import Boid

def limit(vector, max_force):
    if vector.length() > max_force:
        vector = vector.normalize() * max_force
    return vector

class NeighborColBoid(Boid):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)
        
    def update(self):
        super().update()
        if self.neighbours.values():
            # Calculate colour based on the maximum neighbour value
            max_neighbour_value = max(self.neighbours.values())
            self.colour = (255, 255, max(0, 255 - 255 * max_neighbour_value / 100))
        else:
            # Set a default colour or handle the case when there are no neighbours
            self.colour = (255, 255, 255)  # Once no close neighbours, immediately set to Default colour, e.g., white