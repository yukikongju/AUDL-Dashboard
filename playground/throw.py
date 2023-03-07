import pandas as pd
import numpy as np
import random
import os

#  ---------------------------------------------------------------------------

def generate_normal_values(mean, std, n):
    """ 
    Generate n samples using gaussian distribution 
    """
    return round(np.random.normal(loc=mean, scale=std, size=n), 3)


class Throw(object):

    FIELD_WIDTH = 55 # range: (-27.5, 27.5)
    FIELD_LENGTH = 120 # range: (-20, 100)
    RECTANGLE_YARDS_X, RECTANGLE_YARDS_Y = 5, 5 
    EPSILON = 0.05

    def __init__(self, df_throws, throw_name):
        self.throw_name = throw_name
        self.dataframe = self._init_dataframe(df_throws)
        self.field_probability = self._compute_field_probability()
        
    def _init_dataframe(self, df_throws): 
        return df_throws[df_throws['throw_type'] == self.throw_name]

    def _compute_field_probability(self, k=15):
        """ 
        Compute throw success probability for each position on the field

        field_probability: matrix[][]
            #  field_proba[i, j] = {'proba': , 'mean':, 'var':}
            field_proba[i, j] = (proba, mean_x, mean_y, std_x, std_y)
        """
        # init field rectangle
        field_probability = np.array([[0 for _ in range(0, self.FIELD_LENGTH // self.RECTANGLE_YARDS_X)] for _ in range(0, self.FIELD_WIDTH // self.RECTANGLE_YARDS_Y)], dtype=object)

        for x in range(0, self.FIELD_WIDTH // self.RECTANGLE_YARDS_X):
            for y in range(0, self.FIELD_LENGTH // self.RECTANGLE_YARDS_Y):
                mid_x = x * self.RECTANGLE_YARDS_X + self.RECTANGLE_YARDS_X // 2
                mid_y = y * self.RECTANGLE_YARDS_Y + self.RECTANGLE_YARDS_Y // 2
                mid_point = np.array((mid_x, mid_y))

                # compute distance 
                df_distances = self.dataframe.copy()
                df_distances['dist'] = self.dataframe.apply(lambda row: np.linalg.norm(np.array((row.x_field, row.y_field))-mid_point), axis=1)
                df_distances.sort_values('dist', ignore_index = True, inplace = True)
                df_distances = df_distances.head(k)

                # compute proba, mean, variance
                proba = round(len(df_distances[df_distances['throw_outcome'] == 'Completed']) / k, 3)
                mean_x = df_distances['x'].mean(skipna=True)
                mean_y = df_distances['y'].mean(skipna=True)
                std_x = df_distances['x'].std(skipna=True)
                std_y = df_distances['y'].std(skipna=True)
                field_probability[x][y] = (proba, mean_x, mean_y, std_x, std_y)

        return field_probability

    def get_throw_success_probability(self, x_field, y_field):
        """ 
        Get Throw success probability based on field position with luck factor
        """
        i = int((x_field + self.FIELD_WIDTH // 2) // self.RECTANGLE_YARDS_X)
        j = int((y_field + 20.0) // self.RECTANGLE_YARDS_Y)
        
        proba, _, _, _, _ = self.field_probability[i, j]
        luck_factor = random.uniform(0, self.EPSILON)
        proba = min(1.0, proba + luck_factor)

        return proba

    def get_throw_relative_position(self, x_field, y_field):
        """ 
        Given thrower field position, compute throw relative distance. assume
        that the throw is succesful
        """
        i = int((x_field + self.FIELD_WIDTH // 2) // self.RECTANGLE_YARDS_X)
        j = int((y_field + 20.0) // self.RECTANGLE_YARDS_Y)

        proba, mean_x, mean_y, std_x, std_y = self.field_probability[i, j]
        x_throw = generate_normal_values(mean_x, std_x, 1)[0]
        y_throw = generate_normal_values(mean_y, std_y, 1)[0]

        return x_throw, y_throw
        

#  ---------------------------------------------------------------------------

def test_throw_class():
    df_throws = pd.read_csv('~/Projects/tmp/AUDL-Dashboard/data/royal_2022.csv')
    throw = Throw(df_throws, 'Pass')

    #  print(throw.field_probability)
    #  print(throw.get_throw_success_probability(-11.0, -5.0))
    #  print(throw.get_throw_success_probability(20.0, -15.0))
    print(throw.get_throw_relative_position(20.0, -15.0))
    
#  ---------------------------------------------------------------------------

def main():
    test_throw_class()
    

if __name__ == "__main__":
    main()
