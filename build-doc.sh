#!/usr/bin/env sh

BUILDPATH=docs
SOURCEPATH=docs/source

rm $BUILDPATH/*.html
sphinx-build -b html $SOURCEPATH $BUILDPATH

python insert_social_media_links.py
echo "social media links inserted"

echo 'Documentation website in '$BUILDPATH
