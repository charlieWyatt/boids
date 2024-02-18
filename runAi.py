# from gym.envs.registration import register
# print("Registering environment...")
# register(
#     id='PredatorEnv-v0',
#     entry_point='ai.PredatorEnv:PredatorEnv',
# )
# print("Environment registered.")


import gymnasium as gym
from ai.PredatorEnv import PredatorEnv
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env
import numpy as np

def main():
    # Create an instance of your environment using make_vec_env
    # env = gym.make('PredatorEnv-v0')
    # print("made with gym")
    # env = PredatorEnv()
    # check_env(env)
    env = make_vec_env(lambda: PredatorEnv(render_mode='human'), n_envs=1)

    # action = np.random.uniform(low=-1, high=1, size=2)
    # obs = env.reset()
    # print(action)
    # obs, rewards, dones, info = env.step(action)
    # exit()
    # print("made with stable_baselines3")

    # model = PPO("MlpPolicy", env, verbose=1)
    # # # model = PPO.load("ppo_predatorenv", env, verbose=1)

    # # Train the model
    # print("Starting training...")
    # model.learn(total_timesteps=1000000)
    # print("Training completed.")

    # # Save the model
    # model.save("ppo_predatorenv")
    # print("Model saved.")

    # Demonstrate loading and using the model
    model = PPO.load("ppo_predatorenv")

    obs = env.reset()
    total_reward = 0
    for _ in range(1000):
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, dones, info = env.step(action)
        env.render()
        total_reward += rewards

        if dones:
            print(f"Total reward: {total_reward}")
            total_reward = 0
            obs = env.reset()

    env.close()

if __name__ == '__main__':
    main()