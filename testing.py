from pytube import Playlist, YouTube
from pytube.cli import on_progress
from pathlib import Path
from os.path import join
from os import listdir
from os.path import isfile
import os
path = join(r"F:\playlist\romantic")
print(path)
# onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
count=0
print(listdir(path)[0])
# for f in listdir(path):
#     if isfile(join(path, f)):
#         print(f)
from moviepy.editor import *
video = VideoFileClip(listdir(path)[0])
video.audio.write_audiofile(os.path.join(path,"a.mp3"))
# count +=1
print(count +"done")

# # print(onlyfiles)
#     converter = os.system('ffmpeg -i'+ f +'-codec' +f.replace(".mp4",".mp3"))
#     print(converter)
# url="https://www.youtube.com/watch?v=w--g30WTfBs"
# yt= YouTube(url,on_progress_callback=on_progress)
# stream = yt.streams.get_by_itag(140)
# # video title
# print(stream.title)
# download and save to the computer path.
# # stream.download(path)
#
# def get_yt_playlist(playlist=None):
#     """
#     Get the list of youtube urls. Playlist can be used to download playlist as well,
#     but there is no on_progress_callback hence I cannot get the progress bar for each videos.
#     :param playlist:
#         This is the url of the youtube playlist.
#     :return:
#         list of playlist urls.
#     """
#     pl = Playlist(playlist)
#     return [l for l in pl]
#
#
# def download_vid(url=None, path=None):
#     """
#     This function downloads the video from each playlist url,
#     the path is specified with the path keyword.
#     :param url:
#         youtube url
#     :param path:
#         path to save the video in your computer
#     :return:
#         None
#     """
#     # on_progress is a progress bar in the pytube3 module.
#     # the progress bar is shown in sys.stdout.
#     yt = YouTube(url, on_progress_callback=on_progress)
#     stream = yt.streams.get_by_itag(140)
#     # video title
#     print(stream.title)
#     # download and save to the computer path.
#     stream.download(path)
#
#
# if __name__ == "__main__":
#     """
#     This is an example using a youtube playlist.
#     I tried threading, but youtube will reset the connection.
#     So for this example is download one video after video finished,
#     which is very slow.
#     """
#     playlist = "https://www.youtube.com/watch?v=Ps4aVpIESkc&list=PL9bw4S5ePsEEqCMJSiYZ-KTtEjzVy0YvK"
#     collect_list = get_yt_playlist(playlist)
#     path = join(r"F:\playlist\romantic")
#     for pl in collect_list:
#         download_vid(url=pl, path=path)