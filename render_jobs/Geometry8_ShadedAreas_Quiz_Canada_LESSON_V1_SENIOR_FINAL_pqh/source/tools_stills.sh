#!/bin/bash
# usage: tools_stills.sh video events_file outdir
V=$1; E=$2; O=$3; mkdir -p $O; rm -f $O/*.jpg
while IFS='|' read p s t; do ffmpeg -nostdin -v error -y -ss $t -i "$V" -frames:v 1 -vf scale=960:-1 "$O/$(printf "%07.2f" $t)_${p}_${s}.jpg"; done < "$E"
