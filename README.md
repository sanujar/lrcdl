# LRCDL


## Intro

This is a simple Python script that grabs the LRC file for a given song using [https://github.com/akashrchandran/spotify-lyrics-api](https://github.com/akashrchandran/spotify-lyrics-api).

This made with quite a few ChatGPT prompts and some manual debugging based on real-world edge-cases encountered while using this script, but some issues might remain. Please open a PR or issue if so.

***

## Basic flow

1. Requests the path to an audio file: if the audio file has ID3 tags, it uses those to grab the artist, track, and album.
2. Does a Google search for the song to get a track URL, where the user then has to pick a number based on the results that come up (usually 1 should be good but this might depend).
3. Uses the hosted version of akashrchandran's API to grab the synced lyrics.
4. Reads the JSON input and outputs a LRC file to C:\Lyrics by default (this path should be changed before running the script if needed). 

There are many other manual fallbacks I've implemented in this script that can be understood by reading it or by encountering an issue, that aren't covered in the basic flow above.

***

## Requirements

This script (in its default form) requires the following packages to be installed:

```
mutagen
googlesearch-python
```

***

## Example run of the script (main.py)

```
Enter the path to the audio file: D:\Path\To\Song.mp3
Top 5 results:
1. https://website.link.com/track/1
2. https://website.link.com/track/2
3. https://website.link.com/track/3
4. https://website.link.com/track/4
5. https://website.link.com/track/5

Choose a result (1-5): 1
Selected URL: https://website.link.com/track/1
The lrc file has been written.

Process finished with exit code 0
```
