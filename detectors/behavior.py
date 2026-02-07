import time
from collections import defaultdict, deque

REQUEST_TIMES = defaultdict(list)          
FAILED_ACTIONS = defaultdict(int)          
RECENT_PATTERNS = defaultdict(lambda: deque(maxlen=5))  

BURST_WINDOW = 2          # seconds
BURST_THRESHOLD = 8

FAILED_LIMIT = 8

UNIFORM_THRESHOLD = 4

ALLOWED_METHODS = ["get", "post"]

MALICIOUS_USER_AGENTS = [
    "sqlmap",
    "nikto",
    "nmap",
    "acunetix",
    # "curl",
    # "python-requests",
    # "wget",
    "masscan"
]

def burst_detection(ip,now):
    REQUEST_TIMES[ip].append(now)
    recent = [t for t in REQUEST_TIMES[ip] if now - t <= BURST_WINDOW]
    return len(recent) > BURST_THRESHOLD

def failed_action_tracking(ip, action):
    if action == "BLOCK":
        FAILED_ACTIONS[ip] += 1
    else:
        FAILED_ACTIONS[ip] = 0
    
    return FAILED_ACTIONS[ip] >= FAILED_LIMIT  

def uniform_request_pattern(ip, request):
    pattern = f"{request.method}:{request.path}:{request.params}"
    RECENT_PATTERNS[ip].append(pattern)

    if len(RECENT_PATTERNS[ip]) < UNIFORM_THRESHOLD:
        return False

    first = RECENT_PATTERNS[ip][0]
    for p in RECENT_PATTERNS[ip]:
        if p!= first:
            return False
    return True


def method_abuse(method):
    return method.lower() not in ALLOWED_METHODS

def malicious_user_agent(user_agent):
    if not user_agent:
        return True

    ua = user_agent.lower()
    for bad in MALICIOUS_USER_AGENTS:
        if bad in ua:
            return True
    
    return False

def behavior_check(request, previous_action="ALLOW"):

    signals = []
    ip = request.ip
    now = time.time()

    if burst_detection(ip, now):
        signals.append("BURST")

    if failed_action_tracking(ip, previous_action):
        signals.append("FAILED_ACTIONS")

    if uniform_request_pattern(ip, request):
        signals.append("UNIFORM")

    if method_abuse(request.method):
        signals.append("METHOD_ABUSE")

    if malicious_user_agent(request.user_agent):
        signals.append("MALICIOUS_UA")

    return signals
