
# * This is the core file of the whole project.

# ? Made with love by Ansh Malviya.

# ! NOTE: If you want to create an executable file of this code and wish it pack it in a single file (using the '--onefile' arg), then remove codes from the following lines.
# ! 1. 'web/index.html', line 71-79: Remove/Comment whole code.
# ! 2. 'web/js/script.js', line 56: Remove/Comment the code.
# ! 3. 'web/js/script.js', line 62: Remove/Comment and replace the code with the one commented at line 63.
# ? These codes may not interfere when created a 'single-filed' executable but serve no purpose without the codes above. So you may/may not remove them, it is optional and totally on you.
# ? 1. 'YouTube Downloader.py', line 146-150: Remove/Comment the whole code.
# ? 2. 'web/index.html', line 157-185: Remove/Comment the whole code.
# ? 3. 'web/css/style.css', line 578-678: Remove/Comment the whole code.
# ? 4. 'web/js/script.js', line 103-189: Remove/Comment the whole code.
# ? 5. 'web/js/script.js', line 195-231: Remove/Comment the whole code.
# * If you want to create an executable without packing into one file or without the '--onefile' arg, you don't need to remove the codes mentioned above.

# ? Import required modules
import eel
from ssl import SSLError
from urllib.error import URLError
from pytube import YouTube, Stream
from shutil import move, copy
from os.path import join as join_path
from os import remove, makedirs, listdir
from tkinter.messagebox import showerror
from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio

# ? Initialize eel
eel.init("web")

@eel.expose
def create_yt_obj(link: str): 
    """
    Generates a YouTube Object from the link provided.
    Creates lists for available resolutions and streams.
    Called of JavaScript via eel.

    Args:
        link (str): YouTube Video URL.

    Returns:
        list: List of video title (str), video author/artist (str) and available resolutions (list).
    """
    
    global Streams
    global yt_obj
    global Vid_Streams
    
    try: 
        yt_obj = YouTube(link) 
        
        # ? Calls 'on_progress' function to keep updating the download progress on the download popup.
        yt_obj.register_on_progress_callback(on_progress)
        
        title = yt_obj.title
        author = yt_obj.author
        Streams = yt_obj.streams
    except SSLError as Error: 
        eel.show_popup("Couldn't generate YouTube Object", "It seems that the internet connection was disturbed while generating the YouTube Object. <br>Please make sure you have a <b>stable</b> internet connection and try again. <br><br> Error: " + str(Error))
        return
    except URLError: 
        eel.show_popup("Not Connected to Internet", "It seems you are not connected to the internet. <br>Please make sure you have an active internet connection and then try again. <br><br> Error: " + str(Error))
        return
    except Exception as Error:
        eel.show_popup("Invalid YouTube Link", "Failed to generate an YouTube Object via the given link. <br>Please make sure the link is valid and still exists on YouTube and then try again. <br><br>Error: " + str(Error))
        return
    
    Vid_Streams = Streams.filter(type = "video")
    
    # ? Generates a list of resolutions available of the provided YouTube Video, some resolutions may not be available if their progressive = True and no streams of same resolution is available of progressive = False, extremely rare chance and only for very old YouTube Videos.
    available_res = []
    for stream in Vid_Streams:
        if not stream.is_progressive and stream.resolution not in available_res: available_res.append(stream.resolution)
    
    return title, author, available_res

def on_progress(stream: Stream, chunks: bytes, bytes_remaining: int) -> None:
    """
    Updates the download progress popup with the percentage of file size downloaded individually for audio and video (if present).
    Called by pytube while downloading of the stream.

    Args:
        stream (Stream): The stream which is downloading.
        chunks (bytes): ...
        bytes_remaining (int): Number of bytes still remaining to be downloaded.
    """
    
    file_size = stream.filesize
    bytes_recieved = file_size - bytes_remaining
    percentage_completed = int((bytes_recieved/file_size)*100)
    
    eel.update_progress(percentage_completed, stream.type)

