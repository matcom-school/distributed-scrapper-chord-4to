from network import start_node
import sys, time, os
from concurrent.futures import ThreadPoolExecutor
from random import choice

m = int(sys.argv[1])
n = int(sys.argv[2])

MAXRM = pow(2, m)
freeIdList = [ i for i in range(MAXRM) ]

nodes = [11, 3, 20, 26, 31]
accDoor = [None, 11, 3, 20, 26, 31]
for _ in range(n):
    newId = choice(freeIdList)
    freeIdList.remove(newId)
    nodes.append( newId )
    accDoor.append(newId)

#exe = ThreadPoolExecutor()

#for nod in nodes:
#    exe.submit(server_run, nod)
exe = ThreadPoolExecutor()

print("Connected .....")
for nod, ad in zip(nodes, accDoor):
	exe.submit(start_node, nod, m, ad)
	time.sleep(0.5)


time.sleep(1000)
#exe.submit(client_run, chan)
#exe.shutdown(True)
