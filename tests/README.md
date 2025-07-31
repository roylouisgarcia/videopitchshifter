# Tests Directory

This directory contains test scripts to verify the functionality of the Video Pitch Adjuster application.

## Test Files

### `test_pitch_methods.py`
Tests the availability and functionality of different FFMPEG pitch adjustment methods:
- **Rubberband filter**: Best quality pitch adjustment with perfect sync
- **Atempo+asetrate method**: Fallback method for maintaining video sync
- **Basic FFMPEG functionality**: Verifies FFMPEG installation

**Usage:**
```bash
python tests\test_pitch_methods.py
```

### `test_functionality.py`
Tests core application functionality:
- **Unique filename generation**: Tests collision handling and numbering
- **Pitch adjustment buttons**: Tests increment/decrement button logic
- **Boundary conditions**: Tests slider limits and clamping

**Usage:**
```bash
python tests\test_functionality.py
```

### `test_filename_generation.py`
Tests the dynamic filename generation based on pitch direction:
- **Positive pitch**: Tests "_higher" suffix generation
- **Negative pitch**: Tests "_lower" suffix generation  
- **Zero pitch**: Tests "_pitch_adjusted" suffix generation
- **Various file formats**: Tests with different video extensions

**Usage:**
```bash
python tests\test_filename_generation.py
```

## Running All Tests

Use the convenient batch file in the root directory:
```bash
run_tests.bat
```

Or run individual tests as needed for specific functionality verification.

## Test Results

All tests should pass with ✓ marks. If any tests fail with ✗ marks:
1. Check that FFMPEG is properly installed
2. Verify Python environment is set up correctly
3. Ensure all dependencies are available

## Adding New Tests

When adding new functionality to the main application, create corresponding test files in this directory following the existing naming pattern: `test_[feature_name].py`
