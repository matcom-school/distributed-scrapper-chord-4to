from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import  ThreadingMixIn
from .net_manager import NetManager
from scrapper import Color, Parser

def generedServer(manager : NetManager):    
    class Handler(SimpleHTTPRequestHandler):
        seach_param = '?seach='
        def do_GET(self):
            if self.seach_param in self.path:
                url = self.path[(self.path.index(self.seach_param) + len(self.seach_param)): ]
                url = url.replace('%3A', ":")
                url = url.replace('%2F', "/")
                url = url.replace('%20', " ")
                state, html = manager.routing(url)
                
                if state == 200:
                    color = Color()
                    parser = Parser(html)
                    html = parser.Main(color)
                    html = html.replace('[a]', '<a>')
                    html = html.replace('[/a]', '</a>')

                    html = html.replace('[g]', "<span class='green' >")
                    html = html.replace('[/g]', '</span>')

                    html = html.replace('[gr]', "<span class='gray' >")
                    html = html.replace('[/gr]', '</span>')

                    html = html.replace('[r]', "<span class='red' >")
                    html = html.replace('[/r]', '</span>')

                    html = html.replace('[b]', "<span class='blue' >")
                    html = html.replace('[/b]', '</span>')

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode() )
 
            else:
                SimpleHTTPRequestHandler.do_GET(self)

        

    class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
        pass


    return Handler, ThreadedHTTPServer