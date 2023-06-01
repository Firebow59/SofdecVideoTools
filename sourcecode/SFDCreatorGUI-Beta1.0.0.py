from tkinter import filedialog, ttk, messagebox, Frame, LabelFrame, Label, StringVar, Button, Toplevel, IntVar
import tkinter as tk
import os
from os import path
import shutil
import webbrowser

master = tk.Tk()
master.geometry("600x450"), master.title("SFDCreator Beta 1.0.0"), master.resizable(False, False)#, master.iconbitmap("resource/icon/sfdextractor.ico")
advancedopt = Frame(master, bg='#f0f0f0').place(relx=0.0, rely=0.0, relheight=1.006, relwidth=1.004)
dirframe = LabelFrame(master, text="Input Files")
dirframe.place(relx=0.010, rely=0.0, relheight=0.365, relwidth=0.980) #leave this .place seperate from the "dirframe =" to avoid position issue.
outputdirframe = LabelFrame(master, text="Output File").place(relx=0.010, rely=0.37, relheight=0.368, relwidth=0.980)
otherframe = LabelFrame(master, text="Other").place(relx=0.010, rely=0.745, relheight=0.250, relwidth=0.300) #alternate box: .place(relx=0.010, rely=0.745, relheight=0.250, relwidth=0.570)

def GetVideo():
    video = filedialog.askopenfilename(title="Select A Video File", filetypes=[("Video files", ".mpeg .mpg .m1v .mp4 .avi .wmv .mkv .mov")])
    filePathvideo.set(video)

def GetAud1():
    audt1 = filedialog.askopenfilename(title="Select A Audio File for Track 1", filetypes=[("Audio files", ".wav .mp3 .flac .mp2 .adx .ogg")])
    filePathaudt1.set(audt1)

def GetAud2():
    audt2 = filedialog.askopenfilename(title="Select A Audio File for Track 2", filetypes=[("Audio files", ".wav .mp3 .flac .mp2 .adx .ogg")])
    filePathaudt2.set(audt2)

def ChooseExportDir():
    exportpath = filedialog.askdirectory(title="Choose An Output Directory")
    dirPath.set(exportpath)
    if not os.path.exists(dirPath.get()):
     tk.messagebox.showerror(title='Directory Error', message="Can't find the directory selected. Try again, or select a different directory.")

def openrepo():
 webbrowser.open("https://github.com/Firebow59/SofdecVideoTools")

def openissuespage():
 webbrowser.open("https://github.com/Firebow59/SofdecVideoTools/issues")

def aboutprogram():
 link = 'This tool is intended for creating Sofdec video files (or SFD files for short) for use in various games. Developed by Firebow59.'
 aboutprogramwindow = tk.messagebox.showinfo(title='About Program', message=link)

def showoptionswin():
    optwin.deiconify()

def optwinclosing():
    optwin.withdraw()

