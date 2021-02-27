# go.py

go.py is a Python script to convert eight games from the "SNK 40th Anniversary Collection" (PC version) to MAME 2003 ROMS.

## List of games converted by the script

The games are:

* Marvin's Maze
* Athena
* Guerrilla War
* Ikari Warriors
* TNK III
* Paddle Mania
* Victory Road
* Alpha Mission (ASO: Armored Scrum Object)

## Installation

Place all the files in a directory of your choice. The files are:

    go
    go.py
    marvinsmaze2003.xml
	athena2003.xml
	guerrillawar2003.xml
	ikari2003.xml
	tank32003.xml
	paddlemania2003.xml
	victoryroad2003.xml
	aso2003.xml

## Usage

1. Install the software quickbms from Luigi Auriemma (https://aluigi.altervista.org/quickbms.htm)
2. Download the script to extract files from mbundles files. It's available from Luigi Auriemma web site: "Sf30 Mbundle . Street Fighter 30th Anniversary Collection mbundle". Rename it to "sf30_mbundle.bms" (with no space in the name). It is available here: [sf30_mbundle.bms](https://aluigi.altervista.org/bms/sf30_mbundle.bms)
3. Edit the script "go" to set the variables MY_QUICKBMS, MY_QUICKBMS_SCRIPT, MY_SNK_DIR, MY_RAW_ROMS_DIR to the right paths:
  - MY_QUICKBMS should point to the directory in which quickbms is located.
  - MY_QUICKBMS_SCRIPT should point to the directory where "sf30_mbundle.bms" is located.
  - MY_SNK_DIR should point to a directory with a copy of the "Bundle" directory. Example: "/mnt/hugeEXT4/games/Windows/SNK 40th Anniversary Collection/Bundle/"
  - MY_RAW_ROMS_DIR should point to a directory where you have (or will have, once extracted by quickbms) the eight games. These files are not usable by MAME.
4. Run the script `./go`: it only outputs text (with echo commands) and does not perform any operation.
5. If things seem correct to you (no errors) run the script again with redirection to a text file:
`./go >a.txt`

Choose step 6, 7 or 8:

6. If you only want to extract the files from the mbundle file, use the following commands:
grep -vw python3 a.txt >a1.txt
The file a1.txt should contain the commands to extract the relevant files without converting them to MAME ROMs. You may start the command with:
`bash a1.txt`
7. If you only want to convert the files extracted from the mbundle file to ROMS compatible with MAME, use the following command:
`grep -w python3 a.txt >a1.txt`
`bash a1.txt`
8. If you want to extract the files from the mbundle and convert them to ROMS compatible with MAME, use :
`bash a.txt`

Example:

	python3 go.py "/home/lionel/provi/rawroms/ikari2003" ikari2003.xml

Output:

	List of complete ROM sets:
	['ikari', 'ikarijp']
	List of missing files:
	[('ikarijpb', 'ik1')]
It means that it created a complete romset for `ikari` and `ikarijp`. It also tried to create `ikarijpb`, however, the file `ik1` was missing  to create the romset `ikarijpb`.

## Background and information

A useful script to extract and convert games from "SNK 40th Anniversary Collection" (PC version) is available as STEAM-865940.sh from Vaiski at: https://gitlab.com/vaiski/romextract. Another one in Python is here: https://github.com/ValadAmoleo/sf30ac-extractor/tree/mame

I wrote a first python script as STEAM-865940.sh did not extract some of the games that I wanted and that were in "SNK 40th Anniversary Collection": (Marvin's Maze, Ikari Warrior, Athena and a few others). The method used is a brute force approach:

	1. Set i=0.
	2. Take N bytes from the original file starting at index i.
	N is the length of the target file for MAME (as given in mame2003-plus.xml file).
	3. Compute the CRC32: if it matches, compute the SHA1.
	If the SHA1 matches, then save the N bytes as the MAME file. Exit.
	4. i=i+1 and go to step 2.

As it turns out, it was more complex than what I expected:

* Problem 1. Some files (3 pal files) were not only saved as one file, with three nibbles (4 bits) packed as two bytes, but they were also scrambled in some games (example: athena).
* Problem 2. Some files from `paddlemania2003.xml` were missing.
* Problem 3. Some files for Bermuda Triangle, Psycho Soldier and World Wars are missing (five pal files are needed, my script can only find three).

I solved problem 1 using brute force, by testing all the combinations of 12 bits (3 x 4 bits) until the CRC matches.
I solved problem 2 by splitting all the files into two files, with the odd bytes going into one file and the even bytes going into another one.
I never solved problem 3: feel free to investigate how to extract the two missing pal files: `btj_h.prm` and `btj_v.prm` for the games bermudat (Bermuda Triangle), worldwar (World Wars) and psychos (Psycho Soldier).

Feel free to investigate how to solve problem 3!

## Contributing

Feel free to fork this code, and to solve problem 3!

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.




