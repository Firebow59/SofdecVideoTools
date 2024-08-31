import tkinter as tk
import os
import shutil
import atexit
import subprocess

from tkinter import filedialog, ttk, messagebox, Frame, LabelFrame, Label, StringVar, Button, Toplevel, IntVar
#Make sure you have check_for_ffmpeg.py in the same folder as this PY file, or else the program won't work.
from check_for_ffmpeg import ffmpeg_location_int, ffprobe_location_int, run_ffmpeg_check, update_ffmpeg


master = tk.Tk()
master.geometry("600x300"), master.title("SFDExtractor V1.0.0"), master.resizable(False, False)#, master.iconbitmap("resource/icon/sfdextractor.ico")
page1 = Frame(master, bg='#f0f0f0').place(relx=0.0, rely=0.0, relheight=1.006, relwidth=1.004)
dirframe = LabelFrame(master, text="Directories")
dirframe.place(relx=0.010, rely=0.0, relheight=0.365, relwidth=0.980)
optframe = LabelFrame(master, text="Extraction Type").place(relx=0.010, rely=0.370, relheight=0.350, relwidth=0.340) 
optoptionalframe = LabelFrame(master, text="Extraction Options").place(relx=0.360, rely=0.370, relheight=0.350, relwidth=0.630)
otherframe = LabelFrame(master, text="Other").place(relx=0.010, rely=0.720, relheight=0.270, relwidth=0.300)

#GUI Vars
currentdir = os.getcwd()
SFDfilepath = StringVar()
dirPath = StringVar()
SFDname = StringVar()
vbitrate = StringVar()
crfvalue = StringVar()
showffmpegcommands = IntVar()
deleteoriginalsfd = IntVar()
extracttofolder = IntVar()
autooverwritefiles = IntVar()
useoriginalsfd = IntVar()
copyvideocodec = IntVar()
usebitexact = IntVar()
monoaudio = IntVar()
monocmd = StringVar()
extravideo = IntVar()
vcodec = StringVar()
abitrate = StringVar()

videoextension = StringVar()
extractiontypeoption=IntVar(master, "1")
videotype=IntVar(master, "1")
comboboxvideotype = StringVar()
audiotype=IntVar(master, "1")
comboboxaudiotype = StringVar()
audioextension = StringVar()
audiotracktype=IntVar(master, "1")
comboboxaudiotracktype = StringVar()

def showoptionswin():
  optwin.deiconify()

def optwinclosing():
  optwin.withdraw()


