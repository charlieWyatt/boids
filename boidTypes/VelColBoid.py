import pygame
import sys
import random
import math
from boidTypes.boid import Boid
from colorsys import hls_to_rgb

def limit(vector, max_force):
    if vector.length() > max_force:
        vector = vector.normalize() * max_force
    return vector

class VelColBoid(Boid):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)
        self.colour = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255)) # more likely to be lighter colours

    def velocity_to_color(self, velocity):
        """Map the velocity's angle to a hue in the HSL color space."""
        angle = math.atan2(velocity.y, velocity.x)  # Get the angle in radians
        # Normalize the angle to [0, 2*pi]
        if angle < 0:
            angle += 2 * math.pi
        # Map angle to [0, 1] for hue value (Hue is a circle, so it fits angles well)
        hue = angle / (2 * math.pi)
        # Convert HSL to RGB
        r, g, b = hls_to_rgb(hue, 0.5, 1)  # Fixed saturation=0.5, lightness=1 for vibrant colors
        return int(r * 255), int(g * 255), int(b * 255)  # Convert [0,1] range to [0,255]


    def update(self):
        super().update()
        self.colour = self.velocity_to_color(self.velocity)