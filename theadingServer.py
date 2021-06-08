from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import  ThreadingMixIn
from bs4 import BeautifulSoup
import json

class Color:
    @staticmethod
    def tags(subs):
        return f'<span>{subs}</span>'
    
    @staticmethod
    def endline():
        return '<br/>'

def scrapper(url):
    return '<head></head>'
    
def compose(html):
    return f'<{ Color.tags("heap") }>{Color.endline()}   <{Color.tags("heap")}/>'



class Handler(SimpleHTTPRequestHandler):
    seach_param = '?seach='
    def do_GET(self):
        if self.seach_param in self.path:
            url = self.path[(self.path.index(self.seach_param) + len(self.seach_param)): ]
            html = scrapper(url)
            response = compose(html)

            print(response)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps([response]).encode() )
 
            
           
        else:
            SimpleHTTPRequestHandler.do_GET(self)

        

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

print('Server listening on port 9000 ........')
server = ThreadedHTTPServer(('', 9000), Handler)
server.serve_forever()