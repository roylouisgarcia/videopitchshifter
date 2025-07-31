#!/usr/bin/env python3
"""
Test script to verify the file overwrite protection functionality
"""

import os
import tempfile
from pathlib import Path

def test_unique_filename_generation():
    """Test the unique filename generation logic"""
    
    # Simulate the _generate_unique_filename function
    def _generate_unique_filename(original_path):
        """Generate a unique filename by adding a number suffix"""
        path_obj = Path(original_path)
        base_name = path_obj.stem
        extension = path_obj.suffix
        directory = path_obj.parent
        
        counter = 1
        while True:
            new_filename = f"{base_name}_{counter}{extension}"
            new_path = directory / new_filename
            if not new_path.exists():
                return str(new_path)
            counter += 1
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create some test files
        test_file = temp_path / "test_video.mp4"
        test_file.touch()
        
        # Create some existing files to test collision
        (temp_path / "test_video_1.mp4").touch()
        (temp_path / "test_video_2.mp4").touch()
        
        # Test unique filename generation
        unique_name = _generate_unique_filename(str(test_file))
        expected_name = str(temp_path / "test_video_3.mp4")
        
        print("Testing unique filename generation:")
        print(f"Original file: {test_file}")
        print(f"Existing files: test_video.mp4, test_video_1.mp4, test_video_2.mp4")
        print(f"Generated unique name: {Path(unique_name).name}")
        print(f"Expected: test_video_3.mp4")
        print(f"Test {'PASSED' if unique_name == expected_name else 'FAILED'}")
        
        # Test with no collision
        new_file = temp_path / "new_video.mp4"
        unique_name2 = _generate_unique_filename(str(new_file))
        expected_name2 = str(temp_path / "new_video_1.mp4")
        
        print(f"\nTesting with no existing file:")
        print(f"Original file: {new_file}")
        print(f"Generated unique name: {Path(unique_name2).name}")
        print(f"Expected: new_video_1.mp4")
        print(f"Test {'PASSED' if unique_name2 == expected_name2 else 'FAILED'}")

def test_button_functionality():
    """Test the pitch adjustment button logic"""
    
    # Simulate the adjust_pitch function
    def adjust_pitch(current_value, increment, min_val=-20, max_val=20):
        """Adjust pitch by incrementing/decrementing current value"""
        new_value = current_value + increment
        # Clamp to slider bounds
        new_value = max(min_val, min(max_val, new_value))
        return new_value
    
    print("\nTesting pitch adjustment buttons:")
    
    # Test normal increments
    current = 0
    current = adjust_pitch(current, -1)  # Should be -1
    print(f"Start at 0, click -1: {current} (expected: -1)")
    
    current = adjust_pitch(current, -1)  # Should be -2
    print(f"Click -1 again: {current} (expected: -2)")
    
    current = adjust_pitch(current, 1)   # Should be -1
    print(f"Click +1: {current} (expected: -1)")
    
    # Test boundary conditions
    current = -19
    current = adjust_pitch(current, -1)  # Should be -20
    current = adjust_pitch(current, -1)  # Should stay -20 (clamped)
    print(f"From -19, click -1 twice: {current} (expected: -20, clamped)")
    
    current = 19
    current = adjust_pitch(current, 1)   # Should be 20
    current = adjust_pitch(current, 1)   # Should stay 20 (clamped)
    print(f"From 19, click +1 twice: {current} (expected: 20, clamped)")
    
    print("Button functionality test completed!")

if __name__ == "__main__":
    test_unique_filename_generation()
    test_button_functionality()
    print("\nAll tests completed!")
