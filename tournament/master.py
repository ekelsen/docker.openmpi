import random

import numpy as np

from mpi4py import MPI
from trueskill import Rating, rate_1vs1

def master(agents, stopping_sigma = 1, pick_max_sigma = False):
    comm = MPI.COMM_WORLD
    myid = comm.Get_rank()
    num_workers = comm.Get_size() - 1
    num_agents = len(agents)

    agent_ratings = [ [Rating(), agents[i], i] for i in range(num_agents)]
    agent_ratings_by_sigma = sorted(agent_ratings, key = lambda val: val[0].sigma, reverse=True)

    # first we have to broadcast the agents to the workers
    comm.bcast(agents, root=0)

    # give every worker its initial assignment
    for i in range(num_workers):
        agentid0, agentid1 = np.random.choice(num_agents, 2, replace=False)
        comm.send((agentid0, agentid1), i + 1)

    games_played = 0
    while True:
        if pick_max_sigma:
            if agent_ratings_by_sigma[0][0].sigma < stopping_sigma:
                break
        elif games_played % (10 * num_agents) == 0:
            max_sigma = max([agent_ratings[i][0].sigma for i in range(num_agents)])
            if max_sigma < stopping_sigma:
                break

        # get the next message (can be from any worker)
        send_id, agentid0, agentid1, winner = comm.recv()

        if winner == 0:
            agent_ratings[agentid0][0], agent_ratings[agentid1][0] = rate_1vs1(agent_ratings[agentid0][0], agent_ratings[agentid1][0])
        elif winner == 1:
            agent_ratings[agentid1][0], agent_ratings[agentid0][0] = rate_1vs1(agent_ratings[agentid1][0], agent_ratings[agentid0][0])
        else: # draw
            agent_ratings[agentid1][0], agent_ratings[agentid0][0] = rate_1vs1(agent_ratings[agentid1][0], agent_ratings[agentid0][0], drawn=True)

        # send new work back to the same worker
        # don't play an agent against itself
        if pick_max_sigma:
            # a heap might be better, or a heap plus a sortedlist if we want to
            # pick the max sigma and then choose an opponent with a similar mu
            # using this implementation to experiment with how many fewer games
            # better selection requires.
            # Note that this sort is not likely to bad as bad as it first appears
            # as long as the number of agents remains < few hundred
            # The list will be almost sorted, so timsort will be close to one pass
            # The list should also stay in L2.
            agent_ratings_by_sigma = sorted(agent_ratings_by_sigma, key = lambda val: val[0].sigma, reverse=True)
            agentid0 = agent_ratings_by_sigma[0][2]
            agentid1 = agent_ratings_by_sigma[random.randint(1, num_agents-1)][2]
        else:
            agentid0, agentid1 = np.random.choice(num_agents, 2, replace=False)

        comm.send((agentid0, agentid1), send_id)

        games_played += 1

    # tell the workers to finish
    for i in range(num_workers):
        send_id, _, _, _ = comm.recv()

        comm.send(False, send_id)

    print(games_played)
    for i in range(num_agents):
        print(agent_ratings[i])
