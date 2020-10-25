#!/usr/bin/env sh

BUILDPATH=docs
SOURCEPATH=docs/source

rm $BUILDPATH/*.html
rm -rf $BUILDPATH/_sources
rm -rf $BUILDPATH/_modules
rm -rf $BUILDPATH/_static
rm -rf $BUILDPATH/.doctrees
rm -rf $BUILDPATH/_generated
rm -rf SOURCEPATH/_generated

sphinx-build -b html $SOURCEPATH $BUILDPATH

python $SOURCEPATH/insert_social_media_links.py
echo "social media links inserted"

echo 'Documentation website in '$BUILDPATH
