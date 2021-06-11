import zmq
from concurrent.futures import ThreadPoolExecutor
from zmq.error import ZMQError

class DeamonZmq:
    def __init__(self, idn, host= 'localhost',port_base= 10000) -> None:
        self.id = idn
        self.port = port_base + idn
        self.host = host
        
        self.context = zmq.Context()
        self.exe = ThreadPoolExecutor()
        
    def run(self, func=print):
        self.exe.submit(self.recv, func)

    def recv(self, func):
        rep = self.context.socket(zmq.REP)
        rep.bind("tcp://*:%s" % str(self.port))
        print(f'Deamon listen to {self.host}:{self.port}')

        self.bool = True
        while self.bool:
            try:
                data = rep.recv_json(flags= zmq.NOBLOCK)
                self.exe.submit(func, data)
                rep.send_json(('ok'))
            except ZMQError:
                pass
        
        rep.close()

    def sendTo(self, destination, message, time = 2000):
        req = self.context.socket(zmq.REQ)
        req.setsockopt(zmq.RCVTIMEO, time)
        port = str(destination + self.port - self.id)
        req.connect(f'tcp://{self.host}:{port}')
        req.send_json(message)
        try:
            req.recv_json()
            result = True
        except ZMQError: result = False
        req.disconnect(f'tcp://{self.host}:{port}')
        req.close()
        return result

    def close(self):
        self.bool = False
        self.context.term()
        self.exe.shutdown(True)
        print('closed')