def advancedopt():
  global optwin
  global crfvalue
  crfvalue = StringVar()
  global usebitexact
  usebitexact = IntVar()
  global disableaudiopadding
  disableaudiopadding = IntVar()
  
  optwin = Toplevel(master)
  optwin.geometry("500x250"), optwin.title("Extra Options"), optwin.resizable(False, False)
  ffmpegsettingsframe = LabelFrame(optwin, text="Additional FFmpeg Settings").place(relx=0.010, rely=0.005, relheight=0.390, relwidth=0.983)
  keepframe = LabelFrame(optwin, text="Keep File(s)").place(relx=0.010, rely=0.41, relheight=0.285, relwidth=0.983)

  opengithub = Button(optwin, text="Open GitHub Page", command=openrepo, padx=20, pady=5).place(x=66, y=195)
  openissues = Button(optwin, text="Report an Issue (GitHub)", command=openissuespage, padx=20, pady=5).place(x=251, y=195)

  AVI = ttk.Checkbutton(optwin, text='Keep converted AVI file', variable=keepAVI, onvalue=1, offvalue=0).place(x=11, y=123)
  MPEG = ttk.Checkbutton(optwin, text='Keep converted MPEG file', variable=keepMPEG, onvalue=1, offvalue=0).place(x=11, y=142)
  ADX = ttk.Checkbutton(optwin, text='Keep converted ADX file(s)', variable=keepADX, onvalue=1, offvalue=0).place(x=173, y=123)
  WAV = ttk.Checkbutton(optwin, text='Keep converted WAV file(s)', variable=keepWAV, onvalue=1, offvalue=0).place(x=173, y=142)
  log = ttk.Checkbutton(optwin, text='Keep sfdmux log file', variable=keepsfdmuxlog, onvalue=1, offvalue=0).place(x=348, y=123)

  crfentry = ttk.Entry(optwin, textvariable=crfvalue, width=12)
  crfentry.insert(0, "")
  crfentry.place(x=11, y=41)
  crflbl = Label(optwin, text="CRF Value:", font=("Arial Bold", 8)).place(x=8, y=21)

  if crfentry.get() == '':
   crfentry.insert(0, "01")

  bitexactcheck = ttk.Checkbutton(optwin, text='Use -bitexact for audio', variable=usebitexact, onvalue=1, offvalue=0)
  bitexactcheck.place(x=11, y=70)

  OPTIONS_ffmpegloglevel = ["No Command", "Error + Hide Banner", "Error", "Warning", "Fatal", "Loglevel 0"]

  comboboxffmpegloglevel = StringVar()
  global ffmpegloglevel
  ffmpegloglevel = StringVar()
  ffmpegloglevelbox = ttk.Combobox(optwin, value=OPTIONS_ffmpegloglevel, width=18)
  ffmpegloglevelbox.place(x=110, y=41)
  ffmpegloglevelbox.current(0)
  ffmpegloglevelbox.state(["readonly"])
  ffmpegloglevellbl = Label(optwin, text="FFmpeg Loglevel:", font=("Arial Bold", 8)).place(x=107, y=21)

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
  ffmpegspeedpresetbox.place(x=260, y=341) #.place(x=260, y=41)
  ffmpegspeedpresetbox.current(5)
  ffmpegspeedpresetbox.state(["readonly"])
  ffmpegspeedpresetlbl = Label(optwin, text="FFmpeg Speed Preset:", font=("Arial Bold", 8)).place(x=257, y=321) #.place(x=257, y=21)

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

  optwin.withdraw()

def videoaudio():
 if UseVideoAudio.get() == 1:
  filePathaudt1.set(filePathvideo.get())
 if UseVideoAudio.get() == 0:
  filePathaudt1.set("")
  if copyaudio == 1:
   filePathaudt2.set(filePathvideo.get())

def copyaudio():
 if UseTrack1forTrack2.get() == 1:
  filePathaudt2.set(filePathaudt1.get())
 if UseTrack1forTrack2.get() == 0:
  filePathaudt2.set("")

def docs():
  os.startfile("sfdcreator.pdf")

