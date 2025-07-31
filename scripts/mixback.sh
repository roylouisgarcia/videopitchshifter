# Combine back audio to original video (replacing original audio)
for file in *.mkv; do
  if [ -f "${file%.mkv}.wav" ]; then
    echo "Processing file: $file"
    # ffmpeg -i "$file" "${file%.mkv}.mp3"
    ffmpeg -i "$file" -i "${file%.mkv}.wav" -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 "${file%.mkv}-lower.mp4"
  else
    echo "File not found: ${file%.mkv}.wav"
  fi
done

