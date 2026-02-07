from core.receiver import receive_request, Request
from engine.decision_engine import decide
from core.logger import log_event

previous_action = "ALLOW"

request = Request(
    ip="192.168.1.10",
    method="POST",
    path="/login",
    params={},
    headers={"Content-Type": "application/json"},
    body='{"user":"admin","pass": OR 1=1"}',
    user_agent="Mozilla/5.0"
)

correlation_output = receive_request(request)
action = decide(correlation_output)
log_event(request, correlation_output, action)

print("Risk Score:", correlation_output["score"])
print("Reasons:", correlation_output["reasons"])
print("Final Decision:", action)