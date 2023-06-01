from tkinter import filedialog, ttk, messagebox, Frame, LabelFrame, Label, StringVar, Button, Toplevel, IntVar
import tkinter as tk
import os
import shutil

master = tk.Tk()
master.geometry("600x300"), master.title("SFDExtractor Beta 1.0.0"), master.resizable(False, False)#, master.iconbitmap("resource/icon/sfdextractor.ico")
page1 = Frame(master, bg='#f0f0f0').place(relx=0.0, rely=0.0, relheight=1.006, relwidth=1.004)
dirframe = LabelFrame(master, text="Directories")
dirframe.place(relx=0.010, rely=0.0, relheight=0.365, relwidth=0.980)
optframe = LabelFrame(master, text="Extraction Type").place(relx=0.010, rely=0.370, relheight=0.350, relwidth=0.340) 
optoptionalframe = LabelFrame(master, text="Extraction Options").place(relx=0.360, rely=0.370, relheight=0.350, relwidth=0.630)
otherframe = LabelFrame(master, text="Other").place(relx=0.010, rely=0.720, relheight=0.270, relwidth=0.300)

def GetFilePath():
    file_selected = filedialog.askopenfilename(title="Select A SFD File", filetypes=[("SFD file", ".sfd")])
    filePath.set(file_selected)

def ChooseExportDir():
    exportpath = filedialog.askdirectory(title="Choose An Output Directory")
    dirPath.set(exportpath)

def aboutprogram():
 message = 'This program is intended for extracting (and converting) the files found in Sofdec (SFD) video files.\n\nIf you find any issues, please create an issue on the Github page, which can be found at "https://github.com/Firebow59/SofdecVideoTools/issues".'
 programinfobox = tk.messagebox.showinfo(title='About SFDExtractor Beta 1.0.0', message=message)

def docs():
  os.startfile('sfdextractor.pdf')

def showoptionswin():
    optwin.deiconify()

def optwinclosing():
    optwin.withdraw()

