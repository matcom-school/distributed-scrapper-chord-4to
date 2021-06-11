from deamon import Deamon
from random import choice
from worker import RPC

def explore_network(nBit, port_base=9000):
    d = Deamon(-1, port_base=port_base)
    ports = [ i for i in range(pow(2, nBit))]

    while any(ports):
        print(len(ports), end='\r')
        idp = choice(ports)
        ports.remove(idp)
        if RPC.ping(-1, idp, d.sendTo): return idp

    print("all machines in network is free")
    return None