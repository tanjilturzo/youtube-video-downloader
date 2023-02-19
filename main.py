# complete 




from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.metrics import dp
from pytube import YouTube
import threading
from functools import partial
import os
import shutil

class Main_page(GridLayout):
    # file path
    download_path_video = os.getcwd() + "\\Download\\video\\"
    download_path_audio = os.getcwd() + "\\Download\\audio\\"

    # toggle for audio or video
    def switch_toggle(self, switchObject, switchvalue):
        if switchvalue:
            self.ids.status_label.text = "Audio only"
            self.ids.video_res.disabled = True
        else: 
            self.ids.status_label.text = "Video"
            self.ids.video_res.disabled = False

    # toggle for video resolution
    def video_res_toggle(self, switchObject, switchvalue):
        if switchvalue:
            self.ids.status_label.text = "2160p"
        else: 
            self.ids.status_label.text = "1080p"
        
    # main function
    def start_download(self, Widget):
        if Widget.state == "down":
            self.address_link = self.ids.download_link.text
            if self.address_link != "":
                link = self.address_link   
                if self.ids.switch_audio.active:
                    self.audio_thread = threading.Thread(target=self.download_audio, args=[link])
                    self.audio_thread.start()
                    self.download_status_downloading()

                else:
                    video_thread = threading.Thread(target=self.download_video, args=[link])
                    video_thread.start()
                    self.download_status_downloading()
            else:
                self.ids.status_label.text = "Enter a valid link"

    # for downloading audio
    def download_audio(self, link):
        yt = YouTube(link)
        audio_file = yt.streams.filter(file_extension= "mp4", type= "audio", abr="128kbps").first()
        audio_file.download(filename= "audio.mp4", output_path = self.download_path_audio)
        self.video_name = yt.title
        audio_file.on_complete(self.change_label(self.download_path_audio, self.video_name))
    
    # for downloading video 
    def download_video(self, link):
        if self.ids.video_res.active:
            # 4k video resolution
            yt = YouTube(link)
            self.download_audio(link)
            self.download_status_downloading()
            video_file_4k = yt.streams.filter(res = "2160p", progressive=False).first()
            video_file_4k.download(filename = "video.mp4" ,output_path = self.download_path_video)
            video_file_4k.on_complete(self.change_label(self.download_path_video, self.video_name))
            self.merge_files()
        else:
            # HD video resolution

            yt = YouTube(link)
            self.download_audio(link)
            self.download_status_downloading()
            video_file_hd = yt.streams.filter(res = "1080p", progressive=False).first()
            video_file_hd.download(filename = "video.mp4", output_path = self.download_path_video)
            video_file_hd.on_complete(self.change_label(self.download_path_video, self.video_name))
            self.merge_files()

    # function for changing the label. Takes a directory and name argument
    def change_label(self, location, video_name):
        self.ids.status_label.text = f"{video_name} \nis downloaded in {location}"
        self.download_status_not_downloading()

    # functions for changing the button. 
    def download_status_downloading(self):
        self.ids.status_button.text = f"downloading....."

    def download_status_not_downloading(self):
        self.ids.status_button.text = "Download"

    # Merges the files in shell using ffmpeg and delete the Download folder
    def merge_files(self):
        os.system(f"ffmpeg -i {self.download_path_video}video.mp4 -i {self.download_path_audio}audio.mp4 -c:v copy -c:a copy output.mp4")
        shutil.rmtree("Download") 

class YvDApp(App):
    pass

YvDApp().run()
