#!/bin/bash

# © 2020, Midgard
# License: GPL-3.0-or-later
# This file is not available under the LGPL!

cd $(dirname "$0")/..

if [ ! -t 0 ] ; then
	echo "release.sh must be run with a terminal on stdin" >&2
	exit 1
fi

git status

echo -n "Previous version:  v"
./setup.py --version
read -p "Enter new version: v" version

sed -i 's/version=".*"/version="'"$version"'"/' setup.py
git add setup.py
git commit -m "Bump version to $version"

tagid=v"$version"
echo "Creating git tag $tagid"
git tag -s -m "Version $version" "$tagid"

./setup.py sdist bdist_wheel

read -p "Upload to Framagit and PyPI? (y/N) " confirm
if [ ! "$confirm" = y ]; then "Abort"; exit 1; fi

python3 -m twine upload dist/*-${version}*
git push origin "$tagid"
