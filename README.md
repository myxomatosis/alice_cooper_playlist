# alice_cooper_playlist
A script for archiving the "Nights with Alice Cooper" playlists


You can install the by moving the script to ~/bin/ or downloading it straight there:
```
wget -O ~/bin/alice.sh https://github.com/myxomatosis/alice_cooper_playlist/raw/master/alice.sh
```
Permissions need to allow it to execute:
```
chmod +x ~/bin/alice.sh
```
## Dependencies
html2text

To install on Debian based distros:
```
sudo apt install html2text
```
To install on RedHat based distros:
```
sudo yum install html2text #Requires the epel repo
```

## Running the script
alice.sh is now in beta. There are no known issues except sloppy code.
Running the script with or without arguments will do the same thing.
It will download the entire playlist history for http://www.nightswithalicecooper.com.

Move the script to the directory you would like all the playlists downloaded to and then run:
```
./alice.sh
```

Further explaination:
Everytime it is run it will create a backup of the script in the bak directory. This is for debugging issues later and should probably be commented out. It will take a long time to cause issues though.
It will update itself using sed so I can avoid writing more code. It should use an algerithim to find the oldest playlist but instead it updates every time it runs with what the oldest one was. This helps the script find the oldest playlist faster and reduce the load on http://www.nightswithalicecooper.com.
The main feature of the script is downloading all the playlists to a directory called unaltered, which is created where the script is run from. This is forshadowing later versions or different scripts which will alter the playlists.

I recommend creating a cronjob for the script to run daily or weekly.
