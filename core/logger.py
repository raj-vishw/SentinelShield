import json
from datetime import datetime

LOG_FILE = "data/logs.json"


def log_event(request, correlation_output, action):

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "ip": request.ip,
        "method": request.method,
        "path": request.path,
        "score": correlation_output["score"],
        "reasons": correlation_output["reasons"],
        "action": action
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print("[Logger] Event Logged")
    