import tkinter as tk
import os
import shutil
import webbrowser
import atexit
import subprocess
import zipfile

from tkinter import filedialog, ttk, messagebox, Frame, LabelFrame, Label, StringVar, Button, Toplevel, IntVar, BooleanVar
from os import path, startfile, getcwd, system
from shutil import which, copy, move, rmtree
from webbrowser import open
from atexit import register
from subprocess import run

currentdir = os.getcwd()

ffmpeg_exe_path = currentdir + '/resource/bin/ffmpeg/ffmpeg.exe'
ffprobe_exe_path = currentdir + '/resource/bin/ffmpeg/ffprobe.exe'
def check_for_ffmpeg():
 global ffmpeg_location_int
 global ffprobe_location_int
 #FFmpeg location = 0 means its in SofdecVideoTools folder, 1 means its in PATH
 global previewmode
 previewmode = IntVar() #IntVar for detecting whether to disable buttons based on if FFmpeg is found or missing

 print("Checking for FFmpeg...")

 if os.path.isfile(ffmpeg_exe_path):
  print("FFmpeg.exe found (in SofdecVideoTools' bin folder)")
  ffmpeg_location_int = 0

 elif os.path.isfile('ffmpeg.exe'):
  print("FFmpeg.exe found (in root folder, moving to bin folder...)")
  shutil.move('ffmpeg.exe', ffmpeg_exe_path)
  print("FFmpeg.exe is now in the bin folder")
  ffmpeg_location_int = 0

 elif shutil.which('ffmpeg.exe'):
  print("FFmpeg.exe found (in PATH)")
  ffmpeg_location_int = 1
 else:
   print("FFmpeg.exe unable to be found")
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
    master.title("SFDCreator Beta 2.0.2 (PREVIEW MODE)")



 if os.path.isfile(ffprobe_exe_path):
  print("FFprobe.exe found (in SofdecVideoTools' bin folder)")
  ffprobe_location_int = 0
 
 elif os.path.isfile('ffprobe.exe'):
  print("FFprobe.exe found (in root folder, moving to bin folder...)")
  shutil.move('ffprobe.exe', ffprobe_exe_path)
  print("FFprobe.exe is now in the bin folder")
  ffprobe_location_int = 0
 
 elif shutil.which('ffprobe.exe'):
   print("FFprobe.exe found (in PATH)")
   ffprobe_location_int = 1
 else:
   print("FFprobe.exe unable to be found")
   ffmpegmissing_message = tk.messagebox.askyesno('FFprobe.exe missing', "FFmpeg (and related programs such as ffprobe.exe) could not be found. FFmpeg is required to run these programs. Do you want to download FFmpeg? (This is about 400MB)")
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
    master.title("SFDCreator Beta 2.0.2 (PREVIEW MODE)")
 print("")

master = tk.Tk()
master.geometry("600x450"), master.title("SFDCreator Beta 2.0.2"), master.resizable(False, False)#, master.iconbitmap("resource/icon/sfdextractor.ico")
dirframe = LabelFrame(master, text="Input Files")
dirframe.place(relx=0.010, rely=0.0, relheight=0.365, relwidth=0.980) #leave this .place seperate from the "dirframe =" to avoid position issue.
outputdirframe = LabelFrame(master, text="Output File").place(relx=0.010, rely=0.37, relheight=0.368, relwidth=0.980)
otherframe = LabelFrame(master, text="Other").place(relx=0.010, rely=0.745, relheight=0.250, relwidth=0.550)

def GetVideo():
 video = filedialog.askopenfilename(title="Select A Video File", filetypes=[("Video files", ".mpeg .mpg .mp4 .avi .wmv .mkv .mov")])
 filePathvideo.set(video)
 if autoinputvideoaudio.get() == 1:
  filePathaudt1.set(filePathvideo.get())
  filePathaudt2.set(filePathvideo.get())
  entryaud1.focus()
  entryaud1.xview_moveto(1)
  entryaud1.focus_set()
  entryaud2.focus()
  entryaud2.xview_moveto(1)
  entryaud2.focus_set()
 if setSFDfilenametovideofilename.get() == 1:
  UsevideonameforSFD()
 if setoutputdirectorytovideodirectory.get() == 1:
  setdirectorytovideodirectory()
 entryvid.focus()
 entryvid.xview_moveto(1)
 entryvid.focus_set()
 entryDir.focus()
 entryDir.xview_moveto(1)
 entryDir.focus_set()

def GetAud1():
 audt1 = filedialog.askopenfilename(title="Select A Audio File for Track 1", filetypes=[("Audio files", ".wav .mp3 .flac .mp2 .adx .ogg .mpeg .mpg .mp4 .avi .mkv .mov")])
 filePathaudt1.set(audt1)
 entryaud1.focus()
 entryaud1.xview_moveto(1)
 entryaud1.focus_set()

def GetAud2():
 audt2 = filedialog.askopenfilename(title="Select A Audio File for Track 2", filetypes=[("Audio files", ".wav .mp3 .flac .mp2 .adx .ogg .mpeg .mpg .mp4 .avi .mkv .mov")])
 filePathaudt2.set(audt2)
 entryaud2.focus()
 entryaud2.xview_moveto(1)
 entryaud2.focus_set()

def ChooseExportDir():
 exportpath = filedialog.askdirectory(title="Choose An Output Directory")
 dirPath.set(exportpath)
 if not os.path.exists(dirPath.get()):
  tk.messagebox.showerror(title='Directory Error', message="Can't find the directory selected. Try again, or select a different directory.")
 entryDir.focus()
 entryDir.xview_moveto(1)
 entryDir.focus_set()

def videoaudio():
 if UseVideoAudio.get() == 1:
  filePathaudt1.set(filePathvideo.get())
  entryaud1.focus()
  entryaud1.xview_moveto(1)
  entryaud1.focus_set()
  if UseTrack1forTrack2.get() == 1:
   filePathaudt2.set(filePathvideo.get())
   entryaud2.focus()
   entryaud2.xview_moveto(1)
   entryaud2.focus_set()
 if UseVideoAudio.get() == 0:
  filePathaudt1.set("")
  if UseTrack1forTrack2.get() == 1:
   UseTrack1forTrack2.set(0)
   filePathaudt2.set("")
   entryaud2.focus()
   entryaud2.xview_moveto(1)
   entryaud2.focus_set()

def copyaudio():
 if UseTrack1forTrack2.get() == 1:
  filePathaudt2.set(filePathaudt1.get())
  entryaud2.focus()
  entryaud2.xview_moveto(1)
  entryaud2.focus_set()
 if UseTrack1forTrack2.get() == 0:
  filePathaudt2.set("")

def docs():
  sfdcreatordocs = os.getcwd() + '/resource/docs/documentation.pdf'
  os.startfile(sfdcreatordocs)


