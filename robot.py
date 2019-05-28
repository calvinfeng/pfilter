import math
import random


world_size = 100.0
landmarks = [
    [20.0, 20.0],
    [80.0, 80.0],
    [20.0, 80.0],
    [80.0, 20.0]
]


class Robot:
    def __init__(self):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.theta = random.random() * 2.0 * math.pi
        self.forward_noise = 0.0
        self.turn_noise = 0.0
        self.sense_noise = 0.0

    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise ValueError('x coordinate out of bound')
        if new_y < 0 or new_y >= world_size:
            raise ValueError('y coordinate out of bound')
        if new_orientation < 0 or new_orientation >= 2 * math.pi:
            raise ValueError('orientation must be in [0..2pi]')
        self.x = float(new_x)
        self.y = float(new_y)
        self.theta = float(new_orientation)

    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        self.forward_noise = float(new_f_noise)
        self.turn_noise = float(new_t_noise)
        self.sense_noise = float(new_s_noise)

    def sense(self):
        measurements = []
        for i in range(len(landmarks)):
            dist = math.sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            measurements.append(dist)
        return measurements

    def move(self, turn, forward):
        if forward < 0:
            raise ValueError('robot cant move backwards')

        # Add noises to movements
        orientation = self.theta + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * math.pi

        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (math.cos(orientation) * dist)
        y = self.y + (math.sin(orientation) * dist)

        # Cyclic truncate
        x %= world_size
        y %= world_size

        new_particle = Robot()
        new_particle.set(x, y, orientation)
        new_particle.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)

        return new_particle

    def gaussian(self, mu, sigma, x):
        """
        Calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        """
        return math.exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / math.sqrt(2.0 * math.pi * (sigma ** 2))

    def score(self, measurement):
        """
        Calculates score of a particle using Gaussian probability
        """
        score = 1.0
        for i in range(len(landmarks)):
            dist = math.sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            score *= self.gaussian(dist, self.sense_noise, measurement[i])
        return score

    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.theta))
