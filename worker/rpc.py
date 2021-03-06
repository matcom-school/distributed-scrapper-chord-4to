from concurrent.futures import ThreadPoolExecutor
import time

# RPC services
Chord_Services = 1
Scrapper_Services = 2
Caching_Services = 3
Finish_Services = 0
Ping_Services = 4

REQUEST = 1
RESPONSE = 2
PING = 0

class RPC:
    def __init__(self, idrpc, sender_func) -> None:
        self.id = idrpc
        self.sender_func = sender_func
        self.services = { }
        self.request_list = []
        self.response_dict = {}
        self.exe = ThreadPoolExecutor()

        self.exe.submit(self.run)
    
    @staticmethod
    def static_request(sender, dest, sender_func, service, func, *params):
        return sender_func(dest, (REQUEST, sender, service, (func, params)))     

    def request(self, dest, funcn, service, *params):
        return self.sender_func(dest, (REQUEST, self.id, service, (funcn, params)))

    def response(self, dest, result, service, funcn, *params):
        return self.sender_func(dest, (RESPONSE, self.id, (service, funcn, params), result))

    def worker_func(self, msg):
        try:
            action, sender, metaMsg, request = msg
            if action == REQUEST: self.request_list.append((sender, metaMsg, request))
            if action == RESPONSE: self.response_dict[str(metaMsg)] = request
        except ValueError:
            print('ErrorMessenger')

    def run(self):
        while True:
            if any(self.request_list):
                sender, service, request = self.request_list.pop()
                self.exe.submit(self.response_service, sender, service, request)
                if service == Finish_Services: break

    def response_service(self, sender, service, request):
        try:
            func, respo = self.services[service][request[0]]
            result = func(*request[1])
        except KeyError: self.response(sender, None, service, request[0], *request[1] )
        except Exception as e:
            print(e.args)
        if respo: self.response(sender, result, service, request[0], *request[1] )

    # if params has tuples blocked method
    def caller_rpc(self, service):
        def func(idn, f, *params, wait = True, timeout = 0):
            if idn == self.id: 
                return f(*params)

            try: name = f.__name__
            except AttributeError: name = f
            key = [service, name, list(params)]
            r = self.request(idn, name, service, *params)
            while True:
                if not r and timeout: raise TimeoutError
                if not wait: break
                try: 
                    result = self.response_dict.pop(str(key))
                    if result is None: 
                        time.sleep(1)
                        r = self.request(idn, name, service, *params)
                    else: return result
                except KeyError: pass
        
        return func