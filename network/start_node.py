from deamon import Deamon
from worker import RPC, Chord_Services, Scrapper_Services
from chord import ChordNode
from scrapper import Scrapper

def start_node(idn, nBit, access_door = None):
    try:
        deamon = Deamon(idn, port_base=9000)
        rpc = RPC(idn, sender_func=deamon.sendTo)
        
        chord = ChordNode(idn, nBit)
        scrapper = Scrapper(idn, chord.finger)

        chord.rpc = rpc.caller_rpc(Chord_Services)
        scrapper.rpc = rpc.caller_rpc(Scrapper_Services)
        deamon.run(func= rpc.worker_func)

        if not access_door is None: 
            chord.init_finger_table(access_door)
            chord.update_others()
        
        print(f'\033[93m@@@@@@@@@@@@@@@@ {idn} finish start @@@@@@@@@@@@@@@@@@@@@@@@\033[0m')
        rpc.services[Chord_Services] = chord.services
        rpc.services[Scrapper_Services] = scrapper.services
        #chord.stabilize()

    except Exception as e:
        print(e.args)