@eel.expose
def start_download(file_type: str, video_res: str or None = None, show_preview: bool = False):
    """
    Starts download of Audio and Video streams individually, then merges them into one video file for file_type = "Video".
    Starts download of Audio stream for file_type = "Audio".
    Moves files to the "Downloads" folder in the same directory as this file.
    Called by JavaScript via eel.

    Args:
        file_type (str): Video Type, either "Video" or "Audio".
        video_res (str or None, optional): Video Resolution selected for download. Defaults to None.
        show_preview (bool, optional): A boolean value to show preview or not, only applicable for file_type = "Video". Defaults to False.
    """
    
    if not video_res: video_res = "None"
    eel.update_dl_desc(yt_obj.title, video_res, file_type)
    
    # ? Filters out characters than may interfere in the file processing from the file name.
    invalid_chars = ["\"", "\\", "|", "/", "@", "$", "#", "%", "^", "*"]
    filtered_title = Streams[0].title
    
    for char in invalid_chars: filtered_title = filtered_title.replace(char, "")
    
    if file_type == "Audio":
        try: audio_file = Streams.filter(type = "audio")[0].download(filename = filtered_title + ".mp3")
        except Exception as Error: 
            eel.show_popup("Failed in Downloading the Audio", "There was an error while downloading the audio file. This may be caused due to disturbance in the download, or loss of the internet connection. <br>Please check you connection is proper and there is enough storage in your device and try again. <br><br>Error: " + str(Error))
            eel.reset_dl_popup()
            return
        
        try: move(filtered_title + ".mp3", join_path("Downloads", filtered_title + ".mp3"))
        except: 
            makedirs("Downloads")
            move(filtered_title + ".mp3", join_path("Downloads", filtered_title + ".mp3"))
            
        # ? If show_preview is True, then make a copy of the downloaded file in the 'temp_files' folder under 'web' folder so that JavaScript can access it.
        # ? This copy of the file will later be deleted when the localhost is exited.
        try: 
            if show_preview: copy(join_path("Downloads", filtered_title + ".mp3"), join_path("web", "temp_files", filtered_title + ".mp3"))
        except: 
            makedirs(join_path("web", "temp_files"))
            copy(join_path("Downloads", filtered_title + ".mp3"), join_path("web", "temp_files", filtered_title + ".mp3"))
        
        eel.reset_dl_popup()
        eel.after_download(file_type, join_path("..", "temp_files", filtered_title + ".mp3"), show_preview)
            
    else: 
        try:
            audio_file = Streams.filter(type = "audio")[0].download(filename = filtered_title + " (audio).mp3")
            
            try: video_file = Vid_Streams.filter(resolution = video_res)[1].download(filename = filtered_title + "(video).mp4")
            except: video_file = Vid_Streams.filter(resolution = video_res)[0].download(filename = filtered_title + "(video).mp4")
        
        except Exception as Error:
            eel.reset_dl_popup()
            eel.after_download(None, False)
            eel.show_popup("Failed in Downloading the Video", "There was an error while downloading the video. This may be caused due to disturbance in the download, or loss of the internet connection. <br>Please check you connection is proper and there is enough storage in your device and try again. <br><br>Error: " + str(Error))
            return
        
        eel.reset_dl_popup()
        ffmpeg_merge_video_audio(audio_file, video_file, filtered_title + ".mp4")
        
        try: move(filtered_title + ".mp4", join_path("Downloads", filtered_title + ".mp4"))
        except:
            makedirs("Downloads")
            move(filtered_title + ".mp4", join_path("Downloads", filtered_title + ".mp4"))
            
        remove(audio_file)
        remove(video_file)
        
        # ? If show_preview is True, then make a copy of the downloaded file in the 'temp_files' folder under 'web' folder so that JavaScript can access it.
        # ? This copy of the file will later be deleted when the localhost is exited.
        try: 
            if show_preview: copy(join_path("Downloads", filtered_title + ".mp4"), join_path("web", "temp_files", filtered_title + ".mp4"))
        except: 
            makedirs(join_path("web", "temp_files"))
            copy(join_path("Downloads", filtered_title + ".mp4"), join_path("web", "temp_files", filtered_title + ".mp4"))
        
        eel.after_download(file_type, join_path("temp_files", filtered_title + ".mp4"), show_preview)

@eel.expose
def clear_temp_files(route = None, websockets = None):
    """
    Clears the 'temp_files' folder.
    Terminates the program if route arg is not None.
    
    Called by JavaScript via eel (route will be None for this case, thus the program won't be terminated).
    Called by eel on closing the localhost (route will be 'index.html', thus the program will be terminated).

    Args:
        route (optional): Defaults to None.
        websockets (optional): Defaults to None.
    """

    try: 
        for file in listdir(join_path("web", "temp_files")): remove(join_path("web", "temp_files", file))
    except Exception as Error: pass
    if route: exit()

available_modes = ["chrome", "electron", "edge"]

for mode in available_modes:
    try: 
        eel.start("index.html", mode = mode, start = (900, 600), close_callback = clear_temp_files)
        break
    except Exception as Error: 
        if mode == available_modes[-1]: showerror("Couldn't Start Application", "It seems that you don't have any of the supported web browers. \n\nInstall any one of the following browsers and try again: \n    →Google Chrome \n    →Microsoft Edge \n    →Electron")