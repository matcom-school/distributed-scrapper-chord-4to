from .finger_table import FingerTable
import time, random

class ChordNode:
    def __init__(self, idn, nBits) -> None:
        self.id = idn
        self.finger = FingerTable(idn, nBits)
        self.rpc = None

    @property
    def services(self):
        return {
            self.successor.__name__ : (self.successor, True),
            self.predecessor.__name__: (self.predecessor, True),
            self.find_successor.__name__: (self.find_successor, True),
            self.closest_preceding_finger.__name__: (self.closest_preceding_finger, True),   
            self.update_finger_table.__name__: (self.update_finger_table, False),
            self.finger_table.__name__: (self.finger_table, False),
            self.notify.__name__: (self.notify, False),
            'find' : (self.finger.find_key, True),
            'down' : (self.finger.down, False),
        }

    def finger_table(self):
        self.finger.print()

    def successor(self):
        return self.finger.nodes[1]
    

    def predecessor(self):
        return self.finger.nodes[0]

###########################################################################################################
    def find_successor(self, idn):
        n = self.find_predecessor(idn)
        return self.rpc(n, self.successor)

    def find_predecessor(self, idn):
        n = self.id

        while True:
            nsucc = self.rpc(n, self.successor)
            if self.finger.in_open_closed(key=idn, a=n, b=nsucc): break
            n = self.rpc(n, self.closest_preceding_finger, idn)
        return n
    
    def closest_preceding_finger(self, idn):
        for i in range(self.finger.m):
            j = self.finger.m - i
            if self.finger.in_open_interval(key=self.finger.nodes[j], a=self.id, b=idn):
                return self.finger.nodes[j]
        return self.id

############################################################################################################
    def init_finger_table(self, n):
        self.finger.nodes[1] = self.rpc(n, self.find_successor, self.finger.start[1])
        self.finger.nodes[0] = self.rpc(self.successor(), self.predecessor) 
        self.rpc(self.successor(), self.update_finger_table, self.id, 0, wait = False)
        print(f'{self.id} init_finger_table ................')

        for i in range(1, self.finger.m):
            key = self.finger.start[i+1]
            if self.finger.in_closed_open(key, a=self.id, b=self.finger.nodes[i] ):                
                self.finger.nodes[i+1] = self.finger.nodes[i]
            else:
                #self.finger.nodes[i+1] = self.rpc(n, self.find_successor, self.finger.start[ i+1 ])                
                temp = self.rpc(n, self.find_successor, self.finger.start[ i+1 ])                
                self.finger.set_node(i, temp)
                #if self.finger.in_open_closed(key, a=self.id, b=temp):
                #    self.finger.nodes[i+1] = temp
                #else: self.finger.nodes[i+1] = self.id
        
        print(f'{self.id} init_finger_table .........finsih')
           
    def update_others(self):
        for i in range(1, self.finger.m + 1):
            poww = self.id - pow(2, i-1)
            poww += 0 if poww >= 0 else self.finger.max_index
            p = self.find_predecessor( poww )
            self.rpc(p, self.update_finger_table, self.id, i, wait = False)

    def update_finger_table(self, s, i):
        if i == 0: self.finger.nodes[0] = s
        elif  self.finger.in_closed_open(key=s, a=self.id, b=self.finger.nodes[i]):
            self.finger.set_node(i, s)
            if not self.predecessor() == s: self.rpc(self.predecessor(),self.update_finger_table, s,i, wait = False)
        

######################## stabilize ##########################################################            
    def succ_stabilize(self):
        x = self.rpc(self.successor(), self.predecessor) 
        if self.finger.in_open_interval(x, self.id, self.successor(), False):
            self.finger.nodes[1] = x 
        self.rpc(self.successor(), self.notify, self.id, wait=False)
    
    def notify(self, n):
        if self.finger.in_open_interval(n, self.predecessor(), self.id, False):
            self.finger.nodes[0] = n

    def fix_fingers(self):
        try:
            i = self.finger.get_index()
            obj = self.finger.start[i]  if not self.finger.nodes[i] == self.id else self.finger.succ(self.finger.start[i])
            self.finger.set_node(i, self.find_successor( obj ))
        except IndexError:
            pass
    #def update_others(self):
    #    for i in range(1, self.finger.m + 1):
    #        if not self.finger.nodes[i] == self.id:
    #            self.rpc(self.finger.nodes[i], self.update_finger_table, self.id, i, wait = False)
    #
    #def update_finger_table(self, s, i):
    #    if i == 0: self.finger.nodes[0] = s
    #    else: 
    #        if not self.predecessor() == s: self.rpc(self.predecessor(), self.update_finger_table, s, i, wait = False)
    #        self.finger.update(s)