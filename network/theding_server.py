from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import  ThreadingMixIn
from bs4 import BeautifulSoup
from .net_manager import NetManager

def generedServer(manager : NetManager):    
    class Handler(SimpleHTTPRequestHandler):
        seach_param = '?seach='
        def do_GET(self):
            if self.seach_param in self.path:
                url = self.path[(self.path.index(self.seach_param) + len(self.seach_param)): ]
                url = url.replace('%3A', ":")
                url = url.replace('%2F', "/")
                url = url.replace('%20', " ")
                html = manager.routing(url)
      
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode() )
 
            else:
                SimpleHTTPRequestHandler.do_GET(self)

        

    class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
        pass


    return Handler, ThreadedHTTPServer