def advancedopt():
  global optwin
  global crfvalue
  crfvalue = StringVar()
  global usebitexact
  usebitexact = IntVar()
  
  optwin = Toplevel(master)
  optwin.geometry("600x400"), optwin.title("Extra Options"), optwin.resizable(False, False)
  ffmpegsettingsframe = LabelFrame(optwin, text="Additional FFmpeg Settings").place(relx=0.010, rely=0.005, relheight=0.350, relwidth=0.983)
  qualitysettings = LabelFrame(optwin, text="QoL Settings").place(relx=0.010, rely=0.365, relheight=0.28, relwidth=0.41)
  miscprogramsettingsframe = LabelFrame(optwin, text="Misc. Program Settings").place(relx=0.43, rely=0.365, relheight=0.280, relwidth=0.561)
  keepframe = LabelFrame(optwin, text="Keep File(s)").place(relx=0.010, rely=0.67, relheight=0.31, relwidth=0.41)
  #issueframe = LabelFrame(optwin, text="Report an Issue/Bug").place(relx=0.43, rely=0.77, relheight=0.21, relwidth=0.56)

  AVI = ttk.Checkbutton(optwin, text='Keep converted AVI file', variable=keepAVI, onvalue=1, offvalue=0).place(x=11, y=286)
  MPEG = ttk.Checkbutton(optwin, text='Keep converted MPEG file', variable=keepMPEG, onvalue=1, offvalue=0).place(x=11, y=305)
  ADX = ttk.Checkbutton(optwin, text='Keep converted ADX file(s)', variable=keepADX, onvalue=1, offvalue=0).place(x=11, y=324)
  WAV = ttk.Checkbutton(optwin, text='Keep converted MP3/WAV file(s)', variable=keepWAV, onvalue=1, offvalue=0).place(x=11, y=343)
  log = ttk.Checkbutton(optwin, text='Keep sfdmux log file', variable=keepsfdmuxlog, onvalue=1, offvalue=0).place(x=11, y=362)

  crfentry = ttk.Entry(optwin, textvariable=crfvalue, width=12)
  crfentry.insert(0, "")
  crfentry.place(x=11, y=41)
  crflbl = Label(optwin, text="CRF Value:", font=("Arial Bold", 8)).place(x=8, y=21)

  if crfentry.get() == '':
   crfentry.insert(0, "01")

  bitexactcheck = ttk.Checkbutton(optwin, text='Use -bitexact for audio', variable=usebitexact, onvalue=1, offvalue=0).place(x=11, y=70)

  global useWAVforconversion
  global audiofiletype
  useWAVforconversion = BooleanVar()
  audiofiletype = StringVar()
  useWAVforADXconversion = ttk.Checkbutton(optwin, text='Use WAV for conversion to ADX', variable=useWAVforconversion, onvalue=1, offvalue=0).place(x=11, y=90)

  OPTIONS_ffmpegloglevel = ["No Command", "Error + Hide Banner", "Error", "Warning", "Fatal", "Loglevel 0"]

  comboboxffmpegloglevel = StringVar()
  global ffmpegloglevel
  ffmpegloglevel = StringVar()
  ffmpegloglevelbox = ttk.Combobox(optwin, value=OPTIONS_ffmpegloglevel, width=18)
  ffmpegloglevelbox.place(x=100, y=41)
  ffmpegloglevelbox.current(0)
  ffmpegloglevelbox.state(["readonly"])
  ffmpegloglevellbl = Label(optwin, text="FFmpeg Loglevel:", font=("Arial Bold", 8)).place(x=97, y=21)

  def updateffmpegloglevel(*args):
   ffmpegloglevelbox.selection_clear()
   selectedaudiotracktype = ffmpegloglevelbox.get()
   if selectedaudiotracktype == "No Command":
    ffmpegloglevel.set("")
    ffmpegloglevelbox.selection_clear()
   elif selectedaudiotracktype == "Error + Hide Banner":
    ffmpegloglevel.set("-hide_banner -loglevel error")
    ffmpegloglevelbox.selection_clear()
   elif selectedaudiotracktype == "Error":
    ffmpegloglevel.set("-loglevel error")
    ffmpegloglevelbox.selection_clear()
   elif selectedaudiotracktype == "Warning":
    ffmpegloglevel.set("-loglevel warning")
    ffmpegloglevelbox.selection_clear()
   elif selectedaudiotracktype == "Fatal":
    ffmpegloglevel.set("-loglevel fatal")
    ffmpegloglevelbox.selection_clear()
   elif selectedaudiotracktype == "Loglevel 0":
    ffmpegloglevel.set("-loglevel 0")
    ffmpegloglevelbox.selection_clear()

  ffmpegloglevel.trace_add('write', updateffmpegloglevel)
  updateffmpegloglevel()
  ffmpegloglevelbox.bind("<<ComboboxSelected>>", updateffmpegloglevel)

  OPTIONS_ffmpegspeedpreset = ["Ultrafast", "Superfast", "Veryfast", "Faster", "Fast", "Medium (Default)", "Slow", "Slower", "Very Slow"]

  comboboxffmpegspeedpreset = StringVar()
  global ffmpegspeedpreset
  ffmpegspeedpreset = StringVar()
  ffmpegspeedpresetbox = ttk.Combobox(optwin, value=OPTIONS_ffmpegspeedpreset, width=18)
  ffmpegspeedpresetbox.place(x=960, y=41) #ffmpegspeedpresetbox.place(x=260, y=41)
  ffmpegspeedpresetbox.current(5)
  ffmpegspeedpresetbox.state(["readonly"])
  #ffmpegspeedpresetlbl = Label(optwin, text="FFmpeg Speed Preset:", font=("Arial Bold", 8)).place(x=257, y=21)

  def updateffmpegspeedpreset(*args):
   ffmpegspeedpresetbox.selection_clear()
   selectedspeedpresettype = ffmpegspeedpresetbox.get()
   if selectedspeedpresettype == "Ultrafast":
    ffmpegspeedpreset.set("-preset ultrafast")
    ffmpegspeedpresetbox.selection_clear()
   elif selectedspeedpresettype == "Superfast":
    ffmpegspeedpreset.set("-preset superfast")
    ffmpegspeedpresetbox.selection_clear()
   elif selectedspeedpresettype == "Veryfast":
    ffmpegspeedpreset.set("-preset veryfast")
    ffmpegspeedpresetbox.selection_clear()
   elif selectedspeedpresettype == "Faster":
    ffmpegspeedpreset.set("-preset faster")
    ffmpegspeedpresetbox.selection_clear()
   elif selectedspeedpresettype == "Fast":
    ffmpegspeedpreset.set("-preset fast")
    ffmpegspeedpresetbox.selection_clear()
   elif selectedspeedpresettype == "Medium (Default)":
    ffmpegspeedpreset.set("-preset medium")
    ffmpegspeedpresetbox.selection_clear()
   elif selectedspeedpresettype == "Slow":
    ffmpegspeedpreset.set("-preset slow")
    ffmpegspeedpresetbox.selection_clear()
   elif selectedspeedpresettype == "Slower":
    ffmpegspeedpreset.set("-preset slower")
    ffmpegspeedpresetbox.selection_clear()
   elif selectedspeedpresettype == "Very Slow":
    ffmpegspeedpreset.set("-preset veryslow")
    ffmpegspeedpresetbox.selection_clear()

  ffmpegspeedpreset.trace_add('write', updateffmpegspeedpreset)
  updateffmpegspeedpreset()
  ffmpegspeedpresetbox.bind("<<ComboboxSelected>>", updateffmpegspeedpreset)

  global enablevideoffmpegduration
  global videostarttimedurationvalue
  global videoendtimedurationvalue
  enablevideoffmpegduration = BooleanVar()
  videostarttimedurationvalue = StringVar()
  videoendtimedurationvalue = StringVar()
  
  global videostarttimeentry
  videostarttimeentry = ttk.Entry(optwin, state=tk.DISABLED, textvariable=videostarttimedurationvalue, width=11)
  videostarttimeentry.insert(0, "")
  videostarttimeentry.place(x=247, y=61)

  global videoendtimeentry
  videoendtimeentry = ttk.Entry(optwin, state=tk.DISABLED, textvariable=videoendtimedurationvalue, width=11)
  videoendtimeentry.insert(0, "")
  videoendtimeentry.place(x=330, y=61)

  def toggledurationentriesstate():
    if enablevideoffmpegduration.get() == 1:
     videostarttimeentry.config(state=tk.NORMAL)
     videoendtimeentry.config(state=tk.NORMAL)
    else:
     videostarttimeentry.config(state=tk.DISABLED)
     videoendtimeentry.config(state=tk.DISABLED)

  enablecustomdurationcheck = ttk.Checkbutton(optwin, text='Use custom video duration', variable=enablevideoffmpegduration, command=toggledurationentriesstate, onvalue=1, offvalue=0)
  enablecustomdurationcheck.place(x=244, y=18)

  durationstarttimelbl = Label(optwin, text="Start Time:", font=("Arial Bold", 8)).place(x=242, y=40)
  durationendtimelbl = Label(optwin, text="Clip Length:", font=("Arial Bold", 8)).place(x=326, y=40)

  global enableaudioffmpegduration
  global audiostarttimedurationvalue
  global audioendtimedurationvalue
  enableaudioffmpegduration = BooleanVar()
  audiostarttimedurationvalue = StringVar()
  audioendtimedurationvalue = StringVar()
  
  global audiostarttimeentry
  audiostarttimeentry = ttk.Entry(optwin, state=tk.DISABLED, textvariable=audiostarttimedurationvalue, width=11)
  audiostarttimeentry.insert(0, "")
  audiostarttimeentry.place(x=425, y=61)

  global audioendtimeentry
  audioendtimeentry = ttk.Entry(optwin, state=tk.DISABLED, textvariable=audioendtimedurationvalue, width=11)
  audioendtimeentry.insert(0, "")
  audioendtimeentry.place(x=505, y=61)

  def toggledurationentriesstate():
    if enableaudioffmpegduration.get() == 1:
     audiostarttimeentry.config(state=tk.NORMAL)
     audioendtimeentry.config(state=tk.NORMAL)
    else:
     audiostarttimeentry.config(state=tk.DISABLED)
     audioendtimeentry.config(state=tk.DISABLED)

  enableaudiocustomdurationcheck = ttk.Checkbutton(optwin, text='Use custom audio duration', variable=enableaudioffmpegduration, command=toggledurationentriesstate, onvalue=1, offvalue=0)
  enableaudiocustomdurationcheck.place(x=423, y=18)

  audiodurationstarttimelbl = Label(optwin, text="Start Time:", font=("Arial Bold", 8)).place(x=421, y=40)
  audiodurationendtimelbl = Label(optwin, text="Clip Length:", font=("Arial Bold", 8)).place(x=502, y=40)
  
  global useidenticalcustomdurations
  useidenticalcustomdurations = IntVar()
  useidenticalcustomdurations.set(0)  #Fix for the checkbox automatically being ticked
  identicaldurations = ttk.Checkbutton(optwin, text='Use custom video duration for audio', variable=useidenticalcustomdurations, onvalue=1, offvalue=0)
  identicaldurations.place(x=11, y=110)

  previous_audstartdurationvalue = StringVar()
  previous_audenddurationvalue = StringVar()
  def changedurationvalues(*args):
    if useidenticalcustomdurations.get() == 1:
     previous_audstartdurationvalue.set(audiostarttimedurationvalue.get())
     previous_audenddurationvalue.set(audioendtimedurationvalue.get())
     audioendtimeentry.delete(0, tk.END)
     audioendtimeentry.insert(0, audioendtimedurationvalue.get())
     audiostarttimeentry.delete(0, tk.END)
     audiostarttimeentry.insert(0, audiostarttimedurationvalue.get())
     if useidenticalcustomdurations.get() == 1:
      audiostarttimedurationvalue.set(videostarttimedurationvalue.get())
      audioendtimedurationvalue.set(videoendtimedurationvalue.get())
     if useidenticalcustomdurations.get() == 0:
      audiostarttimedurationvalue.set(previous_audstartdurationvalue.get())
      audioendtimedurationvalue.set(previous_audenddurationvalue.get())
  useidenticalcustomdurations.trace('w', changedurationvalues)
  changedurationvalues()

  def autoinputaudio():
   if autoinputvideoaudio.get() == 1:
    filePathaudt1.set(filePathvideo.get())
    filePathaudt2.set(filePathvideo.get())
   if autoinputvideoaudio.get() == 0:
    filePathaudt1.set('')
    filePathaudt2.set('')

  global autoinputvideoaudio
  autoinputvideoaudio = IntVar()
  autoinput_audiofromvideo = ttk.Checkbutton(optwin, text='Automatically use audio from video', variable=autoinputvideoaudio, command=autoinputaudio, onvalue=1, offvalue=0)
  autoinput_audiofromvideo.place(x=11, y=165)

  global setoutputdirectorytovideodirectory
  setoutputdirectorytovideodirectory = IntVar()
  setoutputdirectorytovideodirectorycheck = ttk.Checkbutton(optwin, text='Use video directory for output directory', variable=setoutputdirectorytovideodirectory, onvalue=1, offvalue=0)
  setoutputdirectorytovideodirectorycheck.place(x=11, y=185)

  global setdirectorytovideodirectory
  def setdirectorytovideodirectory(*args):
   if setoutputdirectorytovideodirectory.get() == 1:
    filePathvideo_novideofile = StringVar()
    filePathvideo_novideofile.set(os.path.dirname(filePathvideo.get()))
    dirPath.set(filePathvideo_novideofile.get())
   if setoutputdirectorytovideodirectory.get() == 0:
    dirPath.set('')
  setoutputdirectorytovideodirectory.trace('w', setdirectorytovideodirectory)

  global setSFDfilenametovideofilename
  setSFDfilenametovideofilename = IntVar()
  setSFDfilenametovideofilenamecheck = ttk.Checkbutton(optwin, text='Use video name for SFD name', variable=setSFDfilenametovideofilename, onvalue=1, offvalue=0)
  setSFDfilenametovideofilenamecheck.place(x=11, y=205)

  global UsevideonameforSFD
  def UsevideonameforSFD(*args): 
   if setSFDfilenametovideofilename.get() == 1:
    videofilename = os.path.basename(filePathvideo.get())
    videofilename_noextension = os.path.splitext(videofilename)[0]
    SFDfilename.set(videofilename_noextension)
   if setSFDfilenametovideofilename.get() == 0:
    SFDfilename.set('')
  setSFDfilenametovideofilename.trace('w', UsevideonameforSFD)

  global createsfdtofolder
  createsfdtofolder = IntVar()
  createsfdtofoldercheck = ttk.Checkbutton(optwin, text='Create SFD to folder', variable=createsfdtofolder, onvalue=1, offvalue=0)
  #createsfdtofoldercheck.place(x=11, y=225)


  #Misc Program Options
  global disableaudiopadding
  disableaudiopadding = IntVar()
  disableaudiopaddingcheck = ttk.Checkbutton(optwin, text='Disable blank audio padding', variable=disableaudiopadding, onvalue=1, offvalue=0)
  disableaudiopaddingcheck.place(x=266, y=165)

  global addaudiotracks
  addaudiotracks = IntVar()

  global aud2select
  aud2select = Label(dirframe, text="Audio for Track 2:", font = ("Arial Bold", 8))

  global moreaudiotracks
  moreaudiotracks = Button(text="Additional Audio Tracks", command=extraaudiotracks, padx=10, pady=3)

  global browseaud2
  browseaud2 = Button(text="Browse", command=GetAud2, padx=40, pady=5)

  def showaudiotracksbutton(*args):
   if addaudiotracks.get() == 1:
    moreaudiotracks.place(x=425, y=108)
    aud2select.place_forget()
    entryaud2.place_forget()
    browseaud2.place_forget()
   else:
    aud2select.place(x=3, y=76.47)
    moreaudiotracks.place_forget()
    entryaud2.place(x=5, y=95.8)
    browseaud2.place(x=455, y=105)
  addaudiotracks.trace("w", showaudiotracksbutton)

  addaudiotrackscheck = ttk.Checkbutton(optwin, text='Enable additional audio tracks', variable=addaudiotracks, command=showaudiotracksbutton, onvalue=1, offvalue=0)
  addaudiotrackscheck.place(x=266, y=185)

  if addaudiotracks.get() == 0:  #set place positions on program boot
   entryaud2.place(x=5, y=95.8)
   aud2select.place(x=3, y=76.499999999999992)
   moreaudiotracks.place_forget()
   browseaud2.place(x=455, y=105)


  global showffmpegcommands
  showffmpegcommands = IntVar()
  showffmpegcommandscheck = ttk.Checkbutton(optwin, text='Show FFmpeg output', variable=showffmpegcommands, onvalue=1, offvalue=0)
  showffmpegcommandscheck.place(x=266, y=205)
  showffmpegcommands.set(0)


  def chooseexternalsfdmuxer():
   global external_sfdmuxer
   external_sfdmuxer = filedialog.askopenfilenames(title='Choose an SFD muxer (+ any other files it requires)')
   global muxer_files
   muxer_files = []
   for files in external_sfdmuxer:
     files_name = os.path.basename(files)
     externalmuxer_copypath = os.path.join(currentdir, files_name)
     shutil.copy(files, externalmuxer_copypath)
     muxer_files.append(externalmuxer_copypath)


  global useexternalsfdmuxer
  useexternalsfdmuxer = IntVar()
  useexternalsfdmuxercheck = ttk.Checkbutton(optwin, text='Use external SFD muxer', variable=useexternalsfdmuxer, command=chooseexternalsfdmuxer, onvalue=1, offvalue=0)
  #useexternalsfdmuxercheck.place(x=266, y=225)
  useexternalsfdmuxer.set(0)

  optwin.withdraw()


