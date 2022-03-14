from deamon import Deamon
from worker import RPC, Chord_Services, Scrapper_Services
from chord import ChordNode
from scrapper import Scrapper, Color
import time, random

def start_node(idn, nBit, access_door = None):
    try:
        deamon = Deamon(idn, port_base=9000)
        rpc = RPC(idn, sender_func=deamon.sendTo)
        
        chord = ChordNode(idn, nBit)
        scrapper = Scrapper(idn)

        chord.rpc = rpc.caller_rpc(Chord_Services)
        scrapper.rpc = rpc.caller_rpc(Scrapper_Services)
        deamon.run(func= rpc.worker_func)

        if not access_door is None: 
            chord.init_finger_table(access_door)
            chord.update_others()
        
        print(Color.yellow(f'.............. {idn} finish start ......................'))
        rpc.services[Chord_Services] = chord.services
        rpc.services[Scrapper_Services] = scrapper.services
        
        while True:
            time.sleep(random.randint(10, 20))
            print(f'.........{idn} stabilize .............')
            chord.succ_stabilize()
            time.sleep(2)
            chord.fix_fingers()
            time.sleep(2)
            list_ = scrapper.hashs()
            key, dest = chord.finger.checking_property(list(list_))
            if not key is None: scrapper.replace(key, dest)

    except Exception as e:
        print(e.args)