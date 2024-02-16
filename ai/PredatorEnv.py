import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np
import random
from controller import create_boid, create_predator

class PredatorEnv(gym.Env):
    metadata = {'render_modes': ['human', 'rgb_array'], 'render_fps': 30}

    def __init__(self, render_mode=None):
        super(PredatorEnv, self).__init__()
        self.render_mode = render_mode
        pygame.init()
        pygame.font.init()  # Initialize the font module
        self.font = pygame.font.SysFont(None, 24)  # Create a font object with default font and size 24
        self.width, self.height = 1400, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.starting_boids = 50
        self.starting_predators = 1 
        self.max_objects = 100  # Maximum number of boids and predators combined

        # Define a continuous action space where each action is a 2D vector for acceleration
        self.action_space = spaces.Box(low=-10, high=10, shape=(2,), dtype=np.float32)

        

        # Observation space: positions and velocities of all boids and predators
        # Adjust `shape` based on the maximum expected number of boids and predators
        # Here, we arbitrarily choose 100 entities (boids and predators combined) as a placeholder
        # Each entity is represented by 4 values (x position, y position, x velocity, y velocity)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(self.max_objects, 4), dtype=np.float32)

        self.predator = None
        self.boids = []
        self.predators = []
        self.reset()

    def step(self, action):
        # Implement the action logic here
        self.predator.accelerate(action)

        self._update_game_state()

        # Calculate the observation
        observation = self._get_observation()

        # Reward is +1 for surviving a step
        reward = 1

        # Check if the game is over (e.g., predator dies or some end condition is met)
        if len(self.predators) == 0:
            done = True
        else:
            done = False  # You'll need to implement logic to set this appropriately

        info = {}  # Additional data, not used here but required by Gym's interface
        truncated = done
        return observation, reward, done, truncated, info

    def reset(self, seed=None, options=None):
        # Reset the environment to an initial state
        # Reinitialize boids, predators, etc.
        # Return the initial observation
        self.boids = [create_boid(random.randint(0, self.width), random.randint(0, self.height), self.screen) for _ in range(self.starting_boids)]
        self.predators = [create_predator(random.randint(0, self.width), random.randint(0, self.height), self.screen) for _ in range(self.starting_predators)]  # Reset or reinitialize predators
        self.predator = self.predators[0]

        return self._get_observation(), {}

    def render(self, mode='human'):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                return
        if mode == 'human':
            self.screen.fill((0, 0, 0))
            
            for boid in self.boids:
                boid.show(self.screen)
            for predator in self.predators:
                predator.show(self.screen)

        #### Stats Display Logic #####
        # Display the count of boids and predators
        boid_count = len(self.boids)
        predator_count = len(self.predators)
        boid_count_text = self.font.render(f'Boids: {boid_count}', True, (255, 255, 255))
        predator_count_text = self.font.render(f'Predators: {predator_count}', True, (255, 255, 255))

        # Display the text on the screen at the top-left corner
        self.screen.blit(boid_count_text, (10, 10))
        self.screen.blit(predator_count_text, (10, 30))
        pygame.display.flip()
        self.clock.tick(self.metadata['render_fps'])

    def close(self):
        pygame.quit()

    def _get_observation(self):
        # Compile the observation data from the positions and velocities of boids and predators
        # This should return a flat array containing all position and velocity data
        observation = []
        for boid in self.boids:
            observation.append([boid.position[0], boid.position[1], boid.velocity[0], boid.velocity[1]])
        for predator in self.predators:
            observation.append([predator.position[0], predator.position[1], predator.velocity[0], predator.velocity[1]])
        # Fill the rest of the observation array with zeros if necessary
        while len(observation) < self.max_objects:
            observation.append([0, 0, 0, 0])
        return np.array(observation, dtype=np.float32)
    
    def _update_game_state(self):
        # This function replaces the main loop logic for updating game objects in the Gym environment

        # First, update predators
        for predator in self.predators:
            # Check if the predator is still alive (assuming an `update` method exists that returns a boolean)
            alive = predator.update()
            if not alive:
                self.predators.remove(predator)
                continue

            # Check if the predator eats any boids
            if predator.eat(self.boids):
                # Implement logic for what happens when a predator eats a boid
                pass

            # Calculate and apply hunting force
            hunt_force = predator.hunt(self.boids)
            predator.velocity += hunt_force
            # Update the predator again, for example, to decrease its size over time
            predator.update()

        # Then, update boids
        for boid in self.boids:
            # Apply flocking behavior
            boid.apply_flocking(self.boids)
            # Flee from predators
            for predator in self.predators:
                flee_force = boid.flee(predator.position)
                boid.velocity += flee_force
            # Update boid's position and other properties
            boid.update()
