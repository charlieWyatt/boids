import pygame
import sys
import random
import math

from boidTypes.boid import Boid
from boidTypes.avgColBoid import AvgColBoid
from boidTypes.neighborColBoid import NeighborColBoid


from predator import Predator

boid_types = {
    "Boid": Boid,
    "AvgColBoid": AvgColBoid,
    "NeighborColBoid": NeighborColBoid
}

BOID_TYPE = "NeighborColBoid" # the desired boid for the session

def create_boid(x, y, screen, boid_type=BOID_TYPE):
    return boid_types[boid_type](x, y, screen)


# Initialize Pygame
pygame.init()
pygame.font.init()  # Initialize the font module
font = pygame.font.SysFont(None, 24)  # Create a font object with default font and size 24
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

print(screen.get_width(), screen.get_height())

# Boids list
boids = [create_boid(random.randint(0, width), random.randint(0, height), screen) for _ in range(50)]

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
                boids.append(create_boid(x, y, screen))
            elif event.button == 3:  # Right click for Predator
                predators.append(Predator(x, y, screen))

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
        boid.apply_flocking(boids)
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
