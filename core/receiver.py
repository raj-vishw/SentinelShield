from core.inspector import inspect_request

class Request:
    def __init__(self, ip, method, path, params, headers=None, body="", user_agent=""):
        self.ip = ip
        self.method = method
        self.path = path
        self.params = params
        self.headers = headers or {}
        self.body = body
        self.user_agent = user_agent

def receive_request(request):
    print("[Receiver] Request received from", request.ip)

    return inspect_request(request)