def gui_elements_mainmenu():
 def GetFilePath():
  sfdfile = filedialog.askopenfilename(title="Select A SFD File", filetypes=[("SFD file", ".sfd")])
  SFDfilepath.set(sfdfile)
  entrySFD.focus()
  entrySFD.xview_moveto(1)
  entrySFD.focus_set()
  if setoutputdirectorytoSFDdirectory.get() == 1:
   setdirectorytoSFDdirectorycmd()
  else:
   pass

 def ChooseExportDir():
  exportpath = filedialog.askdirectory(title="Choose An Output Directory")
  dirPath.set(exportpath)
  entryDir.focus()
  entryDir.xview_moveto(1)
  entryDir.focus_set()

 def aboutprogram():
  message = 'This program is intended for extracting (and converting) the files found in Sofdec (SFD) video files.\n\nIf you find any issues, please create an issue on the Github page, which can be found at "https://github.com/Firebow59/SofdecVideoTools/issues".'
  programinfobox = tk.messagebox.showinfo(title='About SFDExtractor Beta 2.0.2', message=message)

 def docs():
  sfdextractordocs = os.getcwd() + '/resource/docs/documentation.pdf'
  os.startfile(sfdextractordocs)

 def enable_extractsfdbutton(*args):
  if not SFDfilepath.get() == '' and not dirPath.get() == '':
   sfdripperbtn.config(state=tk.NORMAL)
  else:
   sfdripperbtn.config(state=tk.DISABLED)
 SFDfilepath.trace('w', enable_extractsfdbutton)
 dirPath.trace('w', enable_extractsfdbutton)

 #Buttons and labels
 browsesfd = Button(text="Browse", command=GetFilePath, padx=40, pady=5).place(x=455, y=25)
 browseexport = Button(text="Browse", command=ChooseExportDir, padx=40, pady=5).place(x=455, y=65)
 sfdripperbtn = Button(text="Extract/Convert the SFD!", command=SFDripper, padx=130, pady=15, state=tk.DISABLED)
 sfdripperbtn.place(x=195, y=232)
 aboutextractor = Button(text="About Program", command=aboutprogram, padx=30, pady=1).place(x=18, y=234)
 programdocuments = Button(text="Documentation", command=docs, padx=30, pady=1).place(x=18, y=264)
 openextraoptionswin = Button(text="Extra Options", command=showoptionswin, padx=36, pady=1).place(x=18, y=234)

 sfdselect = Label(dirframe, text="Select A SFD File:", font = ("Arial Bold", 8)).place(x=3, y=-1)
 dirselect = Label(dirframe, text="Select An Output Directory:", font = ("Arial Bold", 8)).place(x=3, y=39)
 audiotypelbl = Label(optoptionalframe, text="Extract Audio As:", font = ("Arial Bold", 8)).place(x=338, y=140)
 videotypelbl = Label(optoptionalframe, text="Extract Video As:", font = ("Arial Bold", 8)).place(x=223, y=140)
 audiotracktypelbl = Label(optoptionalframe, text="Extract Audio From:", font = ("Arial Bold", 8)).place(x=453, y=140)
 

 extractiontyperadio = ttk.Radiobutton(master, text='Extract Video and Audio', variable=extractiontypeoption, value=1)
 extractiontyperadio.place(x=27, y=132)
 extractiontyperadio = ttk.Radiobutton(master, text='Extract Only Video', variable=extractiontypeoption, value=2)
 extractiontyperadio.place(x=27, y=157)
 extractiontyperadio = ttk.Radiobutton(master, text='Extract Only Audio', variable=extractiontypeoption, value=3)
 extractiontyperadio.place(x=27, y=182)

 entrySFD = ttk.Entry(dirframe, textvariable=SFDfilepath, width=72)
 entrySFD.insert(0, "")
 entrySFD.place(x=5, y=16)
 entryDir = ttk.Entry(dirframe, textvariable=dirPath, width=72)
 entryDir.insert(0, "")
 entryDir.place(x=5, y=56)


 OPTIONS_videotype = ["MP4", "AVI", "MPEG"]
 videoformatbox = ttk.Combobox(master, value=OPTIONS_videotype, width=12)
 videoformatbox.place(x=226, y=160)
 videoformatbox.current(0)
 videoformatbox.state(["readonly"])

 def updatevideotype(event):
   videoformatbox.selection_clear()
   selectedvideotype = videoformatbox.get()
   if selectedvideotype == "MP4":
    videotype.set("1")
    videoextension.set('.mp4')
    videoformatbox.selection_clear()
   elif selectedvideotype == "AVI":
    videotype.set("2")
    videoextension.set('.avi')
    videoformatbox.selection_clear()
   elif selectedvideotype == "MPEG":
    videotype.set("3")
    videoextension.set('.mpeg')
    videoformatbox.selection_clear()
 videoformatbox.bind("<<ComboboxSelected>>", updatevideotype)
 videoextension.set('.mp4')


 OPTIONS_audiotype = ["MP3", "OGG", "FLAC", "WAV", "ADX"]
 audioformatbox = ttk.Combobox(master, value=OPTIONS_audiotype, width=12)
 audioformatbox.place(x=341, y=160)
 audioformatbox.current(0)
 audioformatbox.state(["readonly"])

 def updateaudioformat(event):
   audioformatbox.selection_clear()
   selectedaudiotype = audioformatbox.get()
   if selectedaudiotype == "MP3":
    audiotype.set("1")
    audioextension.set('.mp3')
    audioformatbox.selection_clear()
   elif selectedaudiotype == "OGG":
    audiotype.set("2")
    audioextension.set('.ogg')
    audioformatbox.selection_clear()
   elif selectedaudiotype == "FLAC":
    audiotype.set("3")
    audioextension.set('.flac')
    audioformatbox.selection_clear()
   elif selectedaudiotype == "WAV":
    audiotype.set("4")
    audioextension.set('.wav')
    audioformatbox.selection_clear()
   elif selectedaudiotype == "ADX":
    audiotype.set("5")
    audioextension.set('.adx')
    audioformatbox.selection_clear()
 audioformatbox.bind("<<ComboboxSelected>>", updateaudioformat)
 audioextension.set('.mp3')


 OPTIONS_audiotracktype = ["All Tracks", "Only Track 1", "Only Track 2", "Only Track 3", "Only Track 4"]
 audiotracktypebox = ttk.Combobox(master, value=OPTIONS_audiotracktype, width=16)
 audiotracktypebox.place(x=456, y=160)
 audiotracktypebox.current(0)
 audiotracktypebox.state(["readonly"])

 def updateaudiotracktype(event):
   audiotracktypebox.selection_clear()
   selectedaudiotracktype = audiotracktypebox.get()
   if selectedaudiotracktype == "All Tracks":
    audiotracktype.set("1")
    audiotracktypebox.selection_clear()
   elif selectedaudiotracktype == "Only Track 1":
    audiotracktype.set("2")
    audiotracktypebox.selection_clear()
   elif selectedaudiotracktype == "Only Track 2":
    audiotracktype.set("3")
    audiotracktypebox.selection_clear()
   elif selectedaudiotracktype == "Only Track 3":
    audiotracktype.set("4")
    audiotracktypebox.selection_clear()
   elif selectedaudiotracktype == "Only Track 4":
    audiotracktype.set("5")
    audiotracktypebox.selection_clear()
 audiotracktypebox.bind("<<ComboboxSelected>>", updateaudiotracktype)


 def enable_and_disable_dropdownmenus(*args):
  if extractiontypeoption.get() == 1:
   videoformatbox.config(state=tk.NORMAL)
   audioformatbox.config(state=tk.NORMAL)
   audiotracktypebox.config(state=tk.NORMAL)
  if extractiontypeoption.get() == 2:
   audiotracktypebox.config(state=tk.DISABLED)
   audioformatbox.config(state=tk.DISABLED)
   videoformatbox.config(state=tk.NORMAL)
  if extractiontypeoption.get() == 3:
   videoformatbox.config(state=tk.DISABLED)
   audioformatbox.config(state=tk.NORMAL)
   audiotracktypebox.config(state=tk.NORMAL)
 extractiontypeoption.trace('w', enable_and_disable_dropdownmenus)

 def setdefaultoptionvalues():
  audiotracktype.set("1")
  audioextension.set('.mp3')
  videoextension.set('.mp4')
  extractiontypeoption.set(1)
  vbitrate.set('150000')
  abitrate.set('320k')
  crfvalue.set('01')
 setdefaultoptionvalues()