def SFDmux():
    videofile = StringVar.get(filePathvideo)
    if not os.path.exists(StringVar.get(filePathvideo)):
     videomissing = tk.messagebox.showerror(title='File Error', message='No video file was selected! Please select a video file to continue.')
     return
    if not os.path.exists(dirPath.get()):
     tk.messagebox.showerror(title='Directory Error', message="Can't find the directory selected. Try again, or select a different directory.")
     return

    audio1 = filePathaudt1.get()
    if not os.path.exists(StringVar.get(filePathaudt1)):
      print("No audio found for track 1, filling with padding audio")
      silentfile = 'blank.wav'
      ffprobe_cmd = f'ffprobe -i "{videofile}" -show_entries format=duration -v quiet -of csv="p=0"'
      duration = float(os.popen(ffprobe_cmd).read().strip())
      ffmpeg_cmd = f'ffmpeg -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=11025 -t {duration} -b:a 8k -shortest "blank.wav"'
      os.system(ffmpeg_cmd)
      filePathaudt1.set(silentfile)

    audio2 = filePathaudt2.get()
    if not os.path.exists(StringVar.get(filePathaudt2)):
      print("No audio found for track 2, filling with padding audio")
      silentfile = 'blankt2.wav'
      ffprobe_cmd = f'ffprobe -i "{videofile}" -show_entries format=duration -v quiet -of csv="p=0"'
      duration = float(os.popen(ffprobe_cmd).read().strip())
      ffmpeg_cmd = f'ffmpeg -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=11025 -t {duration} -b:a 2k -shortest "blankt2.wav"'
      os.system(ffmpeg_cmd)
      filePathaudt2.set(silentfile)

    command=f"ffmpeg -y {ffmpegloglevel.get()} -i {videofile} {ffmpegspeedpreset.get()} -crf 01 -b:v 30000000 {framerate.get()} {resolution.get()} {vratio.get()} AVIconvert.avi"
    os.system(command)
    command=f"ffmpeg -y {ffmpegloglevel.get()} -i AVIconvert.avi {ffmpegspeedpreset.get()} -crf 01 -b:v {vbitrate.get()} {framerate.get()} {resolution.get()} -c:v mpeg1video newvideo.mpeg"
    os.system(command)
    command=f"ffmpeg -y {ffmpegloglevel.get()} -i {audio1} -b:a {abitrate.get()} -ar {aHz.get()} {audiochannel.get()} track1.wav"
    os.system(command)
    command=f"ffmpeg -y {ffmpegloglevel.get()} -i track1.wav -b:a {abitrate.get()} -ar {aHz.get()} {audiochannel.get()} track1.adx"
    os.system(command)
    command=f"ffmpeg -y {ffmpegloglevel.get()} -i {audio2} -b:a {abitrate.get()} -ar {aHz.get()} {audiochannel.get()} track2.wav"
    os.system(command)
    command=f"ffmpeg -y {ffmpegloglevel.get()} -i track2.wav -b:a {abitrate.get()} -ar {aHz.get()} {audiochannel.get()} track2.adx"
    os.system(command)
    command=f"sfdmux.exe newSFD.sfd newvideo.mpeg track1.adx track2.adx"
    os.system(command)
    if os.path.exists('blank.wav'):
     os.remove('blank.wav')
    else:
     pass
    if os.path.exists('blankt2.wav'):
     os.remove('blankt2.wav')
    else:
     pass

    min_file_size = 1024
    file_size_kb = os.path.getsize('newSFD.sfd') // 1024
    if file_size_kb < min_file_size:
     SFDfilesizeerror = tk.messagebox.showerror('SFD Error', "newSFD.sfd couldn't be properly created. Try creating the file again.")
     os.remove("newSFD.sfd")
    else:
     SFDCreated = tk.messagebox.showinfo('SFD Created', "newSFD.sfd was successfully created! Enjoy!")
    
    currentdir = os.getcwd()
    source_filesfd = os.path.join(currentdir, 'newSFD.sfd')
    if os.path.exists(source_filesfd):
     dest_dir_sfd = dirPath.get()
     dest_filesfd = os.path.join(dest_dir_sfd, 'newSFD.sfd')
     shutil.move(source_filesfd, dest_filesfd)
    
    if IntVar.get(keepAVI) == 1:
     currentdir = os.getcwd()
     source_fileavi = os.path.join(currentdir, 'AVIconvert.avi')
     if os.path.exists(source_fileavi):
      dest_dir_avi = dirPath.get()
      dest_fileavi = os.path.join(dest_dir_avi, 'AVIconvert.avi')
      shutil.move(source_fileavi, dest_fileavi)
    else:
     os.remove('AVIconvert.avi')
    
    if IntVar.get(keepMPEG) == 1:
     currentdir = os.getcwd()
     source_filempg = os.path.join(currentdir, 'newvideo.mpeg')
     if os.path.exists(source_filempg):
      dest_dirmpg = dirPath.get()
      dest_filempg = os.path.join(dest_dirmpg, 'newvideo.mpeg')
      shutil.move(source_filempg, dest_filempg)
    else:
     os.remove('newvideo.mpeg')
    
    if IntVar.get(keepsfdmuxlog) == 1:
     currentdir = os.getcwd()
     source_filelog = os.path.join(currentdir, 'log.txt')
     if os.path.exists(source_filelog):
      dest_dirlog = dirPath.get()
      dest_filelog = os.path.join(dest_dirlog, 'log.txt')
      shutil.move(source_filelog, dest_filelog)
    else:
     os.remove('log.txt')

    if IntVar.get(keepWAV) == 1:
     currentdir = os.getcwd()
     source_filea1 = os.path.join(currentdir, 'track1.wav')
     if os.path.exists(source_filea1):
      dest_diradx1 = dirPath.get()
      dest_fileaud1 = os.path.join(dest_diradx1, 'track1.wav')
      if os.path.exists(source_filea1):
       shutil.move(source_filea1, dest_fileaud1)
      else:
       print("track1.wav not found, unable to move to destination directory.")
    else:
     currentdir = os.getcwd()
     source_filea1 = os.path.join(currentdir, 'track1.wav')
     if os.path.exists(source_filea1):
      os.remove(source_filea1)

    if IntVar.get(keepADX) == 1:
     currentdir = os.getcwd()
     source_fileadx1 = os.path.join(currentdir, 'track1.adx')
     if os.path.exists(source_fileadx1):
      dest_diradx1 = dirPath.get()
      dest_fileadx1 = os.path.join(dest_diradx1, 'track1.adx')
      if os.path.exists(source_fileadx1):
       shutil.move(source_fileadx1, dest_fileadx1)
      else:
       print("track1.adx not found, unable to move to destination directory.")
    else:
     currentdir = os.getcwd()
     source_fileadx1 = os.path.join(currentdir, 'track1.adx')
     if os.path.exists(source_fileadx1):
      os.remove(source_fileadx1)

    if IntVar.get(keepWAV) == 1:
     source_filea2 = os.path.join(currentdir, 'track2.wav')
     if os.path.exists(source_filea2):
      dest_dira2 = dirPath.get()
      dest_filea2 = os.path.join(dest_dira2, 'track2.wav')
      if os.path.exists(source_filea2):
       shutil.move(source_filea2, dest_filea2)
      else:
       print("track2.wav not found, unable to move to destination directory.")
    else:
     currentdir = os.getcwd()
     source_filea2 = os.path.join(currentdir, 'track2.wav')
     if os.path.exists(source_filea2):
      os.remove(source_filea2)
    
    if IntVar.get(keepADX) == 1:
     source_fileadx2 = os.path.join(currentdir, 'track2.adx')
     if os.path.exists(source_fileadx2):
      dest_diradx2 = dirPath.get()
      dest_fileadx2 = os.path.join(dest_diradx2, 'track2.adx')
      if os.path.exists(source_fileadx2):
       shutil.move(source_fileadx2, dest_fileadx2)
      else:
       print("track2.adx not found, unable to move to destination directory.")
    else:
     currentdir = os.getcwd()
     source_fileadx2 = os.path.join(currentdir, 'track2.adx')
     if os.path.exists(source_fileadx2):
      os.remove(source_fileadx2)
    
    return

