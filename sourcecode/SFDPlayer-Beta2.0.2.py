import os
import tkinter as tk
import sys
import shutil
import subprocess
import atexit
import zipfile

from tkinter import IntVar, messagebox, StringVar, Frame, LabelFrame, Label, Button, Toplevel, filedialog, ttk
from os import path
from sys import exit
from subprocess import run
from shutil import which
from atexit import register

currentdir = os.getcwd()

ffmpeg_exe_path = currentdir + '/resource/bin/ffmpeg/ffmpeg.exe'
ffplay_exe_path = currentdir + '/resource/bin/ffmpeg/ffplay.exe'
def check_for_ffmpeg():
 global ffmpeg_location_int
 global ffplay_location_int
 ffmpeg_location_int = IntVar()
 ffplay_location_int = IntVar()
 #FFmpeg location = 0 means its in SofdecVideoTools folder, 1 means its in PATH
 global previewmode
 previewmode = IntVar() #IntVar for detecting whether to disable buttons based on if FFmpeg is found or missing

 print("Checking for FFmpeg...")

 if os.path.isfile(ffmpeg_exe_path):
  print("FFmpeg.exe found (in SofdecVideoTools' bin folder)")
  ffmpeg_location_int.set(0)

 elif os.path.isfile('ffmpeg.exe'):
  print("FFmpeg.exe found (in root folder, moving to bin folder...)")
  shutil.move('ffmpeg.exe', ffmpeg_exe_path)
  print("FFmpeg.exe is now in the bin folder")
  ffmpeg_location_int.set(0)

 elif shutil.which('ffmpeg.exe'):
  print("FFmpeg.exe found (in PATH)")
  ffmpeg_location_int.set(1)
 else:
   print("FFmpeg.exe unable to be found")
   ffmpegmissing_message = tk.messagebox.askyesno('FFmpeg.exe missing', "FFmpeg (and related programs such as ffplay.exe) could not be found. FFmpeg is required to run these programs. Do you want to download FFmpeg? (This is about 400MB)")
   if ffmpegmissing_message:
    if os.path.isfile('ffmpeg.zip'):
     os.remove('ffmpeg.zip')
    if os.path.isfile('ffmpeg-master-latest-win64-gpl.zip'):
     os.remove('ffmpeg-master-latest-win64-gpl.zip')
    wget_location = os.getcwd() + '/resource/bin/wget.exe'
    downloadffmpeg=f'"{wget_location}" https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip'
    subprocess.run(downloadffmpeg, stderr=subprocess.STDOUT, shell=True)
    os.rename('ffmpeg-master-latest-win64-gpl.zip', 'ffmpeg.zip')
   
    with zipfile.ZipFile('ffmpeg.zip', 'r') as ffmpeg_zip:
     ffmpeg_zip.extractall(currentdir + '/resource/bin/ffmpeg')
     ffmpeg_zip.close()
     os.remove('ffmpeg.zip')
     ffmpeg_exe_extractedzip = currentdir + '/resource/bin/ffmpeg/ffmpeg-master-latest-win64-gpl/bin'
     ffmpeg_exe_newlocation_binfolder = currentdir + '/resource/bin/ffmpeg'
     shutil.move(ffmpeg_exe_extractedzip + '/ffmpeg.exe', ffmpeg_exe_newlocation_binfolder + '/ffmpeg.exe')
     shutil.move(ffmpeg_exe_extractedzip + '/ffprobe.exe', ffmpeg_exe_newlocation_binfolder + '/ffprobe.exe')
     shutil.move(ffmpeg_exe_extractedzip + '/ffplay.exe', ffmpeg_exe_newlocation_binfolder + '/ffplay.exe')
     shutil.rmtree(currentdir + '/resource/bin/ffmpeg/ffmpeg-master-latest-win64-gpl')
     print("FFmpeg installed!")
     ffmpeginstallmessage = tk.messagebox.showinfo(title='FFmpeg Installed', message='FFmpeg has been installed!')
   else:
    previewmode.set(1)
    print("FFmpeg (and/or related EXEs) not found, program launched in preview mode. SFD files will not be able to be created.")
    master.title("SFDPlayer Beta 2.0.2 (PREVIEW MODE)")


 if os.path.isfile(ffplay_exe_path):
  print("FFplay.exe found (in SofdecVideoTools' bin folder)")
  ffplay_location_int.set(0)

 elif os.path.isfile('ffplay.exe'):
  print("FFplay.exe found (in root folder, moving to bin folder...)")
  shutil.move('ffplay.exe', ffplay_exe_path)
  print("FFplay.exe is now in the bin folder")
  ffplay_location_int.set(0)

 elif shutil.which('ffplay.exe'):
  print("FFplay.exe found (in PATH)")
  ffplay_location_int.set(1)
 else:
   print("FFplay.exe unable to be found")
   ffmpegmissing_message = tk.messagebox.askyesno('FFmpeg.exe missing', "FFmpeg (and related programs such as ffprobe.exe) could not be found. FFmpeg is required to run these programs. Do you want to download FFmpeg? (This is about 400MB)")
   if ffmpegmissing_message:
    if os.path.isfile('ffmpeg.zip'):
     os.remove('ffmpeg.zip')
    if os.path.isfile('ffmpeg-master-latest-win64-gpl.zip'):
     os.remove('ffmpeg-master-latest-win64-gpl.zip')
    wget_location = os.getcwd() + '/resource/bin/wget.exe'
    downloadffmpeg=f'"{wget_location}" https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip'
    subprocess.run(downloadffmpeg, stderr=subprocess.STDOUT, shell=True)
    os.rename('ffmpeg-master-latest-win64-gpl.zip', 'ffmpeg.zip')
   
    with zipfile.ZipFile('ffmpeg.zip', 'r') as ffmpeg_zip:
     ffmpeg_zip.extractall(currentdir + '/resource/bin/ffmpeg')
     ffmpeg_zip.close()
     os.remove('ffmpeg.zip')
     ffmpeg_exe_extractedzip = currentdir + '/resource/bin/ffmpeg/ffmpeg-master-latest-win64-gpl/bin'
     ffmpeg_exe_newlocation_binfolder = currentdir + '/resource/bin/ffmpeg'
     shutil.move(ffmpeg_exe_extractedzip + '/ffmpeg.exe', ffmpeg_exe_newlocation_binfolder + '/ffmpeg.exe')
     shutil.move(ffmpeg_exe_extractedzip + '/ffprobe.exe', ffmpeg_exe_newlocation_binfolder + '/ffprobe.exe')
     shutil.move(ffmpeg_exe_extractedzip + '/ffplay.exe', ffmpeg_exe_newlocation_binfolder + '/ffplay.exe')
     shutil.rmtree(currentdir + '/resource/bin/ffmpeg/ffmpeg-master-latest-win64-gpl')
     print("FFmpeg installed!")
     ffmpeginstallmessage = tk.messagebox.showinfo(title='FFmpeg Installed', message='FFmpeg has been installed!')
   else:
    previewmode.set(1)
    print("FFmpeg (and/or related EXEs) not found, program launched in preview mode. SFD files will not be able to be created.")
    master.title("SFDPlayer Beta 2.0.2 (PREVIEW MODE)")