def advancedoptions():
  global optwin
  optwin = Toplevel(master, bg=f'{bgcolor.get()}')
  optwin.geometry("400x120"), optwin.title("Extra Options"), optwin.resizable(False, False)
  #optwin.geometry("400x300")
  ffmpegsettingsframe = LabelFrame(optwin, text="Additional FFmpeg Settings").place(relx=0.010, rely=0.005, relheight=0.980, relwidth=0.983)
  #ffmpegsettingsframe = LabelFrame(optwin, text="Additional FFmpeg Settings").place(relx=0.010, rely=0.005, relheight=0.430, relwidth=0.983)

  monoaudcheck = ttk.Checkbutton(optwin, text='Force audio to mono', variable=monoaudio, onvalue=1, offvalue=0)
  monoaudcheck.place(x=10, y=42)

  def updatemonocmd(*args):
   if monoaudio.get() == 1:
    monocmd.set('-ac 1')
   else:
    monocmd.set('')
  monoaudio.trace('w', updatemonocmd)

  extractextravideocheck = ttk.Checkbutton(optwin, text='Extract Extra Video Track', variable=extravideo, onvalue=1, offvalue=0)
  extractextravideocheck.place(x=165, y=22)

  OPTIONS_videoEncoder = ["libx264", "libx265", "libxvid", "mpeg1video", "mpeg2video"]

  comboboxvideoencoder = StringVar()
  videoencoderbox = ttk.Combobox(optwin, value=OPTIONS_videoEncoder, width=12)
  videoencoderbox.place(x=293, y=87)
  videoencoderbox.current(0)
  videoencoderbox.state(["readonly"])
  mp4encoderlbl = Label(optwin, text="Video Codec:", font=("Arial Bold", 8)).place(x=290, y=67)

  def updatevideoencoder(event):
   videoencoderbox.selection_clear()
   selected_videoencoder = videoencoderbox.get()
   if selected_videoencoder == "libx264":
    vcodec.set("libx264")
    videoencoderbox.selection_clear()
   elif selected_videoencoder == "libx265":
    vcodec.set("libx265")
    videoencoderbox.selection_clear()
   elif selected_videoencoder == "libxvid":
    vcodec.set("libxvid")
    videoencoderbox.selection_clear()
   elif selected_videoencoder == "mpeg1video":
    vcodec.set("mpeg1video")
    videoencoderbox.selection_clear()
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

  videotype.trace_add('write', updatevideoencoderoptions)
  updatevideoencoderoptions()

  videoencoderbox.bind("<<ComboboxSelected>>", updatevideoencoder)

  crfentry = ttk.Entry(optwin, textvariable=crfvalue, width=12)
  crfentry.insert(0, "")
  crfentry.place(x=10, y=87)
  crflbl = Label(optwin, text="CRF Value:", font=("Arial Bold", 8)).place(x=7, y=67)

  if crfentry.get() == '':
   crfentry.insert(0, "01")

  vbitrateentry = ttk.Entry(optwin, textvariable=vbitrate, width=12)
  vbitrateentry.insert(0, "")
  vbitrateentry.place(x=103, y=87)
  vbitratelbl = Label(optwin, text="Video Bitrate:", font=("Arial Bold", 8)).place(x=100, y=67)

  if vbitrateentry.get() == '':
   if videotype.get() == 1:
    vbitrateentry.delete(0, tk.END)
    vbitrateentry.insert(0, "150000")
    vbitrate.set('150000')
   
   elif videotype.get() == 2:
    vbitrateentry.delete(0, tk.END)
    vbitrateentry.insert(0, "30000000")
    vbitrate.set('30000000')
   
   elif videotype.get() == 3:
    vbitrateentry.delete(0, tk.END)
    vbitrateentry.insert(0, "8000000")
    vbitrate.set('8000000')

   def updatevbitrateoptions(*args):
    selected_type_bitrate = videotype.get()
    if selected_type_bitrate == 1:
     vbitrate.set('150000')
    elif selected_type_bitrate == 2:
     vbitrate.set('30000000')
    elif selected_type_bitrate == 3:
     vbitrate.set('8000000')

  videotype.trace_add('write', updatevbitrateoptions)
  updatevbitrateoptions()

  abitrateentry = ttk.Entry(optwin, textvariable=abitrate, width=12)
  abitrateentry.insert(0, "")
  abitrateentry.place(x=200, y=87)
  abitratelbl = Label(optwin, text="Audio Bitrate:", font=("Arial Bold", 8)).place(x=197, y=67)

  if abitrateentry.get() == '':
   abitrateentry.insert(0, "320k")

  bitexactcheck = ttk.Checkbutton(optwin, text='Use -bitexact for audio', variable=usebitexact, onvalue=1, offvalue=0)
  bitexactcheck.place(x=10, y=22)

  def usebitexactchanged(*args):
    if usebitexact.get() == 1:
     abitrate.set('-bitexact')
     abitrateentry.delete(0, tk.END)
     abitrateentry.insert(0, "-bitexact")
    else:
     abitrate.set('320k')
     abitrateentry.delete(0, tk.END)
     abitrateentry.insert(0, "320k")
  usebitexact.trace('w', usebitexactchanged)

  optwin.withdraw()


