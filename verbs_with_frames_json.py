#!/usr/bin/env python3
import sys, os, json

# Ensure the api directory is on the path
sys.path.insert(0, os.path.abspath('api'))

from verbnet import VerbNetParser

def main():
    vnp = VerbNetParser(version='3.4')
    verb_to_frames = {}

    # Walk through each verb class and its frames
    for vc in vnp.get_verb_classes():
        if not vc.members:
            continue
        for frame in vc.frames:
            # For each member verb in this class
            for member in vc.members:
                verb = member.name
                # Build a frame pattern with the actual verb in place of the VERB slot
                parts = []
                for role in frame.syntax:
                    if role.POS in ('VERB', 'V'):
                        parts.append(f"<{verb}>")
                    elif role.value:
                        parts.append(role.value[0])
                    else:
                        parts.append(role.POS)
                pattern = " ".join(parts)
                # Add pattern to this verb's list, avoiding duplicates
                frames = verb_to_frames.setdefault(verb, [])
                if pattern not in frames:
                    frames.append(pattern)

    # Print the result as JSON
    print(json.dumps(verb_to_frames, indent=2))

if __name__ == '__main__':
    main() 