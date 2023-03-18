# The work of quite a few ChatGPT prompts and quite a bit of Googling and debugging.

import json
import requests
import mutagen
# import subprocess                 # uncomment if using the manual process
from googlesearch import search     # comment out if using the manual process


# Prompt the user to enter the path to the audio file
audio_file_path = input("Enter the path to the audio file: ")

# Load the audio file using Mutagen
audio = mutagen.File(audio_file_path, easy=True)

# Extract the tags from the audio file
if audio.tags:
	title = audio.tags.get("title", [""])[0]
	artist = audio.tags.get("artist", [""])[0]
	album = audio.tags.get("album", [""])[0]
else:
	# Prompt the user for input if the tags are not available
	artist = input("Please enter the artist: ")
	title = input("Please enter the title: ")
	album = input("Please enter the album: ")

# Google Search from within Python
# If this fails, comment this out and uncomment the manual search path code block below as a failover.

query = f"{title} {artist} spotify track"

# Use the search function to get the top 5 results
results = search(query, num_results=5)

# Print the results
print("Top 5 results:")
for i, result in enumerate(results):
	print(f"{i+1}. {result}")

# Get the user's choice of result
choice = int(input("Choose a result (1-5): "))

SURL = list(search(query, num_results=choice))[-1]

print("Selected URL:", SURL)

# ##### Manual search path - deprecated in favour of search within Python
# # Search query
#
# query = f"{title} {artist} spotify track"
# searchurl = f"https://www.google.com/search?q={query}"
#
#
# chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"  # Change to your Chrome path
# subprocess.Popen([chrome_path, "--incognito", searchurl])
#
#
# # Prompt the user for the value of SURL
# SURL = input("Please enter the SURL: ")



# Build the URL for the JSON file using SURL
url = "https://spotify-lyric-api.herokuapp.com/?url={}&format=lrc".format(SURL)

# Make a GET request to the API
response = requests.get(url)

if response.status_code == 404:
	print("Error: URL not found")
	print(response.content.decode('utf-8'))
else:
	# Parse the response JSON data
	data = json.loads(response.content.decode('utf-8'))
	if data.get("syncType") == "LINE_SYNCED":
		lines = data['lines']

		title = title.replace('/', '-')  # Replace forward slash with hyphen
		with open(r'C:\Lyrics\{} - {}.lrc'.format(artist, title), 'w', encoding='utf-8') as f:
			# Write the inputs at the top of the output file
			f.write('[ar: "{}"]\n'.format(artist))
			f.write('[ti: "{}"]\n'.format(title))
			f.write('[al: "{}"]\n\n'.format(album))
			for item in lines:
				if isinstance(item, dict) and "timeTag" in item and "words" in item:
					time_tag = item["timeTag"]
					words = item["words"]
					f.write('[{}]{}\n'.format(time_tag, words))
				else:
					print("Error: Invalid data format")
			print("The lrc file has been written.")
	else:
		print("Error: The JSON file does not contain the required syncType.")