def SFDripper():
  filename = filePath.get()
  global fileextensionvideo
  global fileextensionaud1
  global fileextensionaud2
  global fileextensionaud3
  global fileextensionaud4
  fileextensionvideo = StringVar()
  fileextensionaud1 = StringVar()
  fileextensionaud2 = StringVar()
  fileextensionaud3 = StringVar()
  fileextensionaud4 = StringVar()
  only1audtrack = IntVar()
  overwritevariable = StringVar()
  currentdir = os.getcwd()
  destdir = dirPath.get()
  crf = StringVar()
  crf.set(crfvalue.get())

  if not os.path.exists(filePath.get()):
   tk.messagebox.showerror(title='No SFD Found', message="The SFD file could not be found. Please try to reselect the SFD file again, or choose a different one.")
   return

  if not os.path.exists(dirPath.get()):
   tk.messagebox.showerror(title='Directory Invalid', message="The directory could not be found. Please try to reselect the directory again, or choose a different one.")
   return

  if audiotype.get() == 1:
   fileextensionaud1.set('track1.mp3')
   fileextensionaud2.set('track2.mp3')
   fileextensionaud3.set('track3.mp3')
   fileextensionaud4.set('track4.mp3')
  if audiotype.get() == 2:
   fileextensionaud1.set('track1.wav')
   fileextensionaud2.set('track2.wav')
   fileextensionaud3.set('track3.wav')
   fileextensionaud4.set('track4.wav')
  if audiotype.get() == 3:
   fileextensionaud1.set('track1.adx')
   fileextensionaud2.set('track2.adx')
   fileextensionaud3.set('track3.adx')
   fileextensionaud4.set('track4.adx')

  if videotype.get() == 1:
   fileextensionvideo.set('sfdvideo.mp4')
   extravideoextension.set('sfdvideo2.mp4')
  
  if videotype.get() == 2:
   fileextensionvideo.set('sfdvideo.avi')
   extravideoextension.set('sfdvideo2.avi')
  
  if videotype.get() == 3:
   fileextensionvideo.set('sfdvideo.mpg')
   extravideoextension.set('sfdvideo2.mpg')

  if audiotracktype.get() == 1:
   only1audtrack.set(0)
  
  if audiotracktype.get() == 2:
   only1audtrack.set(1)
  
  if audiotracktype.get() == 3:
   only1audtrack.set(2)

  if audiotracktype.get() == 4:
   only1audtrack.set(3)

  if audiotracktype.get() == 5:
   only1audtrack.set(4)

  if option.get() == 1:
   if os.path.isfile(os.path.join(destdir, fileextensionvideo.get())):
    videofilealreadyexists = tk.messagebox.askyesno(title='File Already Exists', message=f'The file "{fileextensionvideo.get()}" is already in the export folder. Continuing will overwrite the file. Do you want to overwrite it?')
    if videofilealreadyexists == True:
     overwritevariable.set('-y')
     pass
    else:
     fileextensionvideo.set('')
     overwritevariable.set('-y')
     #overwritevariable.set('-n')
  
   if os.path.isfile(os.path.join(destdir, fileextensionaud1.get())):
    aud1filealreadyexists = tk.messagebox.askyesno(title='File Already Exists', message=f'The file "{fileextensionaud1.get()}" is already in the export folder. Continuing will overwrite the file. Do you want to overwrite it?')
    if aud1filealreadyexists == True:
     overwritevariable.set('-y')
     pass
    else:
     fileextensionaud1.set('')
     overwritevariable.set('-y')

   if os.path.isfile(os.path.join(destdir, fileextensionaud2.get())):
    aud2filealreadyexists = tk.messagebox.askyesno(title='File Already Exists', message=f'The file "{fileextensionaud2.get()}" is already in the export folder. Continuing will overwrite the file. Do you want to overwrite it?')
    if aud2filealreadyexists == True:
     overwritevariable.set('-y')
     pass
    else:
     fileextensionaud2.set('')
     overwritevariable.set('-y')

  elif option.get() == 2:
   if os.path.isfile(os.path.join(destdir, fileextensionvideo.get())):
    videofilealreadyexists = tk.messagebox.askyesno(title='File Already Exists', message=f'The file "{fileextensionvideo.get()}" is already in the export folder. Continuing will overwrite the file. Do you want to overwrite it?')
    if videofilealreadyexists == True:
     overwritevariable.set('-y')
     pass
    else:
     fileextensionvideo.set('')
     overwritevariable.set('-y')

  elif option.get() == 3:
    if os.path.isfile(os.path.join(destdir, fileextensionaud1.get())):
     aud1filealreadyexists = tk.messagebox.askyesno(title='File Already Exists', message=f'The file "{fileextensionaud1.get()}" is already in the export folder. Continuing will overwrite the file. Do you want to overwrite it?')
     if aud1filealreadyexists == True:
      overwritevariable.set('-y')
      pass
     else:
      fileextensionaud1.set('')
      overwritevariable.set('-y')

    if os.path.isfile(os.path.join(destdir, fileextensionaud2.get())):
     aud2filealreadyexists = tk.messagebox.askyesno(title='File Already Exists', message=f'The file "{fileextensionaud2.get()}" is already in the export folder. Continuing will overwrite the file. Do you want to overwrite it?')
     if aud2filealreadyexists == True:
      overwritevariable.set('-y')
      pass
     else:
      fileextensionaud2.set('')
      overwritevariable.set('-y')



  if option.get() == 1:
   command=f"ffmpeg -y -i {filename} -crf {crf.get()} -map 0:v:0 -c:v {str(vcodec.get())} -b:v {str(vbitrate.get())} {fileextensionvideo.get()}"
   exit_code = os.system(command)
   if exit_code == 0:
    videocreated = True
    if os.path.exists(os.path.join(currentdir, fileextensionvideo.get())):
     shutil.move(os.path.join(currentdir, fileextensionvideo.get()), os.path.join(destdir, fileextensionvideo.get()))
   
   if extravideo.get() == 1:
    command=f"ffmpeg -y -i {filename} -crf {crf.get()} -map 0:v:1 -c:v {str(vcodec.get())} -b:v {str(vbitrate.get())} {extravideoextension.get()}"
    os.system(command)
    if os.path.exists(os.path.join(currentdir, extravideoextension.get())):
     shutil.move(os.path.join(currentdir, extravideoextension.get()), os.path.join(destdir, extravideoextension.get()))

   command=f"ffmpeg {overwritevariable.get()} -err_detect ignore_err -i {filename} -b:a {str(abitrate.get())} {str(monocmd.get())} -map 0:a:0? {fileextensionaud1.get()}"
   os.system(command)

   command=f"ffmpeg {overwritevariable.get()} -err_detect ignore_err -i {filename} -b:a {str(abitrate.get())} {str(monocmd.get())} -map 0:a:1 {fileextensionaud2.get()}"
   os.system(command)

   command=f"ffmpeg {overwritevariable.get()} -err_detect ignore_err -i {filename} -b:a {str(abitrate.get())} {str(monocmd.get())} -map 0:a:2 {fileextensionaud3.get()}"
   os.system(command)

   command=f"ffmpeg {overwritevariable.get()} -err_detect ignore_err -i {filename} -b:a {str(abitrate.get())} {str(monocmd.get())} -map 0:a:3 {fileextensionaud4.get()}"
   os.system(command)



  elif option.get() == 2:
   command=f"ffmpeg {overwritevariable.get()} -i {filename} -crf {crf.get()} -map 0:v:0 -b:v {vbitrate.get()} -c:v {str(vcodec.get())} {fileextensionvideo.get()} {extravideocmd.get()}"
   exit_code = os.system(command)
   if exit_code == 0:
    videocreated = True
    if os.path.exists(os.path.join(currentdir, fileextensionvideo.get())):
     shutil.move(os.path.join(currentdir, fileextensionvideo.get()), os.path.join(destdir, fileextensionvideo.get()))
   if extravideo.get() == 1:
    command=f"ffmpeg -y -i {filename} -crf {crf.get()} -map 0:v:1 -c:v {str(vcodec.get())} -b:v {str(vbitrate.get())} {extravideoextension.get()}"
    os.system(command)
    if os.path.exists(os.path.join(currentdir, extravideoextension.get())):
     shutil.move(os.path.join(currentdir, extravideoextension.get()), os.path.join(destdir, extravideoextension.get()))



  elif option.get() == 3:
   command=f"ffmpeg {overwritevariable.get()} -i {filename} -b:a {str(abitrate.get())} {monocmd.get()} -map 0:a:0? {fileextensionaud1.get()}"
   os.system(command)
   
   command=f"ffmpeg {overwritevariable.get()} -i {filename} -b:a {str(abitrate.get())} {monocmd.get()} -map 0:a:1 {fileextensionaud2.get()}"
   os.system(command)

   command=f"ffmpeg {overwritevariable.get()} -i {filename} -b:a {str(abitrate.get())} {monocmd.get()} -map 0:a:2 {fileextensionaud3.get()}"
   os.system(command)

   command=f"ffmpeg {overwritevariable.get()} -i {filename} -b:a {str(abitrate.get())} {monocmd.get()} -map 0:a:3 {fileextensionaud4.get()}"
   os.system(command)

  if only1audtrack.get() == 1:
   if os.path.exists(os.path.join(currentdir, fileextensionaud1.get())):
    shutil.move(os.path.join(currentdir, fileextensionaud1.get()), os.path.join(destdir, fileextensionaud1.get()))
    if os.path.exists(os.path.join(currentdir, fileextensionaud2.get())):
     os.remove(fileextensionaud2.get())
    if os.path.exists(os.path.join(currentdir, fileextensionaud3.get())):
     os.remove(fileextensionaud3.get())
    if os.path.exists(os.path.join(currentdir, fileextensionaud4.get())):
     os.remove(fileextensionaud4.get())
  
  if only1audtrack.get() == 2:
   if os.path.exists(os.path.join(currentdir, fileextensionaud2.get())):
    shutil.move(os.path.join(currentdir, fileextensionaud2.get()), os.path.join(destdir, fileextensionaud2.get()))
    if os.path.exists(os.path.join(currentdir, fileextensionaud1.get())):
     os.remove(fileextensionaud1.get())
    if os.path.exists(os.path.join(currentdir, fileextensionaud3.get())):
     os.remove(fileextensionaud3.get())
    if os.path.exists(os.path.join(currentdir, fileextensionaud4.get())):
     os.remove(fileextensionaud4.get())
  
  if only1audtrack.get() == 3:
   if os.path.exists(os.path.join(currentdir, fileextensionaud3.get())):
    shutil.move(os.path.join(currentdir, fileextensionaud3.get()), os.path.join(destdir, fileextensionaud3.get()))
    if os.path.exists(os.path.join(currentdir, fileextensionaud1.get())):
     os.remove(fileextensionaud1.get())
    if os.path.exists(os.path.join(currentdir, fileextensionaud2.get())):
     os.remove(fileextensionaud2.get())
    if os.path.exists(os.path.join(currentdir, fileextensionaud4.get())):
     os.remove(fileextensionaud4.get())

  if only1audtrack.get() == 4:
   if os.path.exists(os.path.join(currentdir, fileextensionaud4.get())):
    shutil.move(os.path.join(currentdir, fileextensionaud4.get()), os.path.join(destdir, fileextensionaud4.get()))
    if os.path.exists(os.path.join(currentdir, fileextensionaud1.get())):
     os.remove(fileextensionaud1.get())
    if os.path.exists(os.path.join(currentdir, fileextensionaud2.get())):
     os.remove(fileextensionaud2.get())
    if os.path.exists(os.path.join(currentdir, fileextensionaud3.get())):
     os.remove(fileextensionaud3.get())
  
  else:
   if os.path.exists(os.path.join(currentdir, fileextensionaud1.get())):
    shutil.move(os.path.join(currentdir, fileextensionaud1.get()), os.path.join(destdir, fileextensionaud1.get()))
   if os.path.exists(os.path.join(currentdir, fileextensionaud2.get())):
    shutil.move(os.path.join(currentdir, fileextensionaud2.get()), os.path.join(destdir, fileextensionaud2.get()))
   if os.path.exists(os.path.join(currentdir, fileextensionaud3.get())):
    shutil.move(os.path.join(currentdir, fileextensionaud3.get()), os.path.join(destdir, fileextensionaud3.get()))
   if os.path.exists(os.path.join(currentdir, fileextensionaud4.get())):
    shutil.move(os.path.join(currentdir, fileextensionaud4.get()), os.path.join(destdir, fileextensionaud4.get()))
  
  doneextracting = tk.messagebox.showinfo(title='Extraction Completed', message="The SFD has been extracted/converted! Enjoy!")
  return


