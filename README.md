# Video Pitch Adjuster GUI

A user-friendly GUI application that uses FFMPEG to adjust the pitch of audio in video files. This application extracts audio from video, adjusts the pitch by a specified amount, and merges the adjusted audio back with the original video.

## Screenshot

![Video Pitch Adjuster GUI](images/screenshot.png)

*The intuitive interface allows easy video selection, pitch adjustment, and real-time processing feedback.*

## Features

- **Easy-to-use GUI**: Intuitive interface built with tkinter
- **Flexible pitch adjustment**: Adjust pitch from -20 to +20 semitones
- **Preset buttons**: Quick access to common adjustments (-1, 0, +1 semitones)
- **Real-time feedback**: Progress tracking and detailed processing logs
- **Multiple video formats**: Supports MP4, MKV, AVI, MOV, WMV, FLV
- **Auto-naming**: Automatically suggests unique output filenames based on pitch direction
  - Positive pitch: `filename_higher.ext`
  - Negative pitch: `filename_lower.ext` 
  - Zero pitch: `filename_pitch_adjusted.ext`
- **File protection**: Warns before overwriting existing files
- **Background processing**: Non-blocking UI during video processing

## Prerequisites

### FFMPEG Installation
This application requires FFMPEG to be installed and accessible from the command line.

