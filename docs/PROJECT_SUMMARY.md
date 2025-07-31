# Video Pitch Adjuster Project Summary

## What was created:

### Main Application
- **video_pitch_adjuster.py** - Complete GUI application with the following features:
  - Browse and select input video files
  - Set output location with auto-naming
  - Pitch adjustment slider (-20 to +20 semitones)
  - Preset buttons for quick adjustments (-5, 0, +5)
  - Real-time processing with progress bar
  - Detailed logging of all operations
  - Error handling and validation

### Supporting Files
- **README.md** - Comprehensive documentation
- **requirements.txt** - Dependencies information
- **config.ini** - Configuration settings (optional)
- **run_video_pitch_adjuster.bat** - Windows launcher script

### Original Files (preserved)
- **mixback.sh** - Original script for audio merging
- **convert2mp3.sh** - Original script for audio extraction  
- **lower_automate.sh** - Original automation script
- **codes.txt** - Original FFMPEG command references

## Key Features Implemented:

1. **Video Input**: Supports multiple formats (MP4, MKV, AVI, MOV, WMV, FLV)
2. **Audio Extraction**: Extracts audio as high-quality WAV
3. **Pitch Adjustment**: Uses advanced FFMPEG filters to preserve video sync
   - First tries `rubberband` filter (best quality, maintains sync)
   - Falls back to `asetrate` + `atempo` combination if rubberband unavailable
4. **Audio Merging**: Combines adjusted audio back with original video
5. **User Interface**: 
   - Intuitive file selection with auto-naming
   - Visual pitch adjustment slider (-20 to +20 semitones)
   - Increment/decrement buttons (-1, 0, +1) that work correctly
   - Real-time progress feedback
   - Detailed process logging
6. **File Protection**: 
   - Warns before overwriting existing files
   - Auto-generates unique filenames when conflicts occur
   - Gives users choice to overwrite, rename, or cancel
7. **Error Handling**: Validates inputs and provides helpful error messages

## How to Use:

1. **Quick Start**: Double-click `run_video_pitch_adjuster.bat`
2. **Manual Start**: Run `python video_pitch_adjuster.py`
3. **Select Video**: Browse for your input video file
4. **Adjust Pitch**: Use slider or preset buttons
5. **Process**: Click "Process Video" and wait for completion

## Technical Implementation:

The application uses a 3-step process with improved sync preservation:
1. Extract audio: `ffmpeg -i video.mp4 -vn -acodec pcm_s16le audio.wav`
2. Adjust pitch (Method 1): `ffmpeg -i audio.wav -af "rubberband=pitch=ratio" pitched.wav`
   Adjust pitch (Method 2): `ffmpeg -i audio.wav -af "asetrate=44100*ratio,aresample=44100,atempo=tempo_ratio" pitched.wav`
3. Merge back: `ffmpeg -i video.mp4 -i pitched.wav -c:v copy -c:a aac output.mp4`

## Recent Improvements:

✅ **Fixed sync issues**: Audio now maintains original duration while changing pitch
✅ **Fixed button functionality**: -1/+1 buttons now work correctly for multiple clicks
✅ **Added file protection**: Warns before overwriting existing files
✅ **Auto-unique naming**: Generates unique filenames to prevent conflicts
✅ **Better error handling**: More robust validation and user feedback

## Requirements Met:

✅ GUI application with video input
✅ Extract MP3/audio from video  
✅ Pitch adjustment with slider (+5/-5 and custom values)
✅ Merge adjusted audio back to video
✅ Uses FFMPEG for all operations
✅ User-friendly interface
✅ Progress feedback and error handling
✅ Cross-platform compatibility (Windows focus)

The application is ready to use and provides a complete solution for video pitch adjustment!