def advancedoptions():
  global optwin
  optwin = Toplevel(master)
  optwin.geometry("600x220"), optwin.title("Extra Options"), optwin.resizable(False, False)
  ffmpegsettingsframe = LabelFrame(optwin, text="Additional FFmpeg Settings").place(relx=0.010, rely=0.005, relheight=0.540, relwidth=0.983)
  QoLsettingsframe = LabelFrame(optwin, text="QoL Settings").place(relx=0.010, rely=0.580, relheight=0.390, relwidth=0.390)
  miscsettingsframe = LabelFrame(optwin, text="Misc. Program Settings").place(relx=0.417, rely=0.580, relheight=0.390, relwidth=0.393)

  def updatemonocmd(*args):
   if monoaudio.get() == 1:
     monocmd.set('-ac 1')
   else:
     monocmd.set('')
  monoaudio.trace('w', updatemonocmd)


  crfentry = ttk.Entry(optwin, textvariable=crfvalue, width=12)
  crfentry.insert(0, "")
  crfentry.place(x=198, y=35)
  crflbl = Label(optwin, text="CRF Value:", font=("Arial Bold", 8)).place(x=195, y=15)

  if crfentry.get() == '':
   crfentry.insert(0, "01")


  vbitrateentry = ttk.Entry(optwin, textvariable=vbitrate, width=12)
  vbitrateentry.insert(0, "")
  vbitrateentry.place(x=293, y=35)
  vbitratelbl = Label(optwin, text="Video Bitrate:", font=("Arial Bold", 8)).place(x=290, y=15)

  def updatevbitrateoptions(*args):
    selectedtype_bitrate = videotype.get()
    if selectedtype_bitrate == 1:
     vbitrate.set('150000')
    elif selectedtype_bitrate == 2:
     vbitrate.set('30000000')
    elif selectedtype_bitrate == 3:
     vbitrate.set('8000000')
  videotype.trace_add('write', updatevbitrateoptions)
  updatevbitrateoptions()


  abitrateentry = ttk.Entry(optwin, textvariable=abitrate, width=12)
  abitrateentry.insert(0, "")
  abitrateentry.place(x=388, y=35)
  abitratelbl = Label(optwin, text="Audio Bitrate:", font=("Arial Bold", 8)).place(x=385, y=15)
  if abitrateentry.get() == '':
   abitrateentry.insert(0, "320k")


  OPTIONS_videoEncoder = ["libx264", "libx265", "libxvid", "mpeg1video", "mpeg2video"]
  videoencoderbox = ttk.Combobox(optwin, value=OPTIONS_videoEncoder, width=12)
  videoencoderbox.place(x=483, y=35)
  videoencoderbox.current(0)
  videoencoderbox.state(["readonly"])
  videoencoderlbl = Label(optwin, text="Video Codec:", font=("Arial Bold", 8)).place(x=480, y=15)
  previous_vcodecvalue = StringVar()

  def updatevideoencoder(event):
   videoencoderbox.selection_clear()
   selected_videoencoder = videoencoderbox.get()
   if selected_videoencoder == "libx264":
    vcodec.set("libx264")
    previous_vcodecvalue.set(vcodec.get())
    videoencoderbox.selection_clear()
   elif selected_videoencoder == "libx265":
    vcodec.set("libx265")
    previous_vcodecvalue.set(vcodec.get())
    videoencoderbox.selection_clear()
   elif selected_videoencoder == "libxvid":
    vcodec.set("libxvid")
    previous_vcodecvalue.set(vcodec.get())
    videoencoderbox.selection_clear()
   elif selected_videoencoder == "mpeg1video":
    vcodec.set("mpeg1video")
    previous_vcodecvalue.set(vcodec.get())
    videoencoderbox.selection_clear()
    previous_vcodecvalue.set(vcodec.get())
   elif selected_videoencoder == "mpeg2video":
    vcodec.set("mpeg2video")
  
  def updatevideoencoderoptions(*args):
    selected_type = videotype.get()
    if selected_type == 1:
     options = ["libx264", "libx265"]
     vcodec.set(options[0])
    elif selected_type == 2:
     options = ["libxvid"]
     vcodec.set(options[0])
    elif selected_type == 3:
     options = ["mpeg1video", "mpeg2video"]
     vcodec.set(options[0])
    else:
     options = OPTIONS_videoEncoder
    videoencoderbox['values'] = options
    videoencoderbox.set(options[0])

  videoencoderbox.set('libx264')
  videotype.trace_add('write', updatevideoencoderoptions)
  updatevideoencoderoptions()
  videoencoderbox.bind("<<ComboboxSelected>>", updatevideoencoder)


  OPTIONS_VRes = ["Same as Video", #0
  "320/426 x 240 (240p)",   #1
  "480/640 x 360 (360p)",   #2
  "640/848 x 480 (480p)",   #3
  "960/1280 x 720 (720p)",  #4
  ]

  global outputresolution
  outputresolution = StringVar()
  comboboxvres = StringVar()
  vres = ttk.Combobox(optwin, value=OPTIONS_VRes, width=19)
  vres.place(x=197, y=85)
  vres.current(0)
  videoreslabel = Label(optwin, text="Video Resolution:", font = ("Arial Bold", 8)).place(x=195, y=65)

  def updatevres(event):
   selected_vresvalue = vres.get()
   if "x" in selected_vresvalue:
    custom_resolution = selected_vresvalue.split("x")
    if len(custom_resolution) == 2:
      try:
       width = int(custom_resolution[0])
       height = int(custom_resolution[1])
       outputresolution.set(f'-vf "scale={width}:{height},pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black"')
       comboboxvres.set(selected_vresvalue)
       vres.selection_clear()
      except ValueError:
       pass
   if selected_vresvalue == "Same As Video":
    comboboxvres.set("Same As Video")
    outputresolution.set("")
    vres.selection_clear()
   elif selected_vresvalue in OPTIONS_VRes[1:]:
    index = OPTIONS_VRes.index(selected_vresvalue)
    comboboxvres.set(OPTIONS_VRes[index])
    height = int(OPTIONS_VRes[index].split(" ")[-1][1:-2])
    outputresolution.set(f'-vf "scale=-2:{height},pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black"')
    vres.selection_clear()
   elif selected_vresvalue == "320/426 x 240 (240p)":
    comboboxvres.set(OPTIONS_VRes[1])
    outputresolution.set('-vf "scale=-2:240,pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black"')
    vres.selection_clear()
   elif selected_vresvalue == "480/640 x 360 (360p)":
    comboboxvres.set(OPTIONS_VRes[2])
    outputresolution.set('-vf "scale=-2:360,pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black"')
    vres.selection_clear()
   elif selected_vresvalue == "640/848 x 480 (480p)":
    comboboxvres.set(OPTIONS_VRes[3])
    outputresolution.set('-vf "scale=-2:480,pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black"')
    vres.selection_clear()
   elif selected_vresvalue == "960/1280 x 720 (720p)":
    comboboxvres.set(OPTIONS_VRes[3])
    outputresolution.set('-vf "scale=-2:720,pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black"')
    vres.selection_clear()
  vres.bind("<<ComboboxSelected>>", updatevres)
  vres.bind("<KeyRelease>", updatevres)


  monoaudcheck = ttk.Checkbutton(optwin, text='Extract audio in mono', variable=monoaudio, onvalue=1, offvalue=0).place(x=10, y=42)
  extractextravideocheck = ttk.Checkbutton(optwin, text='Extract extra video track', variable=extravideo, onvalue=1, offvalue=0).place(x=10, y=62)
  bitexactcheck = ttk.Checkbutton(optwin, text='Use -bitexact for audio', variable=usebitexact, onvalue=1, offvalue=0).place(x=10, y=22)
  showffmpegcommandscheck = ttk.Checkbutton(optwin, text='Show FFmpeg output', variable=showffmpegcommands, onvalue=1, offvalue=0).place(x=10, y=82)

  def printffmpegcommandsstate(*args):
   if showffmpegcommands.get() == 1:
    print("Show FFmpeg commands enabled")
   if showffmpegcommands.get() == 0:
    print("Show FFmpeg commands disabled")
  showffmpegcommands.trace('w', printffmpegcommandsstate)


  #QoL Settings
  global setoutputdirectorytoSFDdirectory
  setoutputdirectorytoSFDdirectory = IntVar()
  useidenticaldirectorypaths = ttk.Checkbutton(optwin, text='Use SFD directory for output directory', variable=setoutputdirectorytoSFDdirectory, onvalue=1, offvalue=0)
  useidenticaldirectorypaths.place(x=11, y=146)

  global setdirectorytoSFDdirectorycmd
  def setdirectorytoSFDdirectorycmd(*args):
   if setoutputdirectorytoSFDdirectory.get() == 1:
    global SFDfilePathdir
    SFDfilePathdir = StringVar()
    SFDfilePathdir.set(os.path.dirname(SFDfilepath.get()))
    dirPath.set(SFDfilePathdir.get())
   if setoutputdirectorytoSFDdirectory.get() == 0:
    dirPath.set('')
  setoutputdirectorytoSFDdirectory.trace('w', setdirectorytoSFDdirectorycmd)

  extracttofoldercheck = ttk.Checkbutton(optwin, text='Extract SFD to folder', variable=extracttofolder, onvalue=1, offvalue=0).place(x=10, y=166)
  autooverwritefilescheck = ttk.Checkbutton(optwin, text='Automatically overwrite files', variable=autooverwritefiles, onvalue=1, offvalue=0).place(x=10, y=186)


  #Misc. Program Options
  deleteoriginalsfdcheck = ttk.Checkbutton(optwin, text='Delete selected SFD after extraction', variable=deleteoriginalsfd, onvalue=1, offvalue=0).place(x=255, y=146)
  #runfromoriginalfile = ttk.Checkbutton(optwin, text="Don't copy SFD (use original)", variable=useoriginalsfd, onvalue=1, offvalue=0).place(x=255, y=166)
  disablevideoreencode = ttk.Checkbutton(optwin, text="Don't re-encode video (use -c:v copy)", variable=copyvideocodec, onvalue=1, offvalue=0).place(x=255, y=166) #.place(x=255, y=196)

  def copyvideocodec_cmd(*args):
   if copyvideocodec.get() == 1:
    vcodec.set('copy')
   else:
    vcodec.set(previous_vcodecvalue.get())
  copyvideocodec.trace('w', copyvideocodec_cmd)

  optwin.withdraw()


