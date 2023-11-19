#!/bin/sh

if [ $PWD = /Users/vinayedupuganti/Documents/SWM_Project/public_mm ]; then
  echo "You can't run this in the MetaMap base directory: /Users/vinayedupuganti/Documents/SWM_Project/public_mm"
  echo "Please run this from a directory outside of the base directory"
fi

CHOICE=no

read -p "Do you really want to uninstall MetaMap? [no/yes] " CHOICE
if [ "$CHOICE" = "" ]; then
   CHOICE=no
fi     
if [ "$CHOICE" = "no" ]; then
  echo "Aborting uninstall."
  exit 0
fi

echo "Removing Tagger Server"
rm -rf /Users/vinayedupuganti/Documents/SWM_Project/public_mm/MedPost-SKR
echo "Removing WSD Server"
rm -rf /Users/vinayedupuganti/Documents/SWM_Project/public_mm/WSD_Server
echo "Removing Lexicon"
rm -rf /Users/vinayedupuganti/Documents/SWM_Project/public_mm/lexicon
echo "Removing MetaMap Databases"
rm -rf /Users/vinayedupuganti/Documents/SWM_Project/public_mm/DB
echo "Removing Programs"
rm -rf /Users/vinayedupuganti/Documents/SWM_Project/public_mm/bin
echo "Removing Base Directory"
cd /Users/vinayedupuganti/Documents/SWM_Project/public_mm/..
rm -rf /Users/vinayedupuganti/Documents/SWM_Project/public_mm

if [ -e /Users/vinayedupuganti/Documents/SWM_Project/public_mm ]; then
    echo "Error: MetaMap installation not fully removed!!"
else
    echo "Removal of MetaMap installation successful."
fi
exit 0





