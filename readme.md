# Advent of code Preparator 🎄 🎅

This scripts makes it possible to download a puzzle of a specific day and year of the Advent of Code challenges.  
The user needs to set their session cookie in the script so that the puzzles can be accessed.

Possible selections:  
**Years:** &ensp; 2015 .. year of last christmas  
**Days:** &ensp; 1 .. 25

The script also generates a **folder structure** based on the selected year and day and a basic **source code file**, so that no manual setup is necessary:
* The basic source code file reads in the input and prints it out
* The generated folders and files have the following structure:
    root/  
    └── AoC_\[Year\]/  
        └── \[Day\]_\[Language\]  
             ├── \[Day\]_1  
             |      ├── input.txt  
             |      └── 10_01.\[Language\]  
             └── \[Day\]_2  
                    ├── input.txt  
                    └── 10_02.\[Language\]  

