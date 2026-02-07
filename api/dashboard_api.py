import json
from flask import Blueprint, jsonify

dashboard_api = Blueprint("dashboard_api", __name__)

LOG_FILE = "data/logs.json"

def read_logs():
    logs = []
    try:
        with open(LOG_FILE) as f:
            for line in f:
                logs.append(json.loads(line))
    except FileNotFoundError:
        pass
    return logs


@dashboard_api.route("/api/events")
def events():
    return jsonify(read_logs()[-50:])


@dashboard_api.route("/api/stats")
def stats():
    logs = read_logs()

    total = len(logs)
    blocked = len([l for l in logs if l["action"] == "BLOCK"])
    allowed = len([l for l in logs if l["action"] == "ALLOW"])
    highrisk = len([l for l in logs if l["score"] >= 60])

    return jsonify({
        "totalRequests": total,
        "blocked": blocked,
        "allowed": allowed,
        "highRisk": highrisk
    })