browsevid = Button(text="Browse", command=GetVideo, padx=40, pady=5).place(x=455, y=25)
browseaud1 = Button(text="Browse", command=GetAud1, padx=40, pady=5).place(x=455, y=65)
browseaud2 = Button(text="Browse", command=GetAud2, padx=40, pady=5).place(x=455, y=105)
browseexport = Button(text="Browse", command=ChooseExportDir, padx=40, pady=5).place(x=455, y=195)
SFDmuxer = Button(text="Create the SFD!", command=SFDmux, padx=150, pady=15).place(x=200, y=368)
extraoptions = Button(text="Extra Options", command=showoptionswin, padx=36.3, pady=1).place(x=18, y=354)
#opengithubrepo = Button(text="Open GitHub Repo", command=openrepo, padx=21.5, pady=1).place(x=183, y=354)
aboutcreator = Button(text="About Program", command=aboutprogram, padx=30.4, pady=1).place(x=18, y=384)
programdocuments = Button(text="Documentation", command=docs, padx=30.3, pady=1).place(x=18, y=414)

vidselect = Label(dirframe, text="Select A Video File:", font = ("Arial Bold", 8)).place(x=3, y=-1)
aud1select = Label(dirframe, text="Select An Audio File for Track 1:", font = ("Arial Bold", 8)).place(x=3, y=39)
aud2select = Label(dirframe, text="Select An Audio File for Track 2:", font = ("Arial Bold", 8)).place(x=3, y=79)
outputdirselect = Label(outputdirframe, text="Select An Output Directory:", font = ("Arial Bold", 8)).place(x=9, y=184)
videoreslabel = Label(outputdirframe, text="Video Resolution:", font = ("Arial Bold", 8)).place(x=10, y=240)
videoframeratelabel = Label(outputdirframe, text="Video Framerate:", font = ("Arial Bold", 8)).place(x=169, y=240)
vidbitrateselect = Label(outputdirframe, text="Video Bitrate:", font = ("Arial Bold", 8)).place(x=332, y=240)
audbitrateselect = Label(outputdirframe, text="Audio Bitrate:", font = ("Arial Bold", 8)).place(x=9, y=285)
audhzselect = Label(outputdirframe, text="Audio Hz:", font = ("Arial Bold", 8)).place(x=119, y=285)
audchannelselect = Label(outputdirframe, text="Audio Channel Type:", font = ("Arial Bold", 8)).place(x=230, y=285)
videoratiooptions = Label(outputdirframe, text="Scale/Crop Settings:", font = ("Arial Bold", 8)).place(x=448, y=240)

