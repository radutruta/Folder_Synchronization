Dependencies:
-are listed in requirements.txt

How to:

Script requires the following mandatory parameters: 
-s: source directory path; 
-r: replica directory path;
-f: expected frequency expressed in seconds; 
-f: log file name and path desired. 

Command example:
python synchronize_folders.py -s ~/Folder1 -r ~/Folder2 -f 5 -l ~/Test.txt
