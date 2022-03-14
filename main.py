from network import generedServer, NetManager, start_node
from worker import RPC, Chord_Services, Scrapper_Services
from deamon import Deamon
from concurrent.futures import ThreadPoolExecutor
from scrapper import Color
import time

port = 9000
nBits = 5

exe = ThreadPoolExecutor()

d = Deamon(-1, port_base=port)
rpc = RPC(-1, d.sendTo)
d.run(func= rpc.worker_func)
nm = NetManager(nBits, rpc.caller_rpc(Chord_Services), rpc.caller_rpc(Scrapper_Services), exe)
access = None
for i in range(nBits):
    access = nm.run(access)
    time.sleep(1)

Handler, ThreadedHTTPServer = generedServer(nm)
print(Color.blueBack(f'.... Server ready open http://localhost:{port + 100} ........'))
server = ThreadedHTTPServer(('', port + 100), Handler)
server.serve_forever()