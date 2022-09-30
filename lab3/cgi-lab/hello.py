#!/usr/bin/env python3

import os
import json

#env = {}
#for key, value in os.environ.items():
#        env[key] = value
#print("Content-Type: application/json")
#print()
#print(json.dumps(env))

print("Content-Type: text/html\n")
print(f"<p>QUERY_STRING={os.environ['QUERY_STRING']}</p>")