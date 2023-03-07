import numpy as np
import pandas as pd
import gymnasium as gym
import math
import random

from gymnasium.spaces import Discrete, Box
from throw import Throw


class GameEnvironment(gym.Env):

    ACTIONS_SPACE_DICT = {'Pass': 0, 'Dump': 1, 'Dish': 2, 'Swing': 3, 'Huck': 4}
    ACTIONS_SPACE_INVERSE_DICT = {0: 'Pass', 1: 'Dump', 2: 'Dish', 3: 'Swing', 4: 'Huck'}
    OBSERVATIONS_SPACE_DICT = {'Completed': 0, 'Throwaway': 1, 'First': 2}

    def __init__(self, df_throws):
        self.df_throws = df_throws

        self.action_space = Discrete(len(self.ACTIONS_SPACE_DICT))
        self.observation_space = Discrete(len(self.OBSERVATIONS_SPACE_DICT))
        self.reward = 0
        self.done = False
        self.state = self.OBSERVATIONS_SPACE_DICT.get('First')

        self.x_field, self.y_field = self._reset_disc_position()
        self.throw_probability_dict = self._init_throw_probability_dict()

    def reset(self):
        self.state = self.OBSERVATIONS_SPACE_DICT.get('First')
        self.reward = 0
        self.done = False
        self.x_field, self.y_field = self._reset_disc_position()
        return self.state

    def step(self, action):
        # calculating if throw was completed or throwaway + disc position if sucess
        if self._is_throw_completed(action):
            # update disc position
            self._update_disc_postion(action)

            # check if disc is inside field
            if self._is_disc_inside_field():
                self.reward += 1 
            else: 
                self.done = True

            # check if point is won
            if self._is_point_win():
                self.reward += 100
                self.done = True

        else:
            self.done = True
            self.reward -= 50

        # 
        info = {}

        return self.state, self.reward, self.done, info
        
    def render(self): # visualize code
        pass

    def _is_point_win(self):
        """ 
        check if point is won: check if disc is in endzone
        """
        if self.y_field > 80:
            return True
        return False
        

    def _is_disc_inside_field(self):
        """ 
        Return true if disc is inside field else false
        """
        # check x
        if self.x_field > 25 or self.x_field < -25:
            return False

        # check y
        if self.y_field > 100 or self.y_field < -20:
            return False

        return True


    def _update_disc_postion(self, action): 
        #  if ACTIONS_SPACE_DICT.get(action)
        x_throw, y_throw = self.throw_probability_dict[action].get_throw_relative_position(self.x_field, self.y_field)
        self.x_field += x_throw
        self.y_field += y_throw


    def _is_throw_completed(self, action):
        """ 
        Check if throw is completed: throw success + within field
        """
        threshold = self.throw_probability_dict[action].get_throw_success_probability(self.x_field, self.y_field)
        proba = random.random()
        if proba < threshold:
            return True

        return False


    def _reset_disc_position(self): 
        """ 
        Initialize disc position 
        
        AUDL field Dimension: 
        - length: 80 yards with 20 yard endzone
        - width: 53 1/3
        """
        y = round(random.uniform(-20, 30), 3)
        x = round(random.uniform(-25, 25))
        return x, y

    def _init_throw_probability_dict(self):
        """ 
        proba_dict = {'Pass': throw.field_probability}
        """
        proba_dict = {}
        for throw_type in self.ACTIONS_SPACE_DICT.keys():
            throw = Throw(self.df_throws, throw_type)
            proba_dict[throw_type] = throw

        return proba_dict


#  -----------------------------------------------------------------------------

def test_environment():
    df_throws = pd.read_csv('~/Projects/tmp/AUDL-Dashboard/data/royal_2022.csv')
    env = GameEnvironment(df_throws)
    #  print(env.throw_probability_dict['Pass'].field_probability)

def test_naive_episode():
    df_throws = pd.read_csv('~/Projects/tmp/AUDL-Dashboard/data/royal_2022.csv')
    env = GameEnvironment(df_throws)
    num_steps = 20
    done = False
    score = 0

    state = env.reset()
    for episode in range(num_steps):
        action = env.action_space.sample()
        action_name = env.ACTIONS_SPACE_INVERSE_DICT.get(action)
        n_state, reward, done, info = env.step(action_name)
        score += reward

        if done: 
            env.reset()

        print('Episode: {} Score: {}'.format(episode, score))

    env.close()

#  -----------------------------------------------------------------------------

def main():
    #  test_environment()
    test_naive_episode()

if __name__ == "__main__":
    main()
