# oagamepack_scripts
Script to generate the Radiant ent file from csv files.

Requires python3 and pandas.
I had hoped to only use pure python without libraries but the build in csv reader was not good enough.


./create_ent.py will print the ent file to stdout.

There are no keys at the moment. Only descriptions from the source.

Notes:
The panda package is called python3-pandas in Ubuntu.

Output is located in the output folder.

# License
Data in entities.csv is extracted from OpenArena source and is under GPLv2 or later and so is the rest of the data and therefore also the result.
The script is MIT licensed.