master = tk.Tk()
master.geometry("300x130"), master.title("SFDPlayer Beta 2.0.2"), master.resizable(False, False)#, master.iconbitmap("resource/icon/sfdplayer.ico")


audiomap = StringVar()
audiotracknumber = StringVar()
sfdfilepath = StringVar()
sfdname = StringVar()
outputdir_path = StringVar()
programresolution = StringVar()
aspectratio = StringVar()


programresolution.set('-x 640 -y 400') #Set FFplay box size
#aspectratio.set('-aspect 4:3')

def selectvideo():
 SFDfile = filedialog.askopenfilename(title="Select A SFD File", filetypes=[("SFD file", ".sfd")])
 sfdfilepath.set(SFDfile)
 sfdname.set(os.path.basename(sfdfilepath.get()))
 toggleplaybutton()


def playvideo():
 if sfdfilepath.get() == '':
  tk.messagebox.showerror('File Error', "No SFD was provided. Please provide an SFD to continue.")
  return

 global sfdfolder
 sfdfolder = os.getcwd() + f'/sfdfile/{sfdname.get()}'
 if os.path.exists("sfdfile"):
  if os.path.isfile(sfdfolder):
   if os.path.isfile(sfdname.get()):
    os.remove(sfdname.get())
    shutil.move(sfdfolder, os.getcwd())
  os.removedirs("sfdfile")
 if os.path.isfile(sfdname.get()): #if file exists in the same directory as SFDplayer, move it to a temp folder to prevent copy error
  os.mkdir("sfdfile")
  shutil.move(sfdname.get(), "sfdfile")
  sfdfilepath.set(sfdfolder)
 
 if os.path.exists(sfdfilepath.get()):
  outputdir = os.path.join(os.getcwd() + '/' + sfdname.get())
  shutil.copy(sfdfilepath.get(), outputdir)
  outputdir_path.set(outputdir)
  sfdname.set(os.path.basename(outputdir_path.get()))
  os.rename(sfdname.get(), 'sfd.sfd')


 #Set ffmpeg command properly if it's on the user's PATH
 if ffmpeg_location_int.get() == 1:
  ffmpeg_exe_path = 'ffmpeg.exe'
 else:
  ffmpeg_exe_path = currentdir + '/resource/bin/ffmpeg/ffmpeg.exe'
 if ffplay_location_int.get() == 1:
   ffplay_exe_path = 'ffplay.exe'
 else:
  ffplay_exe_path = currentdir + '/resource/bin/ffmpeg/ffplay.exe'


 print("")
 print("Copying SFD video...")
 command=f'"{ffmpeg_exe_path}" -i sfd.sfd -c:v copy -an sfd.mpeg'
 subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)

 if disableaudio.get() == 1:
  print("Disable audio checked, skipping audio conversion...")
 else:
  print("Converting audio to playable format...")
  command = f'"{ffmpeg_exe_path}" -y -i sfd.sfd -map {audiomap.get()} audio.mp3'
  subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)


 if os.path.isfile('audio.mp3'):
  min_file_size = 5
  file_size_kb = os.path.getsize('audio.mp3') // 5
  if file_size_kb < min_file_size:
   print("Audio track unable to be converted, no audio will be played alongside the SFD.")
   os.remove('audio.mp3')
 else:
  if disableaudio.get() == 1:
   pass
  else:
   print("No audio in selected audio track (or possibly any of the audio tracks), skipping audio...")


 if os.path.isfile('audio.mp3'):
  print("Putting extracted audio into video...")
  command=f'"{ffmpeg_exe_path}" -y -i sfd.mpeg -i audio.mp3 -c:v copy -c:a copy sfdwithaudio.mpeg'
  subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
  print(f"Playing {sfdname.get()} with audio track {audiotracknumber.get()}.")
 else:
  command=f'"{ffmpeg_exe_path}" -y -i sfd.mpeg -c:v copy sfdwithaudio.mpeg'
  subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
  print(f"Playing {sfdname.get()} without audio.")


 ffplaycmd=f'"{ffplay_exe_path}" {programresolution.get()} {aspectratio.get()} sfdwithaudio.mpeg'
 subprocess.run(ffplaycmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
 print("")


 if os.path.isfile('sfd.sfd'):
  os.remove('sfd.sfd')
 if os.path.isfile('sfdwithaudio.mpeg'):
  os.remove('sfdwithaudio.mpeg')
 if os.path.isfile('sfd.mpeg'):
  os.remove('sfd.mpeg')
 if os.path.isfile('audio.mp3'):
  os.remove('audio.mp3')


 if os.path.exists(sfdfolder):
  shutil.move(sfdfolder, os.getcwd())
  os.removedirs('sfdfile')

 return


def opendocspdf():
 sfdplayerdocs = os.getcwd() + '/resource/docs/documentation.pdf'
 os.startfile(sfdplayerdocs)

chooseSFD = Button(text="Browse", command=selectvideo, padx=45, pady=5).place(x=10, y=55)
playSFD = Button(text="Play SFD", command=playvideo, state=tk.DISABLED, padx=40, pady=5)
playSFD.place(x=155, y=55) #leave seperate to fix issue with "None"
opendocs = Button(text="Documentation", command=opendocspdf, padx=93).place(x=10, y=95) #padx=22

def toggleplaybutton():
 if sfdfilepath.get() == '':
  playSFD.config(state=tk.DISABLED)
 else:
  playSFD.config(state=tk.NORMAL)

vbitrate = StringVar()
vidbitrateselect = Label(text="Video Bitrate:", font = ("Arial Bold", 8)).place(x=4700, y=87)
videobitrateentry = ttk.Entry(textvariable=vbitrate, width=15)
videobitrateentry.place(x=5000, y=105)
vbitratevalue = f'-b:a {vbitrate.get()}'

audtrackselect = Label(text="Use Audio Track:", font = ("Arial Bold", 8)).place(x=179, y=8)
audiotracktype=IntVar(master, "1")
audiomap.set('0:a:0')
audiotracknumber.set('1')

OPTIONS_audiotracktype = ["Track 1", "Track 2", "Track 3", "Track 4"]
comboboxaudiotracktype = StringVar()
audiotracktypebox = ttk.Combobox(master, value=OPTIONS_audiotracktype, width=12)
audiotracktypebox.place(x=182, y=25)
audiotracktypebox.current(0)
audiotracktypebox.state(["readonly"])

def updateaudiotracktype(event):
   audiotracktypebox.selection_clear()
   selectedaudiotracktype = audiotracktypebox.get()
   if selectedaudiotracktype == "Track 1":
    audiotracktype.set("1")
    audiomap.set('0:a:0')
    audiotracknumber.set('1')
    audiotracktypebox.selection_clear()
   elif selectedaudiotracktype == "Track 2":
    audiotracktype.set("2")
    audiomap.set('0:a:1')
    audiotracknumber.set('2')
    audiotracktypebox.selection_clear()
   elif selectedaudiotracktype == "Track 3":
    audiotracktype.set("3")
    audiomap.set('0:a:2')
    audiotracknumber.set('3')
    audiotracktypebox.selection_clear()
   elif selectedaudiotracktype == "Track 4":
    audiotracktype.set("4")
    audiomap.set('0:a:3')
    audiotracknumber.set('4')
    audiotracktypebox.selection_clear()
audiotracktypebox.bind("<<ComboboxSelected>>", updateaudiotracktype)


disableaudio = IntVar()
def toggleaudiotrackselector():
 if disableaudio.get() == 1:
  audiotracktypebox.config(state=tk.DISABLED)
 else:
  audiotracktypebox.config(state=tk.NORMAL)
  audiotracknumber.set('1')
  audiomap.set('0:a:0')

disableaudiocheck = ttk.Checkbutton(text='Disable audio', variable=disableaudio, command=toggleaudiotrackselector, onvalue=1, offvalue=0)
disableaudiocheck.place(x=10, y=10)
disableaudio.set(1)
disableaudio.set(0)

def changeffplayresolution():
 if playatoriginalresolution.get() == 1:
  programresolution.set('')
 else:
  programresolution.set('-x 640 -y 400')

playatoriginalresolution = IntVar()
playatoriginalresolutioncheck = ttk.Checkbutton(text="Play at original resolution", variable=playatoriginalresolution, command=changeffplayresolution, onvalue=1, offvalue=0)
playatoriginalresolutioncheck.place(x=10, y=27)
playatoriginalresolution.set(1)
playatoriginalresolution.set(0)


def removefiles():
 if os.path.isfile('sfd.sfd'):
  os.remove('sfd.sfd')
 else:
  pass
 if os.path.isfile('sfdwithaudio.mpeg'):
  os.remove('sfdwithaudio.mpeg')
 else:
  pass
 if os.path.isfile('audio.mp3'):
  os.remove('audio.mp3')
 else:
  pass
 if os.path.isfile('sfd.mpeg'):
  os.remove('sfd.mpeg')
 else:
  pass
 #if os.path.exists(sfdfolder):
  #shutil.move(sfdfolder, os.getcwd())
  #os.removedirs('sfdfile')


def closeprogram():
  os.system("taskkill /f /im ffplay.exe")
  sys.exit(0)

def updater_exe():
 updaterlocation = os.getcwd() + '/updater.exe'
 if os.path.isfile(updaterlocation):
  runupdater = f'"{updaterlocation}"'
  subprocess.run(runupdater, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
 else:
  print("Unable to find updater.exe, program will not be able to update.")
  pass


check_for_ffmpeg()
removefiles() #Run removefiles() to delete any files that are left over on program boot.
updater_exe()

atexit.register(removefiles)
atexit.register(closeprogram)

master.mainloop()