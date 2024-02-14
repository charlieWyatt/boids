import pygame
import sys
import random
import math


from boid import Boid

class Predator(Boid):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)
        self.size = 4  # Initial size
        self.max_speed = 6
        self.max_force = 0.2
        self.shrink_rate = 0.01  # Rate at which the predator shrinks over time
        self.screen_width, self.screen_height = screen.get_width(), screen.get_height()

    def show(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.position.x), int(self.position.y)), max(2, self.size))


    def hunt(self, boids):
        closest = None
        closest_distance = math.inf
        for boid in boids:
            vector_to_boid = self.get_adjusted_vector(self.position, boid.position, self.screen_width, self.screen_height)
            distance = vector_to_boid.length()
            if distance < closest_distance:
                closest = boid
                closest_distance = distance

        if closest is not None:
            adjusted_vector = self.get_adjusted_vector(self.position, closest.position, self.screen_width, self.screen_height)
            desired_velocity = adjusted_vector.normalize() * self.max_speed
            steering = desired_velocity - self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
            return steering
        else:
            return pygame.Vector2(0, 0)
        

    def eat(self, boids):
        global eaten  # This will track the boids that have been eaten
        eaten = False
        for boid in boids[:]:  # Iterate over a slice copy of the list
            distance = self.position.distance_to(boid.position)
            if distance < self.size:  # Collision detection based on size
                boids.remove(boid)  # Remove the eaten boid
                self.size += 1
                #self.max_speed *= 0.95  # Decrease speed slightly
                eaten = True
        return eaten
    
    def update(self):
        super().update()
        self.size -= self.shrink_rate  # Continually decrease size
        if self.size <= 2:
            return False  # Indicate removal
        return True  # Indicate no removal needed