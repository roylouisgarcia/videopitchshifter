#!/usr/bin/env python3
"""
Test script to verify the dynamic filename generation based on pitch adjustment
"""

from pathlib import Path

def test_filename_generation():
    """Test the filename generation logic"""
    
    def generate_filename(input_filename, pitch_value):
        """Simulate the filename generation logic"""
        input_path = Path(input_filename)
        
        # Determine the appropriate suffix based on pitch direction
        if abs(pitch_value) < 0.1:  # Close to zero
            suffix = "pitch_adjusted"
        elif pitch_value > 0:
            suffix = "higher"
        else:  # pitch_value < 0
            suffix = "lower"
        
        # Generate new output filename
        output_filename = f"{input_path.stem}_{suffix}{input_path.suffix}"
        return output_filename
    
    print("Testing dynamic filename generation based on pitch adjustment:")
    print("=" * 60)
    
    test_cases = [
        ("my_video.mp4", -5.0, "my_video_lower.mp4"),
        ("my_video.mp4", -1.0, "my_video_lower.mp4"),
        ("my_video.mp4", -0.5, "my_video_lower.mp4"),
        ("my_video.mp4", 0.0, "my_video_pitch_adjusted.mp4"),
        ("my_video.mp4", 0.5, "my_video_higher.mp4"),
        ("my_video.mp4", 1.0, "my_video_higher.mp4"),
        ("my_video.mp4", 5.0, "my_video_higher.mp4"),
        ("test.mkv", -3.0, "test_lower.mkv"),
        ("test.mkv", 3.0, "test_higher.mkv"),
        ("sample.avi", 0.0, "sample_pitch_adjusted.avi"),
    ]
    
    for input_file, pitch, expected in test_cases:
        result = generate_filename(input_file, pitch)
        status = "✓" if result == expected else "✗"
        print(f"{status} Input: {input_file:20} | Pitch: {pitch:5.1f} | Output: {result}")
        if result != expected:
            print(f"  Expected: {expected}")
    
    print("\n" + "=" * 60)
    print("Dynamic filename generation based on pitch direction:")
    print("• Positive pitch (+0.1 to +20): '_higher' suffix")
    print("• Negative pitch (-0.1 to -20): '_lower' suffix") 
    print("• Zero pitch (-0.1 to +0.1): '_pitch_adjusted' suffix")

if __name__ == "__main__":
    test_filename_generation()
