import game

from mpi4py import MPI

def worker():
    comm = MPI.COMM_WORLD
    myid = comm.Get_rank()

    unused = None
    agents = comm.bcast(unused, root=0)

    while True:
        packet = comm.recv()
        if packet == False:
            break

        agent_id0, agent_id1 = packet

        winner = game.NormalGame.play(agents[agent_id0], agents[agent_id1])
        comm.send((myid, agent_id0, agent_id1, winner), 0)