def SFDripper():
  print("")
  destdir = dirPath.get()
  bitexactcmd = StringVar()
  mp3extractioncheck = IntVar()

  if not os.path.exists(SFDfilepath.get()):
   tk.messagebox.showerror(title='No SFD Found', message="The SFD file could not be found. Please try to reselect the SFD file again, or choose a different one.")
   return

  if not os.path.exists(dirPath.get()):
   tk.messagebox.showerror(title='Directory Invalid', message="The directory could not be found. Please try to reselect the directory again, or choose a different one.")
   return


  if os.path.isfile('extractsfd.sfd'):
   os.remove('extractsfd.sfd')

  if usebitexact.get() == 1:
   bitexactcmd.set('-bitexact')
  else:
   pass

  #Create output names for extracted files
  sfdname = os.path.basename(SFDfilepath.get())
  sfdname_noextension = os.path.splitext(sfdname)[0]

  #Set ffmpeg command properly if it's on the user's PATH
  if ffmpeg_location_int.get() == 1:
   ffmpeg_exe_path = 'ffmpeg.exe'
  else:
   ffmpeg_exe_path = currentdir + '/resource/bin/ffmpeg/ffmpeg.exe'
  #if ffprobe_location_int == 1:
    #ffprobe_exe_path = 'ffprobe.exe'
  #else:
   #ffprobe_exe_path = currentdir + '/resource/bin/ffmpeg/ffprobe.exe'

  filename = SFDfilepath.get()
  #Move file to temp folder if it's in the root SofdecVideoTools folder.
  if useoriginalsfd.get() == 1:
   filename = SFDfilepath.get()
  else:
   sfdfolder = StringVar()
   sfdfolder = os.getcwd() + f'/sfdfile/{SFDname.get()}'
   if os.path.exists("sfdfile"):
    if os.path.isfile(sfdfolder):
     if os.path.isfile(SFDname.get()):
      os.remove(SFDname.get())
      shutil.move(sfdfolder, os.getcwd())
    os.removedirs("sfdfile")
    if os.path.isfile(SFDname.get()):
     os.mkdir("sfdfile")
     shutil.move(SFDname.get(), "sfdfile")
     SFDfilepath.set(sfdfolder)

   extracttofolder_name = f'{sfdname_noextension}' + '-extracted'
   if extracttofolder.get() == 1:
    if os.path.exists(dirPath.get() + '/' + extracttofolder_name):
     folderalreadyexists = tk.messagebox.askyesnocancel(title='Folder Already Exists', message=f'A folder named {extracttofolder_name}" already exists in the export folder. Do you want to overwrite this folder?')
     if folderalreadyexists == True:
      shutil.rmtree(dirPath + '/' + extracttofolder_name)
      os.mkdir(extracttofolder_name)
     elif folderalreadyexists == False:
      pass
    else:
     os.mkdir(extracttofolder_name)

  outputvideoname = sfdname_noextension + '-video' + videoextension.get()
  outputextravideoname = sfdname_noextension + '-video_2' + videoextension.get()
  tempvideoname = f'video{videoextension.get()}'
  tempvideoname_vtrack2 = f'video2{videoextension.get()}'

  outputaudiotrack1name = sfdname_noextension + '-track1' + audioextension.get()
  tempaudiotrack1name = f'audio1{audioextension.get()}'

  outputaudiotrack2name = sfdname_noextension + '-track2' + audioextension.get()
  tempaudiotrack2name = f'audio2{audioextension.get()}'
  
  outputaudiotrack3name = sfdname_noextension + '-track3' + audioextension.get()
  tempaudiotrack3name = f'audio3{audioextension.get()}'

  outputaudiotrack4name = sfdname_noextension + '-track4' + audioextension.get()
  tempaudiotrack4name = f'audio4{audioextension.get()}'


  #Check for AIX audio
  def searchfor_AIX():
    phrase = 'AIXP'
    chunk_size = 1024

    with open(filename, 'rb') as file:
     while True:
      chunk = file.read(chunk_size)
      if not chunk:
       break
      hex_data = chunk.hex()
      if phrase in hex_data:
       print('AIX audio detected, some (or all) audio tracks may not be extracted.')
       return
  searchfor_AIX()

  cancelextraction = IntVar()
  videooverwritevalue = IntVar()
  audio1overwritevalue = IntVar()
  audio2overwritevalue = IntVar()
  audio3overwritevalue = IntVar()
  audio4overwritevalue = IntVar()

  def cancel_and_delete_extractionsfd():
   cancelextraction.set(1)
   if os.path.isfile('extractsfd.sfd'):
    os.remove('extractsfd.sfd')
   return

  def checkaudio1file():
   if cancelextraction.get() == 1:
    pass
   else:
    if audiotracktype.get() == 1 or audiotracktype.get() == 2:
     if not os.path.isfile(os.path.join(destdir, outputaudiotrack1name)):
      audio1overwritevalue.set(1)
     if os.path.isfile(os.path.join(destdir, outputaudiotrack1name)):
      if autooverwritefiles.get() == 1:
        audio1overwritevalue.set(1)
      else:
       aud1filealreadyexists = tk.messagebox.askyesnocancel(title='File Already Exists', message=f'The file "{outputaudiotrack1name}" is already in the export folder. Do you want to overwrite the file?')
       if aud1filealreadyexists == True:
        audio1overwritevalue.set(1)
       elif aud1filealreadyexists == False:
        pass
       else:
        cancel_and_delete_extractionsfd()

  def checkaudio2file():
   if cancelextraction.get() == 1:
    pass
   else:
    if audiotracktype.get() == 1 or audiotracktype.get() == 3:
     if not os.path.isfile(os.path.join(destdir, outputaudiotrack2name)):
      audio2overwritevalue.set(1)
     if os.path.isfile(os.path.join(destdir, outputaudiotrack2name)):
      if autooverwritefiles.get() == 1:
        audio2overwritevalue.set(1)
      else:
       aud2filealreadyexists = tk.messagebox.askyesnocancel(title='File Already Exists', message=f'The file "{outputaudiotrack2name}" is already in the export folder. Do you want to overwrite the file?')
       if aud2filealreadyexists == True:
         audio2overwritevalue.set(1)
       elif aud2filealreadyexists == False:
        pass
       else:
        cancel_and_delete_extractionsfd()

  def checkaudio3file():
   if cancelextraction.get() == 1:
    pass
   else:
    if audiotracktype.get() == 1 or audiotracktype.get() == 4:
     if not os.path.isfile(os.path.join(destdir, outputaudiotrack3name)):
      audio3overwritevalue.set(1)
     if os.path.isfile(os.path.join(destdir, outputaudiotrack3name)):
      if autooverwritefiles.get() == 1:
        audio3overwritevalue.set(1)
      else:
       aud3filealreadyexists = tk.messagebox.askyesnocancel(title='File Already Exists', message=f'The file "{outputaudiotrack3name}" is already in the export folder. Do you want to overwrite the file?')
       if aud3filealreadyexists == True:
         audio3overwritevalue.set(1)
       elif aud3filealreadyexists == False:
        pass
       else:
        cancel_and_delete_extractionsfd()

  def checkaudio4file():
   if cancelextraction.get() == 1:
    pass
   else:
    if audiotracktype.get() == 1 or audiotracktype.get() == 5:
     if not os.path.isfile(os.path.join(destdir, outputaudiotrack4name)):
      audio4overwritevalue.set(1)
     if os.path.isfile(os.path.join(destdir, outputaudiotrack4name)):
      if autooverwritefiles.get() == 1:
        audio4overwritevalue.set(1)
      else:
       aud4filealreadyexists = tk.messagebox.askyesnocancel(title='File Already Exists', message=f'The file "{outputaudiotrack4name}" is already in the export folder. Do you want to overwrite the file?')
       if aud4filealreadyexists == True:
         audio4overwritevalue.set(1)
       elif aud4filealreadyexists == False:
        pass
       else:
        cancel_and_delete_extractionsfd()


  def extractvideotracks():
   print("Checking video track...")
   if not os.path.isfile(os.path.join(destdir, outputvideoname)):
    videooverwritevalue.set(1)
   if os.path.isfile(os.path.join(destdir, outputvideoname)):
      if autooverwritefiles.get() == 1:
        videooverwritevalue.set(1)
      else:
       videofilealreadyexists = tk.messagebox.askyesnocancel(title='File Already Exists', message=f'The file "{outputvideoname}" is already in the export folder. Do you want to overwrite the file?')
       if videofilealreadyexists == True:
        videooverwritevalue.set(1)
       elif videofilealreadyexists == False:
        pass
       else:
        cancel_and_delete_extractionsfd()

   if cancelextraction.get() == 1:
    pass
   else:
     print('Extracting video track...')
     if videooverwritevalue.get() == 1:
      if showffmpegcommands.get() == 1:
       video1extractcmd=f'{ffmpeg_exe_path} -y -i "{filename}" -an -crf {crfvalue.get()} -map 0:v:0 -c:v {vcodec.get()} {outputresolution.get()} -b:v {vbitrate.get()} {tempvideoname}'
       os.system(video1extractcmd)
      else:
       video1extractcmd=f'{ffmpeg_exe_path} -y -i "{filename}" -an -crf {crfvalue.get()} -map 0:v:0 -c:v {vcodec.get()} {outputresolution.get()} -b:v {vbitrate.get()} {tempvideoname}'
       subprocess.run(video1extractcmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
       if os.path.isfile(f'{tempvideoname}'):
        print('Video track extracted!')
     else:
      pass
   

      if extravideo.get() == 1:
       if not os.path.isfile(os.path.join(destdir, outputextravideoname)):
        videooverwritevalue.set(1)
       if os.path.isfile(os.path.join(destdir, outputextravideoname)):
        if autooverwritefiles.get() == 1:
         videooverwritevalue.set(1)
        else:
         videofilealreadyexists = tk.messagebox.askyesnocancel(title='File Already Exists', message=f'The file "{outputextravideoname}" is already in the export folder. Do you want to overwrite the file?')
         if videofilealreadyexists == True:
          videooverwritevalue.set(1)
         elif videofilealreadyexists == False:
          pass
         else:
          cancel_and_delete_extractionsfd()
       if showffmpegcommands.get() == 1:
        video2extractcmd=f'{ffmpeg_exe_path} -y -i "{filename}" -an -crf {crfvalue.get()} -map 0:v:1 -c:v {vcodec.get()} {outputresolution.get()} -b:v {vbitrate.get()} {tempvideoname_vtrack2}'
        os.system(video2extractcmd)
       else:
        video2extractcmd=f'{ffmpeg_exe_path} -y -i "{filename}" -an -crf {crfvalue.get()} -map 0:v:1 -c:v {vcodec.get()} {outputresolution.get()} -b:v {vbitrate.get()} {tempvideoname_vtrack2}'
        subprocess.run(video2extractcmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
        if os.path.isfile({tempvideoname_vtrack2}):
         print('Extracting extra video track...')
       if os.path.exists(os.path.join(currentdir, tempvideoname_vtrack2)):
        print("Extra video track extracted!")



  def extractaudiotracks():
    print("Checking audio tracks...")
    checkaudio1file()
    checkaudio2file()
    checkaudio3file()
    checkaudio4file()


    if audioextension.get() == ".mp3": #Fix for MP3 extraction errors, see convertbacktomp3() for the conversion stuff.
     mp3extractioncheck.set(1)
     audioextension.set('.ogg')

    if cancelextraction.get() == 1:
     pass
    else:
     if audiotracktype.get() == 2:
      if audio1overwritevalue.get() == 1:
       if showffmpegcommands.get() == 1:
        aud1extractcmd=f'{ffmpeg_exe_path} -err_detect ignore_err -i "{filename}" -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} -map 0:a:0 {tempaudiotrack1name}'
        os.system(aud1extractcmd)
       else:
        aud1extractcmd=f'{ffmpeg_exe_path} -err_detect ignore_err -i "{filename}" -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} -map 0:a:0 {tempaudiotrack1name}'
        print('Extracting audio track 1...')
        subprocess.run(aud1extractcmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
        if os.path.isfile(f'{tempaudiotrack1name}'):
         print('Done!')
        else:
         print("Unable to extract audio track 1...")
      else:
       pass

    if cancelextraction.get() == 1:
     pass
    else:
     if audiotracktype.get() == 3:
      if audio2overwritevalue.get() == 1:
       if showffmpegcommands.get() == 1:
        aud2extractcmd=f'{ffmpeg_exe_path} -err_detect ignore_err -i "{filename}" -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} -map 0:a:1 {tempaudiotrack2name}'
        os.system(aud2extractcmd)
       else:
        aud2extractcmd=f'{ffmpeg_exe_path} -err_detect ignore_err -i "{filename}" -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} -map 0:a:1 {tempaudiotrack2name}'
        print('Extracting audio track 2...')
        subprocess.run(aud2extractcmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
        if os.path.isfile(f'{tempaudiotrack2name}'):
         print('Done!')
        else:
         print("Unable to extract audio track 2...")
     else:
       pass
  
    if cancelextraction.get() == 1:
     pass
    else:
     if audiotracktype.get() == 4:
      if audio3overwritevalue.get() == 1:
       if showffmpegcommands.get() == 1:
        aud3extractcmd=f'{ffmpeg_exe_path} -err_detect ignore_err -i "{filename}" -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} -map 0:a:2 {tempaudiotrack3name}'
        os.system(aud3extractcmd)
       else:
        aud3extractcmd=f'{ffmpeg_exe_path} -err_detect ignore_err -i "{filename}" -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} -map 0:a:2 {tempaudiotrack3name}'
        print('Extracting audio track 3...')
        subprocess.run(aud3extractcmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
        if os.path.isfile(f'{tempaudiotrack3name}'):
         print('Done!')
        else:
         print("Unable to extract audio track 3...")
      else:
       pass

    if cancelextraction.get() == 1:
     pass
    else:
     if audiotracktype.get() == 5:
      if audio4overwritevalue.get() == 1:
       if showffmpegcommands.get() == 1:
        aud4extractcmd=f'{ffmpeg_exe_path} -err_detect ignore_err -i "{filename}" -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} -map 0:a:3 {tempaudiotrack4name}'
        os.system(aud4extractcmd)
       else:
        aud4extractcmd=f'{ffmpeg_exe_path} -err_detect ignore_err -i "{filename}" -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} -map 0:a:3 {tempaudiotrack4name}'
        print('Extracting audio track 4...')
        subprocess.run(aud4extractcmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
        if os.path.isfile(f'{tempaudiotrack4name}'):
         print('Done!')
        else:
         print("Unable to extract audio track 4...")
     else:
       pass


    if audiotracktype.get() == 1:
     if cancelextraction.get() == 1:
      pass
     else:
      print('Extracting audio tracks...')
      if audio1overwritevalue.get() == 1:
       if showffmpegcommands.get() == 1:
        aud1extractcmd=f'{ffmpeg_exe_path} -err_detect ignore_err -i "{filename}" -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} -map 0:a:0 {tempaudiotrack1name}'
        os.system(aud1extractcmd)
       else:
        aud1extractcmd=f'{ffmpeg_exe_path} -err_detect ignore_err -i "{filename}" -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} -map 0:a:0 {tempaudiotrack1name}'
        subprocess.run(aud1extractcmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
       if os.path.exists(os.path.join(currentdir, tempaudiotrack1name)):
        print("Audio track 1 extracted!")
       else:
        print("Unable to extract audio track 1...")
      else:
       pass

     if audio2overwritevalue.get() == 1:
      if showffmpegcommands.get() == 1:
       aud2extractcmd=f'{ffmpeg_exe_path} -err_detect ignore_err -i "{filename}" -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} -map 0:a:1 {tempaudiotrack2name}'
       os.system(aud2extractcmd)
      else:
       aud2extractcmd=f'{ffmpeg_exe_path} -err_detect ignore_err -i "{filename}" -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} -map 0:a:1 {tempaudiotrack2name}'
       subprocess.run(aud2extractcmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
      if os.path.exists(os.path.join(currentdir, tempaudiotrack2name)):
       print("Audio track 2 extracted!")
      else:
       print("Unable to extract audio track 2...")
     else:
      pass

     if audio3overwritevalue.get() == 1:
      if showffmpegcommands.get() == 1:
       aud3extractcmd=f'{ffmpeg_exe_path} -err_detect ignore_err -i "{filename}" -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} -map 0:a:2 {tempaudiotrack3name}'
       os.system(aud3extractcmd)
      else:
       aud3extractcmd=f'{ffmpeg_exe_path} -err_detect ignore_err -i "{filename}" -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} -map 0:a:2 {tempaudiotrack3name}'
       subprocess.run(aud3extractcmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
      if os.path.exists(os.path.join(currentdir, tempaudiotrack3name)):
       print("Audio track 3 extracted!")
      else:
       print("Unable to extract audio track 3...")
     else:
      pass

     if audio4overwritevalue.get() == 1:
      if showffmpegcommands.get() == 1:
       aud4extractcmd=f'{ffmpeg_exe_path} -err_detect ignore_err -i "{filename}" -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} -map 0:a:3 {tempaudiotrack4name}'
       os.system(aud4extractcmd)
      else:
       aud4extractcmd=f'{ffmpeg_exe_path} -err_detect ignore_err -i "{filename}" -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} -map 0:a:3 {tempaudiotrack4name}'
       subprocess.run(aud4extractcmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
      if os.path.exists(os.path.join(currentdir, tempaudiotrack4name)):
       print("Audio track 4 extracted!")
      else:
       print("Unable to extract audio track 4...")
     else:
      pass

  def convertbacktomp3():
   mp3_track1command=f'{ffmpeg_exe_path} -i audio1.ogg -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} audio1.mp3'
   subprocess.run(mp3_track1command, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
   mp3_track2command=f'{ffmpeg_exe_path} -i audio2.ogg -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} audio2.mp3'
   subprocess.run(mp3_track2command, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
   mp3_track3command=f'{ffmpeg_exe_path} -i audio3.ogg -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} audio3.mp3'
   subprocess.run(mp3_track3command, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
   mp3_track4command=f'{ffmpeg_exe_path} -i audio4.ogg -vn -b:a {abitrate.get()} {bitexactcmd.get()} {monocmd.get()} audio4.mp3'
   subprocess.run(mp3_track4command, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
   if os.path.isfile('audio1.ogg'):
    os.remove('audio1.ogg')
   if os.path.isfile('audio2.ogg'):
    os.remove('audio2.ogg')
   if os.path.isfile('audio3.ogg'):
    os.remove('audio3.ogg')
   if os.path.isfile('audio4.ogg'):
    os.remove('audio4.ogg')


  def movefiles():
   #Convert files back to MP3 from OGG to prevent error
   if mp3extractioncheck.get() == 1:
    audioextension.set('.mp3')
    convertbacktomp3()
   else:
    pass


   print("Moving files to output directory...")
   if os.path.exists(os.path.join(currentdir, tempvideoname)):
      os.rename(tempvideoname, outputvideoname)
   if os.path.exists(os.path.join(currentdir, tempvideoname_vtrack2)):
      os.rename(tempvideoname_vtrack2, outputextravideoname)
   if os.path.exists(os.path.join(currentdir, tempaudiotrack1name)):
      os.rename(tempaudiotrack1name, outputaudiotrack1name)
   if os.path.exists(os.path.join(currentdir, tempaudiotrack2name)):
      os.rename(tempaudiotrack2name, outputaudiotrack2name)
   if os.path.exists(os.path.join(currentdir, tempaudiotrack3name)):
      os.rename(tempaudiotrack3name, outputaudiotrack3name)
   if os.path.exists(os.path.join(currentdir, tempaudiotrack4name)):
      os.rename(tempaudiotrack4name, outputaudiotrack4name)

   if os.path.exists(extracttofolder_name):
    if os.path.exists(os.path.join(currentdir, outputvideoname)):
     shutil.move(os.path.join(currentdir, outputvideoname), os.path.join(currentdir, extracttofolder_name))
    if os.path.exists(os.path.join(currentdir, outputextravideoname)):
     shutil.move(os.path.join(currentdir, outputextravideoname), os.path.join(currentdir, extracttofolder_name))
    if os.path.exists(os.path.join(currentdir, outputaudiotrack1name)):
     shutil.move(os.path.join(currentdir, outputaudiotrack1name), os.path.join(currentdir, extracttofolder_name))
    if os.path.exists(os.path.join(currentdir, outputaudiotrack2name)):
     shutil.move(os.path.join(currentdir, outputaudiotrack2name), os.path.join(currentdir, extracttofolder_name))
    if os.path.exists(os.path.join(currentdir, outputaudiotrack3name)):
     shutil.move(os.path.join(currentdir, outputaudiotrack3name), os.path.join(currentdir, extracttofolder_name))
    if os.path.exists(os.path.join(currentdir,outputaudiotrack4name)):
     shutil.move(os.path.join(currentdir, outputaudiotrack4name), os.path.join(currentdir, extracttofolder_name))
    
    #Move folder to output directory
    shutil.move(os.path.join(extracttofolder_name), os.path.join(destdir, extracttofolder_name))
    print("Done!")
   else:
     if os.path.exists(os.path.join(currentdir, outputvideoname)):
      shutil.move(os.path.join(currentdir, outputvideoname), os.path.join(destdir, outputvideoname))
     if os.path.exists(os.path.join(currentdir, outputextravideoname)):
      shutil.move(os.path.join(currentdir, outputextravideoname), os.path.join(destdir, outputextravideoname))
     if os.path.exists(os.path.join(currentdir, outputaudiotrack1name)):
      shutil.move(os.path.join(currentdir, outputaudiotrack1name), os.path.join(destdir, outputaudiotrack1name))
     if os.path.exists(os.path.join(currentdir, outputaudiotrack2name)):
      shutil.move(os.path.join(currentdir, outputaudiotrack2name), os.path.join(destdir, outputaudiotrack2name))
     if os.path.exists(os.path.join(currentdir, outputaudiotrack3name)):
      shutil.move(os.path.join(currentdir, outputaudiotrack3name), os.path.join(destdir, outputaudiotrack3name))
     if os.path.exists(os.path.join(currentdir,outputaudiotrack4name)):
      shutil.move(os.path.join(currentdir, outputaudiotrack4name), os.path.join(destdir, outputaudiotrack4name))
     print("Done!")

  if extractiontypeoption.get() == 1:
   extractvideotracks()
   extractaudiotracks()
  elif extractiontypeoption.get() == 2:
   extractvideotracks()
  elif extractiontypeoption.get() == 3:
   extractaudiotracks()
  movefiles()

  def deleteoriginalsfdcmd():
   os.remove(f'{SFDfilepath.get()}')
   print("Done!")
  if deleteoriginalsfd.get() == 1:
   print("Deleting original SFD file...")
   deleteoriginalsfdcmd()
  else:
   pass

  cleanup_files()
  
  #Reset dirPath to parent directory if extracttofolder was used
  if extracttofolder.get() == 1:
   if dirPath.get().endswith(extracttofolder_name):
    dirPath.set(dirPath.get()[:-len(extracttofolder_name)])

  if cancelextraction.get() == 1:
   print("SFD extraction canceled")
   canceledextractingmessagebox = tk.messagebox.showinfo(title='Extraction Canceled', message="SFD extraction cancelled.")
  else:
   doneextracting = tk.messagebox.showinfo(title='Extraction Completed', message="The SFD has been extracted/converted! Enjoy!")
  return



def updater_exe():
 updaterlocation = os.getcwd() + '/updater.exe'
 if os.path.isfile(updaterlocation):
  runupdater = f'"{updaterlocation}"'
  subprocess.run(runupdater, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
 else:
  print("Unable to find updater.exe, program will not be able to update.")
  print("")
  pass

def cleanup_files():
 if os.path.isfile('extractsfd.sfd'):
  os.remove('extractsfd.sfd')
 if os.path.isfile(f'{SFDname.get()}' + f'{videoextension.get()}'):
  os.remove(f'{SFDname.get()}' + f'{videoextension.get()}')
 if os.path.isfile('audio1.ogg'):
  os.remove('audio1.ogg')
 if os.path.isfile('audio2.ogg'):
  os.remove('audio2.ogg')
 if os.path.isfile('audio3.ogg'):
  os.remove('audio3.ogg')
 if os.path.isfile('audio4.ogg'):
  os.remove('audio4.ogg')



def closeprogram():
 killffmpeg = 'taskkill /F /IM ffmpeg.exe'
 subprocess.run(killffmpeg, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
 os._exit(0)


updater_exe()
cleanup_files()
run_ffmpeg_check()  #Set up FFmpeg location ints
gui_elements_mainmenu()
advancedoptions()

optwin.protocol("WM_DELETE_WINDOW", optwinclosing)

atexit.register(cleanup_files)
atexit.register(closeprogram)

master.mainloop()