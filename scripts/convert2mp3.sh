#!/bin/bash

#Use ffmepg to convert all videos with extension mp4 to mp3 in a directory.
for file in *.mp4; do
    ffmpeg -i "$file" "${file%.mp4}.mp3"
done