def openpresetwindow():
 global presetwindow
 presetwindow = Toplevel(master)
 presetwindow.geometry("550x400"), presetwindow.title("Preset Window"), presetwindow.resizable(False, False)

 global presetopener
 presetopener = IntVar()
 presetopener.set('')
 openpresetentry = ttk.Entry(presetwindow, textvariable=presetopener, width=50)
 openpresetentry.insert(0, "")
 openpresetentry.place(x=45, y=9)



 def openpreset():
  filePathpreset = StringVar()
  presetfolder = os.getcwd() + '/preset'
  preset = filedialog.askopenfilename(title="Select A Preset File", filetypes=[("Preset files", ".preset")], initialdir=presetfolder)
  filePathpreset.set(preset)

 def onfileselect(event):
  selected_file = whitebox.get("current linestart", "current lineend")
  openpresetentry.delete(0, tk.END)
  openpresetentry.insert(0, selected_file)

 def listfiles(directory, file_extension):
  files = [file for file in os.listdir(directory) if file.endswith(file_extension)]
  return files

 global displayfilelist
 def displayfilelist():
  directory = os.getcwd() + '/preset'
  file_extension = ".preset"
  files = listfiles(directory, file_extension)
  file_list = '\n'.join(files)
  whitebox.config(state=tk.NORMAL)
  whitebox.delete(1.0, tk.END)
  whitebox.insert(tk.END, file_list)
  whitebox.config(state=tk.DISABLED)

 def applypreset():
  print('applypreset')

 def createpreset():
  print('makepreset')

 openpresetbtn = Button(presetwindow, text="Open File", command=openpreset, padx=40, pady=2).place(x=360, y=5)
 applypresetbtn = Button(presetwindow, text="Apply Preset", command=applypreset, padx=40, pady=5).place(x=380, y=350)
 createpresetbtn = Button(presetwindow, text="Create New Preset", command=createpreset, padx=40, pady=5).place(x=11, y=350)
 whitebox = tk.Text(presetwindow, bg="#ffffff", state=tk.DISABLED, height=18, width=50, font=("Arial", 9))
 whitebox.place(x=60, y=50)
 whitebox.bind("<<Selection>>", onfileselect)
 displayfilelist()


def extraaudiotracks():
 global extraaudiotrackswin
 extraaudiotrackswin = Toplevel(master)
 extraaudiotrackswin.geometry("300x230"), extraaudiotrackswin.title("Additional Audio Tracks"), extraaudiotrackswin.resizable(False, False)
 
 def GetAud1():
  audt1 = filedialog.askopenfilename(title="Select A Audio File for Track 1", filetypes=[("Audio files", ".wav .mp3 .flac .mp2 .adx .ogg .mpeg .mpg .mp4 .avi .mkv .mov")])
  filePathaudt1.set(audt1)
  entryaud1.focus()
  entryaud1.xview_moveto(1)
  entryaud1.focus_set()

 def GetAud2():
  audt2 = filedialog.askopenfilename(title="Select A Audio File for Track 2", filetypes=[("Audio files", ".wav .mp3 .flac .mp2 .adx .ogg .mpeg .mpg .mp4 .avi .mkv .mov")])
  filePathaudt2.set(audt2)
  entryaud2.focus()
  entryaud2.xview_moveto(1)
  entryaud2.focus_set()

 def GetAud3():
  audt3 = filedialog.askopenfilename(title="Select A Audio File for Track 3", filetypes=[("Audio files", ".wav .mp3 .flac .mp2 .adx .ogg .mpeg .mpg .mp4 .avi .mkv .mov")])
  filePathaudt3.set(audt3)
  entryaud3.focus()
  entryaud3.xview_moveto(1)
  entryaud3.focus_set()

 def GetAud4():
  audt4 = filedialog.askopenfilename(title="Select A Audio File for Track 4", filetypes=[("Audio files", ".wav .mp3 .flac .mp2 .adx .ogg .mpeg .mpg .mp4 .avi .mkv .mov")])
  filePathaudt4.set(audt4)
  entryaud4.focus()
  entryaud4.xview_moveto(1)
  entryaud4.focus_set()

 entryaud1_lbl = Label(extraaudiotrackswin, text="Audio for Track 1:", font = ("Arial Bold", 8)).place(x=2, y=10)
 entryaud1 = ttk.Entry(extraaudiotrackswin, textvariable=filePathaudt1, width=26)
 entryaud1.insert(0, "")
 entryaud1.place(x=5, y=26)
 browseaud1 = Button(extraaudiotrackswin, text="Browse", command=GetAud1, padx=35, pady=5).place(x=175, y=20)

 entryaud2_lbl = Label(extraaudiotrackswin, text="Audio for Track 2:", font = ("Arial Bold", 8)).place(x=2, y=60)
 entryaud2 = ttk.Entry(extraaudiotrackswin, textvariable=filePathaudt2, width=26)
 entryaud2.insert(0, "")
 entryaud2.place(x=5, y=76)
 browseaud2 = Button(extraaudiotrackswin, text="Browse", command=GetAud2, padx=35, pady=5).place(x=175, y=70)

 entryaud3_lbl = Label(extraaudiotrackswin, text="Audio for Track 3:", font = ("Arial Bold", 8)).place(x=2, y=110)
 entryaud3 = ttk.Entry(extraaudiotrackswin, textvariable=filePathaudt3, width=26)
 entryaud3.insert(0, "")
 entryaud3.place(x=5, y=126)
 browseaud3 = Button(extraaudiotrackswin, text="Browse", command=GetAud3, padx=35, pady=5).place(x=175, y=120)

 entryaud4_lbl = Label(extraaudiotrackswin, text="Audio for Track 4:", font = ("Arial Bold", 8)).place(x=2, y=160)
 entryaud4 = ttk.Entry(extraaudiotrackswin, textvariable=filePathaudt4, width=26)
 entryaud4.insert(0, "")
 entryaud4.place(x=5, y=176)
 browseaud4 = Button(extraaudiotrackswin, text="Browse", command=GetAud4, padx=35, pady=5).place(x=175, y=170)


