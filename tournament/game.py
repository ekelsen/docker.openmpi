import random

class Game(object):
    def play(agent0, agent1):
        pass

class Agent(object):
    pass

class NormalAgent(Agent):
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

class NormalGame(Game):
    def play(self, agent0, agent1):
        score0 = random.normalvariate(agent0.mu, agent0.sigma)
        score1 = random.normalvariate(agent1.mu, agent1.sigma)
        if score0 == score1:
            return None
        return int(score0 < score1)
