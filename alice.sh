#!/bin/bash
# Version 0.0.2

# Define site URL
site="http://www.nightswithalicecooper.com/on-the-air/last-nights-music/page"

# Find the oldest playlist
old () {
while true ; do
	entry="entry-title"
	for pg in {1795..9999} ; do 
		entry=$(curl -ks $site/$pg | grep -o entry-title)
		if [ ! "$entry" == "entry-title" ] ; then
			break
		fi
	done
	if [ ! "$entry" == "entry-title" ] ; then
		break
	fi
done
echo "$site/$(($pg - 1))"
lastpg=$(($pg -1))
export lastpg
}

check_if_uptodate () {
# Check the latest has been downloaded
ls unaltered/playlist.$lastpg
if [ $? -eq 0 ] ; then
	echo "Everything is up-to-date!"
else
	get_playlists
fi
}

get_playlists () {
echo "Getting missing playlists"
if [ ! -d unaltered ] ; then
	echo "Making unaltered directory"
	mkdir unaltered
	for pg in $(eval echo {$lastpg..1}) ; do
		echo "Downloading playlist.$((($lastpg - $pg + 1))) $site/$pg"
		wget -qO unaltered/playlist.$((($lastpg - $pg + 1))) $site/$pg
	done
else
	lastpl=$(ls -v unaltered | tail -n1 | sed 's/playlist.//')
	if [ "$lastpl" == "" ] ; then
		lastpl=1
		echo "Starting with $lastpl as none seem to exist"
	else
		lastpl=$((($lastpl + 1)))
		echo "Starting with $lastpl"
	fi
	for pg in $(eval echo {$((($lastpg - $lastpl + 1)))..1}) ; do
		echo "Downloading playlist.$((($lastpg - $pg + 1))) $site/$pg"
		wget -qO unaltered/playlist.$((($lastpg - $pg + 1))) $site/$pg
	done
fi
}

echo "running old"
old
echo "running check_if_uptodate"
check_if_uptodate
