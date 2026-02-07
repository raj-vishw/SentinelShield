import json
import re

SIGNATURE_FILE = "data/signature.json"

def load_signatures():
    with open(SIGNATURE_FILE, "r") as f:
        return json.load(f)

SIGNATURE_DB = load_signatures()

def normalize_request(request):
    values = "".join(str(v) for v in request.params.values())
    data = request.path + values + request.body
    return data

def signature_check(request):

    data = normalize_request(request)

    for attack_type, patterns in SIGNATURE_DB.items():
        for pattern in patterns:
            if re.search(pattern, data, re.IGNORECASE):
                print(f"[Signature] Detected {attack_type}")
                return attack_type

    return None
