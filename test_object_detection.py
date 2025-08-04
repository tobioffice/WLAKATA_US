import sys
import os
sys.path.append('./utils')

from checkObject import detect_object_presence

def test_object_detection():
    """Test object detection with different burned states"""
    background_path = "images/no_object.png"
    
    test_images = [
        "images/burnedStates/overBurned.png",
        "images/burnedStates/good.png", 
        "images/burnedStates/unBurned.png",
        "images/burnedStates/underBurned.png",
        "images/pra_cropped.png"
    ]
    
    print("=== Testing Object Detection with Different Burned States ===\n")
    
    for img_path in test_images:
        if os.path.exists(img_path):
            print(f"Testing: {img_path}")
            print("-" * 50)
            
            try:
                is_detected, result_img, diff_img, clean_mask = detect_object_presence(background_path, img_path)
                
                if is_detected:
                    print("✓ OBJECT DETECTED")
                else:
                    print("✗ NO OBJECT DETECTED")
                    
            except Exception as e:
                print(f"Error: {e}")
            
            print()
        else:
            print(f"Image not found: {img_path}")

if __name__ == "__main__":
    test_object_detection()
