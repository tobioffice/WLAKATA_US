import sys
import os
sys.path.append('./utils')

from checkObject import detect_object_presence

# Test background vs background (should detect NO object)
result = detect_object_presence("images/no_object.png", "images/no_object.png")
print(f"Background vs Background: {'DETECTED' if result[0] else 'NOT DETECTED'}")

# Test background vs overburned (should detect object)
result = detect_object_presence("images/no_object.png", "images/burnedStates/overBurned.png")
print(f"Background vs Overburned: {'DETECTED' if result[0] else 'NOT DETECTED'}")
