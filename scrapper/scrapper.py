import requests
from requests.models import Response
from .color import Color

class Scrapper:
    def __init__(self, idn):
        self.id = idn
        self.state = True
        self.caching = {}
        self.rpc = None
    
    @property
    def services(self):
        return {
            self.beFree.__name__ : (self.beFree, True),
            self.get.__name__: (self.get, True),
            self.cache.__name__: (self.cache, True),
            self.inCache.__name__: (self.inCache, True),    
        }

    def inCache(self, url): 
        return url in self.caching

    def beFree(self): return self.state
    
    def get(self, url, hsh, index):
        if url in self.caching: 
            print(Color.green(f'{self.id} answer with cache about {url}'))
            return True, self.caching[url][1]

        html = self.download(url, hsh)
        if self.id == index: return self.cache(html, url, hsh)
        return self.rpc(index, self.cache, html, url, hsh)
    
    def download(self,url, hsh):
        print(Color.blue(f'{self.id} download {url} with hash {hsh}'))
        self.state = False
        try: 
            response = requests.get(url)
            print(Color.green(f'{self.id} finish with {url}'))
            self.state = True
            return response._content.decode()
        except requests.ConnectionError: pass
        except requests.exceptions.SSLError: pass
        except Exception as e: print(e.args)
        self.state = True
        print(Color.red(f'{self.id} ERROR with {url}'))
        return False

    def cache(self, result, url, hsh):
        if result:
            self.caching[url] = (hsh, result)
            return True, result
        
        return False, ''
    
    def hashs(self):
        return set([(key, self.caching[key][0]) for key in self.caching])
    
    def replace(self, key, dest):
        try:
            hsh, result = self.caching[key]
            self.rpc(dest, self.cache, result, key, hsh, timeout=5)
            self.caching.pop(key)
        except TimeoutError: pass