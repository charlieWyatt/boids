import pygame
import sys
import random
import math

def limit(vector, max_force):
    if vector.length() > max_force:
        vector = vector.normalize() * max_force
    return vector

class Boid:
    def __init__(self, x, y, screen):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.max_speed = 4
        self.max_force = 0.1
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_width(), screen.get_height()
        self.neighbours = {}
        self.colour = (255, 255, 255)
        
    def update(self):
        self.position += self.velocity
        # Add simple wrapping around the screen
        self.position.x %= self.screen_width
        self.position.y %= self.screen_height

    def show(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.position.x), int(self.position.y)), 2)

    def get_adjusted_vector(self, source, target, width, height):
        direct_vector = target - source
        wrapped_vector_x = direct_vector.x
        wrapped_vector_y = direct_vector.y

        if abs(direct_vector.x) > width / 2:
            if direct_vector.x > 0:
                wrapped_vector_x -= width
            else:
                wrapped_vector_x += width

        if abs(direct_vector.y) > height / 2:
            if direct_vector.y > 0:
                wrapped_vector_y -= height
            else:
                wrapped_vector_y += height

        return pygame.Vector2(wrapped_vector_x, wrapped_vector_y)

    def apply_flocking(self, boids):
        # does alignment, cohesion, and separation
        alignment_steering = pygame.Vector2(0, 0)
        cohesion_steering = pygame.Vector2(0, 0)
        separation_steering = pygame.Vector2(0, 0)
        total_nearby = 0

        new_neighbours = {}
        for other_boid in boids:
            if other_boid != self:
                distance = self.position.distance_to(other_boid.position)
                if distance < 50:  # Assuming the same perception radius for simplicity
                    # alignment
                    alignment_steering += other_boid.velocity
                    # cohesion
                    cohesion_steering += other_boid.position
                    # separation
                    diff = self.position - other_boid.position
                    separation_steering += diff.normalize() / distance if distance > 0 else pygame.Vector2()
                    total_nearby += 1

                    if other_boid in self.neighbours:
                        # If the neighbor was already known, increment the duration
                        new_neighbours[other_boid] = self.neighbours[other_boid] + 1
                    else:
                        # If this is a new neighbor, initialize duration
                        new_neighbours[other_boid] = 1
        self.neighbours = new_neighbours
        

        if total_nearby > 0:
            # Alignment
            if alignment_steering.length_squared() > 0:  # Use length_squared() to avoid calculating the square root unnecessarily
                alignment_steering = (alignment_steering / total_nearby).normalize() * self.max_speed
            alignment_steering = limit(alignment_steering - self.velocity, self.max_force)

            # Cohesion
            if cohesion_steering.length_squared() > 0:
                average_position = cohesion_steering / total_nearby
                direction_to_average = average_position - self.position
                if direction_to_average.length_squared() > 0:
                    cohesion_steering = direction_to_average.normalize() * self.max_speed
                else:
                    cohesion_steering = pygame.Vector2(0, 0)  # Handle the case when the direction is a zero vector
            cohesion_steering = limit(cohesion_steering - self.velocity, self.max_force)

            # Separation
            if separation_steering.length_squared() > 0:
                separation_steering = (separation_steering / total_nearby).normalize() * self.max_speed
            separation_steering = limit(separation_steering - self.velocity, self.max_force)

        self.velocity += alignment_steering + cohesion_steering + separation_steering
        self.velocity = limit(self.velocity, self.max_speed)

    
    def flee(self, predator_pos):
        flee_distance = 100
        flee_force = pygame.Vector2(0, 0)
        adjusted_vector = self.get_adjusted_vector(self.position, predator_pos, self.screen_width, self.screen_height)
        if adjusted_vector.length() < flee_distance:
            flee_force = adjusted_vector.normalize() * -self.max_speed
            flee_force -= self.velocity
            if flee_force.length() > self.max_force:
                flee_force.scale_to_length(self.max_force)
        return flee_force