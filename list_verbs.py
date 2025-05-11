#!/usr/bin/env python3
import sys, os

# Ensure the api directory is on the path
sys.path.insert(0, os.path.abspath('api'))

from verbnet import VerbNetParser

def main():
    # Initialize the parser for version 3.4
    vnp = VerbNetParser(version='3.4')
    # Retrieve all member verbs
    members = vnp.get_members()
    # Extract unique names and sort them
    names = sorted({m.name for m in members})
    # Print each verb name
    for name in names:
        print(name)

if __name__ == '__main__':
    main() 