def createSFD():
   global ffprobe_exe_path #Fix for FFprobe EXE error when not on user's path
   global ffmpeg_location_int
   global ffprobe_location_int

   if previewmode.get() == 1:
    previewmodeenabled_error = tk.messagebox.showerror(title='Error', message='SFDs cannot be created, as the program is running in preview mode. Please close the program, re-open it and install FFmpeg in order to create SFDs.')
    return
   if disableaudiopadding.get() == 1 and filePathaudt1.get() == '' and filePathaudt2.get() == '':
     audiorequired = tk.messagebox.showerror(title='Audio Error', message='No audio file was provided for any track. Please either input an audio file or untick the "Disable audio padding" checkbox in the Extra Options menu to continue.')
     return
   if SFDfilename.get() == '':
     filenamemissing = tk.messagebox.showerror(title='File Error', message='No filename was inputted for the SFD file. Please go back and input a name for the output SFD file.')
     return
    
   if os.path.isfile(dirPath.get() + '/' + SFDfilename.get() + '.sfd'):
    sfdalreadyexists_messagebox = tk.messagebox.askyesno(title='File Error', message='An SFD file with the same name already exists in the output directory. Do you want to overwrite it?')
    if sfdalreadyexists_messagebox:
     os.remove(dirPath.get() + '/' + SFDfilename.get() + '.sfd')
     pass
    else:
     print("SFD creation cancelled, SFD will not be overwritten.")
     return

   #Store file locations before creation begins
   previous_filePathvideovalue = StringVar()
   previous_filePathaudt1value = StringVar()
   previous_filePathaudt2value = StringVar()
   previous_filePathaudt3value = StringVar()
   previous_filePathaudt4value = StringVar()
   def getpreviousfilevalues():
    previous_filePathvideovalue.set(filePathvideo.get())
    previous_filePathaudt1value.set(filePathaudt1.get())
    previous_filePathaudt2value.set(filePathaudt2.get())
    previous_filePathaudt3value.set(filePathaudt3.get())
    previous_filePathaudt4value.set(filePathaudt4.get())
   getpreviousfilevalues()


   #remove ".sfd" if it was included on SFDfilename
   if SFDfilename.get().endswith(".sfd"):
     SFDfilename.set(SFDfilename.get()[:-4])

   #Set ffmpeg command properly if it's on the user's PATH
   if ffmpeg_location_int == 1:
     ffmpeg_exe_path = 'ffmpeg.exe'
   else:
     ffmpeg_exe_path = currentdir + '/resource/bin/ffmpeg/ffmpeg.exe'
   if ffprobe_location_int == 1:
     ffprobe_exe_path = 'ffprobe.exe'
   else:
     ffprobe_exe_path = currentdir + '/resource/bin/ffmpeg/ffprobe.exe'

   global previousvideovalue
   ffmpegstartdurationcmd = StringVar()
   ffmpegenddurationcmd = StringVar()
   previousvideovalue = StringVar()

   #Fix framerate if it's set to Same as Video
   if framerate.get() == 'Same as Video':
     framerate.set('')
   if comboboxframerate.get() == 'Same as Video':
     framerate.set('')
   if comboboxframerate.get() == '-r Same as Video':
     framerate.set('')
   if framerate.get() == '-r Same as Video':
     framerate.set('')

   #Misc Error messages
   videofile = filePathvideo.get()
   if not os.path.exists(StringVar.get(filePathvideo)):
     videomissing = tk.messagebox.showerror(title='File Error', message='No video file was selected! Please select a video file to continue.')
     return
   if not os.path.exists(dirPath.get()):
     tk.messagebox.showerror(title='Directory Error', message="Can't find the directory selected. Try again, or select a different directory.")
     return

   #Check for custom duration settings
   if enablevideoffmpegduration.get() == 1 and videostarttimedurationvalue.get() == '':
     tk.messagebox.showerror(title='FFmpeg Duration Error', message="To use a custom video duration, you must input both the length of the clip and the start time of the clip into their respective boxes. Please enter the time you want the video to start in the first box to continue, or disable the custom duration checkbox.")
     return
   if enablevideoffmpegduration.get() == 1 and videoendtimedurationvalue.get() == '':
     tk.messagebox.showerror(title='FFmpeg Duration Error', message="To use a custom video duration, you must input both the length of the clip and the start time of the clip into their respective boxes. Please enter the length you want the video in the second box to be to continue, or disable the custom duration checkbox.")
     return
   if enablevideoffmpegduration.get() == 1 and videostarttimedurationvalue.get() == '' and videoendtimedurationvalue.get() == '':
     tk.messagebox.showerror(title='FFmpeg Duration Error', message="No values were inputed for a custom duration. Please disable the custom duration checkbox to continue, or input values into the proper boxes.")
     return

   if useWAVforconversion.get() == 1:
     audiofiletype.set('WAV')
   if useWAVforconversion.get() == 0:
     audiofiletype.set('MP3')

   if os.path.exists(filePathvideo.get()):
     if UseVideoAudio.get() == 1:
      filePathaudt1.set(filePathvideo.get())
      entryaud1.focus()
      entryaud1.xview_moveto(1)
      entryaud1.focus_set()
     if UseTrack1forTrack2.get() == 1:
      filePathaudt2.set(filePathaudt1.get())
      entryaud2.focus()
      entryaud2.xview_moveto(1)
      entryaud2.focus_set()

   if autoinputvideoaudio.get() == 1:
     filePathaudt1.set(filePathvideo.get())
     filePathaudt2.set(filePathvideo.get())

   if UseVideoAudio.get() == 1:
     filePathaudt1.set(filePathvideo.get())
   if UseTrack1forTrack2.get() == 1:
     filePathaudt2.set(filePathaudt1.get())
    
   if usebitexact.get() == 1:
     bitexactcmd.set('-bitexact')
   else:
     bitexactcmd.set('')

   if enablevideoffmpegduration.get() == 1:
     if not videostarttimedurationvalue.get().startswith('-ss '):
      videostarttimedurationvalue.set('-ss ' + videostarttimedurationvalue.get())
     if not videoendtimedurationvalue.get().startswith('-ss '):
      videoendtimedurationvalue.set('-ss ' + videoendtimedurationvalue.get())

   if enableaudioffmpegduration.get() == 1:
     if not audiostarttimedurationvalue.get().startswith('-ss '):
      audiostarttimedurationvalue.set('-ss ' + audiostarttimedurationvalue.get())
     if not audioendtimedurationvalue.get().startswith('-ss '):
      audioendtimedurationvalue.set('-ss ' + audioendtimedurationvalue.get())

   #if useexternalsfdmuxer.get() == 1:
    #externalsfdmuxer_cmd = input("Use external SFD muxer enabled, please input the command to run using the follow values:\nVideo file: newvideo.mpeg\nAudio file(s) = TrackX.adx (X being either 1, 2, 3 or 4)\n ")



   videofile = filePathvideo.get()
   audio1 = StringVar()
   audio1 = filePathaudt1.get()
   audio2 = StringVar()
   audio2 = filePathaudt2.get()
   audio3 = StringVar()
   audio3 = filePathaudt3.get()
   audio4 = StringVar()
   audio4 = filePathaudt4.get()

   def createaudiopadding():
    if disableaudiopadding.get() == 1:
     pass
    else:
     if not os.path.exists(filePathaudt1.get()):
      print("No audio found for track 1, filling with padding audio")
      ffprobe_cmd = f'"{ffprobe_exe_path}" -i "{videofile}" -show_entries format=duration -v quiet -of csv="p=0"'
      input(ffprobe_cmd)
      duration = float(os.popen(ffprobe_cmd).read().strip())
      ffmpeg_blankaudio_track1_cmd = f'"{ffmpeg_exe_path}" -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=11025 -t {duration} -b:a 8k -shortest "blank.{audiofiletype.get()}"'
      if showffmpegcommands == 1:
       subprocess.run(ffmpeg_blankaudio_track1_cmd, stderr=subprocess.STDOUT, shell=True)
      else:
       subprocess.run(ffmpeg_blankaudio_track1_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
      filePathaudt1.set('blank.mp3')


    if disableaudiopadding.get() == 1:
     pass
    else:
     if not os.path.exists(filePathaudt2.get()):
      print("No audio found for track 2, filling with padding audio")
      ffprobe_cmd = f'"{ffprobe_exe_path}" -i "{videofile}" -show_entries format=duration -v quiet -of csv="p=0"'
      duration = float(os.popen(ffprobe_cmd).read().strip())
      ffmpeg_blankaudio_track2_cmd = f'"{ffmpeg_exe_path}" -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=11025 -t {duration} -b:a 8k -shortest "blankt2.{audiofiletype.get()}"'
      if showffmpegcommands.get() == 1:
       subprocess.run(ffmpeg_blankaudio_track2_cmd, stderr=subprocess.STDOUT, shell=True)
      else:
       subprocess.run(ffmpeg_blankaudio_track2_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
      filePathaudt2.set('blankt2.mp3')


    if disableaudiopadding.get() == 1:
     pass
    else:
     if addaudiotracks.get() == 1 and not os.path.exists(filePathaudt3.get()):
      print("No audio found for track 3, filling with padding audio")
      ffprobe_cmd = f'"{ffprobe_exe_path}" -i "{videofile}" -show_entries format=duration -v quiet -of csv="p=0"'
      duration = float(os.popen(ffprobe_cmd).read().strip())
      ffmpeg_blankaudio_track3_cmd = f'"{ffmpeg_exe_path}" -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=11025 -t {duration} -b:a 8k -shortest "blankt3.{audiofiletype.get()}"'
      if showffmpegcommands.get() == 1:
       subprocess.run(ffmpeg_blankaudio_track3_cmd, stderr=subprocess.STDOUT, shell=True)
      else:
       subprocess.run(ffmpeg_blankaudio_track3_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
      filePathaudt3.set('blankt3.mp3')


    if disableaudiopadding.get() == 1:
     pass
    else:
     if addaudiotracks.get() == 1 and not os.path.exists(filePathaudt4.get()):
      print("No audio found for track 4, filling with padding audio")
      ffprobe_cmd = f'"{ffprobe_exe_path}" -i "{videofile}" -show_entries format=duration -v quiet -of csv="p=0"'
      duration = float(os.popen(ffprobe_cmd).read().strip())
      ffmpeg_blankaudio_track4_cmd = f'"{ffmpeg_exe_path}" -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=11025 -t {duration} -b:a 8k -shortest "blankt4.{audiofiletype.get()}"'
      if showffmpegcommands.get() == 1:
       subprocess.run(ffmpeg_blankaudio_track4_cmd, stderr=subprocess.STDOUT, shell=True)
      else:
       subprocess.run(ffmpeg_blankaudio_track4_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
      filePathaudt4.set('blankt4.mp3')
   
   if disableaudiopadding.get() == 1:
    pass
   else:
    createaudiopadding()

   if os.path.isfile('blank.mp3') and disableaudiopadding.get() == 1:
     os.remove('blank.mp3')
   if os.path.isfile('blankt2.mp3') and disableaudiopadding.get() == 1:
     os.remove('blankt2.mp3')
   if os.path.isfile('blankt3.mp3') and disableaudiopadding.get() == 1:
     os.remove('blankt3.mp3')
   if os.path.isfile('blankt4.mp3') and disableaudiopadding.get() == 1:
     os.remove('blankt4.mp3')

   outputT1 = f'track1.{audiofiletype.get()}'
   outputT2 = f'track2.{audiofiletype.get()}'
   outputT3 = f'track3.{audiofiletype.get()}'
   outputT4 = f'track4.{audiofiletype.get()}'
    
   if os.path.isfile(f'blank.{audiofiletype.get()}'):
     audio1 = f'blank.{audiofiletype.get()}'
   if os.path.isfile(f'blankt2.{audiofiletype.get()}'):
     audio2 = f'blankt2.{audiofiletype.get()}'
   if os.path.isfile(f'blankt3.{audiofiletype.get()}'):
     audio3 = f'blankt3.{audiofiletype.get()}'
   if os.path.isfile(f'blankt4.{audiofiletype.get()}'):
     audio4 = f'blankt4.{audiofiletype.get()}'


   global outputmpegextension
   outputmpegextension = StringVar()
   if sofdecstreamtype.get() == '0' or 0 or '1' or 1:
    outputmpegextension.set('m1v')
   if sofdecstreamtype.get() == '2' or 2:
    outputmpegextension.set('mpeg')

   if sofdecstreamtype.get() == '0' and resolution_streamtype1.get() == '':
    resolution_streamtype1.set('480:336')
    updatevratio_streamtype1()

   
   convert_avi_cmd=f'"{ffmpeg_exe_path}" -y {ffmpegloglevel.get()} -i "{filePathvideo.get()}" {ffmpegspeedpreset.get()} -crf {crfvalue.get()} -b:v 30000000 {framerate.get()} {resolution.get()} {vratio.get()} {videostarttimedurationvalue.get()} {videoendtimedurationvalue.get()} AVIconvert.avi'
   print("Converting video to AVI...")
   if showffmpegcommands.get() == 1:
     subprocess.run(convert_avi_cmd, stderr=subprocess.STDOUT, shell=True)
   else:
     subprocess.run(convert_avi_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
   if os.path.isfile('AVIconvert.avi'):
     pass
   else:
     print("AVIconvert.avi was unable to be created.")
     avimissing = tk.messagebox.showerror('FFmpeg Error', "AVIconvert.avi could not be created. Try creating the SFD again. If this issue persists, it could be a problem with the video file.")
     return


   if sofdecstreamtype.get() == '0':
    convert_mpeg_cmd=f'"{ffmpeg_exe_path}" -y {ffmpegloglevel.get()} -i AVIconvert.avi {ffmpegspeedpreset.get()} -crf {crfvalue.get()} -b:v 30000000 {framerate.get()} -vf "{vratio_streamtype1.get()}" {ffmpegstartdurationcmd.get()} -b:v {vbitrate.get()} -c:v mpeg1video newvideo.{outputmpegextension.get()}'
   else:
    convert_mpeg_cmd=f'"{ffmpeg_exe_path}" -y {ffmpegloglevel.get()} -i AVIconvert.avi {ffmpegspeedpreset.get()} -crf {crfvalue.get()} -b:v 30000000 {framerate.get()} {vratio.get()} {ffmpegstartdurationcmd.get()} -b:v {vbitrate.get()} {framerate.get()} {resolution.get()} -c:v mpeg1video newvideo.{outputmpegextension.get()}'
   print("Converting video to MPEG...")
   if showffmpegcommands.get() == 1:
     subprocess.run(convert_mpeg_cmd, stderr=subprocess.STDOUT, shell=True)
   else:
     subprocess.run(convert_mpeg_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
   if os.path.isfile(f'newvideo.{outputmpegextension.get()}'):
     pass
   else:
     print(f"newvideo.{outputmpegextension.get()} was unable to be created.")
     mpegmissing = tk.messagebox.showerror('FFmpeg Error', f"newvideo.{outputmpegextension.get()} could not be created. Try creating the SFD again. If this issue persists, it could be a problem with the video file.")
     os.remove('AVIconvert.avi')
     return
   

   #Fix for if disable audio padding enabled, but no track in track 1 (so SFD would fail to be created with 1999 Muxer)
   if sofdecstreamtype.get() == '0' and disableaudiopadding.get() == 1 and filePathaudt1.get() == '' and not filePathaudt2.get() == '':
       audio1 = 'track1.mp3'
       ffprobe_cmd = f'"{ffprobe_exe_path}" -i "{videofile}" -show_entries format=duration -v quiet -of csv="p=0"'
       duration = float(os.popen(ffprobe_cmd).read().strip())
       ffmpeg_blankaudio_track1_cmd = f'"{ffmpeg_exe_path}" -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=11025 -t {duration} -b:a 8k -shortest {audio1}'
       if showffmpegcommands == 1:
        subprocess.run(ffmpeg_blankaudio_track1_cmd, stderr=subprocess.STDOUT, shell=True)
       else:
        subprocess.run(ffmpeg_blankaudio_track1_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)


   convert_audio1_cmd=f'"{ffmpeg_exe_path}" -y {ffmpegloglevel.get()} -i "{audio1}" -b:a {abitrate.get()} {bitexactcmd.get()} -ar {aHz.get()} {audiochannel.get()} {ffmpegstartdurationcmd.get()} {audiostarttimedurationvalue.get()} {ffmpegenddurationcmd.get()} {audioendtimedurationvalue.get()} {outputT1}'
   if showffmpegcommands.get() == 1:
     subprocess.run(convert_audio1_cmd, stderr=subprocess.STDOUT, shell=True)
   else:
     subprocess.run(convert_audio1_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
     print(f"Converting audio track 1 to {audiofiletype.get()}...")

   convert_audio1_adx_cmd=f'"{ffmpeg_exe_path}" -y {ffmpegloglevel.get()} -i {outputT1} -b:a {abitrate.get()} {bitexactcmd.get()} -ar {aHz.get()} {audiochannel.get()} track1.adx'
   if showffmpegcommands.get() == 1:
     subprocess.run(convert_audio1_adx_cmd, stderr=subprocess.STDOUT, shell=True)
   else:
     subprocess.run(convert_audio1_adx_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
     print(f"Converting audio track 1 to ADX...")


   convert_audio2_cmd=f'"{ffmpeg_exe_path}" -y {ffmpegloglevel.get()} -i "{audio2}" -b:a {abitrate.get()} {bitexactcmd.get()} -ar {aHz.get()} {audiochannel.get()} {ffmpegstartdurationcmd.get()} {audiostarttimedurationvalue.get()} {ffmpegenddurationcmd.get()} {audioendtimedurationvalue.get()} {outputT2}'
   if showffmpegcommands.get() == 1:
     subprocess.run(convert_audio2_cmd, stderr=subprocess.STDOUT, shell=True)
   else:
     subprocess.run(convert_audio2_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
     print(f"Converting audio track 2 to {audiofiletype.get()}...")

   convert_audio2_adx_cmd=f'"{ffmpeg_exe_path}" -y {ffmpegloglevel.get()} -i {outputT2} -b:a {abitrate.get()} {bitexactcmd.get()} -ar {aHz.get()} {audiochannel.get()} track2.adx'
   if showffmpegcommands.get() == 1:
     subprocess.run(convert_audio2_adx_cmd, stderr=subprocess.STDOUT, shell=True)
   else:
     subprocess.run(convert_audio2_adx_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
     print(f"Converting audio track 2 to ADX...")
 

   if addaudiotracks.get() == 1:
     convert_audio3_cmd=f'"{ffmpeg_exe_path}" -y {ffmpegloglevel.get()} -i "{audio3}" -b:a {abitrate.get()} {bitexactcmd.get()} -ar {aHz.get()} {audiochannel.get()} {ffmpegstartdurationcmd.get()} {audiostarttimedurationvalue.get()} {ffmpegenddurationcmd.get()} {audioendtimedurationvalue.get()} {outputT3}'
     if showffmpegcommands.get() == 1:
      subprocess.run(convert_audio3_cmd, stderr=subprocess.STDOUT, shell=True)
     else:
      subprocess.run(convert_audio3_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
      print(f"Converting audio track 3 to {audiofiletype.get()}...")

     convert_audio3_adx_cmd=f'"{ffmpeg_exe_path}" -y {ffmpegloglevel.get()} -i {outputT3} -b:a {abitrate.get()} {bitexactcmd.get()} -ar {aHz.get()} {audiochannel.get()} track3.adx'
     if showffmpegcommands.get() == 1:
      subprocess.run(convert_audio3_adx_cmd, stderr=subprocess.STDOUT, shell=True)
     else:
      subprocess.run(convert_audio3_adx_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
      print(f"Converting audio track 3 to ADX...")

     convert_audio4_cmd=f'"{ffmpeg_exe_path}" -y {ffmpegloglevel.get()} -i "{audio4}" -b:a {abitrate.get()} {bitexactcmd.get()} -ar {aHz.get()} {audiochannel.get()} {ffmpegstartdurationcmd.get()} {audiostarttimedurationvalue.get()} {ffmpegenddurationcmd.get()} {audioendtimedurationvalue.get()} {outputT4}'
     if showffmpegcommands.get() == 1:
      subprocess.run(convert_audio4_cmd, stderr=subprocess.STDOUT, shell=True)
     else:
      subprocess.run(convert_audio4_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
      print(f"Converting audio track 4 to {audiofiletype.get()}...")

     convert_audio4_adx_cmd=f'"{ffmpeg_exe_path}" -y {ffmpegloglevel.get()} -i {outputT4} -b:a {abitrate.get()} {bitexactcmd.get()} -ar {aHz.get()} {audiochannel.get()} track4.adx'
     if showffmpegcommands.get() == 1:
      subprocess.run(convert_audio4_adx_cmd, stderr=subprocess.STDOUT, shell=True)
     else:
      subprocess.run(convert_audio4_adx_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
      print(f"Converting audio track 4 to ADX...")




   if sofdecstreamtype.get() == '0' or '1':
    adx_to_sfa_converter = os.getcwd() + '/resource/bin/legaladx/legaladx.exe'
    def convertadx_to_sfa():
      if os.path.isfile('track1.adx'):
       legaladxcmd_track1 = f'"{adx_to_sfa_converter}" track1.adx track1.sfa'
       subprocess.run(legaladxcmd_track1, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
      if os.path.isfile('track2.adx'):
       legaladxcmd_track2 = f'"{adx_to_sfa_converter}" track2.adx track2.sfa'
       subprocess.run(legaladxcmd_track2, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
      if os.path.isfile('track3.adx'):
       legaladxcmd_track2 = f'"{adx_to_sfa_converter}" track3.adx track3.sfa'
       subprocess.run(legaladxcmd_track2, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
      if os.path.isfile('track4.adx'):
       legaladxcmd_track2 = f'"{adx_to_sfa_converter}" track4.adx track4.sfa'
       subprocess.run(legaladxcmd_track2, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
    convertadx_to_sfa()


   if sofdecstreamtype.get() == '0':
     sfdmux_streamtype1_1999muxer_location = os.getcwd() + '/resource/bin/SFDmux_CRI1999/SFDmux.exe'
     print("Creating SFD...")
    
  
     #Fix for error in SFDMUX where SFD would be unable to be made due to it having the extension '.mpeg' and not '.m1v'
     if os.path.isfile("newvideo.mpeg"):
      if os.path.isfile('newvideo.m1v'):
       os.remove('newvideo.m1v')
      outputmpegextension.set('m1v')
      fixmpegvideo_ffmpegcmd = f'"{ffmpeg_exe_path}" -i newvideo.mpeg -crf {crfvalue.get()} -b:v 30000000 newvideo.m1v'
      subprocess.run(fixmpegvideo_ffmpegcmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)


     if addaudiotracks.get() == 1:
      sfdmux_4track_cmd=f'"{sfdmux_streamtype1_1999muxer_location}" -v=newvideo -a=track1 -a=track2 -a=track3 -a=track4 -s=file'
      if showffmpegcommands.get() == 1:
       subprocess.run(sfdmux_4track_cmd, stderr=subprocess.STDOUT, shell=True)
      else:
       subprocess.run(sfdmux_4track_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
     else:
      sfdmux_2track_cmd=f'"{sfdmux_streamtype1_1999muxer_location}" -v=newvideo -a=track1 -a=track2 -s=file'
      if showffmpegcommands.get() == 1:
       subprocess.run(sfdmux_2track_cmd, stderr=subprocess.STDOUT, shell=True)
      else:
       subprocess.run(sfdmux_2track_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)


   if sofdecstreamtype.get() == '1':
     sfdmux_streamtype1_location = os.getcwd() + '/resource/bin/SofdecStream1_muxer/SFD_Muxer.exe'
     print("Creating SFD...")

     if addaudiotracks.get() == 1:
      sfdmux_4track_cmd=f'"{sfdmux_streamtype1_location}" -v newvideo.m1v -a track1.sfa -a track2.sfa -a track3.sfa -a track4.sfa -s 1 -o file.sfd'
      if showffmpegcommands.get() == 1:
       subprocess.run(sfdmux_4track_cmd, stderr=subprocess.STDOUT, shell=True)
      else:
       subprocess.run(sfdmux_4track_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
     else:
      sfdmux_2track_cmd=f'"{sfdmux_streamtype1_location}" -v newvideo.m1v -a track1.sfa -a track2.sfa -s 1 -o file.sfd'
      if showffmpegcommands.get() == 1:
       subprocess.run(sfdmux_2track_cmd, stderr=subprocess.STDOUT, shell=True)
      else:
       subprocess.run(sfdmux_2track_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)


   if sofdecstreamtype.get() == '2':
     sfdmuxlocation = os.getcwd() + '/resource/bin/sfdmux.exe'
     if os.path.isfile(sfdmuxlocation):
       pass
     else:
      print("sfdmux.exe unable to be found.")
      return
     print("Creating SFD...")
     if not addaudiotracks.get() == 1:
       sfdmux_2track_cmd=f'"{sfdmuxlocation}" file.sfd newvideo.{outputmpegextension.get()} track1.adx track2.adx'
       if showffmpegcommands.get() == 1:
        subprocess.run(sfdmux_2track_cmd, stderr=subprocess.STDOUT, shell=True)
       else:
        subprocess.run(sfdmux_2track_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)

     if addaudiotracks.get() == 1:
      sfdmux_4track_cmd=f'"{sfdmuxlocation}" file.sfd newvideo.{outputmpegextension.get()} track1.adx track2.adx track3.adx track4.adx'
      if showffmpegcommands.get() == 1:
       subprocess.run(sfdmux_4track_cmd, stderr=subprocess.STDOUT, shell=True)
      else:
       subprocess.run(sfdmux_4track_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)


   if os.path.isfile('file.sfd'): #Clean up files if SFD can't be created
     pass
   else:
     print("SFD unable to be created, cleaning up files...")
     print("")
     if os.path.isfile('track1.adx'):
      os.remove('track1.adx')
     if os.path.isfile('track2.adx'):
      os.remove('track2.adx')
     if os.path.isfile('track3.adx'):
      os.remove('track3.adx')
     if os.path.isfile('track4.adx'):
      os.remove('track4.adx')
     if os.path.isfile('track1.sfa'):
      os.remove('track1.sfa')
     if os.path.isfile('track2.sfa'):
      os.remove('track2.sfa')
     if os.path.isfile('track3.sfa'):
      os.remove('track3.sfa')
     if os.path.isfile('track4.sfa'):
      os.remove('track4.sfa')
     if os.path.isfile('log.txt'):
      os.remove('log.txt')
     if os.path.exists(f'blank.{audiofiletype.get()}'):
      os.remove(f'blank.{audiofiletype.get()}')
     if os.path.exists(f'blankt2.{audiofiletype.get()}'):
      os.remove(f'blankt2.{audiofiletype.get()}')
     if os.path.exists(f'blankt3.{audiofiletype.get()}'):
      os.remove(f'blankt3.{audiofiletype.get()}')
     if os.path.exists(f'blankt4.{audiofiletype.get()}'):
      os.remove(f'blankt2.{audiofiletype.get()}')
     if os.path.exists(f'track1.{audiofiletype.get()}'):
      os.remove(f'track1.{audiofiletype.get()}')
     if os.path.exists(f'track2.{audiofiletype.get()}'):
      os.remove(f'track2.{audiofiletype.get()}')
     if os.path.exists(f'track3.{audiofiletype.get()}'):
      os.remove(f'track3.{audiofiletype.get()}')
     if os.path.exists(f'track4.{audiofiletype.get()}'):
      os.remove(f'track4.{audiofiletype.get()}')
     if os.path.isfile('AVIconvert.avi'):
      os.remove('AVIconvert.avi')
     if os.path.isfile(f'newvideo.{outputmpegextension.get()}'):
      os.remove(f'newvideo.{outputmpegextension.get()}')
     if os.path.isfile(f'newvideo.mpeg'): #Just in case fix has to be used for SofdecStream1
      os.remove(f'newvideo.mpeg')
     if os.path.isfile(f'newvideo.m1v'): #Just in case fix has to be used for SofdecStream1
      os.remove(f'newvideo.m1v')
     sfdnotcreated = tk.messagebox.showerror('SFDmux Error', f"{SFDfilename.get()}.sfd could not created. Try creating the SFD again. If this occurs, it could be a problem with the input video file, or the audio files may not have been properly created.")
     return

   def cleanup_files():
    if os.path.isfile('file.sfd'):
      os.remove('file.sfd')
    if os.path.isfile('track1.adx'):
      os.remove('track1.adx')
    if os.path.isfile('track2.adx'):
      os.remove('track2.adx')
    if os.path.isfile('track3.adx'):
      os.remove('track3.adx')
    if os.path.isfile('track4.adx'):
      os.remove('track4.adx')
    if os.path.isfile('track1.sfa'):
      os.remove('track1.sfa')
    if os.path.isfile('track2.sfa'):
      os.remove('track2.sfa')
    if os.path.isfile('track3.sfa'):
      os.remove('track3.sfa')
    if os.path.isfile('track4.sfa'):
      os.remove('track4.sfa')
    if os.path.isfile('log.txt'):
      os.remove('log.txt')
    if os.path.exists(f'blank.{audiofiletype.get()}'):
      os.remove(f'blank.{audiofiletype.get()}')
    if os.path.exists(f'blankt2.{audiofiletype.get()}'):
      os.remove(f'blankt2.{audiofiletype.get()}')
    if os.path.exists(f'blankt3.{audiofiletype.get()}'):
      os.remove(f'blankt3.{audiofiletype.get()}')
    if os.path.exists(f'blankt4.{audiofiletype.get()}'):
      os.remove(f'blankt2.{audiofiletype.get()}')
    if os.path.exists(f'track1.{audiofiletype.get()}'):
      os.remove(f'track1.{audiofiletype.get()}')
    if os.path.exists(f'track2.{audiofiletype.get()}'):
      os.remove(f'track2.{audiofiletype.get()}')
    if os.path.exists(f'track3.{audiofiletype.get()}'):
      os.remove(f'track3.{audiofiletype.get()}')
    if os.path.exists(f'track4.{audiofiletype.get()}'):
      os.remove(f'track4.{audiofiletype.get()}')
    if os.path.isfile('AVIconvert.avi'):
      os.remove('AVIconvert.avi')
    if os.path.isfile(f'newvideo.{outputmpegextension.get()}'):
      os.remove(f'newvideo.{outputmpegextension.get()}')
    if os.path.isfile(f'newvideo.mpeg'): #Just in case fix has to be used for SofdecStream1
      os.remove(f'newvideo.mpeg')
    if os.path.isfile(f'newvideo.m1v'): #Just in case fix has to be used for SofdecStream1
      os.remove(f'newvideo.m1v')

   if os.path.exists(f'blank.{audiofiletype.get()}'):
     os.remove(f'blank.{audiofiletype.get()}')
   if os.path.exists(f'blankt2.{audiofiletype.get()}'):
     os.remove(f'blankt2.{audiofiletype.get()}')
   if os.path.exists(f'blankt3.{audiofiletype.get()}'):
     os.remove(f'blankt3.{audiofiletype.get()}')
   if os.path.exists(f'blankt4.{audiofiletype.get()}'):
     os.remove(f'blankt4.{audiofiletype.get()}')


   def move_or_remove_sfdcreation_files():
     if IntVar.get(keepAVI) == 1:
      if os.path.exists(os.path.join(currentdir, 'AVIconvert.avi')):
       shutil.move(os.path.join(currentdir, 'AVIconvert.avi'), os.path.join(dirPath.get(), 'AVIconvert.avi'))
     
     if IntVar.get(keepMPEG) == 1:
      if os.path.exists(os.path.join(currentdir, f'newvideo.{outputmpegextension.get()}')):
       shutil.move(os.path.join(currentdir, f'newvideo.{outputmpegextension.get()}'), os.path.join(dirPath.get(), f'newvideo.{outputmpegextension.get()}'))
     
     if IntVar.get(keepsfdmuxlog) == 1:
      if os.path.exists(os.path.join(currentdir, 'log.txt')):
       shutil.move(os.path.join(currentdir, 'log.txt'), os.path.join(dirPath.get(), 'log.txt'))

     #Keep Track 1 & 2 ADXs
     if IntVar.get(keepADX) == 1:
      if os.path.exists(os.path.join(currentdir, 'track1.adx')):
       shutil.move(os.path.join(currentdir, 'track1.adx'), os.path.join(dirPath.get(), 'track1.adx'))
      else:
       print(f"track1.adx not found, unable to move to destination directory.")
      if os.path.exists(os.path.join(currentdir, 'track2.adx')):
       shutil.move(os.path.join(currentdir, 'track2.adx'), os.path.join(dirPath.get(), 'track2.adx'))
      else:
       print(f"track2.adx not found, unable to move to destination directory.")

     #Keep Track 3 and 4 ADXs
     if IntVar.get(keepADX) == 1 and addaudiotracks.get() == 1:
      if os.path.exists(os.path.join(currentdir, 'track3.adx')):
       shutil.move(os.path.join(currentdir, 'track3.adx'), os.path.join(dirPath.get(), 'track3.adx'))
      else:
       print(f"track3.adx not found, unable to move to destination directory.")
      if os.path.exists(os.path.join(currentdir, 'track4.adx')):
       shutil.move(os.path.join(currentdir, 'track4.adx'), os.path.join(dirPath.get(), 'track4.adx'))
      else:
       print(f"track4.adx not found, unable to move to destination directory.")

     #Keep Track 1 and 2 SFA files
     if IntVar.get(keepADX) == 1:
      if os.path.exists(os.path.join(currentdir, 'track1.sfa')):
       shutil.move(os.path.join(currentdir, 'track1.sfa'), os.path.join(dirPath.get(), 'track1.sfa'))
      else:
       print(f"track1.sfa not found, unable to move to destination directory.")
      if os.path.exists(os.path.join(currentdir, 'track2.sfa')):
       shutil.move(os.path.join(currentdir, 'track2.sfa'), os.path.join(dirPath.get(), 'track2.sfa'))
      else:
       print(f"track2.sfa not found, unable to move to destination directory.")

     #Keep Track 3 and 4 SFA files
     if IntVar.get(keepADX) == 1 and addaudiotracks.get() == 1:
      if os.path.exists(os.path.join(currentdir, 'track3.sfa')):
       shutil.move(os.path.join(currentdir, 'track3.sfa'), os.path.join(dirPath.get(), 'track3.sfa'))
      else:
       print(f"track3.sfa not found, unable to move to destination directory.")
      if os.path.exists(os.path.join(currentdir, 'track4.sfa')):
       shutil.move(os.path.join(currentdir, 'track4.sfa'), os.path.join(dirPath.get(), 'track4.sfa'))
      else:
       print(f"track4.sfa not found, unable to move to destination directory.")

     #Keep Track 1 and 2 WAV/MP3 files
     if IntVar.get(keepWAV) == 1:
      if os.path.exists(os.path.join(currentdir, f'track1.{audiofiletype.get()}')):
       shutil.move(os.path.join(currentdir, f'track1.{audiofiletype.get()}'), os.path.join(dirPath.get(), f'track1.{audiofiletype.get()}'))
      else:
       print(f"track1.{audiofiletype.get()} not found, unable to move to destination directory.")
      if os.path.exists(os.path.join(currentdir, f'track2.{audiofiletype.get()}')):
       shutil.move(os.path.join(currentdir, f'track2.{audiofiletype.get()}'), os.path.join(dirPath.get(), f'track2.{audiofiletype.get()}'))
      else:
       print(f"track2.{audiofiletype.get()} not found, unable to move to destination directory.")
    
    #Keep Track 3 and 4 WAV/MP3 files
     if IntVar.get(keepWAV) == 1 and addaudiotracks.get() == 1:
      if os.path.exists(os.path.join(currentdir, f'track3.{audiofiletype.get()}')):
       shutil.move(os.path.join(currentdir, f'track3.{audiofiletype.get()}'), os.path.join(dirPath.get(), f'track3.{audiofiletype.get()}'))
      else:
       print(f"track3.{audiofiletype.get()} not found, unable to move to destination directory.")
      if os.path.exists(os.path.join(currentdir, f'track4.{audiofiletype.get()}')):
       shutil.move(os.path.join(currentdir, f'track4.{audiofiletype.get()}'), os.path.join(dirPath.get(), f'track4.{audiofiletype.get()}'))
      else:
       print(f"track4.{audiofiletype.get()} not found, unable to move to destination directory.")


   #Reset audio tracks if they're set to a blank file
   if filePathaudt1.get() == 'blank.mp3' or 'blank.wav':
    filePathaudt1.set("")
   if filePathaudt2.get() == 'blankt2.mp3' or 'blankt2.wav':
    filePathaudt2.set("")
   if filePathaudt3.get() == 'blankt3.mp3' or 'blankt3.wav':
    filePathaudt3.set("")
   if filePathaudt4.get() == 'blankt4.mp3' or 'blankt4.wav':
    filePathaudt4.set("")

   SFDname_withextension = StringVar()
   SFDname_withextension = SFDfilename.get() + '.sfd'

   min_file_size = 50
   file_size_kb = os.path.getsize('file.sfd') // 50
   print("Checking SFD file...")
   if file_size_kb < min_file_size:
     SFDfilesizeerror = tk.messagebox.showerror('SFD Error', f"{SFDname_withextension} couldn't be properly created. Try creating the file again.")
     if os.path.isfile(SFDname_withextension):
      os.remove(SFDname_withextension)
     cleanup_files()
   else:
     videocheckcommand = f'"{ffprobe_exe_path}" -v error -show_entries stream=codec_type -of default=noprint_wrappers=1 file.sfd -select_streams v:0'
     videocheckcmd_output = subprocess.run(videocheckcommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
     if videocheckcmd_output.returncode == 0:
       os.rename('file.sfd', SFDname_withextension)
       move_or_remove_sfdcreation_files()
       print("Moving SFD file to output directory...")
       if os.path.exists(os.path.join(os.getcwd(), SFDname_withextension)):
        shutil.move(os.path.join(os.getcwd(), SFDname_withextension), os.path.join(dirPath.get(), SFDname_withextension))
        cleanup_files()
        print("SFD successfully created!")
        SFDCreated = tk.messagebox.showinfo('SFD Created', f"{SFDfilename.get() + '.sfd'} was successfully created! Enjoy!")
       else:
        cleanup_files()
        SFDfilesizeerror = tk.messagebox.showerror('SFD Error', f"{SFDfilename.get() + '.sfd'}'s video couldn't be properly created. Try creating the file again.")
     else:
      cleanup_files()
      SFDfilesizeerror = tk.messagebox.showerror('SFD Error', f"{SFDfilename.get() + '.sfd'}'s video couldn't be properly created. Try creating the file again.")

   #Reset to previous values
   filePathvideo.set(previous_filePathvideovalue.get())
   filePathaudt1.set(previous_filePathaudt1value.get())
   filePathaudt2.set(previous_filePathaudt2value.get())
   filePathaudt3.set(previous_filePathaudt3value.get())
   filePathaudt4.set(previous_filePathaudt4value.get())

   print("")
   return


def opengithubrepo():
 webbrowser.open("https://github.com/Firebow59/SofdecVideoTools")

def openissuespage():
 webbrowser.open("https://github.com/Firebow59/SofdecVideoTools/issues")

def aboutprogram():
 link = 'This tool is intended for creating Sofdec video files (or SFD files for short) for use in various games. Developed by Firebow59.'
 aboutprogramwindow = tk.messagebox.showinfo(title='About Program', message=link)



videoreslabel = Label(outputdirframe, text="Video Resolution:", font = ("Arial Bold", 8)).place(x=10, y=240)
videoframeratelabel = Label(outputdirframe, text="Video Framerate:", font = ("Arial Bold", 8)).place(x=169, y=240)
vidbitrateselect = Label(outputdirframe, text="Video Bitrate:", font = ("Arial Bold", 8)).place(x=332, y=240)
audbitrateselect = Label(outputdirframe, text="Audio Bitrate:", font = ("Arial Bold", 8)).place(x=9, y=285)
audhzselect = Label(outputdirframe, text="Audio Hz:", font = ("Arial Bold", 8)).place(x=119, y=285)
audchannelselect = Label(outputdirframe, text="Audio Channel Type:", font = ("Arial Bold", 8)).place(x=230, y=285)
encodeasstreamselect = Label(outputdirframe, text="Encode As:", font = ("Arial Bold", 8)).place(x=390, y=285)
videoratiooptions = Label(outputdirframe, text="Scale/Crop Settings:", font = ("Arial Bold", 8)).place(x=448, y=240)

sofdecstreamtype = StringVar()
vbitrate = StringVar()
abitrate = StringVar()
aHz = StringVar()
videobitrateentry = ttk.Entry(outputdirframe, textvariable=vbitrate, width=15)
vbitrate.set('80000000')
videobitrateentry.place(x=335, y=257)
audiobitrateentry = ttk.Entry(outputdirframe, textvariable=abitrate, width=15)
audiobitrateentry.insert(0, "320k")
audiobitrateentry.place(x=11, y=302)
audiohzentry = ttk.Entry(outputdirframe, textvariable=aHz, width=15)
audiohzentry.insert(0, "44100")
audiohzentry.place(x=122, y=302)


OPTIONS_VRes = ["Same as Video", "320/426 x 240 (240p)", "480/640 x 360 (360p)", "640/848 x 480 (480p)", "960/1280 x 720 (720p)"]
resolution = StringVar()
comboboxvres = StringVar()
resolution_4by3 = StringVar()
outputvideoheight = StringVar()
vres = ttk.Combobox(master, value=OPTIONS_VRes)
vres.place(x=12, y=257)
vres.current(0)

def updatevres(event):
 selected_vresvalue = vres.get()

 def get4by3_resolution(event=None):
  if comboboxvres.get() == OPTIONS_VRes[1]:
   resolution_4by3.set('320:240')
  elif comboboxvres.get() == OPTIONS_VRes[2]:
   resolution_4by3.set('480:360')
  elif comboboxvres.get() == OPTIONS_VRes[3]:
   resolution_4by3.set('640:480')
  elif comboboxvres.get() == OPTIONS_VRes[4]:
   resolution_4by3.set('960:720')
  elif "x" in selected_vresvalue:
   custom_resolution = selected_vresvalue.split("x")
   if len(custom_resolution) == 2:
    height = int(custom_resolution[1])
    resolution_4by3.set(f'-1:{height}')

 if "x" in selected_vresvalue:
  custom_resolution = selected_vresvalue.split("x")
  if len(custom_resolution) == 2:
    try:
     width = int(custom_resolution[0])
     height = int(custom_resolution[1])
     resolution.set(f'-vf "scale={width}:{height},pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black"')
     comboboxvres.set(selected_vresvalue)
     vres.selection_clear()
    except ValueError:
     pass
 if selected_vresvalue == "Same As Video":
   comboboxvres.set("Same As Video")
   resolution.set("")
   vres.selection_clear()
 elif selected_vresvalue in OPTIONS_VRes[1:]:
   index = OPTIONS_VRes.index(selected_vresvalue)
   comboboxvres.set(OPTIONS_VRes[index])
   height = int(OPTIONS_VRes[index].split(" ")[-1][1:-2])
   resolution.set(f'-vf "scale=-2:{height},pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black"')
   outputvideoheight.set(height)
   vres.selection_clear()
 elif selected_vresvalue == "320/426 x 240 (240p)":
   comboboxvres.set(OPTIONS_VRes[1])
   resolution.set('-vf "scale=-2:240,pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black"')
   outputvideoheight.set('240')
   vres.selection_clear()
 elif selected_vresvalue == "480/640 x 360 (360p)":
   comboboxvres.set(OPTIONS_VRes[2])
   resolution.set('-vf "scale=-2:360,pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black"')
   outputvideoheight.set('360')
   vres.selection_clear()
 elif selected_vresvalue == "640/848 x 480 (480p)":
   comboboxvres.set(OPTIONS_VRes[3])
   resolution.set('-vf "scale=-2:480,pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black"')
   outputvideoheight.set('480')
   vres.selection_clear()
 elif selected_vresvalue == "960/1280 x 720 (720p)":
   comboboxvres.set(OPTIONS_VRes[3])
   resolution.set('-vf "scale=-2:720,pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black"')
   outputvideoheight.set('720')
   vres.selection_clear()
 get4by3_resolution()
vres.bind("<<ComboboxSelected>>", updatevres)
vres.bind("<KeyRelease>", updatevres)


def updatemenu_for_streamtype1(*args):
 if sofdecstreamtype.get() == '0':
  vres_streamtype1.place(x=12, y=257)
  vratiobox_streamtype1.place(x=451, y=257)
 else:
  vres_streamtype1.place_forget()
  vratiobox_streamtype1.place_forget()
sofdecstreamtype.trace_add("write", updatemenu_for_streamtype1)



OPTIONS_VRatio = ["None", "Crop (16:9 to 4:3)", "Scale (16:9 to 4:3)", "Stretch (4:3 to 16:9)"] #"Scale (4:3 to 16:9)"]
vratio = StringVar()
outputvideowidth = StringVar()
comboboxvratio = StringVar()
vratiobox = ttk.Combobox(master, value=OPTIONS_VRatio, textvariable=comboboxvratio, width=18)
vratiobox.place(x=451, y=257)
vratiobox.current(0)
vratiobox.state(["readonly"])

def updatevratio(event):
 selected_vratiovalue = comboboxvratio.get()
 if selected_vratiovalue == "None":
  comboboxvratio.set(OPTIONS_VRatio[0])
  vratio.set('')
  vratiobox.selection_clear()
 elif selected_vratiovalue == "Crop (16:9 to 4:3)":
  comboboxvratio.set(OPTIONS_VRatio[1])
  vratio.set('-vf "crop=(ih*4/3):ih"')
  vratiobox.selection_clear()
 elif selected_vratiovalue == "Scale (16:9 to 4:3)":
  comboboxvratio.set(OPTIONS_VRatio[2])
  vratio.set('-filter:v "pad=iw:iw*3/4:(ow-iw)/2:(oh-ih)/2"')
  vratiobox.selection_clear()
 elif selected_vratiovalue == "Stretch (4:3 to 16:9)":
  comboboxvratio.set(OPTIONS_VRatio[3])
  vratio.set('-vf "crop=(ih*16/9):ih"')
  vratiobox.selection_clear()
 elif selected_vratiovalue == "Scale (4:3 to 16:9)":
  comboboxvratio.set(OPTIONS_VRatio[4])
  vratio.set('')
  vratiobox.selection_clear()
 updatevres(event)
vratiobox.bind("<<ComboboxSelected>>", updatevratio)


OPTIONS_VRes_streamtype1 = ["Same as Video", "128 x 128", "160 x 128", "320 x 240", "256 x 256", "480 x 336", "320 x 480", "640 x 480"]
resolution_streamtype1 = StringVar()
comboboxvres_streamtype1 = StringVar()
vres_streamtype1 = ttk.Combobox(master, value=OPTIONS_VRes_streamtype1)
vres_streamtype1.current(5)
vres_streamtype1.state(["readonly"]) #Lock combobox since muxer used for Stream1 SFDs only works with specific resolutions.

def updatevres_streamtype1(event):
 selected_vresvalue = vres_streamtype1.get()
 if "x" in selected_vresvalue:
  custom_resolution = selected_vresvalue.split("x")
  if len(custom_resolution) == 2:
    try:
     width = int(custom_resolution[0])
     height = int(custom_resolution[1])
     resolution_streamtype1.set(f'scale={width}:{height},pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black')
     comboboxvres_streamtype1.set(selected_vresvalue)
     vres_streamtype1.selection_clear()
    except ValueError:
     pass
 if selected_vresvalue == "Same As Video":
   comboboxvres_streamtype1.set(OPTIONS_VRes_streamtype1[0])
   comboboxvres_streamtype1.set("Same As Video")
   resolution_streamtype1.set("")
   vres_streamtype1.selection_clear()
 elif selected_vresvalue == "128 x 128":
   comboboxvres_streamtype1.set(OPTIONS_VRes_streamtype1[1])
   resolution_streamtype1.set('128:128')
   vres_streamtype1.selection_clear()
 elif selected_vresvalue == "160 x 128":
   comboboxvres_streamtype1.set(OPTIONS_VRes_streamtype1[2])
   resolution_streamtype1.set('160:128')
   vres_streamtype1.selection_clear()
 elif selected_vresvalue == "320 x 240":
   comboboxvres_streamtype1.set(OPTIONS_VRes_streamtype1[3])
   resolution_streamtype1.set('320:240')
   vres_streamtype1.selection_clear()
 elif selected_vresvalue == "256 x 256":
   comboboxvres_streamtype1.set(OPTIONS_VRes_streamtype1[3])
   resolution_streamtype1.set('256:256')
   vres_streamtype1.selection_clear()
 elif selected_vresvalue == "480 x 336":
   comboboxvres_streamtype1.set(OPTIONS_VRes_streamtype1[4])
   resolution_streamtype1.set('480:336')
   vres_streamtype1.selection_clear()
 elif selected_vresvalue == "320 x 480":
   comboboxvres_streamtype1.set(OPTIONS_VRes_streamtype1[5])
   resolution_streamtype1.set('320:480')
   vres_streamtype1.selection_clear()
 elif selected_vresvalue == "640 x 480":
   comboboxvres_streamtype1.set(OPTIONS_VRes_streamtype1[6])
   resolution_streamtype1.set('640:480')
   vres_streamtype1.selection_clear()
 updatevratio_streamtype1(event=None)
vres_streamtype1.bind("<<ComboboxSelected>>", updatevres_streamtype1)
vres_streamtype1.bind("<KeyRelease>", updatevres_streamtype1)



OPTIONS_VRatio_streamtype1 = ["Crop to Resolution", "Squish to Resolution", "Scale to Resolution"]
vratio_streamtype1 = StringVar()
comboboxvratio_streamtype1 = StringVar()
vratiobox_streamtype1 = ttk.Combobox(master, value=OPTIONS_VRatio_streamtype1, textvariable=comboboxvratio_streamtype1, width=18)
vratiobox_streamtype1.place(x=451, y=257)
vratiobox_streamtype1.current(2)
vratiobox_streamtype1.state(["readonly"])

def updatevratio_streamtype1(event=None):
 selected_vratiovalue_streamtype1 = comboboxvratio_streamtype1.get()
 global output_resolutionwidth
 output_resolutionwidth = resolution_streamtype1.get().split(":")[0]

 if selected_vratiovalue_streamtype1 == "Crop to Resolution":
  comboboxvratio_streamtype1.set(OPTIONS_VRatio_streamtype1[0])
  vratio_streamtype1.set(f'crop={resolution_streamtype1.get()}')
  vratiobox_streamtype1.selection_clear()
 elif selected_vratiovalue_streamtype1 == "Squish to Resolution":
  comboboxvratio_streamtype1.set(OPTIONS_VRatio_streamtype1[1])
  vratio_streamtype1.set(f'scale={resolution_streamtype1.get()},setsar=1/2')
  vratiobox_streamtype1.selection_clear()
 elif selected_vratiovalue_streamtype1 == "Scale to Resolution":
  comboboxvratio_streamtype1.set(OPTIONS_VRatio_streamtype1[2])
  vratio_streamtype1.set(f'scale={output_resolutionwidth}:-1,pad={resolution_streamtype1.get()}:(ow-iw)/2:(oh-ih)/2')
  vratiobox_streamtype1.selection_clear()
vratiobox_streamtype1.bind("<<ComboboxSelected>>", updatevratio_streamtype1)
vratiobox_streamtype1.bind("<KeyRelease>", updatevratio_streamtype1)



OPTIONS_VFrame = ["Same as Video", "24", "29.97", "30", "59.97", "60"]
framerate = StringVar()
comboboxframerate = StringVar()
vframerate = ttk.Combobox(master, value=OPTIONS_VFrame, textvariable=comboboxframerate)
vframerate.place(x=172, y=257)
vframerate.current(0)
vframerate.state(["readonly"])

def update_customframerate(event):
 master.after(2000, updateframerate, event)

def updateframerate(event):
 selected_vframeratevalue = vframerate.get()
 if selected_vframeratevalue == "Same As Video":
  comboboxframerate.set("Same As Video")
  framerate.set("")
  vframerate.selection_clear()
 elif selected_vframeratevalue == "24":
  comboboxframerate.set(OPTIONS_VFrame[1])
  framerate.set("-r 24")
  vframerate.selection_clear()
 elif selected_vframeratevalue == "29.97":
  comboboxframerate.set(OPTIONS_VFrame[2])
  framerate.set("-r 29.97")
  vframerate.selection_clear()
 elif selected_vframeratevalue == "30":
  comboboxframerate.set(OPTIONS_VFrame[3])
  framerate.set("-r 30")
  vframerate.selection_clear()
 elif selected_vframeratevalue == "59.97":
  comboboxframerate.set(OPTIONS_VFrame[4])
  framerate.set("-r 59.97")
  vframerate.selection_clear()
 elif selected_vframeratevalue == "60":
  comboboxframerate.set(OPTIONS_VFrame[5])
  framerate.set("-r 60")
  vframerate.selection_clear()
 elif selected_vframeratevalue not in ('Same As Video', '24', '29.97', '30', '59.97', '60'):
  custom_framerate = float(selected_vframeratevalue)
  comboboxframerate.set(str(custom_framerate))
  framerate.set("-r " + str(custom_framerate))
  vframerate.selection_clear()
vframerate.bind("<<ComboboxSelected>>", updateframerate)
vframerate.bind("<KeyRelease>", update_customframerate)



OPTIONS_AChannel = ["Stereo (2 Channels)", "Mono (1 Channel)"]
audiochannel = StringVar()
comboboxchannel = StringVar()
achannelbox = ttk.Combobox(master, value=OPTIONS_AChannel, textvariable=comboboxchannel)
achannelbox.place(x=233, y=302)
achannelbox.current(0)
achannelbox.state(["readonly"])

def update_achannel(event):
 selected_achannelvalue = comboboxchannel.get()
 if selected_achannelvalue == "Stereo":
  comboboxchannel.set(OPTIONS_AChannel[0])
  audiochannel.set("-ac 2")
  achannelbox.selection_clear()
 elif selected_achannelvalue == "Mono":
  comboboxchannel.set(OPTIONS_AChannel[1])
  audiochannel.set("-ac 1")
  achannelbox.selection_clear()
achannelbox.bind("<<ComboboxSelected>>", update_achannel)


OPTIONS_streamtype = ["V1 (SFDMUX V1.07)", "V1 (alt)", "V2"]
comboboxstreamtype = StringVar()
streamtypebox = ttk.Combobox(master, value=OPTIONS_streamtype, textvariable=comboboxstreamtype)
streamtypebox.place(x=393, y=302)
streamtypebox.current(2)
streamtypebox.state(["readonly"])

def update_streamtype(event):
 selected_streamtypevalue = comboboxstreamtype.get()
 if selected_streamtypevalue == "V1 (SFDMUX V1.07)":
  comboboxstreamtype.set(OPTIONS_streamtype[0])
  sofdecstreamtype.set("0")
  streamtypebox.selection_clear()
 elif selected_streamtypevalue == "V1 (alt)":
  comboboxstreamtype.set(OPTIONS_streamtype[1])
  sofdecstreamtype.set("1")
  streamtypebox.selection_clear()
 elif selected_streamtypevalue == "V2":
  comboboxstreamtype.set(OPTIONS_streamtype[2])
  sofdecstreamtype.set("2")
  streamtypebox.selection_clear()
streamtypebox.bind("<<ComboboxSelected>>", update_streamtype)
sofdecstreamtype.set('2')




def showoptionswin():
    optwin.deiconify()

def optwinclosing():
    optwin.withdraw()

def showextraaudiotrackswin():
    extraaudiotrackswin.deiconify()

def extraaudiotrackswinclosing():
    extraaudiotrackswin.withdraw()


def write_batchmode_info_tofile():
  batchmode.set(1)
  batchsfdfile = currentdir + 'resource/batch/batchcreate.txt'
  batchvideodir = 'vid'
  batchaudio1dir = "aud1"
  batchaudio2dir = "aud2"

  with open(batchsfdfile, "w") as file:
    file.write(f"batchvideodir={batchvideodir}\n")
    file.write(f"batchaudio1dir={batchaudio1dir}\n")
    file.write(f"batchaudio2dir={batchaudio2dir}\n")

  addSFDtolistbtn = Button(text="Add SFD to list", command=write_batchmode_info_tofile, padx=40, pady=5).place(x=1, y=355)

def change_SFDmuxerbtn_batch():
 if batchmode.get() == 1:
  SFDmuxerbtn.config(text="Add to List!", command=write_batchmode_info_tofile, padx=80, pady=15).place(x=345, y=353)
 else:
  SFDmuxerbtn.config(text="Create the SFD!", command=createSFD, padx=80, pady=15).place(x=345, y=353)
#change_SFDmuxerbtn_batch() #Run on boot so that SFD button exists

SFDmuxerbtn = Button(text="Create the SFD!", command=createSFD, padx=80, pady=15).place(x=345, y=363) #.place(x=345, y=353)
extraoptions = Button(text="Extra Options", command=showoptionswin, padx=36.3, pady=1).place(x=12, y=354)
opengithubrepobtn = Button(text="Open GitHub Repo", command=opengithubrepo, padx=23, pady=1).place(x=173, y=354)
aboutcreator = Button(text="About Program", command=aboutprogram, padx=30.4, pady=1).place(x=12, y=384)
programdocuments = Button(text="Documentation", command=docs, padx=30.3, pady=1).place(x=12, y=414)
#settingoptions = Button(text="Setting Options", command=openpresetwindow, padx=32, pady=1).place(x=173, y=384)
#presetbtn = Button(text="Save/Load Preset", command=openpresetwindow, padx=28, pady=1).place(x=173, y=414)

vidselect = Label(dirframe, text="Video File:", font = ("Arial Bold", 8)).place(x=3, y=-1)
aud1select = Label(dirframe, text="Audio for Track 1:", font = ("Arial Bold", 8)).place(x=3, y=39)
outputdirselect = Label(outputdirframe, text="Output Directory:", font = ("Arial Bold", 8)).place(x=127, y=184)
outputsfdnameselect = Label(outputdirframe, text="SFD Filename:", font = ("Arial Bold", 8)).place(x=9, y=184)

UseVideoAudio = IntVar()
videoaudiocheck = ttk.Checkbutton(text='Use Audio from Input Video', variable=UseVideoAudio, command=videoaudio, onvalue=1, offvalue=0).place(x=12, y=137)
UseTrack1forTrack2 = IntVar()
track1fortrack2check = ttk.Checkbutton(text='Use Track 1 Audio for Track 2', variable=UseTrack1forTrack2, command=copyaudio, onvalue=1, offvalue=0).place(x=192, y=137)

batchmode = IntVar()
enablebatchmode = IntVar()
#batchmodecheck = ttk.Checkbutton(text='Enable Batch Mode', variable=enablebatchmode, command=change_SFDmuxerbtn_batch, onvalue=1, offvalue=0).place(x=405, y=410)


keepAVI = IntVar()
keepMPEG = IntVar()
keepADX = IntVar()
keepWAV = IntVar()
keepsfdmuxlog = IntVar()
filePathvideo = StringVar()
filePathaudt1 = StringVar()
filePathaudt2 = StringVar()
filePathaudt3 = StringVar()
filePathaudt4 = StringVar()
SFDfilename = StringVar()
dirPath = StringVar()
bitexactcmd = StringVar()
ffmpegstartdurationcmd = StringVar()
ffmpegenddurationcmd = StringVar()

entryvid = ttk.Entry(dirframe, textvariable=filePathvideo, width=72)
entryvid.insert(0, "")
entryvid.place(x=5, y=15)
browsevid = Button(text="Browse", command=GetVideo, padx=40, pady=5).place(x=455, y=25)

entryaud1 = ttk.Entry(dirframe, textvariable=filePathaudt1, width=72)
entryaud1.insert(0, "")
entryaud1.place(x=5, y=55)
browseaud1 = Button(text="Browse", command=GetAud1, padx=40, pady=5).place(x=455, y=65)

entryaud2 = ttk.Entry(dirframe, textvariable=filePathaudt2, width=72)
entryaud2.insert(0, "")
entryaud2.place(x=5, y=95)

entryDir = ttk.Entry(outputdirframe, textvariable=dirPath, width=52)
entryDir.insert(0, "")
entryDir.place(x=130, y=202)
browseexport = Button(text="Browse", command=ChooseExportDir, padx=40, pady=5).place(x=455, y=195)

entryFilename = ttk.Entry(outputdirframe, textvariable=SFDfilename, width=16)
entryFilename.insert(0, "")
entryFilename.place(x=13, y=202)




advancedopt()
extraaudiotracks()
optwin.protocol("WM_DELETE_WINDOW", optwinclosing)
extraaudiotrackswin.protocol("WM_DELETE_WINDOW", extraaudiotrackswinclosing)
extraaudiotrackswinclosing()


def updater_exe():
 updaterlocation = os.getcwd() + '/updater.exe'
 if os.path.isfile(updaterlocation):
  runupdater = f'"{updaterlocation}"'
  subprocess.run(runupdater, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
 else:
  print("Unable to find updater.exe, program will not be able to update.")
  pass
updater_exe()
check_for_ffmpeg()


readline = 0
def loadsettings():
 global readline
 readline += 1
 settingsini = currentdir + '/bin/settings_sfdcreator.txt'
 with open(settingsini, "r") as file:
   lines = file.readlines()
   if readline >= len(lines):
    print("Settings applied.")
    return
   else:
    if 0 <= readline < len(lines):
     if readline == 1:
      crfvalue.set(lines[readline].strip())
      print(crfvalue.get())
#loadsettings()


def savesettings():
 readline = IntVar()
 readline += 1
 #settingsini = currentdir + '/settings-sfdcreator.ini'
 settingsini = currentdir + '/bin/settings_sfdcreator.ini'
 with open(settingsini, "r") as file:
   lines = file.readlines()
   if readline >= len(lines):
    print("Settings have been applied")
    return
   else:
    if readline == 1:
     lines[0] = f'CRF={crfvalue.get()}\n'
    elif readline == 2:
     lines[1] = '2\n'
   
    #Run loop until settings saved
    with open(settingsini, 'w') as file:
     file.writelines(lines)
    savesettings()
#savesettings()

def checkfiles():
 if os.path.isfile('file.sfd'):
  os.remove('file.sfd')
 videoname = os.path.basename(filePathvideo.get())
 videoextension = os.path.splitext(videoname)[1]
 if os.path.isfile(f'video{videoextension}'):
  os.remove(f'video{videoextension}')
 if os.path.isfile('track1.adx'):
  os.remove('track1.adx')
 if os.path.isfile('track2.adx'):
  os.remove('track2.adx')
 if os.path.isfile('track3.adx'):
  os.remove('track3.adx')
 if os.path.isfile('track4.adx'):
  os.remove('track4.adx')
 if os.path.isfile('track1.sfa'):
  os.remove('track1.sfa')
 if os.path.isfile('track2.sfa'):
  os.remove('track2.sfa')
 if os.path.isfile('track3.sfa'):
  os.remove('track3.sfa')
 if os.path.isfile('track4.sfa'):
  os.remove('track4.sfa')
 if os.path.isfile('log.txt'):
  os.remove('log.txt')
 if os.path.exists(f'blank.{audiofiletype.get()}'):
  os.remove(f'blank.{audiofiletype.get()}')
 if os.path.exists(f'blankt2.{audiofiletype.get()}'):
  os.remove(f'blankt2.{audiofiletype.get()}')
 if os.path.exists(f'blankt3.{audiofiletype.get()}'):
  os.remove(f'blankt3.{audiofiletype.get()}')
 if os.path.exists(f'blankt4.{audiofiletype.get()}'):
  os.remove(f'blankt4.{audiofiletype.get()}')
 if os.path.exists(f'track1.{audiofiletype.get()}'):
  os.remove(f'track1.{audiofiletype.get()}')
 if os.path.exists(f'track2.{audiofiletype.get()}'):
  os.remove(f'track2.{audiofiletype.get()}')
 if os.path.exists(f'track3.{audiofiletype.get()}'):
  os.remove(f'track2.{audiofiletype.get()}')
 if os.path.exists(f'track4.{audiofiletype.get()}'):
  os.remove(f'track2.{audiofiletype.get()}')
 if os.path.isfile('AVIconvert.avi'):
  os.remove('AVIconvert.avi')
 if os.path.isfile(f'newvideo.{outputmpegextension.get()}'):
  os.remove(f'newvideo.{outputmpegextension.get()}')
 if os.path.isfile(f'newvideo.mpeg'): #Just in case fix has to be used for SofdecStream1
  os.remove(f'newvideo.mpeg')
 if useexternalsfdmuxer.get() == 1:
  os.remove(muxer_files)

def closeprogram():
 killffmpeg = 'taskkill /F /IM ffmpeg.exe'
 os.system(killffmpeg)
 os._exit(0)

atexit.register(savesettings)
atexit.register(checkfiles)
atexit.register(closeprogram)
master.mainloop()