#!/bin/sh
#set -o xtrace
# Lionel Cordesses, 2020.
# Part of my scripts to extract a few roms and create the relevant MAME zip.

# Use this to only extract the file and not to process them with the python script:
# ./go >a.txt
# grep -vw python3 a.txt >a1.txt
# bash a1.txt

# Use this to only process the extracted files with the python script:
# ./go >a.txt
# grep -w python3 a.txt >a1.txt
# bash a1.txt

# Use this to extract and process the files:
# ./go >a.txt
# bash a.txt

# MY_QUICKBMS is the path and the name of the executable of quickbms.
MY_QUICKBMS=/home/lionel/provi/quickbms/quickbms
# MY_QUICKBMS_SCRIPT is the path and the name of the sf30_mbundle.bms file.
MY_QUICKBMS_SCRIPT=/home/lionel/Downloads/sf30_mbundle.bms
# MY_SNK_DIR is the path of the SNK 40th Anniversary Collection bundle directory.
MY_SNK_DIR="\"/mnt/hugeExt4/games/Windows/SNK 40th Anniversary Collection/\""
# MY_RAW_ROMS_DIR is the directory where you want to store the rom extracted from the bundle files.
MY_RAW_ROMS_DIR=/home/lionel/provi/rawroms

###################################################################################################     
MY_XML=marvinsmaze2003.xml
# MY_GAME is the basename of the raw roms before converting them to MAME's format.
# It is the output of the quickbms step.
MY_GAME=marvin 
# Create a directory based on $MY_RAW_ROMS_DIR and $MY_XML
MY_TARGET_DIR_p=$MY_RAW_ROMS_DIR/$(basename $MY_XML .xml)
MY_TARGET_DIR="\"$MY_TARGET_DIR_p\""
echo mkdir -p $MY_TARGET_DIR_p
# Run quickbms to extract files related to the game $MY_GAME
echo $MY_QUICKBMS -f \"$MY_GAME*\" \"$MY_QUICKBMS_SCRIPT\" $MY_SNK_DIR $MY_TARGET_DIR 
echo rm $MY_TARGET_DIR_p/*.jpg
echo rm $MY_TARGET_DIR_p/*.png
echo python3 go.py $MY_TARGET_DIR $MY_XML

MY_XML=athena2003.xml
MY_GAME=athena
# Create a directory based on $MY_RAW_ROMS_DIR and $MY_XML
MY_TARGET_DIR_p=$MY_RAW_ROMS_DIR/$(basename $MY_XML .xml)
MY_TARGET_DIR="\"$MY_TARGET_DIR_p\""
echo mkdir -p $MY_TARGET_DIR_p
# Run quickbms to extract files related to the game $MY_GAME
echo $MY_QUICKBMS -f \"$MY_GAME*\" \"$MY_QUICKBMS_SCRIPT\" $MY_SNK_DIR $MY_TARGET_DIR 
echo rm $MY_TARGET_DIR_p/*.jpg
echo rm $MY_TARGET_DIR_p/*.png
echo rm $MY_TARGET_DIR_p/*.ogg
echo rm $MY_TARGET_DIR_p/*.nes
echo python3 go.py $MY_TARGET_DIR $MY_XML

MY_XML=guerrillawar2003.xml
MY_GAME=GuerillaWar
# Create a directory based on $MY_RAW_ROMS_DIR and $MY_XML
MY_TARGET_DIR_p=$MY_RAW_ROMS_DIR/$(basename $MY_XML .xml)
MY_TARGET_DIR="\"$MY_TARGET_DIR_p\""
echo mkdir -p $MY_TARGET_DIR_p
# Run quickbms to extract files related to the game $MY_GAME
echo $MY_QUICKBMS -f \"$MY_GAME*\" \"$MY_QUICKBMS_SCRIPT\" $MY_SNK_DIR $MY_TARGET_DIR 
echo rm $MY_TARGET_DIR_p/*.jpg
echo rm $MY_TARGET_DIR_p/*.png
echo rm $MY_TARGET_DIR_p/*.ogg
echo rm $MY_TARGET_DIR_p/*.nes
echo python3 go.py $MY_TARGET_DIR $MY_XML

MY_XML=ikari2003.xml
MY_GAME=IkariWarriors
# Create a directory based on $MY_RAW_ROMS_DIR and $MY_XML
MY_TARGET_DIR_p=$MY_RAW_ROMS_DIR/$(basename $MY_XML .xml)
MY_TARGET_DIR="\"$MY_TARGET_DIR_p\""
echo mkdir -p $MY_TARGET_DIR_p
# Run quickbms to extract files related to the game $MY_GAME 
echo $MY_QUICKBMS -f \"$MY_GAME*\" \"$MY_QUICKBMS_SCRIPT\" $MY_SNK_DIR $MY_TARGET_DIR 
echo rm $MY_TARGET_DIR_p/*.jpg
echo rm $MY_TARGET_DIR_p/*.png
echo rm $MY_TARGET_DIR_p/*.ogg
echo rm $MY_TARGET_DIR_p/*.nes
echo python3 go.py $MY_TARGET_DIR $MY_XML


MY_XML=tank32003.xml
MY_GAME=TNKIII
# Create a directory based on $MY_RAW_ROMS_DIR and $MY_XML
MY_TARGET_DIR_p=$MY_RAW_ROMS_DIR/$(basename $MY_XML .xml)
MY_TARGET_DIR="\"$MY_TARGET_DIR_p\""
echo mkdir -p $MY_TARGET_DIR_p
# Run quickbms to extract files related to the game $MY_GAME
echo $MY_QUICKBMS -f \"$MY_GAME*\" \"$MY_QUICKBMS_SCRIPT\" $MY_SNK_DIR $MY_TARGET_DIR 
echo rm $MY_TARGET_DIR_p/*.jpg
echo rm $MY_TARGET_DIR_p/*.png
echo rm $MY_TARGET_DIR_p/*.ogg
echo rm $MY_TARGET_DIR_p/*.nes
echo python3 go.py $MY_TARGET_DIR $MY_XML

MY_XML=paddlemania2003.xml
MY_GAME=PaddleMania
# Create a directory based on $MY_RAW_ROMS_DIR and $MY_XML
MY_TARGET_DIR_p=$MY_RAW_ROMS_DIR/$(basename $MY_XML .xml)
MY_TARGET_DIR="\"$MY_TARGET_DIR_p\""
echo mkdir -p $MY_TARGET_DIR_p
# Run quickbms to extract files related to the game $MY_GAME
echo $MY_QUICKBMS -f \"$MY_GAME*\" \"$MY_QUICKBMS_SCRIPT\" $MY_SNK_DIR $MY_TARGET_DIR 
echo rm $MY_TARGET_DIR_p/*.jpg
echo rm $MY_TARGET_DIR_p/*.png
echo rm $MY_TARGET_DIR_p/*.ogg
echo rm $MY_TARGET_DIR_p/*.nes
echo python3 go.py $MY_TARGET_DIR $MY_XML

MY_XML=victoryroad2003.xml
MY_GAME=VictoryRoad
# Create a directory based on $MY_RAW_ROMS_DIR and $MY_XML
MY_TARGET_DIR_p=$MY_RAW_ROMS_DIR/$(basename $MY_XML .xml)
MY_TARGET_DIR="\"$MY_TARGET_DIR_p\""
echo mkdir -p $MY_TARGET_DIR_p
# Run quickbms to extract files related to the game $MY_GAME
echo $MY_QUICKBMS -f \"$MY_GAME*\" \"$MY_QUICKBMS_SCRIPT\" $MY_SNK_DIR $MY_TARGET_DIR 
echo rm $MY_TARGET_DIR_p/*.jpg
echo rm $MY_TARGET_DIR_p/*.png
echo rm $MY_TARGET_DIR_p/*.ogg
echo rm $MY_TARGET_DIR_p/*.nes
echo python3 go.py $MY_TARGET_DIR $MY_XML

MY_XML=aso2003.xml
MY_GAME=ASOArmoredScrumObject
# Create a directory based on $MY_RAW_ROMS_DIR and $MY_XML
MY_TARGET_DIR_p=$MY_RAW_ROMS_DIR/$(basename $MY_XML .xml)
MY_TARGET_DIR="\"$MY_TARGET_DIR_p\""
echo mkdir -p $MY_TARGET_DIR_p
# Run quickbms to extract files related to the game $MY_GAME
echo $MY_QUICKBMS -f \"$MY_GAME*\" \"$MY_QUICKBMS_SCRIPT\" $MY_SNK_DIR $MY_TARGET_DIR 
#/home/lionel/provi/quickbms/quickbms -f "ASOArmoredScrumObject*" "/home/lionel/devel/snk_40th/python/tstXML/sf30_mbundle.bms" "/mnt/hugeEXT4/games/Windows/SNK 40th Anniversary Collection/Bundle/" "/home/lionel/provi/rawroms/aso2003"
#echo rm $MY_TARGET_DIR_p/*.jpg
#echo rm $MY_TARGET_DIR_p/*.png
#echo rm $MY_TARGET_DIR_p/*.ogg
#echo rm $MY_TARGET_DIR_p/*.nes
echo python3 go.py $MY_TARGET_DIR $MY_XML

