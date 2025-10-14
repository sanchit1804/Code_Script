A simple Python CLI tool that calculates the total size of a folder along with the size of the files and subfolders within it.

Features:
- Calculates total folder and subfolder sizes recursively.
- Displays sizes of both subfolders and individual files.
- Outputs total size of the entire directory.
- Displays sizes in human-readable format (KB, MB, GB).

Usage:
'''bash
python folder_size_calculator.py 

Example usage:
python folder_size_calculator.py "D:\Games"

Output:

Calculating folder sizes inside: D:\Games

Game1/                                     = 2.34 GB
Game2/                                     = 512.43 MB
notes.txt                                  = 12.40 KB
Total size of 'D:\Games': 2.85 GB
