import sys
import os
sys.path.append('./utils')

from checkObject import idObjectPresent

# Test with different scenarios
print("=== Testing idObjectPresent function ===")

print("\n1. Testing with default path (pra_cropped_gray.png):")
result1 = idObjectPresent()
print(f"Result: {'DETECTED' if result1 else 'NOT DETECTED'}")

print("\n2. Testing with background image (no_object.png):")
result2 = idObjectPresent("images/no_object.png")
print(f"Result: {'DETECTED' if result2 else 'NOT DETECTED'}")

print("\n3. Testing with overburned image:")
result3 = idObjectPresent("images/burnedStates/overBurned.png")
print(f"Result: {'DETECTED' if result3 else 'NOT DETECTED'}")

print("\n4. Testing with good image:")
result4 = idObjectPresent("images/burnedStates/good.png")
print(f"Result: {'DETECTED' if result4 else 'NOT DETECTED'}")
