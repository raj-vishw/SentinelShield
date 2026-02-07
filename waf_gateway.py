from flask import Flask, request, Response
import requests
from flask_cors import CORS
import json
BANNED_IP_FILE = "data/banned_ips.json"

from core.inspector import inspect_request
from engine.decision_engine import decide
from core.logger import log_event
from core.receiver import Request

from api.dashboard_api import dashboard_api

app = Flask(__name__)
CORS(app)
app.register_blueprint(dashboard_api)


BACKEND_APP = "http://127.0.0.1:9000"

@app.route("/", defaults={"path": ""}, methods=["GET","POST","PUT","DELETE"])
@app.route("/<path:path>", methods=["GET","POST","PUT","DELETE"])
@app.route("/api/ban_ip", methods=["POST"])
def ban_ip():
    data = request.get_json()
    ip = data.get("ip")

    banned_ips = load_banned_ips()
    banned_ips.add(ip)
    save_banned_ips(banned_ips)

    return {"status": "success", "ip": ip}


def load_banned_ips():
    try:
        with open(BANNED_IP_FILE) as f:
            return set(json.load(f))
    except:
        return set()

def save_banned_ips(ips):
    with open(BANNED_IP_FILE, "w") as f:
        json.dump(list(ips), f)

def gateway(path):

    req = Request(
        ip=request.remote_addr,
        method=request.method,
        path="/" + path,
        params=request.args.to_dict(),
        headers=dict(request.headers),
        body=request.get_data(as_text=True),
        user_agent=request.headers.get("User-Agent","")
    )

    correlation_output = inspect_request(req)
    action = decide(correlation_output)

    log_event(req, correlation_output, action)

    if action == "BLOCK":
        return Response("Blocked by SentinelShield", status=403)

    # Forward to backend app
    backend_response = requests.request(
        method=request.method,
        url=f"{BACKEND_APP}/{path}",
        headers=request.headers,
        data=request.get_data(),
        params=request.args
    )
    banned_ips = load_banned_ips()
    if request.remote_addr in banned_ips:
        return Response("IP banned by SentinelShield", status=403)

    return Response(
        backend_response.content,
        backend_response.status_code
    )

if __name__ == "__main__":
    app.run(port=5000)
