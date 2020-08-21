from random import Random
from numpy.random import RandomState
from scipy.stats import expon, poisson

class RandomNumberGenerator():

    def __init__(self, seed: float = 12):
        # initialises the seed of the inner random number generators
        self.rand = Random(seed)
        self.randState = RandomState(seed)

    def exponential(self, lbda):
        return expon.rvs(scale = lbda, random_state = self.randState)

    def poisson(self, mu):
        return poisson.rvs(mu = mu, random_state = self.randState)
    
    def randint(self, min, max):
        return self.rand.randint(min, max)
