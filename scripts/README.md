# Scripts Directory

This directory contains the original shell scripts and reference files that were used as the foundation for creating the Video Pitch Adjuster GUI application.

## Original Scripts

### `convert2mp3.sh`
Original bash script for converting video files to MP3 audio format.
```bash
# Converts all MP4 files in directory to MP3
for file in *.mp4; do
    ffmpeg -i "$file" "${file%.mp4}.mp3"
done
```

### `lower_automate.sh`
Original bash script for extracting audio from MKV video files.
```bash
# Extracts audio from MKV files to MP3
for file in *.mkv; do
  ffmpeg -i "$file" "${file%.mkv}.mp3"
done
```

### `mixback.sh`
Original bash script for combining adjusted audio back with original video.
```bash
# Combines audio with video, replacing original audio
for file in *.mkv; do
  if [ -f "${file%.mkv}.wav" ]; then
    ffmpeg -i "$file" -i "${file%.mkv}.wav" -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 "${file%.mkv}-lower.mp4"
  fi
done
```

## Reference Files

### `codes.txt`
Collection of useful FFMPEG commands and examples:
- Video duration trimming
- Format conversion (MP4 to MOV)
- Audio extraction with specific quality settings
- Audio/video merging commands

## Evolution to GUI

These scripts provided the foundation for the GUI application by demonstrating:
1. **Audio extraction** workflow
2. **Pitch adjustment** concepts (manual process)
3. **Audio/video merging** techniques
4. **Batch processing** patterns

The GUI application automates and enhances these workflows with:
- **Visual interface** instead of command-line
- **Real-time preview** of settings
- **Advanced pitch adjustment** with sync preservation
- **Error handling** and user feedback
- **File protection** against overwrites
- **Dynamic naming** based on adjustments

## Usage

These scripts can still be used independently for batch processing or as reference for understanding the underlying FFMPEG commands used by the GUI application.

**Note**: The GUI application provides a more user-friendly and robust implementation of these concepts.
