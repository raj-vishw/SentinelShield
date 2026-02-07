import string

MAX_URL_LENGTH = 100
MAX_PARAM_COUNT = 12
MAX_SPECIAL_RATIO = 0.30

SPECIAL_CHARS = set(string.punctuation)

def special_char_ratio(text):
    if not text:
        return 0
    count = sum( 1 for c in text if c in SPECIAL_CHARS)
    return count / len(text)

def heuristic_check(request):
    if len(request.path) > MAX_URL_LENGTH:
        print("[Heuristic] Long URL Detected")
        return True
    
    if len(request.params) > MAX_PARAM_COUNT:
        print("[Heuristic] Too many parameters")
        return True

    param_values = "".join(str(v) for v in request.params.values())
    combined = request.path + param_values + request.body
    
    ratio = special_char_ratio(combined)

    if ratio > MAX_SPECIAL_RATIO:
        print("[Heuristic] Excessive special characters")
        return True
    return False
