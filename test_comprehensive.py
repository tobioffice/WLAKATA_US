#!/usr/bin/env python3

import sys
import os

# Add utils directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from checkObject import idObjectPresent

def test_all_burned_states():
    """Test object detection with all burned states"""
    
    test_cases = [
        ("Background (no object)", "images/no_object.png"),
        ("Good state", "images/burnedStates/good.png"),
        ("Overburned state", "images/burnedStates/overBurned.png"),
        ("Unburned state", "images/burnedStates/unBurned.png"),
        ("Underburned state", "images/burnedStates/underBurned.png"),
        ("Cropped image", "images/pra_cropped.png")
    ]
    
    print("=== Object Detection Test for All Burned States ===\n")
    
    for description, image_path in test_cases:
        if os.path.exists(image_path):
            print(f"Testing {description}: {image_path}")
            print("-" * 60)
            
            try:
                result = idObjectPresent(image_path)
                status = "✓ DETECTED" if result else "✗ NOT DETECTED"
                print(f"Result: {status}")
                
            except Exception as e:
                print(f"Error: {e}")
            
            print()
        else:
            print(f"Image not found: {image_path}\n")

if __name__ == "__main__":
    test_all_burned_states()
