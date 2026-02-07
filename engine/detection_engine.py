from detectors.signature import signature_check
from detectors.behavior import behavior_check
from detectors.heuristic import heuristic_check
from engine.correlation_engine import calculate_risk


def run_detection(request, previous_action="ALLOW"):

    sig = signature_check(request)
    beh = behavior_check(request, previous_action)
    heur = heuristic_check(request)

    results = {
        "signature": sig,
        "behavior": beh,
        "heuristic": heur
    }

    score, reasons = calculate_risk(results)

    return {
        "results": results,
        "score": score,
        "reasons": reasons
    }
