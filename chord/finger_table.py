import random

class FingerTable:
    def __init__(self, idn, nBits) -> None:
        self.n = idn
        self.m = nBits
        self.max_index = pow(2, nBits)
        
        pred = idn - 1 if idn > 0 else self.max_index - 1
        self.start = [ pred ] + [ (idn + pow(2, i)) % self.max_index for i in range(nBits) ]
        self.objetive = [pred] + [ (self.start[i+1] + 1) % self.max_index for i in range(nBits) ]
        
        self.nodes = [ idn for _  in range(nBits + 1)]

    def checking_property(self, list_):
        for key, hsh in list_:
            i = self.find_key(hsh)
            if not i == self.n: return key, i
        
        return None, None
        
    def down(self, i):
        for n in range(len(self.nodes)): 
            if self.nodes[n] == i: self.nodes[n] = self.n 

    def pred(self, a): return a - 1 if a > 0 else self.max_index - 1 
    def succ(self, a): return a + 1 if a < self.max_index else 0 

    def set_node(self, i, s):
        if self.start[i] == self.nodes[i] or (not s == self.start[i] and self.in_open_interval(key=s, a=self.start[i], b=self.nodes[i], circle=False)) :
            self.nodes[i] = s
    
    def in_close_interval(self, key, a, b, circle = True):
        if a == b: return key < self.max_index if circle else key == a 
        if a - 1 == b: return key < self.max_index
        if a < b: return a <= key and key <= b

        return (a <= key and key <= b + self.max_index) or (a <= key + self.max_index and key <= b)
    
    def in_closed_open(self, key, a, b, circle = True): return self.in_close_interval(key, a, self.pred(b), circle)
    
    def in_open_closed(self, key, a, b, circle = True): return self.in_close_interval(key, self.succ(a), b, circle)

    def in_open_interval(self, key, a, b, circle = True): 
        if a == b: return not key == a
        if a < b and b-a == 1 : return False 
        return self.in_close_interval(key, self.succ(a), self.pred(b), circle)


    def get_index(self):
        importan_list = []
        list_ = []  
        for i in range(2, self.m + 1):
            if self.nodes[i] == self.start[i] or self.nodes[i] == self.n : importan_list.append(i)
            if self.nodes[i] == self.objetive[i]: continue

            list_.append(i)

        if any(importan_list): return random.choice(importan_list)
        return random.choice(list_)

    def find_key(self, key):
        if self.in_close_interval(key, self.nodes[0] + 1, self.n): 
            return self.n
        if self.in_close_interval(key, self.n + 1, self.nodes[1]): 
            return self.nodes[1]

        for i in range(1, self.m + 1):
            j = (i+1) % self.m
            if self.in_close_interval(key, self.nodes[i], self.nodes[j]):
                return self.nodes[i]
	
    def print(self):
        print('FT[','%04d'%self.n,']: ',[ '%02d'%s + ': ' + '%04d'%n for s, n in zip(self.start, self.nodes)])