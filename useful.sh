#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"


creation () {
#Create directory for altered playlists
if [ ! -d $DIR/altered ] ; then
	mkdir $DIR/altered
fi

# Run playlists through html2text and convert all characters to uppercase
for file in `ls $DIR/unaltered/` ; do
	awk '/entry-title/{a=1} a; /\/div/{a=0}' $DIR/unaltered/$file | html2text | tr '[:lower:]' '[:upper:]' > $DIR/altered/$file
done
}

alter () {
# Remove blank lines
sed -i '/^\s*$/d' $DIR/altered/*

}

#creation
alter
