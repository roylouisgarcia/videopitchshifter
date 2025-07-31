# Documentation Directory

This directory contains project documentation and configuration files.

## Documentation Files

### `PROJECT_SUMMARY.md`
Comprehensive overview of the Video Pitch Adjuster project including:
- **Features implemented**: Complete list of functionality
- **Technical details**: FFMPEG commands and processing steps
- **Recent improvements**: Bug fixes and enhancements
- **Usage guide**: How to use the application
- **Requirements**: System and software dependencies

### `config.ini`
Optional configuration file for customizing application defaults:
- **Audio quality settings**: Bitrate, sample rate, channels
- **UI preferences**: Window size, default paths
- **Processing options**: Codec choices, temporary file settings
- **Pitch adjustment ranges**: Min/max values, step sizes

## Configuration Usage

The `config.ini` file can be modified to change application defaults:

```ini
[DEFAULT_SETTINGS]
# Audio quality
audio_bitrate = 192k
audio_sample_rate = 44100

# UI Settings  
window_width = 800
window_height = 600

# Pitch range
min_pitch = -20
max_pitch = 20
```

**Note**: The GUI application will work without this file using built-in defaults. The configuration file is provided for advanced users who want to customize the application behavior.

## Future Documentation

Additional documentation may be added to this directory:
- **API documentation** (if the application is extended)
- **Troubleshooting guides** for specific issues
- **Advanced usage examples** and tutorials
- **Development guidelines** for contributors
