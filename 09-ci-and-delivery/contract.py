"""A small interface contract for a two-score model response."""
import math

LABELS = ('odd', 'at_least_five')

def validate(payload):
    if not isinstance(payload, dict) or set(payload) != set(LABELS):
        raise ValueError('expected exactly the two documented labels')
    for value in payload.values():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError('scores must be finite numbers between zero and one')
    return payload
