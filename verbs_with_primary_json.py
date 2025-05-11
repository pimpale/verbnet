#!/usr/bin/env python3
import sys, os, json

# Ensure the api directory is on the path
sys.path.insert(0, os.path.abspath('api'))

from verbnet import VerbNetParser

def main():
    # Initialize the parser for VerbNet 3.4
    vnp = VerbNetParser(version='3.4')
    verb_to_primaries = {}

    # Iterate over each verb class and record its primary patterns
    for vc in vnp.get_verb_classes():
        if not vc.members:
            continue
        for frame in vc.frames:
            primary = frame.primary  # a list of strings, e.g. ['NP','V','NP']
            for member in vc.members:
                verb = member.name
                # Ensure we have a list for this verb
                primaries = verb_to_primaries.setdefault(verb, [])
                # Only add if not already present
                if primary not in primaries:
                    primaries.append(primary)

    # Print the JSON mapping: verb -> list of primary lists
    print(json.dumps(verb_to_primaries, indent=2))

if __name__ == '__main__':
    main() 