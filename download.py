import shutil
import sys

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from shutil import move
import time

download_folder = "C:/Users/luluz/Downloads"
zip_folder = download_folder+"/Zip"
power_point_folder = download_folder+"/Power Points"
exe_folder = download_folder+"/Exe"
pictures_folder = download_folder+"/Pictures"
pdf_folder = download_folder+"/PDF"
rom_folder = download_folder+"/Rom"
videos_folder = download_folder+"/Videos"
gifs_folder = download_folder+"/Gifs"
excel_folder = download_folder+"/Excels"
word_folder = download_folder+"/Words"

zip_formats = ("zip")
power_point_formats = ("pptx", "pptm", "ppt")
exe_formats = ("exe")
picture_formats = ("jpg", "jpeg", "png", "ai", "tiff")
pdf_formats = ("pdf")
rom_formats = ("gba", "nds")
video_formats = ("webm", "flv", "avi", "mov", "qt", "mp4", "m4v", "svi", "flv")
gif_formats = ("gif", "gifv")
excel_formats = ("csv", "xlsx")
word_formats = ("docx")

zip = {zip_folder: zip_formats}
power_point = {power_point_folder: power_point_formats}
exe = {exe_folder: exe_formats}
picture = {pictures_folder: picture_formats}
pdf = {pdf_folder: pdf_formats}
rom = {rom_folder: rom_formats}
video = {videos_folder: video_formats}
gif = {gifs_folder: gif_formats}
excel = {excel_folder: excel_formats}
words = {word_folder: word_formats}

extension_list = [zip, power_point, exe, picture, pdf, rom, video, gif, excel, words]

counter = 0


def move_file(name, destination):
    global counter
    source = download_folder + f"/{name}"

    try:
        move(source, destination)
        print(f"{source} was moved to {destination}")
        print(f"Moving operation completed")
        counter = 0

    except shutil.Error:
        name_elements_before_dot = name.split(".")
        name_before_dot = "".join(name_elements_before_dot[0:-1])
        old_counter_str_reversed = str(counter)[::-1]
        counter += 1

        if counter == 1:
            new_name_before_dot = name_before_dot + str(counter)

        else:
            new_counter_str_reversed = str(counter)[::1]
            new_name_before_dot = name_before_dot[::-1].replace(old_counter_str_reversed, new_counter_str_reversed)[
                                  ::-1]

        new_name = new_name_before_dot + "." + name_elements_before_dot[-1]
        new_source = download_folder + f"/{new_name}"
        os.rename(source, new_source)
        print(f"The file {name} already existed so it was renamed {new_name}")
        move_file(new_name, destination)


def clean_all_folder():
    with os.scandir(download_folder) as download:
        for file in download:
            for extension in extension_list:
                elements = list(extension.items())
                folder = elements[0][0]
                formats = elements[0][1]
                if file.name.endswith(formats):
                    print("Moving operation starting")
                    move_file(file.name, folder)


class check_telechargement(FileSystemEventHandler):

    def __init__(self):
        super(check_telechargement, self).__init__()

    def on_created(self, event):
        time.sleep(1)
        name = event.src_path.split("\\")[1]
        with os.scandir(download_folder) as download:
            for file in download:
                if file.name == name:
                    for extension in extension_list:
                        elements = list(extension.items())
                        folder = elements[0][0]
                        formats = elements[0][1]
                        if file.name.endswith(formats):
                            print("Moving operation starting")
                            move_file(name, folder)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        if sys.argv[1] == "clean_all_folder":
            print("Cleaning all folders")
            clean_all_folder()
            exit()
    observer = Observer()
    event_handler = check_telechargement()
    observer.schedule(event_handler, path=download_folder, recursive=True)
    observer.start()
    print("Starting the download tracking program")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Terminating the download tracking program")

    observer.join()
