# YouTube-Downloader
Download your favourite videos/songs from **YouTube**!

## Requirements
In order to use this software, you must have at least one of the following _browsers_:
* **Google Chrome**
* **Electron**
* **Microsoft Edge**

You **must** have _Python_ installed in your device.

It is also recommended to have _Git_ installed in your device for the installation of the reqired modules and packages.

## Installation
To install the software, you can simply run the **setup.py** file. When ran, it will prompt to either create an _executable_ (.exe file) or not, if you want to create an executable, then enter 'Y' or 'y', other values will ignore this step and executable won't be created.

The **setup.py** will install the required modules, alternatively, you can also install the following required modules using pip.
* **MoviePy**:  `pip install moviepy`
* **Eel**:  `pip install eel`
* **PyTube**:  It is recommanded to use the GitHub version on pytube since they are of the latest version and pip version of pytube contains some bugs. Use `pip install git+https://github.com/pytube/pytube` command to install it, note that this need _Git_ to be installed in your device. If you don't have _Git_ installed, then download it manually from the [GitHub page of the module](https://github.com/pytube/pytube) and run **setup.py** file from it.

Once the required files are installed, simply run **YouTube Downloader.py** or **YouTube Downloader.exe** (if created an executable) to use the software.

## Eel
Eel is a little Python library for making simple Electron-like offline HTML/JS GUI apps, with full access to Python capabilities and libraries.

Eel allows the use of _HTML_ and _CSS_ to create attractive GUI that an communicate with _Python_ via _JavaScript_. It is simple and gives great results.

You can visit Eel's GitHub page using the [this link](https://github.com/ChrisKnott/Eel).

## How to use
All you need is a _YouTube link_ to download your video. You can simply copy the link address from the video you want to download.

Once you have the YouTube link, paste it in the textbox in the home tab and click the _Continue_ button and wait till it generates a YouTube Object from it, once done, it will take you to the configurations menu where you can set the following attributes: 
* **File Type:** Set which type of file you want to download (defaults to '_Video_').
* **Video Resolution**: Set resolution of video you want to download (defaults to the highest Video Resolutions).
* **Show Preview**: A boolean value based on the state of the check slider. If you want a quick preview for the video/audio, you can turn it on, audio preview comes with an _audio visualizer_ as well. **Note: this is not recommended for very large files.** 

After setting the values of your wish, click on _Download_ button, it will start the download of the streams individually for both audio and video (if present) and then merge them together. 
If the _Show Preview_ slider was 'on', then it will generate a copy of the downloaded file in 'web/temp_files' folder so that JavaScript can access it, this copy will be automatically deleted when you exit the application.

## Known Problems
There are no **Known Problems** yet, if you face one, feel free to inform me in the _issues_ section. I will try to fix as many problems as I can.

## Some Screenshots
![image](https://user-images.githubusercontent.com/76505499/170830547-b18aecb4-e952-4861-8caa-7ad5c3dc137e.png)
![image](https://user-images.githubusercontent.com/76505499/170830560-141a409a-c4eb-47af-bf25-15a166816ae9.png)
![image](https://user-images.githubusercontent.com/76505499/170830575-da3a81ed-8be8-4837-be7b-8f6470960842.png)

**Hope you like this software.**
**Made with love by _Ansh Malviya_**
