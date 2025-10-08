#!/usr/bin/env python3

import json
import sys

# Test JSON parsing
if len(sys.argv) > 1:
    print(f"Received argument: {sys.argv[1]}")
    print(f"Type: {type(sys.argv[1])}")
    print(f"Length: {len(sys.argv[1])}")
    
    try:
        data = json.loads(sys.argv[1])
        print(f"Parsed successfully: {data}")
    except json.JSONDecodeError as e:
        print(f"JSON error: {e}")
        print(f"Character at error: '{sys.argv[1][e.pos-1:e.pos+1]}'")
else:
    print("No arguments provided")