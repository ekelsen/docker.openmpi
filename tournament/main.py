from mpi4py import MPI

import game as Game
import master
import worker

num_agents = 10 # 500-1200 games
# num_agents = 15 # 1200-5000 games
# num_agents = 20 # 100,000 - 1,000,000 games

# experiment to see how much choosing the agent with the highest sigma
# reduces the number of games that need to by played. Implementation
# is not optimal, but gains can be significant especially as the number
# of agents increases
pick_max_sigma = False
stopping_sigma = 1 # all agent's sigmas must fall below this for us to
                   # stop the tournament

if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    myid = comm.Get_rank()
    game = Game.NormalGame()
    if myid == 0:
        # mimics the case where the master has all the agents, depending
        # on how they are stored, it may make more sense to load them in
        # every worker...not enough info in the assignment to know which
        # makes more sense
        agents = [Game.NormalAgent(i, 3) for i in range(num_agents)]
        master.master(agents, stopping_sigma, pick_max_sigma)
    else:
        worker.worker(game)
