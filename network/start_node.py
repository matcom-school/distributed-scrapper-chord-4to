from deamon import Deamon
from worker import RPC, Chord_Services
from chord import ChordNode
from concurrent.futures import ThreadPoolExecutor

def start_node(idn, nBit, access_door = None):
    try:
        exe = ThreadPoolExecutor()
        deamon = Deamon(idn, port_base=9000)
        rpc = RPC(idn, sender_func=deamon.sendTo)
        chord = ChordNode(idn, nBit)
        
        chord.rpc = rpc.caller_rpc(Chord_Services)
        deamon.run(func= rpc.worker_func)

        if not access_door is None: 
            chord.init_finger_table(access_door)
            chord.update_others()
        
        print(f'\033[93m@@@@@@@@@@@@@@@@ {idn} finish start @@@@@@@@@@@@@@@@@@@@@@@@\033[0m')
        rpc.services[Chord_Services] = chord.services
        chord.stabilize()

    except Exception as e:
        print(e.args)