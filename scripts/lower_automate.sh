# Extracting the sounds (mp3) from video (mkv)

for file in *.mkv; do
  ffmpeg -i "$file" "${file%.mkv}.mp3"
done