browsesfd = Button(text="Browse", command=GetFilePath, padx=40, pady=5).place(x=455, y=25)
browseexport = Button(text="Browse", command=ChooseExportDir, padx=40, pady=5).place(x=455, y=65)
sfdripper = Button(text="Extract/Convert the SFD!", command=SFDripper, padx=130, pady=15).place(x=195, y=232)
aboutextractor = Button(text="About Program", command=aboutprogram, padx=30, pady=1).place(x=18, y=234)
programdocuments = Button(text="Documentation", command=docs, padx=30, pady=1).place(x=18, y=264)
openextraoptionswin = Button(text="Extra Options", command=showoptionswin, padx=36, pady=1).place(x=18, y=234)

sfdselect = Label(dirframe, text="Select A SFD File:", font = ("Arial Bold", 8)).place(x=3, y=-1)
dirselect = Label(dirframe, text="Select An Output Directory:", font = ("Arial Bold", 8)).place(x=3, y=39)
audiotypelbl = Label(optoptionalframe, text="Extract Audio As:", font = ("Arial Bold", 8)).place(x=338, y=140)
videotypelbl = Label(optoptionalframe, text="Extract Video As:", font = ("Arial Bold", 8)).place(x=223, y=140)
audiotracktypelbl = Label(optoptionalframe, text="Extract Audio From:", font = ("Arial Bold", 8)).place(x=453, y=140)

