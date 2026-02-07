BLOCK_THRESHOLD = 60
LOG_THRESHOLD = 30


def decide(correlation_output):

    score = correlation_output["score"]

    if score >= BLOCK_THRESHOLD:
        return "BLOCK"

    if score >= LOG_THRESHOLD:
        return "LOG"

    return "ALLOW"
