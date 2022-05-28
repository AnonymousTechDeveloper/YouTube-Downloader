
# * Setup file for installation of YouTube Downloader.
# ? Installs required modules and if working on windows environment, then it will give an option to create an executable.
# ? Creates executable without '--onefile' arg (expected size: 144-145 MB) if you wish to to create executable in a single file, then make sure you follow the steps mentioned in the 'YouTube Downloader.py' file.

import os, sys, shutil

required_modules = [
    'git+https://github.com/pytube/pytube', # ! Requires git to be installed, if you don't have git, then download the github repository 'https://github.com/pytube/pytube', then run 'setup.py' in that package.
    'eel',
    'moviepy'
    ]

generate_exe = False

generate_exe_input = input("\nGenerate an executable file?\nEnter 'Y'/'y' for yes or anything else for no.")
if generate_exe_input.lower() == "y": generate_exe = True

for module in required_modules: os.system("pip install " + module)
if generate_exe: 
    os.system("python -m eel \".\\YouTube Downloader.py\" .\\web\\ --noconsole -i icon.ico")
    shutil.move("dist\\YouTube Downloader", "YouTube Downloader")
    os.remove("dist")
    print("Generated Executable successfully! You are free to delete every file except the files in the 'YouTube Downloader' folder.")

else: os.system("py \"YouTube Downloader.py\"")