vbitrate = StringVar()
crfvalue = StringVar()
usebitexact = IntVar()
darkmode = IntVar()
monoaudio = IntVar()
extravideoextension = StringVar()
monocmd = StringVar()
extravideo = IntVar()
extravideocmd = StringVar()
vcodec = StringVar()
abitrate = StringVar()
global bgcolor
bgcolor = StringVar()

option=IntVar(master, "1")
radio = ttk.Radiobutton(master, text='Extract Video and Audio', variable=option, value=1)
radio.place(x=27, y=132)
radio = ttk.Radiobutton(master, text='Extract Only Video', variable=option, value=2)
radio.place(x=27, y=157)
radio = ttk.Radiobutton(master, text='Extract Only Audio', variable=option, value=3)
radio.place(x=27, y=182)

filePath = StringVar()
dirPath = StringVar()
entrySFD = ttk.Entry(dirframe, textvariable=filePath, width=72)
entrySFD.insert(0, "")
entrySFD.place(x=5, y=16)
entryDir = ttk.Entry(dirframe, textvariable=dirPath, width=72)
entryDir.insert(0, "")
entryDir.place(x=5, y=56)

videotype=IntVar(master, "1")
OPTIONS_videotype = ["MP4", "AVI", "MPEG"]

comboboxvideotype = StringVar()
videotypebox = ttk.Combobox(master, value=OPTIONS_videotype, width=12)
videotypebox.place(x=226, y=160)
videotypebox.current(0)
videotypebox.state(["readonly"])

