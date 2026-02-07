from engine.detection_engine import run_detection 
from core.normalizer import normalize

WHITELIST_PATHS = [
    "/api/",
    "/favicon.ico"
]


def inspect_request(request):
    for safe in WHITELIST_PATHS:
        if request.path.startswith(safe):
            return {
                "results": {"signature": None, "behavior": [], "heuristic": False},
                "score": 0,
                "reasons": []
            }

    print("[Inspector] Inspecting request")

    request.path = normalize(request.path)

    normalized_params = {}
    for k, v in request.params.items():
        normalized_params[k] = normalize(str(v))
    request.params = normalized_params

    normalized_headers = {}
    for k, v in request.headers.items():
        normalized_headers[k.lower()] = normalize(str(v))
    request.headers = normalized_headers

    request.body = normalize(request.body)

    return run_detection(request)