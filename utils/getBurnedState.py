import cv2
import numpy as np
import os

def check_burned_state(image_path="images/pra_cropped.png"):
    """
    Check if the burned state is good
    
    Args:
        image_path: Path to the image file
    
    Returns:
        bool: True if state is 'good', False otherwise (also prints the state)
    """
    # Hardcoded RGB reference values from rgbMap.json
    reference_colors = {
        "unBurned": [
            [254, 255, 254],  # Very light/white colors
            [253, 255, 252],
            [254, 255, 254]
        ],
        "underBurned": [
            [254, 238, 86],   # Yellow tones
            [254, 236, 92],
            [255, 255, 97]
        ],
        "overBurned": [
            [26, 27, 26],     # Very dark/black colors
            [107, 103, 98],   # Dark gray
            [60, 60, 59]
        ],
        "good": [
            [254, 148, 61],   # Orange/brown tones (good state)
            [255, 181, 80],
            [255, 136, 48]
        ]
    }
    
    # Load image
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load image '{image_path}'")
            return False
        
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Calculate average color
        avg_color = np.mean(image_rgb, axis=(0, 1))
        r, g, b = avg_color
        
        print(f"Average image color (RGB): [{r:.1f}, {g:.1f}, {b:.1f}]")
        
    except Exception as e:
        print(f"Error loading image: {e}")
        return False
    
    # Improved classification using realistic color ranges based on actual image analysis
    predicted_state = None
    
    # Very light/grayish colors - unBurned (based on actual unBurned.png: avg ~130,133,128)
    if r > 125 and g > 125 and b > 120 and abs(r - g) < 10 and abs(r - b) < 15:
        predicted_state = "unBurned"
        print("Classification: Light grayish colors detected (unBurned)")
    
    # Yellow/bright tones - underBurned (yellowish with high R and G, lower B)
    elif r > 120 and g > 110 and b < 100 and (r + g - 2*b) > 60:
        predicted_state = "underBurned"
        print("Classification: Yellow/bright tones detected")
    
    # Orange/brown tones - good state (orange-ish with R > G > B)
    elif r > 90 and g > 70 and b < 80 and r > g and g > b and (r - b) > 30:
        predicted_state = "good"
        print("Classification: Orange/brown tones detected")
    
    # Dark colors - overBurned
    elif r < 90 and g < 90 and b < 90:
        predicted_state = "overBurned"
        print("Classification: Dark colors detected")
    
    # If not clearly in any range, use closest color matching
    if predicted_state is None:
        print("Using fallback: closest color matching")
        min_distance = float('inf')
        closest_state = None
        
        for state, colors in reference_colors.items():
            for ref_color in colors:
                # Calculate Euclidean distance
                distance = np.sqrt(sum((avg_color[i] - ref_color[i])**2 for i in range(3)))
                if distance < min_distance:
                    min_distance = distance
                    closest_state = state
        
        predicted_state = closest_state
        print(f"Closest match: {predicted_state} (distance: {min_distance:.2f})")
    
    # Return result
    if predicted_state == 'good':
        print("✓ Result: GOOD")
        return True
    else:
        print(f"✗ State: {predicted_state}")
        return False

# def test_all_images():
#     """Test the function with all available images"""
#     test_images = [
#         "images/pra_cropped.png",
#         "images/no_object.png",
#         "images/pra.png",
#         "images/pra_binary.png", 
#         "images/pra_cropped_gray.png",
#         "images/burnedStates/good.png",
#         "images/burnedStates/overBurned.png",
#         "images/burnedStates/unBurned.png", 
#         "images/burnedStates/underBurned.png"
#     ]
    
#     print("=== Testing All Available Images ===\n")
    
#     for img_path in test_images:
#         if os.path.exists(img_path):
#             print(f"{'='*60}")
#             print(f"Testing: {img_path}")
#             print("-" * 60)
#             result = check_burned_state(img_path)
#             print(f"Final Result: {'GOOD ✓' if result else 'NOT GOOD ✗'}")
#             print()
#         else:
#             print(f"Image not found: {img_path}")

if __name__ == "__main__":
    print("=== Burned State Detection ===\n")
    
    # Test with your specific image
    target_image = "images/pra_cropped.png"
    print(f"Testing target image: {target_image}")
    print("-" * 50)
    result = check_burned_state(target_image)
    print(f"Final Result: {'GOOD ✓' if result else 'NOT GOOD ✗'}")
    print()
    
    # Uncomment the line below if you want to test all images
    # test_all_images()