def updatevideotype(event):
   videotypebox.selection_clear()
   selectedvideotype = videotypebox.get()
   if selectedvideotype == "MP4":
    videotype.set("1")
    videotypebox.selection_clear()
   elif selectedvideotype == "AVI":
    videotype.set("2")
    videotypebox.selection_clear()
   elif selectedvideotype == "MPEG":
    videotype.set("3")
    videotypebox.selection_clear()
videotypebox.bind("<<ComboboxSelected>>", updatevideotype)


audiotype=IntVar(master, "1")
OPTIONS_audiotype = ["MP3", "WAV", "ADX"]

comboboxaudiotype = StringVar()
audiotypebox = ttk.Combobox(master, value=OPTIONS_audiotype, width=12)
audiotypebox.place(x=341, y=160)
audiotypebox.current(0)
audiotypebox.state(["readonly"])

def updateaudiotype(event):
   audiotypebox.selection_clear()
   selectedaudiotype = audiotypebox.get()
   if selectedaudiotype == "MP3":
    audiotype.set("1")
    audiotypebox.selection_clear()
   elif selectedaudiotype == "WAV":
    audiotype.set("2")
    audiotypebox.selection_clear()
   elif selectedaudiotype == "ADX":
    audiotype.set("3")
    audiotypebox.selection_clear()
audiotypebox.bind("<<ComboboxSelected>>", updateaudiotype)


audiotracktype=IntVar(master, "1")
OPTIONS_audiotracktype = ["All Tracks", "Only Track 1", "Only Track 2", "Only Track 3", "Only Track 4"]

comboboxaudiotracktype = StringVar()
audiotracktypebox = ttk.Combobox(master, value=OPTIONS_audiotracktype, width=16)
audiotracktypebox.place(x=456, y=160)
audiotracktypebox.current(0)
audiotracktypebox.state(["readonly"])

def updateaudiotracktype(event):
   audiotracktypebox.selection_clear()
   selectedaudiotracktype = audiotracktypebox.get()
   if selectedaudiotracktype == "All Tracks":
    audiotracktype.set("1")
    videotypebox.selection_clear()
   elif selectedaudiotracktype == "Only Track 1":
    audiotracktype.set("2")
    videotypebox.selection_clear()
   elif selectedaudiotracktype == "Only Track 2":
    audiotracktype.set("3")
    videotypebox.selection_clear()
   elif selectedaudiotracktype == "Only Track 3":
    audiotracktype.set("4")
    videotypebox.selection_clear()
   elif selectedaudiotracktype == "Only Track 4":
    audiotracktype.set("5")
    audiotracktypebox.selection_clear()
audiotracktypebox.bind("<<ComboboxSelected>>", updateaudiotracktype)


advancedoptions()
optwin.protocol("WM_DELETE_WINDOW", optwinclosing)
if os.path.isfile('updater.exe'):
 os.startfile('updater.exe')
else:
 print("Unable to find updater.exe, program will not be able to update.")
 pass
master.mainloop()