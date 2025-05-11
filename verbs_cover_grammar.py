#!/usr/bin/env python3
import sys, os, json

# Ensure the api directory is on the path
sys.path.insert(0, os.path.abspath('api'))

from verbnet import VerbNetParser

# Define helper functions to normalize and validate primary frames
def normalize_primary(primary):
    """Strip annotations and drop trailing PP adjuncts from a primary frame."""
    slots = [p.split('.')[0] for p in primary]
    while slots and slots[-1].startswith('PP'):
        slots.pop()
    return slots

def is_valid_primary(slots):
    """Return True if slots represent NP-V, NP-V-NP, or NP-V-NP-NP."""
    return (
        len(slots) in (2, 3, 4)
        and slots[0] == 'NP'
        and slots[1] == 'V'
        and (len(slots) == 2 or all(s == 'NP' for s in slots[2:]))
    )

def main():
    # Initialize the parser for VerbNet 3.4
    vnp = VerbNetParser(version='3.4')
    verb_to_primaries = {}

    # Collect raw primary patterns per verb
    for vc in vnp.get_verb_classes():
        if not vc.members:
            continue
        for frame in vc.frames:
            primary = frame.primary
            for member in vc.members:
                verb = member.name
                primaries = verb_to_primaries.setdefault(verb, [])
                if primary not in primaries:
                    primaries.append(primary)

    # Simplify to NP-V, NP-V-NP, NP-V-NP-NP patterns
    simple = {}
    for verb, primaries in verb_to_primaries.items():
        simple_frames = set()
        for primary in primaries:
            slots = normalize_primary(primary)
            if is_valid_primary(slots):
                simple_frames.add(tuple(slots))
        if simple_frames:
            # Sort by length then lexicographically for consistency
            simple[verb] = [list(s) for s in sorted(simple_frames, key=lambda x: (len(x), x))]

    # Print the simplified JSON mapping
    print(json.dumps(simple, indent=2))

if __name__ == '__main__':
    main() 