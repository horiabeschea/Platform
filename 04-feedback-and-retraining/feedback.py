"""A small, deliberately synthetic demonstration of split protection."""
import json
from pathlib import Path

PROTECTED = {'test-1', 'test-2'}
BASELINE = [{'id': 'train-1', 'label': 0}, {'id': 'train-2', 'label': 1}]
FEEDBACK = [{'id': 'new-1', 'label': 1, 'reviewed': True},
            {'id': 'test-1', 'label': 0, 'reviewed': True},
            {'id': 'new-2', 'label': 0, 'reviewed': False}]


def build_candidate(feedback):
    accepted = []
    for row in feedback:
        if row['id'] in PROTECTED:
            raise ValueError(f"Protected test ID in feedback: {row['id']}")
        if row['reviewed']:
            accepted.append({'id': row['id'], 'label': row['label']})
    return BASELINE + accepted


if __name__ == '__main__':
    try:
        build_candidate(FEEDBACK)
    except ValueError as error:
        print('Rejected unsafe candidate:', error)
    safe = [item for item in FEEDBACK if item['id'] not in PROTECTED]
    candidate = build_candidate(safe)
    assert {item['id'] for item in candidate}.isdisjoint(PROTECTED)
    assert not any(item['id'] == 'new-2' for item in candidate)
    Path('candidate.json').write_text(json.dumps(candidate, indent=2), encoding='utf-8')
    print('Candidate contains', len(candidate), 'reviewed or baseline rows')
