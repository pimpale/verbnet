#!/usr/bin/env python3
import sys, os

# Ensure the api directory is on the path
sys.path.insert(0, os.path.abspath('api'))

from verbnet import VerbNetParser

def main():
    # Initialize the parser for version 3.4
    vnp = VerbNetParser(version='3.4')
    # Iterate over all verb classes
    for vc in vnp.get_verb_classes():
        # Skip classes without members
        if not vc.members:
            continue
        # Use the first member lexeme as representative verb
        verb = vc.members[0].name
        # For each frame in this class
        for frame in vc.frames:
            # Build a list of role labels and insert the verb at the V node
            parts = []
            for role in frame.syntax:
                if role.POS in ('VERB', 'V'):
                    parts.append(f"<{verb}>")
                elif role.value:
                    parts.append(role.value[0])
                else:
                    parts.append(role.POS)
            # Print the reconstructed frame
            print(" ".join(parts))

if __name__ == '__main__':
    main() 