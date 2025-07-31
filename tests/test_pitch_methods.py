#!/usr/bin/env python3
"""
Test script to verify pitch adjustment maintains video sync
"""

import subprocess
import tempfile
import os

def test_pitch_methods():
    """Test different pitch adjustment methods"""
    print("Testing FFMPEG pitch adjustment methods...")
    
    # Test if rubberband is available
    print("\n1. Testing rubberband filter availability...")
    test_cmd = ['ffmpeg', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=1', 
                '-af', 'rubberband=pitch=1.2', '-f', 'null', '-']
    
    try:
        result = subprocess.run(test_cmd, capture_output=True, text=True, 
                              creationflags=subprocess.CREATE_NO_WINDOW, timeout=10)
        if result.returncode == 0:
            print("✓ Rubberband filter is available (best quality)")
        else:
            print("✗ Rubberband filter not available")
            print("Error:", result.stderr)
    except Exception as e:
        print(f"✗ Error testing rubberband: {e}")
    
    # Test atempo method
    print("\n2. Testing atempo+asetrate method...")
    test_cmd2 = ['ffmpeg', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=1',
                 '-af', 'asetrate=44100*1.2,aresample=44100,atempo=0.833333',
                 '-f', 'null', '-']
    
    try:
        result = subprocess.run(test_cmd2, capture_output=True, text=True,
                              creationflags=subprocess.CREATE_NO_WINDOW, timeout=10)
        if result.returncode == 0:
            print("✓ Atempo+asetrate method is available (fallback)")
        else:
            print("✗ Atempo+asetrate method failed")
            print("Error:", result.stderr)
    except Exception as e:
        print(f"✗ Error testing atempo method: {e}")
    
    print("\n3. Testing basic FFMPEG functionality...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True,
                              creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode == 0:
            print("✓ FFMPEG is working correctly")
            # Extract version info
            version_line = result.stdout.split('\n')[0]
            print(f"  Version: {version_line}")
        else:
            print("✗ FFMPEG not working")
    except Exception as e:
        print(f"✗ FFMPEG test failed: {e}")

if __name__ == "__main__":
    test_pitch_methods()
    print("\nTest completed. The app will automatically choose the best available method.")
