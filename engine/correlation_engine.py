SCORE_TABLE = {
    "SQL_INJECTION": 40,
    "XSS": 35,
    "COMMAND_INJECTION": 40,
    "LFI": 35,
    "SSRF": 35,

    "BURST": 20,
    "UNIFORM": 15,
    "FAILED_ACTIONS": 25,
    "METHOD_ABUSE": 15,
    "MALICIOUS_UA": 30,

    "HEURISTIC": 10
}

def calculate_risk(detection_results):

    score = 0
    reasons = []

    if detection_results["signature"]:
        attack = detection_results["signature"]
        score += SCORE_TABLE.get(attack, 30)
        reasons.append(attack)

    for signal in detection_results["behavior"]:
        score += SCORE_TABLE.get(signal, 10)
        reasons.append(signal)

    if detection_results["heuristic"]:
        score += SCORE_TABLE["HEURISTIC"]
        reasons.append("HEURISTIC")

    return score, reasons