UseVideoAudio = IntVar()
videoaudiocheck = ttk.Checkbutton(text='Use Audio from Input Video', variable=UseVideoAudio, command=videoaudio, onvalue=1, offvalue=0).place(x=12, y=137)
UseTrack1forTrack2 = IntVar()
track1fortrack2check = ttk.Checkbutton(text='Use Track 1 Audio for Track 2', variable=UseTrack1forTrack2, command=copyaudio, onvalue=1, offvalue=0).place(x=192, y=137)

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

OPTIONS_VRes = ["Same as Video", #0
"320/426 x 240 (240p)",   #1
"480/640 x 360 (360p)",   #2
"640/848 x 480 (480p)",   #3
"960/1280 x 720 (720p)",  #4
]

resolution = StringVar()
comboboxvres = StringVar()
vres = ttk.Combobox(master, value=OPTIONS_VRes)
vres.place(x=12, y=257)
vres.current(0)

def updatevres(event):
 selected_vresvalue = vres.get()
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
  vres.selection_clear()
 elif selected_vresvalue == "320/426 x 240 (240p)":
  comboboxvres.set(OPTIONS_VRes[1])
  resolution.set('-vf "scale=-2:240,pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black"')
  vres.selection_clear()
 elif selected_vresvalue == "480/640 x 360 (360p)":
  comboboxvres.set(OPTIONS_VRes[2])
  resolution.set('-vf "scale=-2:360,pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black"')
  vres.selection_clear()
 elif selected_vresvalue == "640/848 x 480 (480p)":
  comboboxvres.set(OPTIONS_VRes[3])
  resolution.set('-vf "scale=-2:480,pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black"')
  vres.selection_clear()
 elif selected_vresvalue == "960/1280 x 720 (720p)":
  comboboxvres.set(OPTIONS_VRes[3])
  resolution.set('-vf "scale=-2:720,pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black"')
  vres.selection_clear()
