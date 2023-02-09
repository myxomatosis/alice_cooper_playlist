# alice_cooper_playlist
A script for archiving the "Nights with Alice Cooper" playlists from http://www.nightswithalicecooper.com.


You can install the script by downloading it to your current working directory as alice.py:
```
wget -O alice.py https://raw.githubusercontent.com/myxomatosis/alice_cooper_playlist/master/WordPress_api_call.py
```
Permissions need to allow it to execute:
```
chmod +x alice.py
```
## Dependencies
python 3.x

## Running the script

Move the script to the directory you would like all the playlists downloaded to and then run:
```
python alice.py
```

Further explaination:

The main feature of the script is downloading all the playlists to a directory called archive, which is created where the script is run from. This is forshadowing later versions or different scripts which will alter the playlists. I recommend creating a cronjob for the script to run daily or weekly to keep the archive up to date.

The script first gets the links to all the posts containing playlists from http://www.nightswithalicecooper.com. It then checks to see if the playlist has already been downloaded. It does this by checking that a file exists by the right name and that it is not empty. It then downloads all the playlists needed to complete the archive. Playlists are stored it json.
