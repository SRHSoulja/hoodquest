import re

with open('/home/arson/rhnftproject/generate_rc3_blueprint.py', 'r') as f:
    text = f.read()

# Let's inspect the sections in generate_rc3_blueprint.py
print("Read", len(text), "bytes")