vres.bind("<<ComboboxSelected>>", updatevres)
vres.bind("<KeyRelease>", updatevres)

OPTIONS_VFrame = ["Same as Video", #0
"24",      #1
"29.97",   #2
"30",      #3
"59.97",   #4
"60",      #5
]

framerate = StringVar()
comboboxframerate = StringVar()
vframerate = ttk.Combobox(master, value=OPTIONS_VFrame, textvariable=comboboxframerate)
vframerate.place(x=172, y=257)
vframerate.current(0)
vframerate.state(["readonly"])

def updateframerate(event):
 selected_value = vframerate.get()
 if selected_value == "Same As Video":
  comboboxframerate.set("Same As Video")
  framerate.set("")
  vframerate.selection_clear()
 elif selected_value == "24":
  comboboxframerate.set(OPTIONS_VFrame[1])
  framerate.set("-r 24")
  vframerate.selection_clear()
 elif selected_value == "29.97":
  comboboxframerate.set(OPTIONS_VFrame[2])
  framerate.set("-r 29.97")
  vframerate.selection_clear()
 elif selected_value == "30":
  comboboxframerate.set(OPTIONS_VFrame[3])
  framerate.set("-r 30")
  vframerate.selection_clear()
 elif selected_value == "59.97":
  comboboxframerate.set(OPTIONS_VFrame[4])
  framerate.set("-r 59.97")
  vframerate.selection_clear()
 elif selected_value == "60":
  comboboxframerate.set(OPTIONS_VFrame[5])
  framerate.set("-r 60")
  vframerate.selection_clear()
vframerate.bind("<<ComboboxSelected>>", updateframerate)

OPTIONS_VRatio = ["None", "Crop (16:9 to 4:3)", "Scale (16:9 to 4:3)", "Stretch (4:3 to 16:9)"] #Add , "Scale (4:3 to 16:9)"]
vratio = StringVar()
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
  vratio.set('-vf "scale=iw*min({vwidth}/iw\\,{vheight}/ih):ih*min({vwidth}/iw\\,{vheight}/ih),pad={vwidth}:(ow-iw)/2:(oh-ih)/2"')
  vratiobox.selection_clear()
 elif selected_vratiovalue == "Stretch (4:3 to 16:9)":
  comboboxvratio.set(OPTIONS_VRatio[3])
  vratio.set('-filter:v "crop=(ih*16/9):ih"')
  vratiobox.selection_clear()
 elif selected_vratiovalue == "Scale (4:3 to 16:9)":
  comboboxvratio.set(OPTIONS_VRatio[4])
  vratio.set('')
  vratiobox.selection_clear()
vratiobox.bind("<<ComboboxSelected>>", updatevratio)

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

keepAVI = IntVar()
keepMPEG = IntVar()
keepADX = IntVar()
keepWAV = IntVar()
keepsfdmuxlog = IntVar()
filePathvideo = StringVar()
filePathaudt1 = StringVar()
filePathaudt2 = StringVar()
dirPath = StringVar()
entryvid = ttk.Entry(dirframe, textvariable=filePathvideo, width=72)
entryvid.insert(0, "")
entryvid.place(x=5, y=15)
entryaud1 = ttk.Entry(dirframe, textvariable=filePathaudt1, width=72)
entryaud1.insert(0, "")
entryaud1.place(x=5, y=55)
entryaud2 = ttk.Entry(dirframe, textvariable=filePathaudt2, width=72)
entryaud2.insert(0, "")
entryaud2.place(x=5, y=95)
entryDir = ttk.Entry(outputdirframe, textvariable=dirPath, width=72)
entryDir.insert(0, "")
entryDir.place(x=12, y=202)

advancedopt()
optwin.protocol("WM_DELETE_WINDOW", optwinclosing)
if os.path.isfile('updater.exe'):
 os.startfile('updater.exe')
else:
 print("Unable to find updater.exe, program will not be able to update.")
 pass
master.mainloop()