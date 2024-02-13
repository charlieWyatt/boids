import pygame
import sys
import random
import math

# Boid class to represent each individual boid
class Boid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.max_speed = 4
        self.max_force = 0.1

    def update(self):
        self.position += self.velocity
        # Add simple wrapping around the screen
        self.position.x %= width
        self.position.y %= height

    def show(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), 2)

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

    def apply_behavior(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohere(boids)
        separation = self.separate(boids)

        self.velocity += alignment
        self.velocity += cohesion
        self.velocity += separation

    def align(self, boids):
        perception_radius = 50
        steering = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self:
                vector_to_boid = self.get_adjusted_vector(self.position, boid.position, width, height)
                if vector_to_boid.length() < perception_radius:
                    steering += boid.velocity
                    total += 1
        if total > 0:
            steering /= total
            if steering.length() > 0:
                steering = steering.normalize() * self.max_speed
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def cohere(self, boids):
        perception_radius = 50
        steering = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self:
                vector_to_boid = self.get_adjusted_vector(self.position, boid.position, width, height)
                if vector_to_boid.length() < perception_radius:
                    steering += boid.position - vector_to_boid  # Adjusted position
                    total += 1
        if total > 0:
            steering /= total
            steering -= self.position
            if steering.length() > 0:
                steering = steering.normalize() * self.max_speed
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def separate(self, boids):
        perception_radius = 25
        steering = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self:
                vector_to_boid = self.get_adjusted_vector(self.position, boid.position, width, height)
                distance = vector_to_boid.length()
                if distance < perception_radius:
                    steering += vector_to_boid.normalize() / distance
                    total += 1
        if total > 0:
            steering /= total
            if steering.length() > 0:
                steering = steering.normalize() * self.max_speed
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering
    
    def flee(self, predator_pos):
        flee_distance = 100
        flee_force = pygame.Vector2(0, 0)
        adjusted_vector = self.get_adjusted_vector(self.position, predator_pos, width, height)
        if adjusted_vector.length() < flee_distance:
            flee_force = adjusted_vector.normalize() * -self.max_speed
            flee_force -= self.velocity
            if flee_force.length() > self.max_force:
                flee_force.scale_to_length(self.max_force)
        return flee_force

# Predator class, inherits from Boid
class Predator(Boid):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = 4  # Initial size
        self.max_speed = 6
        self.max_force = 0.2
        self.shrink_rate = 0.01  # Rate at which the predator shrinks over time

    def show(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.position.x), int(self.position.y)), max(2, self.size))


    def hunt(self, boids):
        closest = None
        closest_distance = math.inf
        for boid in boids:
            vector_to_boid = self.get_adjusted_vector(self.position, boid.position, width, height)
            distance = vector_to_boid.length()
            if distance < closest_distance:
                closest = boid
                closest_distance = distance

        if closest is not None:
            adjusted_vector = self.get_adjusted_vector(self.position, closest.position, width, height)
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
                self.size += 1  # Increase size
                self.max_speed *= 0.95  # Decrease speed slightly
                eaten = True
        return eaten
    
    def update(self):
        super().update()
        self.size -= self.shrink_rate  # Continually decrease size
        if self.size <= 2:
            return False  # Indicate removal
        return True  # Indicate no removal needed

# Initialize Pygame
pygame.init()
pygame.font.init()  # Initialize the font module
font = pygame.font.SysFont(None, 24)  # Create a font object with default font and size 24
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Boids list
boids = [Boid(random.randint(0, width), random.randint(0, height)) for _ in range(50)]

predators = []  # List to store predators

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if event.button == 1:  # Left click for Boid
                boids.append(Boid(x, y))
            elif event.button == 3:  # Right click for Predator
                predators.append(Predator(x, y))

    #### Update game objects ####
    for predator in predators:
        # predator dies if size is too small
        alive = predator.update()
        if not alive:
            predators.remove(predator)
            continue
        
        if predator.eat(boids):
            # Predator eats and grows
            pass
        hunt_force = predator.hunt(boids)
        predator.velocity += hunt_force
        predator.update()  # Now also decreases size over time
        predator.show(screen)

    for boid in boids:
        # Apply behaviors, flee from predators, update, and show for each boid
        boid.apply_behavior(boids)
        for predator in predators:
            flee_force = boid.flee(predator.position)
            boid.velocity += flee_force
        boid.update()
        boid.show(screen)
    
    


    #### Stats Display Logic #####
    # Display the count of boids and predators
    boid_count = len(boids)
    predator_count = len(predators)
    boid_count_text = font.render(f'Boids: {boid_count}', True, (255, 255, 255))
    predator_count_text = font.render(f'Predators: {predator_count}', True, (255, 255, 255))

    # Display the text on the screen at the top-left corner
    screen.blit(boid_count_text, (10, 10))
    screen.blit(predator_count_text, (10, 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