#### Windows:
1. Download FFMPEG from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract the files to a folder (e.g., `D:\NostraProgramFiles\ffmpeg\bin\`)

   ![](https://github.com/roylouisgarcia/videopitchshifter/blob/main/images/path1.png)
3. Add the `bin` folder to your system PATH:
   - Open System Properties → Advanced → Environment Variables
   - Edit the `Path` variable and add `D:\NostraProgramFiles\ffmpeg\bin\`
     - ![Path](https://github.com/roylouisgarcia/videopitchshifter/blob/main/images/path2.png)
     - ![](https://github.com/roylouisgarcia/videopitchshifter/blob/main/images/path3.png)
4. Verify installation by opening Command Prompt and running: `ffmpeg -version`

#### Mac/Linux:
```bash
# Mac (using Homebrew)
brew install ffmpeg

# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# CentOS/RHEL/Fedora
sudo yum install ffmpeg
# or
sudo dnf install ffmpeg
```

### Python Requirements
- Python 3.6 or higher
- tkinter (usually included with Python)

## Installation

1. Clone or download this repository
2. No additional Python packages need to be installed (uses only built-in libraries)
3. Ensure FFMPEG is installed and in your PATH

## Usage

### Running the Application
```bash
python video_pitch_adjuster.py
```

### Using the GUI

1. **Select Input Video**: Click "Browse" next to "Input Video" and select your video file
2. **Choose Output Location**: Click "Browse" next to "Output Video" or let it auto-generate a filename
   - Auto-generated names change based on pitch direction:
     - Positive pitch: `video_higher.mp4`
     - Negative pitch: `video_lower.mp4`
     - Zero pitch: `video_pitch_adjusted.mp4`
3. **Adjust Pitch**: 
   - Use the slider to adjust pitch from -20 to +20 semitones
   - Use preset buttons for quick adjustments (-1, 0, +1)
   - Positive values increase pitch, negative values decrease pitch
4. **Process Video**: Click "Process Video" to start the conversion
   - If the output file already exists, you'll be prompted to:
     - Overwrite the existing file
     - Choose a different filename (auto-generates unique name)
     - Cancel the operation
5. **Monitor Progress**: Watch the progress bar and check the log for detailed information

### Pitch Adjustment Guide

- **-12 semitones**: One octave lower
- **-5 semitones**: Noticeably lower pitch
- **-1 semitone**: Slight decrease
- **0 semitones**: No change (original pitch)
- **+1 semitone**: Slight increase
- **+5 semitones**: Noticeably higher pitch
- **+12 semitones**: One octave higher

## Technical Details

### Processing Steps
1. **Audio Extraction**: Extracts audio from the input video as WAV format
2. **Pitch Adjustment**: Uses FFMPEG's advanced filters to adjust pitch while preserving duration
   - First tries `rubberband` filter (best quality, maintains sync)
   - Falls back to `asetrate` + `atempo` combination if rubberband unavailable
3. **Video Merging**: Combines the pitch-adjusted audio with the original video

### FFMPEG Commands Used

#### Extract Audio:
```bash
ffmpeg -i input_video -vn -acodec pcm_s16le -ar 44100 -ac 2 extracted_audio.wav -y
```

#### Adjust Pitch (Method 1 - Rubberband, preferred):
```bash
ffmpeg -i extracted_audio.wav -af "rubberband=pitch=pitch_ratio" pitched_audio.wav -y
```

#### Adjust Pitch (Method 2 - Fallback, maintains sync):
```bash
ffmpeg -i extracted_audio.wav -af "asetrate=44100*pitch_ratio,aresample=44100,atempo=tempo_ratio" pitched_audio.wav -y
```

#### Merge Audio and Video:
```bash
ffmpeg -i input_video -i pitched_audio.wav -c:v copy -c:a aac -b:a 192k -map 0:v:0 -map 1:a:0 output_video -y
```

## Supported Formats

### Input Formats
- MP4, MKV, AVI, MOV, WMV, FLV
- Any format supported by FFMPEG

### Output Formats
- MP4 (default and recommended)
- MKV, AVI (also supported)

## Troubleshooting

### Common Issues

1. **"FFMPEG not found" error**:
   - Ensure FFMPEG is installed and added to your system PATH
   - Try running `ffmpeg -version` in command prompt/terminal

2. **Video processing fails**:
   - Check that the input video file is not corrupted
   - Ensure sufficient disk space for temporary files
   - Check the process log for detailed error messages

3. **Audio quality issues**:
   - Large pitch adjustments (>±5 semitones) may affect audio quality
   - Consider using smaller adjustments for better results
   - The app automatically tries rubberband filter for best quality

4. **Audio/Video sync issues**:
   - The app now uses advanced methods to maintain video sync
   - If sync issues persist, try smaller pitch adjustments
   - Rubberband filter provides the best sync preservation

5. **File overwrites**:
   - The app will warn you before overwriting existing files
   - Choose "No" to auto-generate a unique filename
   - Auto-generated names use format based on pitch:
     - `filename_higher_1.mp4` (for positive pitch)
     - `filename_lower_1.mp4` (for negative pitch)
     - `filename_pitch_adjusted_1.mp4` (for zero pitch)

6. **Smart filename updates**:
   - Output filename updates automatically as you adjust the pitch slider
   - Provides clear indication of the adjustment direction

7. **Slow processing**:
   - Processing time depends on video length and system performance
   - Larger videos will take longer to process

### Performance Tips

- Close other applications during processing for better performance
- Use SSD storage for faster temporary file operations
- For very large videos, consider splitting them into smaller segments

## File Structure

```
ffmpeg_processing/
├── video_pitch_adjuster.py    # Main GUI application
├── run_video_pitch_adjuster.bat # Windows launcher script
├── README.md                  # This documentation file
├── requirements.txt           # Dependencies information
├── images/                    # Screenshots and visual assets
│   └── screenshot.png         # Application interface screenshot
├── docs/                      # Documentation and configuration
│   ├── PROJECT_SUMMARY.md     # Project overview and features
│   └── config.ini            # Optional configuration settings
├── scripts/                   # Original shell scripts and references
│   ├── mixback.sh            # Original script for audio merging
│   ├── convert2mp3.sh        # Original script for audio extraction
│   ├── lower_automate.sh     # Original automation script
│   └── codes.txt             # Original FFMPEG command references
└── tests/                     # Test scripts and utilities
    ├── test_pitch_methods.py  # Test FFMPEG pitch methods
    ├── test_functionality.py  # Test button and file functionality
    └── test_filename_generation.py # Test dynamic naming logic
```

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application.
