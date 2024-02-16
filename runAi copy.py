from gym.envs.registration import register
import sys
register(
    id='PredatorEnv-v0',
    entry_point='ai.PredatorEnv:PredatorEnv',
)

import gym

def main():
    # Create an instance of your environment
    env = gym.make('PredatorEnv-v0')

    # Reset the environment to start a new episode
    observation = env.reset()

    done = False
    total_reward = 0

    # Run one episode
    while not done:
        # Render the environment to the screen
        env.render()

        # Sample a random action from the action space of the environment
        action = env.action_space.sample()

        # Execute the action
        observation, reward, done, info = env.step(action)
        total_reward += reward

    print(f"Episode finished with total reward: {total_reward}")

    # Close the environment
    env.close()

if __name__ == '__main__':
    main()