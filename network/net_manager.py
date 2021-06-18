import random
from . import start_node
from scrapper import url_hashing
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

class NetManager:
    def __init__(self, nBits, chord_rpc, scrapper_rpc, exe : ThreadPoolExecutor) -> None:
        self.nBits = nBits
        self.max = pow(2, nBits)
        self.freeIds = [i for i in range(self.max)]
        self.activedIds = []
        self.chord = chord_rpc
        self.scrapper = scrapper_rpc
        self.exe = exe

    def run(self, access= None):
        i = random.choice(self.freeIds)
        self.freeIds.remove(i)
        self.activedIds.append(i)
        self.exe.submit(start_node, i, self.nBits, access)
        return i

    def routing(self, url, scale = True):
        urll, hsh = url_hashing(url, self.max)       
        index = self.select(hsh)
        if self.scrapper(index, 'beFree') or self.scrapper(index, 'inCache', urll):
            boool, html = self.scrapper(index, 'get', urll, hsh, index)
        else: boool, html = self.submit(urll, hsh, index)

        if not boool: return 400, f'BadRequest: path {urll} not found'
        if scale: self.exe.submit( self.url_recolected_and_scrapper, html, urll )
        
        return 200, html

    def url_recolected_and_scrapper(self, html, url):
        soup = BeautifulSoup(html, 'html.parser')
        domain = url.split('?')[0].split('/')
        domain = domain[0] + '//' + domain[2]

        for a in soup.find_all('a'):
            link = a.get('href')
            if domain in link: 
                self.routing( link, False) 
        
    def submit(self, url, hsh, index):
        for i in self.activedIds:
            if i == index: continue
            if self.scrapper(i, 'beFree'):
                return self.scrapper(i, 'get', url, hsh, index)
        
        i = self.run(index)
        return self.scrapper(i, 'get', url, hsh, index)

    def select(self, index):
        i = self.activedIds[0]

        while True:
            try: 
                j = self.chord(i, 'find', index, timeout= 5)
                if i == j: return j
            except TimeoutError: j = self.down_notify(i)
                
            i = j
        

    def down_notify(self, i):
        self.activedIds.remove(i)
        self.freeIds.append(i)
        
        for j in self.activedIds:
            try: self.chord(j, 'down', i, timeout= 5)
            except TimeoutError: 
                self.activedIds.remove(j)
                self.freeIds.append(j)

        if not any(self.activedIds): return self.run()
        return self.activedIds[0]