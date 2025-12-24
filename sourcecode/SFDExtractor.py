import tkinter as tk
import os
import shutil
import atexit
import subprocess
from PIL import Image, ImageTk
import argparse

from tkinter import filedialog, ttk, messagebox, Frame, LabelFrame, Label, StringVar, Button, Toplevel, IntVar
#Make sure you have check_for_ffmpeg.py and updater.py in the same folder as this PY file, or else the program won't work.
from check_for_ffmpeg import ffmpeg_location_int, ffprobe_location_int, run_ffmpeg_check, update_ffmpeg
from updater import check_for_new_SofdecVideoTools_version


master = tk.Tk()
master.geometry("600x300"), master.title("SFDExtractor V2.1.1"), master.resizable(False, False)#, master.iconbitmap("resource/icon/sfdextractor.ico")
page1 = Frame(master, bg='#f0f0f0').place(relx=0.0, rely=0.0, relheight=1.006, relwidth=1.004)
dirframe = LabelFrame(master, text="Directories")
dirframe.place(relx=0.010, rely=0.0, relheight=0.365, relwidth=0.980)
optframe = LabelFrame(master, text="Extraction Type").place(relx=0.010, rely=0.370, relheight=0.350, relwidth=0.340) 
optoptionalframe = LabelFrame(master, text="Extraction Options").place(relx=0.360, rely=0.370, relheight=0.350, relwidth=0.630)
otherframe = LabelFrame(master, text="Other").place(relx=0.010, rely=0.720, relheight=0.270, relwidth=0.300)

#GUI Vars
currentdir = os.getcwd()

#Main menu
filePathSFD = StringVar()
dirPath = StringVar()
SFDname = StringVar()
videoextension = StringVar()
extractiontypeoption=IntVar(master, 0)
videotype=IntVar(master, "1")
comboboxvideotype = StringVar()
audiotype=IntVar(master, "1")
comboboxaudiotype = StringVar()
audioextension = StringVar()
comboboxaudiotracktype = StringVar()
skipfileconversion = IntVar()
only_extract_certain_audio_tracks_int = IntVar()
disable_done_text = IntVar()
disable_updater = IntVar()
disable_gui = IntVar()

#Extra options' menu variables
showffmpegcommands = IntVar()
extracttofolder = IntVar()
autooverwritefiles = IntVar()
#unsquishvideo = IntVar()
batch_mode = IntVar()

#Help hint image - define it here so it can be used between both the main and extra options menus.
helphint_image = ImageTk.PhotoImage(Image.open(os.getcwd() + '/resource/img/questionmark.png').resize((10, 13)))


def showoptionswin():
  optwin.deiconify()

def optwinclosing():
  optwin.withdraw()


def gui_elements_mainmenu():
 #def aboutprogram():
  #programinfobox = tk.messagebox.showinfo(title='About SFDExtractor Beta V2.0.0', message='This program is intended for extracting (and converting) the files found in Sofdec (SFD) video files.\n\nIf you find any issues, please create an issue on the Github page, which can be found at "https://github.com/Firebow59/SofdecVideoTools/issues".')

 def docs():
  sfdextractordocs = os.getcwd() + '/resource/docs/documentation.pdf'
  os.startfile(sfdextractordocs)

 
 global show_help_hint
 def show_help_hint(helpmenu_message_index):
  help_message_textbox_title = [
  'Extract Audio Tracks',
  'FFmpeg Custom Settings',
  'Extraction Buffer Size',
  'Split AIX audio into individual tracks',
  ]

  help_messages = [
  '"All Tracks" will play every audio track present in the SFD.\n\n"Custom" will allow you to play only certain audio tracks from an SFD, starting at 0 (the first audio track in the file) and going up to 31. (ex. To only play tracks 1 (the 2nd track in the SFD file) and 3 (the 4th track in the SFD file), you would enter "1, 4", without the quotes.)',
  "These options will allow you to modify the settings for FFmpeg video/audio conversions, as well as print FFmpeg's output to the CMD window.\n\nDo note that these options will not do anything if 'Don't convert video/audio' is toggled on the main menu.", 
  "This option sets the max size of each buffer (of each file's data) used while extracting SFDs.\n\nA higher extraction buffer size = more RAM usage, but less file writes (and thus, a faster extraction). A lower buffer size is the opposite, but may be needed if low amounts of memory are available.\n\nThe default buffer is 50MB, which attempts to strike a balance between RAM usage and the number of file writes. For SFDs larger than a few hundred megabytes, you may want to consider putting this a bit higher (if possible).", 
  "This option will split any AIX audio (5.1 channel audio) present in a SFD file into three individual ADX files, as exists in the AIX file.\n\nThe output ADX files feature the following audio (credit to nebulas-star for this info):\n   - Track 1: Front left and right channels\n   - Track 2: Back left and right channels\n   - Track 3: Front center channel (left channel), Low-frequency       effects channel (right channel).",  #Space on "Track 3" text is for the messagebox to wrap properly
  ]

  help_message_textbox = tk.messagebox.showinfo(title=f'{help_message_textbox_title[helpmenu_message_index]}', message=f'{help_messages[helpmenu_message_index]}')



 def GetFilePath():
  if batch_mode.get() == 1:
   sfdfile = filedialog.askdirectory(title="Select A Folder")
  else:
   sfdfile = filedialog.askopenfilename(title="Select A SFD File", filetypes=[("SFD file", ".sfd")])
  filePathSFD.set(sfdfile)
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

 global enable_extractsfdbutton
 def enable_extractsfdbutton(*args):
  if not filePathSFD.get() == '' and not dirPath.get() == '':
   if videoextension.get() == '' and not skipfileconversion.get() == 1:  #Check for conversion-related video/audio extensions, to not allow SFD extraction if they aren't set to anything.
    sfdripperbtn.config(state=tk.DISABLED)
   elif audioextension.get() == '' and not skipfileconversion.get() == 1:
    sfdripperbtn.config(state=tk.DISABLED)
   else:
    sfdripperbtn.config(state=tk.NORMAL)
  else:
   sfdripperbtn.config(state=tk.DISABLED)
 filePathSFD.trace('w', enable_extractsfdbutton)
 dirPath.trace('w', enable_extractsfdbutton)
 videoextension.trace('w', enable_extractsfdbutton)
 audioextension.trace('w', enable_extractsfdbutton)



 def enable_batch_mode_function():
  if batch_mode.get() == 1:
   print("Batch mode enabled.")
   sfdselect.config(text="Select A Folder:")
  
  else:
   print("Batch mode disabled.")
   sfdselect.config(text="Select A SFD File:")
  
  enable_extractsfdbutton()
  filePathSFD.set('')
  
  return


 browsesfd = Button(text="Browse", command=GetFilePath, padx=40, pady=5).place(x=455, y=25)
 browseexport = Button(text="Browse", command=ChooseExportDir, padx=40, pady=5).place(x=455, y=65)
 sfdripperbtn = Button(text="Extract/Convert the SFD!", command=set_up_SFD_ripper_mode, padx=130, pady=15, state=tk.DISABLED)
 sfdripperbtn.place(x=195, y=225)
 enable_batch_mode = ttk.Checkbutton(master, text="Enable batch mode", variable=batch_mode, command=enable_batch_mode_function).place(x=330, y=280)
 #aboutextractor = Button(text="About Program", command=aboutprogram, padx=30, pady=1).place(x=18, y=234)
 programdocuments = Button(text="Documentation", command=docs, padx=30, pady=1).place(x=18, y=264)
 openextraoptionswin = Button(text="Extra Options", command=showoptionswin, padx=36, pady=1).place(x=18, y=234)

 sfdselect = Label(dirframe, text="Select A SFD File:", font = ("Arial Bold", 8))
 sfdselect.place(x=3, y=-1)  #Leave seperate for config w/batch mode.
 dirselect = Label(dirframe, text="Select An Output Directory:", font = ("Arial Bold", 8)).place(x=3, y=39)
 audiotypelbl = Label(optoptionalframe, text="Extract Audio As:", font = ("Arial Bold", 8)).place(x=338, y=130)
 videotypelbl = Label(optoptionalframe, text="Extract Video As:", font = ("Arial Bold", 8)).place(x=223, y=130)
 audiotracktypelbl = Label(optoptionalframe, text="Extract Audio From:", font = ("Arial Bold", 8)).place(x=453, y=130)
 
 
 extractiontyperadio = ttk.Radiobutton(master, text='Extract Video and Audio', variable=extractiontypeoption, value=0)
 extractiontyperadio.place(x=27, y=132)
 extractiontyperadio = ttk.Radiobutton(master, text='Extract Only Video', variable=extractiontypeoption, value=1)
 extractiontyperadio.place(x=27, y=157)
 extractiontyperadio = ttk.Radiobutton(master, text='Extract Only Audio', variable=extractiontypeoption, value=2)
 extractiontyperadio.place(x=27, y=182)

 #Leave below labels so that these don't make labels have bars over top them
 entrySFD = ttk.Entry(dirframe, textvariable=filePathSFD, width=72)
 entrySFD.insert(0, "")
 entrySFD.place(x=5, y=16)
 entryDir = ttk.Entry(dirframe, textvariable=dirPath, width=72)
 entryDir.insert(0, "")
 entryDir.place(x=5, y=56)



 global videoformatbox
 OPTIONS_videotype = ["MP4", "AVI", "MKV", "Custom: "]
 videoformatbox_stringvariable = StringVar()
 videoformatbox = ttk.Combobox(master, value=OPTIONS_videotype, width=12, textvariable=videoformatbox_stringvariable)
 videoformatbox.place(x=226, y=150)
 videoformatbox.current(0)

 def custom_output_video_type(*args):
    if videotype.get() == 4:  #DON'T compare as a string, it won't work.
     if videoformatbox_stringvariable.get().startswith('Custom: '):
      custom_output_video_format_string = (videoformatbox_stringvariable.get().split('Custom:')[1]).strip()
     else:
      custom_output_video_format_string = (videoformatbox_stringvariable.get()).strip()
     videoextension.set((f'.{custom_output_video_format_string}').lower())

     #Check for if the video formats = M1V or M2V (raw extracted audio formats), due to a bug where if the user entered these, the program would not be able to create the file, or would make a 0kb file.
     if videoextension.get().lower() in ('.m1v', '.m2v'):
      tk.messagebox.showerror(title='Invalid Output Video Format', message=f"Due to a limitation within SFDExtractor, {videoextension.get()[1:].upper()} is not a valid custom output format for converted files.\n\nIf you do need video in this format, try extracting the SFD with 'Don't convert audio/video' toggled.")
      videoextension.set('')
      videoformatbox_stringvariable.set("Custom: ")
      return
 
 def updatevideotype(event):
   if videoformatbox.get() == "MP4":
    videotype.set("1")
    videoextension.set('.mp4')
    videoformatbox_stringvariable.set("MP4")
    videoformatbox.selection_clear()
   elif videoformatbox.get() == "AVI":
    videotype.set("2")
    videoextension.set('.avi')
    videoformatbox_stringvariable.set("AVI")
    videoformatbox.selection_clear()
   elif videoformatbox.get() == "MKV":
    videotype.set("3")
    videoextension.set('.mkv')
    videoformatbox_stringvariable.set("MKV")
    videoformatbox.selection_clear()
   elif videoformatbox.get() == "Custom: ":
    videotype.set("4")
    videoextension.set('')
    videoformatbox.selection_clear()
 videoformatbox.bind("<<ComboboxSelected>>", updatevideotype)
 videoformatbox_stringvariable.trace("w", custom_output_video_type)



 def custom_output_audio_type(*args):
    if audiotype.get() == 4:  #DON'T compare as a string, it won't work.
     if audioformatbox_stringvariable.get().startswith('Custom: '):
      custom_output_audio_format_string = (audioformatbox_stringvariable.get().split('Custom:')[1]).strip()
     else:
      custom_output_audio_format_string = (audioformatbox_stringvariable.get()).strip()
     audioextension.set((f'.{custom_output_audio_format_string}').lower())
     
     #Check for if the audio formats = ADX, AIX or AC3 (raw extracted audio formats), due to a bug where if the user entered any of these, the program would not be able to create the file, or would make a 0kb file.
     if audioextension.get().lower() in ('.aix', '.adx', '.ac3', '.sfa'):
      tk.messagebox.showerror(title='Invalid Output Audio Format', message=f"Due to a limitation within SFDExtractor, {audioextension.get()[1:].upper()} is not a valid custom output format for converted files.\n\nIf you do need audio in this format, try extracting the SFD with 'Don't convert audio/video' toggled.")
      audioextension.set('')
      audioformatbox_stringvariable.set("Custom: ")
      return

 global audioformatbox
 OPTIONS_audiotype = ["MP3", "OGG", "FLAC", "Custom: "]
 audioformatbox_stringvariable = StringVar()
 audioformatbox = ttk.Combobox(master, value=OPTIONS_audiotype, width=12, textvariable=audioformatbox_stringvariable)
 audioformatbox.place(x=341, y=150)
 audioformatbox.current(0)
 audioformatbox.state(["readonly"])

 def updateaudioformat(event):
   if audioformatbox.get() == "MP3":
    audiotype.set("1")
    audioextension.set('.mp3')
    audioformatbox.selection_clear()
   elif audioformatbox.get() == "OGG":
    audiotype.set("2")
    audioextension.set('.ogg')
    audioformatbox.selection_clear()
   elif audioformatbox.get() == "FLAC":
    audiotype.set("3")
    audioextension.set('.flac')
    audioformatbox.selection_clear()
   elif audioformatbox.get() == "Custom: ":
    audiotype.set("4")
    audioextension.set('')
 audioformatbox.bind("<<ComboboxSelected>>", updateaudioformat)
 audioformatbox_stringvariable.trace("w", custom_output_audio_type)



 global custom_audio_track_extraction_list
 def custom_audio_track_extraction_list(*args):
   if not audiotracks_to_extract_combobox.get() == 'All Tracks':
    only_extract_certain_audio_tracks_int.set(1)
    audiotracks_to_extract_combobox.update()  #Bug fix for this variable having an old list of numbers if not updated right before extracting the SFD.
    list_of_audio_tracks_to_extract.clear()  #Also a bug fix for the aforementioned issue.
    for audio_track_number in audiotracks_to_extract_textvariable.get().split(','):
     if not audio_track_number.strip() in list_of_audio_tracks_to_extract and audio_track_number.strip().isdigit():
      list_of_audio_tracks_to_extract.append(audio_track_number.strip())
      master.focus_set()  #Force program to unselect the audioformatbox - fixes a bug where if "Create the SFD!" button was pressed right after audioformatbox, it wouldn't set correctly.
     
     elif not audio_track_number.strip().isdigit() and not audio_track_number.strip() == '':
      #Error message shows when the user attempts to make the SFD, to avoid an error message loop bug.
      only_extract_certain_audio_tracks_int.set(0)
      return
      
   else:
    only_extract_certain_audio_tracks_int.set(0)

 global list_of_audio_tracks_to_extract
 global audiotracks_to_extract_combobox
 global audiotracks_to_extract_textvariable
 list_of_audio_tracks_to_extract = []
 OPTIONS_audiotracktype = ["All Tracks", "Custom"]
 audiotracks_to_extract_textvariable = StringVar()
 audiotracks_to_extract_combobox = ttk.Combobox(master, value=OPTIONS_audiotracktype, textvariable=audiotracks_to_extract_textvariable, width=16)
 audiotracks_to_extract_combobox.place(x=456, y=150)
 audiotracks_to_extract_combobox.current(0)

 audiotracks_to_extract_helphint_label = Label(image=helphint_image)
 audiotracks_to_extract_helphint_label.image = helphint_image
 audiotracks_to_extract_helphint_label.place(x=570, y=130)  #Leave .place seperate to avoid error with bind
 audiotracks_to_extract_helphint_label.bind("<Button-1>", lambda event: show_help_hint(0))  #<Button-1> = left click on the question mark icon

 def updateaudiotracktype(*args):
   if audiotracks_to_extract_combobox.get() == "All Tracks":
    audiotracks_to_extract_combobox.config(state="readonly")
    audiotracks_to_extract_textvariable.set("All Tracks")
    audiotracks_to_extract_combobox.selection_clear()
   elif audiotracks_to_extract_combobox.get() == "Custom":
    audiotracks_to_extract_combobox.config(state="normal")  #Allow typing in the combobox
    audiotracks_to_extract_textvariable.set("")
    audiotracks_to_extract_combobox.selection_clear()
 audiotracks_to_extract_combobox.bind("<<ComboboxSelected>>", updateaudiotracktype)
 audiotracks_to_extract_combobox.bind("<FocusOut>", custom_audio_track_extraction_list)


 global disable_video_and_audio_comboboxes
 def disable_video_and_audio_comboboxes(*args):
   if skipfileconversion.get() == 1:
    videoformatbox.config(state=tk.DISABLED)
    audioformatbox.config(state=tk.DISABLED)
    showffmpegcommandscheck.config(state=tk.DISABLED)
    showffmpegcommands.set(0)
    ffmpeg_custom_video_command_entry.config(state="readonly")
    ffmpeg_custom_audio_command_entry.config(state="readonly")
   else:
    showffmpegcommandscheck.config(state=tk.NORMAL)
    enable_and_disable_options_based_on_extraction_type()  #Reset back to what the options have to be based on extraction type selected.
 disableFFmpegconversions = ttk.Checkbutton(master, text="Don't convert video/audio (leave as raw SFD formats)", variable=skipfileconversion, command=disable_video_and_audio_comboboxes).place(x=248, y=190)


 def enable_and_disable_options_based_on_extraction_type(*args):
  if extractiontypeoption.get() == 0:  #Video and Audio
   videoformatbox.config(state=tk.NORMAL)
   audioformatbox.config(state=tk.NORMAL)
   audiotracks_to_extract_combobox.config(state=tk.NORMAL)
   splitAIXaudio_checkbox.config(state=tk.NORMAL)
   if not skipfileconversion.get() == 1:  #Keep options that should be disabled when raw extractions are enabled disabled.
    ffmpeg_custom_video_command_entry.config(state="normal")
    ffmpeg_custom_audio_command_entry.config(state="normal")
  if extractiontypeoption.get() == 1:  #Video only
   audiotracks_to_extract_combobox.config(state=tk.DISABLED)
   audioformatbox.config(state=tk.DISABLED)
   videoformatbox.config(state=tk.NORMAL)
   splitAIXaudio_checkbox.config(state=tk.DISABLED)
   if not skipfileconversion.get() == 1:
    ffmpeg_custom_video_command_entry.config(state="normal")
    ffmpeg_custom_audio_command_entry.config(state="readonly")
  if extractiontypeoption.get() == 2:  #Audio only
   videoformatbox.config(state=tk.DISABLED)
   audioformatbox.config(state=tk.NORMAL)
   audiotracks_to_extract_combobox.config(state=tk.NORMAL)
   splitAIXaudio_checkbox.config(state=tk.NORMAL)
   if not skipfileconversion.get() == 1:
    ffmpeg_custom_video_command_entry.config(state="readonly")
    ffmpeg_custom_audio_command_entry.config(state="normal")
 extractiontypeoption.trace('w', enable_and_disable_options_based_on_extraction_type)


 def setdefaultoptionvalues():
  audioextension.set('.mp3')
  videoextension.set('.mp4')
  extractiontypeoption.set(0)
  updateaudiotracktype()  #Run at startup so that Audio Tracks to Extract combobox is set correctly on boot
 setdefaultoptionvalues()



def advancedoptions():
  global optwin
  optwin = Toplevel(master)
  optwin.geometry("600x235"), optwin.title("Extra Options"), optwin.resizable(False, False)
  extractionsettingsframe = LabelFrame(optwin, text="Extraction Settings").place(relx=0.010, rely=0.005, relheight=0.540, relwidth=0.383)
  ffmpegsettingsframe = LabelFrame(optwin, text="FFmpeg Settings").place(relx=0.400, rely=0.005, relheight=0.540, relwidth=0.59)
  QoLsettingsframe = LabelFrame(optwin, text="QoL Settings").place(relx=0.010, rely=0.580, relheight=0.390, relwidth=0.390)


  #Extractor settings
  def extraction_buffer_custom_size_enable(*args):
   if not extraction_buffer_textvariable.get() == 'Default (50MB)':
    buffer_size_apply_button.config(state=tk.NORMAL)
    buffer_size_combobox.config(state="normal")  #Allow typing in the combobox
   else:
    buffer_size_apply_button.config(state=tk.DISABLED)
    extraction_buffer_allocated_size.set(50)
    print(f"Extraction buffer set to default (50 MB).")
    buffer_size_combobox.config(state="readonly")

  def extraction_buffer_custom_size_check(*args):
    custom_extraction_buffer_size_split = extraction_buffer_textvariable.get().split("MB")[0].strip()
    if custom_extraction_buffer_size_split < '1':
     tk.messagebox.showerror(title='Buffer Size Invalid', message="The minimum buffer size is 1MB. Please choose a higher buffer size.")
     extraction_buffer_allocated_size.set('')
     return
    if not custom_extraction_buffer_size_split.isdigit():
     tk.messagebox.showerror(title='Buffer Size Invalid', message="The buffer given does not have digits/has non-digit values. Please input only digits for the buffer size.")
     extraction_buffer_allocated_size.set('')
     return
    extraction_buffer_allocated_size.set(custom_extraction_buffer_size_split)
    print(f"Extraction buffer set to {extraction_buffer_allocated_size.get()} MB.")

  global extraction_buffer_allocated_size
  extraction_buffer_allocated_size = StringVar()
  extraction_buffer_textvariable = StringVar()
  buffer_size_options = ['Default (50MB)', 'Custom (in MB):']
  buffer_size_combobox = ttk.Combobox(optwin, width=20, state="readonly", values=buffer_size_options, textvariable=extraction_buffer_textvariable)
  buffer_size_combobox.place(x=13, y=40)
  buffer_size_combobox.current(0)
  buffer_size_combobox_label = Label(optwin, text="Extraction Buffer Size:", font=("Arial Bold", 8)).place(x=11, y=20)
  extraction_buffer_textvariable.trace("w", extraction_buffer_custom_size_enable)
  extraction_buffer_allocated_size.set(50)  #Set the buffer size to the default on boot.
  print(f"Extraction buffer set to default (50 MB).")

  buffer_size_apply_button = ttk.Button(optwin, width=10, text="Apply", command=extraction_buffer_custom_size_check)
  buffer_size_apply_button.place(x=159, y=37.5, height=24)
  buffer_size_apply_button.config(state=tk.DISABLED)  #By default, disable it, since there's a default pre-set for the user.

  buffer_size_helphint_label = Label(optwin, image=helphint_image)
  buffer_size_helphint_label.image = helphint_image
  buffer_size_helphint_label.place(x=140, y=20)  #Leave .place seperate to avoid error with bind
  buffer_size_helphint_label.bind("<Button-1>", lambda event: show_help_hint(2))  #<Button-1> = left click on the question mark icon


  global splitAIXaudio_enable_int
  global splitAIXaudio_checkbox
  splitAIXaudio_enable_int = IntVar()
  splitAIXaudio_checkbox = ttk.Checkbutton(optwin, text="Split AIX audio into individual files", variable=splitAIXaudio_enable_int, onvalue=1, offvalue=0)
  splitAIXaudio_checkbox.place(x=13, y=66.5)  #Leave seperate to avoid errors on enable_and_disable_options_based_on_extraction_type()

  splitAIXaudio_helphint_label = Label(optwin, image=helphint_image)
  splitAIXaudio_helphint_label.image = helphint_image
  splitAIXaudio_helphint_label.place(x=217, y=68.3)  #Leave .place seperate to avoid error with bind
  splitAIXaudio_helphint_label.bind("<Button-1>", lambda event: show_help_hint(3))  #<Button-1> = left click on the question mark icon


  #FFmpeg settings
  global showffmpegcommandscheck
  showffmpegcommandscheck = ttk.Checkbutton(optwin, text='Print FFmpeg output to CMD window', variable=showffmpegcommands, onvalue=1, offvalue=0)
  showffmpegcommandscheck.place(x=247, y=20)  #Leave seperate to avoid errors on enable_and_disable_options_based_on_extraction_type()

  global ffmpeg_custom_video_command
  global ffmpeg_custom_audio_command
  global ffmpeg_custom_video_command_entry
  global ffmpeg_custom_audio_command_entry
  ffmpeg_custom_video_command = StringVar()
  ffmpeg_custom_audio_command = StringVar()
  ffmpeg_custom_video_command_entryboxtext = StringVar()
  ffmpeg_custom_audio_command_entryboxtext = StringVar()

  #Set commands to their defaults, for editing by user if wanted
  ffmpeg_custom_audio_command.set(f'-b:a 320k -bitexact')
  ffmpeg_custom_video_command.set(f'-crf 23 -b:v 80M -an')

  def save_new_custom_FFmpeg_command_values(*args):
   ffmpeg_custom_video_command.set(ffmpeg_custom_video_command_entryboxtext.get())
   ffmpeg_custom_audio_command.set(ffmpeg_custom_audio_command_entryboxtext.get())

  ffmpeg_custom_video_command_label = Label(optwin, text="FFmpeg video settings: ", font=("Arial Bold", 8)).place(x=245, y=45)
  ffmpeg_custom_video_command_entry = ttk.Entry(optwin, width=32, textvariable=ffmpeg_custom_video_command_entryboxtext)
  ffmpeg_custom_video_command_entry.place(x=385, y=45)
  ffmpeg_custom_video_command_entry.insert(0, ffmpeg_custom_video_command.get())

  ffmpeg_custom_audio_command_label = Label(optwin, text="FFmpeg audio settings: ", font=("Arial Bold", 8)).place(x=245, y=75)
  ffmpeg_custom_audio_command_entry = ttk.Entry(optwin, width=32, textvariable=ffmpeg_custom_audio_command_entryboxtext)
  ffmpeg_custom_audio_command_entry.place(x=385, y=75)
  ffmpeg_custom_audio_command_entry.insert(0, ffmpeg_custom_audio_command.get())

  ffmpeg_custom_command_note = Label(optwin, text='NOTE: Exclude the -i and output file info in the boxes above.', font=("Arial Bold", 8)).place(x=247, y=100)
  ffmpeg_custom_video_command_entryboxtext.trace("w", save_new_custom_FFmpeg_command_values)
  ffmpeg_custom_audio_command_entryboxtext.trace("w", save_new_custom_FFmpeg_command_values)

  ffmpeg_custom_commands_helphint_label = Label(optwin, image=helphint_image)
  ffmpeg_custom_commands_helphint_label.image = helphint_image
  ffmpeg_custom_commands_helphint_label.place(x=574, y=14)  #Leave .place seperate to avoid error with bind
  ffmpeg_custom_commands_helphint_label.bind("<Button-1>", lambda event: show_help_hint(1))  #<Button-1> = left click on the question mark icon


  #QoL Settings
  global setoutputdirectorytoSFDdirectory
  setoutputdirectorytoSFDdirectory = IntVar()
  useidenticaldirectorypaths = ttk.Checkbutton(optwin, text='Use SFD directory for output directory', variable=setoutputdirectorytoSFDdirectory, onvalue=1, offvalue=0)
  useidenticaldirectorypaths.place(x=10, y=156)

  global setdirectorytoSFDdirectorycmd
  def setdirectorytoSFDdirectorycmd(*args):
   if setoutputdirectorytoSFDdirectory.get() == 1:
    global filePathSFDdir
    filePathSFDdir = StringVar()
    filePathSFDdir.set(os.path.dirname(filePathSFD.get()))
    dirPath.set(filePathSFDdir.get())
   if setoutputdirectorytoSFDdirectory.get() == 0:
    dirPath.set('')
  setoutputdirectorytoSFDdirectory.trace('w', setdirectorytoSFDdirectorycmd)

  extracttofoldercheck = ttk.Checkbutton(optwin, text='Extract SFD to folder', variable=extracttofolder, onvalue=1, offvalue=0).place(x=10, y=176)
  extracttofolder.set(1)  #Enable by default
  autooverwritefilescheck = ttk.Checkbutton(optwin, text='Automatically overwrite files', variable=autooverwritefiles, onvalue=1, offvalue=0).place(x=10, y=196)
  
  optwin.withdraw()


def set_up_SFD_ripper_mode():
 custom_audio_track_extraction_list()  #Update the list to grab any possible new data, since it may not have registered if the user went directly from the Audio Tracks box (if custom tracks entered) to extracting the SFD.
 if only_extract_certain_audio_tracks_int.get() == 0 and not audiotracks_to_extract_combobox.get() == "All Tracks":
  tk.messagebox.showerror(title='Invalid Input for Custom Audio Extraction', message="The input provided for custom audio track extraction was invalid.\n\nPlease ensure only numbers are present in the box, and that it's written in the format 'A, B, C, ...' (ex. 1, 12, 4, 5, 2)")
  return

 if batch_mode.get() == 1:
  if not autooverwritefiles.get() == 1:
   ask_auto_overwrite_files_in_batch_mode = tk.messagebox.askyesno(title='Enable Auto Overwrite Files?', message='"Auto Overwrite Files" is currently disabled in the options. Not enabling it will force you to manually choose for each file that may already exist. Do you want to enable the option?')
   if ask_auto_overwrite_files_in_batch_mode == True:
    autooverwritefiles.set(1)
   else:
    autooverwritefiles.set(0)

  batch_list_of_SFD_files = []  #Keep this outside of the "for" loop to prevent it being reset every time this function runs  
  for list_of_SFD_files_in_folder in os.listdir(dirPath.get()):
   if list_of_SFD_files_in_folder.lower().endswith('.sfd'):
    batch_list_of_SFD_files.append(list_of_SFD_files_in_folder)

  for list_of_SFD_files_in_folder in batch_list_of_SFD_files:
    filePathSFD.set(dirPath.get() + '/' + list_of_SFD_files_in_folder)
    batch_list_of_SFD_files_current_index = batch_list_of_SFD_files.index(list_of_SFD_files_in_folder)
    SFDripper(batch_list_of_SFD_files, batch_list_of_SFD_files_current_index)
 else:
  batch_list_of_SFD_files = ''
  batch_list_of_SFD_files_current_index = ''
  SFDripper(batch_list_of_SFD_files, batch_list_of_SFD_files_current_index)  #Add these in here to prevent error where program would crash due to the missing variables


def SFDripper(batch_list_of_SFD_files, batch_list_of_SFD_files_current_index):
    #print("------------------------------------------------------------------------")
    print("")
    if not os.path.exists(filePathSFD.get()):
     if batch_mode.get() == 1:
      tk.messagebox.showerror(title='Input Directory Issue', message="The input directory could not be found/does not exist. Please try to reselect it again, or choose a different one.")
     else:
      tk.messagebox.showerror(title='No SFD Found', message="The SFD file could not be found. Please try to reselect the SFD file again, or choose a different one.")
     return
    
    if not os.path.exists(dirPath.get()):
     tk.messagebox.showerror(title='Output Directory Error', message="The output directory could not be found. Please try to reselect the directory again, or choose a different one.")
     return
  
    list_of_final_output_files_for_file_movement = []
    list_of_files_to_not_overwrite = []
    SFD_original_filename = StringVar()
    SFD_original_filename.set(os.path.basename(filePathSFD.get()[:-4]))  #Name of SFD, without the extension (the [:-4] is for removing the extension)


    def extract_SFD():
     print(f"Extracting {os.path.basename(filePathSFD.get())}...")
   
     extracted_audio_extension = StringVar()
     currentoffset_readSFD_file = IntVar()
     SFD_current_file_type = StringVar()
     current_track_number = IntVar()
     find_format_header_start = IntVar()
     start_of_segment_data = IntVar()
     list_of_name_buffers = []
     list_of_data_buffers = []
     list_of_output_file_names_for_buffers = []
     list_of_files_checked_for_starting_data_offset = []
     list_of_starting_data_offsets_for_files = []

     #Get filesize of file, to use for updating the extraction complete bar.
     size_of_SFD_in_bytes = os.stat(filePathSFD.get()).st_size
     size_of_SFD_in_MB = int(size_of_SFD_in_bytes) / (1024 * 1024)
     print(f"0 MB of {size_of_SFD_in_MB} MB extracted... (0%) ", end='\r')
     buffer_allocated_size_in_bytes = int((int(extraction_buffer_allocated_size.get()) * (1024 * 1024)) - 0.5)  #Minus 0.5 so that buffer doesn't go over the allotted size.

     with open(filePathSFD.get(), 'rb') as SFD_file_extract:
       while True:  #Loop to read all video/audio data
         SFD_file_extract.seek(currentoffset_readSFD_file.get())
         read_segment = SFD_file_extract.read(0x800) #0x800 = length of each header/video/audio segment

         #Get format based on 0xF byte of first line of segment header:
          #CX = audio, X being the track number (0 = first track, 1 = 2nd track, etc.)
          #DX = audio, X being the track number - I've never seen a SFD use this many tracks, since in reality it'd be quite inefficient, but it's here for completeness sake.
          #EX = video, X being the track number
          #BF = SofdecStream header/before SFD video/audio starts
          #BB = pre-SofdecStream header
         SFD_file_extract.seek(currentoffset_readSFD_file.get() + 0xF)
         SFD_read_current_file_type = SFD_file_extract.read(1)

         #Get current file type/format of segment, + track number of it
         SFD_current_file_type.set(str(SFD_read_current_file_type)[4:][:-2])
         current_track_number.set(int(SFD_read_current_file_type.hex()[1:], 16)) #If the current track is represented as a letter in the file (ex. "c"), convert it to decimal to avoid any errors later on.
        
         #Skip data in files to not overwrite by setting it to data not read by the program
         if f'{SFD_current_file_type.get()}{current_track_number.get()}' in list_of_files_to_not_overwrite:
            current_track_number.set('')
            SFD_current_file_type.set('f')

         #If the current track isn't in the list to be extracted, just skip it
         if SFD_current_file_type.get() == 'c' or SFD_current_file_type.get() == 'd': 
            if only_extract_certain_audio_tracks_int.get() == 1 and not str(current_track_number.get()) in list_of_audio_tracks_to_extract:  #Keep this code seperate from prev. line to avoid error where only "d" tracks were extracted.
             current_track_number.set('')
             SFD_current_file_type.set('f')

         #If the audio is a "d" track, fix the current track number to be above 16 (since "c" audio goes from 0x0 to 0xF (15), so putting d tracks as 15-31 ensures the program grabs the right data).
         #When later writing the file though, the filename will be reset back to 0 like "c" tracks)
         if SFD_current_file_type.get() == 'd' and int(current_track_number.get()) < 16:
            current_track_number.set(int(current_track_number.get()) + 16)

         #If not video or audio data, skip it - can't just check if it's b or f due to V1.0.1b SFDs starting with the SofdecStream header, leading to a "20" byte being found and a IndexError occurring if so.
         if SFD_current_file_type.get() not in ('c', 'd', 'e'):
           currentoffset_readSFD_file.set(currentoffset_readSFD_file.get() + 0x800)  #Skip to next header (0x7E2 of data, + 0x1E of header data that was previously read)
           current_track_number.set('')




         elif SFD_current_file_type.get() in ('c', 'd') and not extractiontypeoption.get() == 1:  #Audio extraction
            #Set up start offset, length to read, etc.
            seek_to_2nd_line_of_header = SFD_file_extract.seek(currentoffset_readSFD_file.get() + find_format_header_start.get() + 0x10)
            audio_buffer_list_name = f'{SFD_current_file_type.get()}{current_track_number.get()}'
          
            #Figure out where audio data actually starts from the start of the segment header (0x19 or 0x1E from the start of the first line of the segment header usually)
            #Also determine the audio track format the track is
            if not audio_buffer_list_name in list_of_files_checked_for_starting_data_offset:  #Only runs on first read of the file data
             #SFA = modified version of ADX audio
             #AIX = combination of mulitple ADX files to make a 5.1 channel sound. (Multiple ADX files used due to ADX files having a limit of 2 tracks/stereo audio per file)
             #AC3 = Dolby Digital format, likely to get the same result that AIX audio does. 
             possible_audio_formats = ['SFA', 'AIX', 'AC3']
             possible_audio_formats_identifiers = [b'\x80', b'\x41', b'\x0b\x77']  #NOTE: x77 will show as "w" and x41 will show as "A" if attempting to use an input or print to see this list.
             for file_format_identifier in possible_audio_formats_identifiers:
               if not extracted_audio_extension.get() == '':  #Extension is now set for this audio file
                 pass
               else:
                 possible_audio_formats_identifiers_current_index = possible_audio_formats_identifiers.index(file_format_identifier)
                 SFD_file_extract.seek(seek_to_2nd_line_of_header)  #Seek back to give the full distance from the start of the 2nd header to the data start.
                 length_until_segment_data_starts = SFD_file_extract.read(0x12).find(file_format_identifier)  #Read 12 bytes (until the end of the header/start of audio data), and search for start location of audio.
                 if not length_until_segment_data_starts == -1:  #If one of the file formats matches, apply the correct extension to the file.
                    extracted_audio_extension.set(possible_audio_formats[possible_audio_formats_identifiers_current_index])
                 elif length_until_segment_data_starts == -1 and possible_audio_formats_identifiers_current_index == 2:  #Audio isn't SFA, AIX, or AC3.
                    tk.messagebox.showinfo(title='Audio Format Issue', message=f"Audio track {current_track_number.get()} appears to be a format not currently supported in SofdecVideoTools!\n\nDue to this, the current audio track will not be extracted.\n\nIf possible, please reach out either on SofdecVideoTools' GitHub or GameBanana pages with the following info:\n- the game's name\n- the SFD's filename\n- the console the game is on\n- the current audio track (Audio Track {current_track_number.get()})\n\nThanks!")
                    list_of_files_to_not_overwrite.append(audio_buffer_list_name)
                    length_until_segment_data_starts = ''  #Reset variable for next run of loop
             
             if audio_buffer_list_name in list_of_files_to_not_overwrite:
              pass
             else:
              list_of_files_checked_for_starting_data_offset.append(audio_buffer_list_name)
              list_of_starting_data_offsets_for_files.append(length_until_segment_data_starts)
            
            if audio_buffer_list_name in list_of_files_to_not_overwrite:
              pass
            else:
             index_of_audio_track_in_starting_data_offset_buffers = list_of_files_checked_for_starting_data_offset.index(audio_buffer_list_name)
             length_until_segment_data_starts = list_of_starting_data_offsets_for_files[index_of_audio_track_in_starting_data_offset_buffers]
          

             SFD_file_extract.seek(seek_to_2nd_line_of_header)  #Seek back to before the location start check
             start_of_segment_data.set(currentoffset_readSFD_file.get() + 0x10 + length_until_segment_data_starts)  #0x10 is to skip the first line of data

             #Find how long the segment's audio data is.
             SFD_file_extract.seek(seek_to_2nd_line_of_header)
             segment_length = (int.from_bytes(SFD_file_extract.read(2)) - int(length_until_segment_data_starts)) + 0x2  #Add 0x2 to account for the bytes already read
             SFD_file_extract.seek(start_of_segment_data.get())
             read_SFD_segment = SFD_file_extract.read(segment_length)


             #Set output name details
             if SFD_current_file_type.get() == 'd' and current_track_number.get() > 15: #Reset dX track back to 0-15 (0xF) range, for the output file's name.
              current_track_number.set(current_track_number.get() - 16)
             output_data_file_name = SFD_original_filename.get() + '_' + f'audiotrack_{SFD_current_file_type.get()}{current_track_number.get()}.{extracted_audio_extension.get()}'

             #Write data to buffer, for later writing to file
             if audio_buffer_list_name in list_of_files_to_not_overwrite:
               pass
             else:
              if not audio_buffer_list_name in list_of_name_buffers:
               #Check if file already exists in the output folder, and ask if the user wants to overwrite it.
               if extracttofolder.get() == 1:
                if skipfileconversion.get() == 1:
                 file_to_check_to_see_if_it_already_exists = dirPath.get() + '/' f'{SFD_original_filename.get()}-extracted' + '/' + output_data_file_name
                else:
                 file_to_check_to_see_if_it_already_exists = dirPath.get() + '/' f'{SFD_original_filename.get()}-extracted' + '/' + output_data_file_name[:-4] + audioextension.get()
               
               if extracttofolder.get() == 0:
                if skipfileconversion.get() == 1:
                 file_to_check_to_see_if_it_already_exists = dirPath.get() + '/' + output_data_file_name
                else:
                 file_to_check_to_see_if_it_already_exists = dirPath.get() + '/' + output_data_file_name[:-4] + audioextension.get()

               if os.path.isfile(file_to_check_to_see_if_it_already_exists):
                if autooverwritefiles.get() == 1:
                 os.remove(file_to_check_to_see_if_it_already_exists)
                else:
                 filealreadyexists = tk.messagebox.askyesno(title='File Already Exists', message=f'{os.path.basename(file_to_check_to_see_if_it_already_exists)} already exists in the output folder. Do you want to overwrite this file?')
                 if filealreadyexists == True:
                  os.remove(file_to_check_to_see_if_it_already_exists)
                 else:
                  list_of_files_to_not_overwrite.append(audio_buffer_list_name)


               if audio_buffer_list_name in list_of_files_to_not_overwrite:
                pass
               else:
                audio_buffer_list_data = bytearray()
                list_of_name_buffers.append(audio_buffer_list_name)
                list_of_data_buffers.append(audio_buffer_list_data)
              
              if audio_buffer_list_name in list_of_files_to_not_overwrite:  #Check again so that no ValueError is thrown when getting the index of the audio buffer, since if it's supposed to be skipped, it shouldn't exist in the list.
               pass
              else:
               index_of_current_audio_buffer = int(list_of_name_buffers.index(audio_buffer_list_name))
               list_of_data_buffers[index_of_current_audio_buffer].extend(read_SFD_segment) #Use the index from the "name" list for writing to the right data list - the indexes for each file of data will be the same between them
               if not output_data_file_name in list_of_output_file_names_for_buffers:
                if not extracted_audio_extension.get() == '':  #Bug fix for filenames w/the extensions missing would be added to the list, doubling it's size and messing up the extraction
                 list_of_output_file_names_for_buffers.append(output_data_file_name)
            read_SFD_segment = b'' #Reset to avoid any writes to the wrong buffer




         elif SFD_current_file_type.get() == 'e' and not extractiontypeoption.get() == 2:  #Video extraction
            #Set up start offset, length to read, etc.
            seek_to_2nd_line_of_header = SFD_file_extract.seek(currentoffset_readSFD_file.get() + find_format_header_start.get() + 0x10)
            video_buffer_list_name = f'{SFD_current_file_type.get()}{current_track_number.get()}'

            #Figure out where video data actually starts from the start of the segment header (usually 0x1E from the start of the segment header)
            if not (video_buffer_list_name) in list_of_files_checked_for_starting_data_offset:  #Only runs on first read of the file data
             if not SFD_file_extract.read(4) == b'\x00\x00\x01\xB3': #(00 00 01 B3 = MPEG video data start)
              SFD_file_extract.seek(seek_to_2nd_line_of_header)  #Seek back to the start of the 2nd header to give the full distance from the start of the 2nd header
              #Read 14 bytes (end line of header/start of video data), and search for start location of video.
              length_until_segment_data_starts = SFD_file_extract.read(0x14).find(b'\x00\x00\x01\xB3')  #The max the 'B3' should be away is 12 bytes (0x1E), but use 14 instead just in case.
             else:
              length_until_segment_data_starts = 0xE  #0x1E after first byte of header
             list_of_files_checked_for_starting_data_offset.append(video_buffer_list_name)
             list_of_starting_data_offsets_for_files.append(length_until_segment_data_starts)

             #Check if video is MPEG-2 or MPEG-1 (only the PS2 & PS3 support MPEG-2 video)
             SFD_file_extract.seek(currentoffset_readSFD_file.get() + 0x10 + length_until_segment_data_starts)
             #MPEG-2 video is determined by finding a 00 00 01 B5 header, going 4 bytes after the B5 byte, and seeing if it = 01. If so, it's (likely) MPEG-2 video.
             find_if_MPEG_2_header_exists = SFD_file_extract.read(0xC8).find(b'\x00\x00\x01\xB5')  #0xC8 = 200 bytes of video file data
             if not find_if_MPEG_2_header_exists == -1:
              SFD_file_extract.seek(currentoffset_readSFD_file.get() + 0x10 + length_until_segment_data_starts)  #Seek back to start of video data
              #find_if_MPEG_2_header_exists serves as the length until the 00 00 01 B5 header if it's not -1.
              SFD_file_extract.seek(SFD_file_extract.tell() + find_if_MPEG_2_header_exists + 0x7)  # "+ 0x7" to get to the 01 byte that should exist 4 bytes after the B5 byte.
              if SFD_file_extract.read(1) == b'\x01':
               extracted_video_extension = 'm2v'
              else:
               extracted_video_extension = 'm1v'  #If the 01 check fail, set to MPEG-1 video extension.
             else:
              extracted_video_extension = 'm1v'  #If any checks fail, set to MPEG-1 video extension.

            else:
             index_of_video_track_in_starting_data_offset_buffers = list_of_files_checked_for_starting_data_offset.index(video_buffer_list_name)
             length_until_segment_data_starts = list_of_starting_data_offsets_for_files[index_of_video_track_in_starting_data_offset_buffers]

            SFD_file_extract.seek(seek_to_2nd_line_of_header)  #Seek back to before the location start check
            start_of_segment_data.set(currentoffset_readSFD_file.get() + 0x10 + length_until_segment_data_starts)  #0x10 is to skip the first line of data

            #Find how long the segment's data actually is.
            SFD_file_extract.seek(seek_to_2nd_line_of_header)
            segment_length = (int.from_bytes(SFD_file_extract.read(2)) - int(length_until_segment_data_starts)) + 0x2  #Add 0x2 to account for the bytes already read
            SFD_file_extract.seek(start_of_segment_data.get())
            read_SFD_segment = SFD_file_extract.read(segment_length)

            #Write data to buffer, for later writing to file
            video_buffer_list_name = f'{SFD_current_file_type.get()}{current_track_number.get()}'
            output_data_file_name = SFD_original_filename.get() + '_' + f'videotrack_{SFD_current_file_type.get()}{current_track_number.get()}.{extracted_video_extension}'
            if video_buffer_list_name in list_of_files_to_not_overwrite:
              pass
            else:
             if not video_buffer_list_name in list_of_name_buffers:
               #Check if file already exists in the output folder, and ask if the user wants to overwrite it.
               if extracttofolder.get() == 1:
                if skipfileconversion.get() == 1:
                 file_to_check_to_see_if_it_already_exists = dirPath.get() + '/' f'{SFD_original_filename.get()}-extracted' + '/' + output_data_file_name
                else:
                 file_to_check_to_see_if_it_already_exists = dirPath.get() + '/' f'{SFD_original_filename.get()}-extracted' + '/' + output_data_file_name[:-4] + videoextension.get()
               
               if extracttofolder.get() == 0:
                if skipfileconversion.get() == 1:
                 file_to_check_to_see_if_it_already_exists = dirPath.get() + '/' + output_data_file_name
                else:
                 file_to_check_to_see_if_it_already_exists = dirPath.get() + '/' + output_data_file_name[:-4] + videoextension.get()

               if os.path.isfile(file_to_check_to_see_if_it_already_exists):
                if autooverwritefiles.get() == 1:
                 os.remove(file_to_check_to_see_if_it_already_exists)
                else:
                 filealreadyexists = tk.messagebox.askyesno(title='File Already Exists', message=f'{os.path.basename(file_to_check_to_see_if_it_already_exists)} already exists in the output folder. Do you want to overwrite this file?')
                 if filealreadyexists == True:
                  os.remove(file_to_check_to_see_if_it_already_exists)
                 else:
                  list_of_files_to_not_overwrite.append(video_buffer_list_name)


               if video_buffer_list_name in list_of_files_to_not_overwrite:  #Avoid writing anything to the buffer to ensure the files to not be overwritten aren't replaced with just the header of the file
                pass
               else:
                video_buffer_list_data = bytearray()
                list_of_name_buffers.append(video_buffer_list_name)
                list_of_data_buffers.append(video_buffer_list_data)
          
             if video_buffer_list_name in list_of_files_to_not_overwrite:  #Only used when video_buffer_list_name isn't in the list of name buffers.
               pass
             else:
              index_of_current_video_buffer = int(list_of_name_buffers.index(video_buffer_list_name))
              list_of_data_buffers[index_of_current_video_buffer].extend(read_SFD_segment) #Use the index from the "name" list for writing to the right data list - the indexes for each file of data will be the same between them
              if not output_data_file_name in list_of_output_file_names_for_buffers:
               if not extracted_video_extension == '':  #Bug fix for filenames w/out extensions being be added to the list, doubling the list size and messing up the extraction (due to changing indexes)
                list_of_output_file_names_for_buffers.append(output_data_file_name)
            read_SFD_segment = b'' #Reset to avoid any writes to the wrong buffer
       
       



         #Write SFD data to buffer/files
         if SFD_current_file_type.get() in ('c', 'd', 'e'):
           try:
            for current_data_buffer in list_of_name_buffers:
             if current_data_buffer in list_of_files_to_not_overwrite:
              pass
             else:
              current_index_in_buffer_list = list_of_name_buffers.index(current_data_buffer)
              #Use index from name list, since the indexes will be the same between lists, and check if the buffer actually contains data
              if int(len(list_of_data_buffers[current_index_in_buffer_list])) >= buffer_allocated_size_in_bytes and not current_data_buffer == b'':
               output_data_file_name = list_of_output_file_names_for_buffers[current_index_in_buffer_list]
               buffer_data_to_write_to_file = list_of_data_buffers[current_index_in_buffer_list]

               with open(output_data_file_name, 'ab') as write_SFD_segment_to_new_file:
                 write_SFD_segment_to_new_file.write(buffer_data_to_write_to_file)
                 write_SFD_segment_to_new_file.close()
               list_of_data_buffers[current_index_in_buffer_list].clear()  #Clear to fix bug where it would keep writing the data to the file until stopped by user and/or crash/memory error.
           except OSError as write_extracted_segment_data:
            error_messagebox = tk.messagebox.showerror('Output file creation/writing error', f"{output_data_file_name} could not be created/written to. Try extracting the SFD again.\n\nIf this error continues to occur, make sure ample space is available on your hard drive, and that the output directory exists.")

           read_SFD_segment = b'' #Reset read_SFD_segment to prevent the final file from having the same 2nd segment repeated twice in the file.
           start_of_segment_data.set('') #Reset var to prevent issue where wrong data would be written to file
           extracted_audio_extension.set('')  #Reset audio extension variable every time loop runs
           SFD_file_extract.seek(currentoffset_readSFD_file.get() + 0x800)  #Seek to next segment
           currentoffset_readSFD_file.set(hex(SFD_file_extract.tell()))





         #Update completion percentage and % complete text, break loop if extraction complete
         current_percentage_of_SFD_extracted = f"{round(((currentoffset_readSFD_file.get() / size_of_SFD_in_MB) / (1024 * 1024)) * 100, 2)}"
         print(f"{round(currentoffset_readSFD_file.get() / (1024 * 1024), 2):.2f} MB of {round(size_of_SFD_in_MB, 2)} MB extracted... ({current_percentage_of_SFD_extracted:.5}%) ", end='\r')

         if current_percentage_of_SFD_extracted == '100.0':
           print("", end='\n')

           #Write any remaining data in buffers to their respective files
           try:
            for current_data_buffer in list_of_name_buffers:
             current_index_in_buffer_list = list_of_name_buffers.index(current_data_buffer)
             output_data_file_name = list_of_output_file_names_for_buffers[current_index_in_buffer_list]
             buffer_data_to_write_to_file = list_of_data_buffers[current_index_in_buffer_list]

             with open(output_data_file_name, 'ab') as write_SFD_segment_to_new_file:
               write_SFD_segment_to_new_file.write(buffer_data_to_write_to_file)
               write_SFD_segment_to_new_file.close()
               buffer_data_to_write_to_file.clear()
           except OSError as write_extracted_segment_data:
            tk.messagebox.showerror('Output file creation/writing error (final write)', f"{output_data_file_name} could not be created/written to. Try extracting the SFD again.\n\nIf this error continues to occur, make sure ample space is available on your hard drive, and that the output directory exists.")
            cleanup_files()
            break
        
           #Clear any buffers, variables, etc. for if user does another extraction afterwards.
           read_SFD_segment = b''
           start_of_segment_data.set('')
           extracted_audio_extension.set('')
           currentoffset_readSFD_file.set('')
           SFD_current_file_type.set('')
           current_track_number.set('')
           find_format_header_start.set('')

           list_of_name_buffers.clear()
           list_of_data_buffers.clear()
           list_of_output_file_names_for_buffers.clear()
           list_of_files_checked_for_starting_data_offset.clear()
           list_of_starting_data_offsets_for_files.clear()
           
           break
    extract_SFD()

  
    def split_AIX_tracks_to_ADX_function():
     if splitAIXaudio_enable_int.get() == 1 and not extractiontypeoption.get() == 1:
      print("")
      aix2adx_path = os.getcwd() + '/resource/bin/aix2adx01/aix2adx.exe'
      for AIX_file in os.listdir(os.getcwd()):
       if AIX_file.lower().endswith(".aix"):
        if not os.path.isfile(os.getcwd() + '/' + AIX_file):
         tk.messagebox.showerror(f'AIX File Error', f"{AIX_file} could not be found, and will be skipped. If this error consistently appears with this SFD, reach out on SofdecVideoTools' GitHub or GameBanana page with the following info:\n\n- Game name + console\n- The SFD file's name\n- Your current output file settings\n- Any other info that may be useful.")
        else:
         if extracttofolder.get() == 1:
          file_to_check_to_see_if_it_already_exists = dirPath.get() + '/' + f'{SFD_original_filename.get()}-extracted' + '/' + AIX_file  #Check for if the original .AIX file is in the output folder, split tracks checked in the next loop.
         else:
          file_to_check_to_see_if_it_already_exists = dirPath.get() + '/' + AIX_file
         if os.path.isfile(file_to_check_to_see_if_it_already_exists):
          if autooverwritefiles.get() == 1:
           os.remove(file_to_check_to_see_if_it_already_exists)
          else:
           filealreadyexists = tk.messagebox.askyesno(title='File Already Exists', message=f'{os.path.basename(file_to_check_to_see_if_it_already_exists)} already exists in the output folder. Do you want to overwrite this file?')
           if filealreadyexists == True:
            os.remove(file_to_check_to_see_if_it_already_exists)
           else:
            list_of_files_to_not_overwrite.append(AIX_file)

         if AIX_file in list_of_files_to_not_overwrite:
          if os.path.isfile(AIX_file):
           os.remove(AIX_file)
         else:
          print(f"Splitting {AIX_file} down to individual ADX tracks...", end='\r')
          try:
            split_AIX_to_ADX_cmd=f'{aix2adx_path} {AIX_file}'
            subprocess.run(split_AIX_to_ADX_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
          except IOError as AIX_to_ADX_rename_error:
             tk.messagebox.showerror('AIX -> ADX conversion error', f"{AIX_file} could not be split into individual ADX tracks. Try extracting the SFD again.\n\nIf this error continues to occur, make sure ample space is available on your hard drive for at least double the AIX filesize.")
             cleanup_files()
             break
          print(f"Splitting {AIX_file} down to individual ADX tracks... DONE!", end='\n')
          if os.path.isfile(AIX_file):
           os.remove(AIX_file)  #Remove original AIX file after it's split
      

      #Rename file to avoid it being hard to read (ex. change it from audiotrack_c300000.adx to audiotrack_c3_track0.adx)
      list_of_split_AIX_data_to_rename = os.listdir(os.getcwd())
      for split_AIX_file in list_of_split_AIX_data_to_rename:
          if split_AIX_file.lower().endswith(".adx"):
            split_original_ADX_name_for_track_number = split_AIX_file[:-4][30:] #Remove everything BUT the ADX track number (last digit before ".adx" extension)
            renamed_split_ADX_file_name = split_AIX_file[:-9] + '_AIXtrack' + split_original_ADX_name_for_track_number + '.adx'
           
            if extracttofolder.get() == 1:
             file_to_check_to_see_if_it_already_exists = dirPath.get() + '/' + f'{SFD_original_filename.get()}-extracted' + '/' + renamed_split_ADX_file_name
            else:
             file_to_check_to_see_if_it_already_exists = dirPath.get() + '/' + renamed_split_ADX_file_name
            if os.path.isfile(file_to_check_to_see_if_it_already_exists):
             if autooverwritefiles.get() == 1:
              os.remove(file_to_check_to_see_if_it_already_exists)
             else:
              filealreadyexists = tk.messagebox.askyesno(title='File Already Exists', message=f'{os.path.basename(file_to_check_to_see_if_it_already_exists)} already exists in the output folder. Do you want to overwrite this file?')
              if filealreadyexists == True:
               os.remove(file_to_check_to_see_if_it_already_exists)
              else:
               list_of_files_to_not_overwrite.append(renamed_split_ADX_file_name)           


            if renamed_split_ADX_file_name in list_of_files_to_not_overwrite:
             if os.path.isfile(split_AIX_file):
              os.remove(split_AIX_file)
            else:
             try:
              os.rename(split_AIX_file, renamed_split_ADX_file_name)
             except IOError as AIX_to_ADX_rename_error:
              tk.messagebox.showerror('ADX Filename Error', f"{split_AIX_file} could not be renamed to {renamed_split_ADX_file_name}.\n\nPlease try extracting the SFD again.\n\nIf the issue still persists, report the bug with the following info:\n\n- Game name + console\n- The SFD file's name\n- Your current output file settings\n- Any error messages that may have appeared on the CMD window\n- Any other info that may be useful.")
              cleanup_files()
              break
    split_AIX_tracks_to_ADX_function()


    def convert_SFD_contents():
      if skipfileconversion.get() == 1:  #If skipfileconversion.get() is enabled, just add the list of extracted files to the final output list for moving to the output folder later
       for list_of_extracted_files in os.listdir(os.getcwd()):
         if list_of_extracted_files.lower().endswith(('.m1v', '.m2v', '.adx', '.sfa', '.aix', '.ac3')):
          list_of_final_output_files_for_file_movement.append(list_of_extracted_files)
      else:
       print("")
       if ffmpeg_location_int.get() == 1:
        ffmpeg_exe_path = 'ffmpeg.exe'  #For if it's on user's PATH variables
       else:
        ffmpeg_exe_path = currentdir + '/resource/bin/ffmpeg/ffmpeg.exe'

       subprocess_runcommand = StringVar()
       if showffmpegcommands.get() == 1:
        subprocess_runcommand.set('{"stderr": subprocess.STDOUT, "shell": True}')
       else:
        subprocess_runcommand.set('{"creationflags": subprocess.CREATE_NO_WINDOW, "shell": True, "capture_output": True, "text": True}')
       subprocessoptions = eval(subprocess_runcommand.get())

       #Video conversion
       if not extractiontypeoption.get() == 2:
        for extracted_video_files_to_convert in os.listdir(os.getcwd()):
         if extracted_video_files_to_convert.lower().endswith((".m1v", ".m2v")):
          extracted_video_files_to_convert_new_filetype = extracted_video_files_to_convert[:-4] + videoextension.get()
          if not os.path.isfile(extracted_video_files_to_convert):
           tk.messagebox.showerror(f'Extracted Video File Error', f"{extracted_video_files_to_convert} could not be found, and will be skipped. If this error consistently appears with this SFD, reach out on SofdecVideoTools' GitHub or GameBanana page with the following info:\n\n- Game name + console\n- The SFD file's name\n- Your current output file settings\n- Any error messages that may have appeared on the CMD window\n- Any other info that may be useful.")
          else:
           if batch_mode.get() == 1:
            print(f"Converting {SFD_original_filename.get()} to {videoextension.get().upper()[1:]}/{audioextension.get().upper()[1:]}...")
           else:
            print(f"Converting {extracted_video_files_to_convert[:-4]} to {videoextension.get().upper()[1:]}...", end='\r')
          
           try:
            video_convert_FFmpeg_cmd=f'{ffmpeg_exe_path} -y -i "{extracted_video_files_to_convert}" {ffmpeg_custom_video_command.get()} {extracted_video_files_to_convert_new_filetype}'
            subprocess.run(video_convert_FFmpeg_cmd, **subprocessoptions)
           except IOError as video_conversion_error:
             print("Video conversion failed, see the error message for details.")
             cleanup_files()
             video_conversion_error_message = video_convert_FFmpeg_cmd.stderr or video_convert_FFmpeg_cmd.stdout or "An unknown error occurred."
             tk.messagebox.showerror('FFmpeg Error', f"{extracted_video_files_to_convert} could not be created, and FFmpeg gave the following error:\n\n{video_conversion_error_message}")
             return
          
           if batch_mode.get() == 0:  #Only print if batch mode disabled to clean up CMD window for batch extractions
            print(f"Converting {extracted_video_files_to_convert[:-4]} to {videoextension.get().upper()[1:]}... DONE!", end='\n')
           
           if not os.path.isfile(extracted_video_files_to_convert_new_filetype):
            tk.messagebox.showerror(f'Converted Video File Error', f"{extracted_video_files_to_convert_new_filetype} could not be found, and will be skipped.\n\nIf you used any custom FFmpeg commands, ensure there's no errors in the command.\n\nIf this error still consistently appears with this SFD, reach out on SofdecVideoTools' GitHub or GameBanana page with the following info:\n\n- Game name + console\n- The SFD file's name\n- Your current output file settings\n- Any error messages that may have appeared on the CMD window\n- Any other info that may be useful.")
           else:
            list_of_final_output_files_for_file_movement.append(extracted_video_files_to_convert_new_filetype)
           
           if os.path.isfile(extracted_video_files_to_convert):
            os.remove(extracted_video_files_to_convert)  #Delete original MPEG extracted data after the conversion is complete


       #Audio conversion - convert audio data to desired output format with FFmpeg
       if not extractiontypeoption.get() == 1:
        for extracted_audio_files_to_convert in os.listdir(os.getcwd()):
         if extracted_audio_files_to_convert.lower().endswith((".adx", ".aix", ".sfa", ".ac3")):
          extracted_audio_files_to_convert_new_filetype = extracted_audio_files_to_convert[:-4] + audioextension.get()
          if not os.path.isfile(extracted_audio_files_to_convert):
           tk.messagebox.showerror(f'Extracted Audio File Error', f"{extracted_audio_files_to_convert} could not be found, and will be skipped. If this error consistently appears with this SFD, reach out on SofdecVideoTools' GitHub or GameBanana page with the following info:\n\n- Game name + console\n- The SFD file's name\n- Your current output file settings\n- Any error messages that may have appeared on the CMD window\n- Any other info that may be useful.")
          else:
           if batch_mode.get() == 0:
            print(f"Converting {extracted_audio_files_to_convert_new_filetype} to {audioextension.get().upper()[1:]}...", end='\r')
          
           try:
            audio_convert_FFmpeg_cmd=f'{ffmpeg_exe_path} -y -i "{extracted_audio_files_to_convert}" {ffmpeg_custom_audio_command.get()} {extracted_audio_files_to_convert_new_filetype}'
            subprocess.run(audio_convert_FFmpeg_cmd, **subprocessoptions)
           except IOError as SFA_audio_to_ADX_error:
             print("Audio conversion failed, see the error message for details.")
             cleanup_files()
             audio_conversion_error_message = audio_convert_FFmpeg_cmd.stderr or audio_convert_FFmpeg_cmd.stdout or "An unknown error occurred."
             tk.messagebox.showerror('FFmpeg Error', f"{extracted_audio_files_to_convert} could not be created, and FFmpeg gave the following error:\n\n{audio_conversion_error_message}")
             return
          
           if batch_mode.get() == 0:  #Only print if batch mode disabled to clean up CMD window for batch extractions
            print(f"Converting {extracted_audio_files_to_convert[:-4]} to {audioextension.get().upper()[1:]}... DONE!", end='\n')

           if not os.path.isfile(extracted_audio_files_to_convert_new_filetype):
            tk.messagebox.showerror(f'Converted Audio File Error', f"{extracted_audio_files_to_convert_new_filetype} could not be found, and will be skipped.\n\nIf you used any custom FFmpeg commands, ensure there's no errors in the command.\n\nIf this error still consistently appears with this SFD, reach out on SofdecVideoTools' GitHub or GameBanana page with the following info:\n\n- Game name + console\n- The SFD file's name\n- Your current output file settings\n- Any error messages that may have appeared on the CMD window\n- Any other info that may be useful.")
           else:
            list_of_final_output_files_for_file_movement.append(extracted_audio_files_to_convert_new_filetype)
           
           if os.path.isfile(extracted_audio_files_to_convert):
            os.remove(extracted_audio_files_to_convert)  #Delete original audio file after it's done converting
    convert_SFD_contents()

  
    def move_files_to_output_location_and_finish_up():
     extracttofolder_name = f'{SFD_original_filename.get()}' + '-extracted'
     if extracttofolder.get() == 1:
       extract_to_folder_full_path = dirPath.get() + '/' + extracttofolder_name
       if os.path.exists(extract_to_folder_full_path):
        pass
       else:
        os.mkdir(extract_to_folder_full_path)
       dirPath.set(extract_to_folder_full_path)

     if batch_mode.get() == 0:  #Only print if batch mode disabled to clean up CMD window for batch extractions
      print("")

     if not dirPath.get() == os.getcwd() and not extracttofolder.get() == 1:
      print(f"Moving output files to {os.path.basename(dirPath.get())}...", end='\r')
     for output_files in list_of_final_output_files_for_file_movement:
      try:
       if os.path.isfile(output_files):
        if dirPath.get() == os.getcwd():
         pass
        else:
         shutil.move(os.getcwd() + '/' + output_files, dirPath.get())
       else:
        tk.messagebox.showerror(f'Shutil/File Move Error', f"{output_files} could not be found and moved to the destination folder. If you had no previous errors before this one during the extraction and/or conversion, try extracting/converting the SFD again. If this error still consistently appears with this SFD, reach out on SofdecVideoTools' GitHub or GameBanana page with the following info:\n\n- Game name + console\n- The SFD file's name\n- Your current output file setting\n- Any error messages that may have appeared on the CMD window\n- Any other info that may be useful.")
      except FileExistsError:
       tk.messagebox.showerror('File Moving/Existing Error', f"{output_files} could not be found, and thus likely does not exist. Please try again.\n\nIf this error continually appears, reach out on SofdecVideoTools' GitHub or GameBanana with details about the error, settings, the file's origin and name, etc.")
       return
     if not dirPath.get() == os.getcwd() and not extracttofolder.get() == 1:
      print(f"Moving output files to {os.path.basename(dirPath.get())}... DONE!", end='\n')

     if extracttofolder.get() == 1:  #Fix for UnboundLocalError when "Extract SFD to folder" isn't enabled.
      dirPath.set(extract_to_folder_full_path[:-(len('/' + extracttofolder_name))])  #Reset dirPath back to it's previous state that the user originally defined.
     list_of_final_output_files_for_file_movement.clear()



     if disable_done_text.get() == 1:
      pass
     else:
      #Set up "Complete" message variables, etc.
      if extracttofolder.get() == 1 and not batch_mode.get() == 1:
       additional_details_of_folder_name_for_complete_message = f'\n\nThe files can be found in a folder called "{extracttofolder_name}", in the path where you set the output directory.'
      else:
       additional_details_of_folder_name_for_complete_message = f''

      if skipfileconversion.get() == 1 and batch_mode.get() == 0:
       print("SFD extraction complete!")
      else:
       if batch_mode.get() == 0:
        print("SFD extraction and conversion complete!")
       if extractiontypeoption.get() == 0:
          video_and_audio_converted_format_complete_message = f'{videoextension.get()[1:].upper()}/{audioextension.get()[1:].upper()}'
       if extractiontypeoption.get() == 1:
          video_and_audio_converted_format_complete_message = f'{videoextension.get()[1:].upper()}'
       if extractiontypeoption.get() == 2:
          video_and_audio_converted_format_complete_message = f'{audioextension.get()[1:].upper()}'
      
      if dirPath.get() == os.getcwd() and not extracttofolder.get() == 1:
       SFD_extracted_files_in_root_dir_message = 'The extracted files can be found in the same folder as SFDExtractor.exe.'
      else:
       SFD_extracted_files_in_root_dir_message = ''

      if not audiotracks_to_extract_combobox.get() == "All Tracks":
       SFD_complete_custom_audiotrack_extraction_message = "\n\n(NOTE: if you don't see the audio track you set in the output folder, the SFD likely does not contain an audio file at that high of a track number. Alternatively, the SFD may not contain any audio at all.)\n\n"
      else:
       SFD_complete_custom_audiotrack_extraction_message = '\n\n'

      if skipfileconversion.get() == 1:
       SFD_complete_messagebox_title = 'SFD Extraction Complete!'
       #NOTE: the \n\n before the Enjoy text is set in the message above instead of in these lines
       if batch_mode.get() == 1:
        SFD_complete_messagebox_message = f'SFD files were successfully extracted. {SFD_extracted_files_in_root_dir_message}{additional_details_of_folder_name_for_complete_message}{SFD_complete_custom_audiotrack_extraction_message}Enjoy!'
       else:
        SFD_complete_messagebox_message = f'{SFD_original_filename.get() + '.sfd'} was successfully extracted. {SFD_extracted_files_in_root_dir_message}{additional_details_of_folder_name_for_complete_message}{SFD_complete_custom_audiotrack_extraction_message}Enjoy!'
      else:  #If conversions enabled
       SFD_complete_messagebox_title = 'SFD Extraction & Conversion Complete!'
       if batch_mode.get() == 1:
        SFD_complete_messagebox_message = f'SFDs was successfully extracted, and the file(s) were converted to {video_and_audio_converted_format_complete_message}. {SFD_extracted_files_in_root_dir_message}{additional_details_of_folder_name_for_complete_message}{SFD_complete_custom_audiotrack_extraction_message}Enjoy!'
       else:
        SFD_complete_messagebox_message = f'{SFD_original_filename.get() + '.sfd'} was successfully extracted, and the file(s) were converted to {video_and_audio_converted_format_complete_message}. {SFD_extracted_files_in_root_dir_message}{additional_details_of_folder_name_for_complete_message}{SFD_complete_custom_audiotrack_extraction_message}Enjoy!'

      if batch_mode.get() == 0:
       print("")
       tk.messagebox.showinfo(title=f'{SFD_complete_messagebox_title}', message=f'{SFD_complete_messagebox_message}')
      elif batch_mode.get() == 1:
       print("-----------------------------------------------------------")  #Extra line to split each file conversion in batch mode
       #If every file in the folder has been extracted in batch mode:
       #The -1 is used on the len since it starts at 1, whereas the current index starts at 0, thus fixing a bug where it would never trigger the message since they never aligned.
       if (len(batch_list_of_SFD_files) - 1) == batch_list_of_SFD_files_current_index:
        tk.messagebox.showinfo(title=f'{SFD_complete_messagebox_title}', message=f'{SFD_complete_messagebox_message}')
        os._exit(0)
     
     if disable_gui.get() == 1:  #If the GUI is disabled, and all extractions are finished, exit the program so it doesn't hang indefinitely.
      if batch_mode.get() == 1:
       if (len(batch_list_of_SFD_files) - 1) == batch_list_of_SFD_files_current_index:
        os._exit(0)
       else:
        pass
      else:
       os._exit(0)
    move_files_to_output_location_and_finish_up()



def updater_exe():
 check_for_new_SofdecVideoTools_version()

def cleanup_files():
 for list_of_files_in_root_dir in os.listdir(os.getcwd()):
  if list_of_files_in_root_dir.lower().endswith(('.m1v', '.m2v', '.adx', '.sfa', '.aix', '.ac3')):
   os.remove(list_of_files_in_root_dir)

def closeprogram():
 killffmpeg = 'taskkill /f /im ffmpeg.exe'
 subprocess.run(killffmpeg, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
 os._exit(0)


#CMD support, to allow use of the extractor in SFDPlayer
if __name__ == "__main__":
 parser = argparse.ArgumentParser(description='Extracts/converts SFD files.')
 parser.add_argument('-cmdmode', action='store_true', help='Disables the GUI/runs the program in command line mode. Required for the rest of the options to work.')
 parser.add_argument('-batch', action='store_true', help='Enables batch mode.')
 parser.add_argument('-file', type=str, help='Input file/directory.')
 parser.add_argument('-outputfolder', type=str, help='Output directory for extracted/converted files.')
 parser.add_argument('-extractiontype', type=int, help='What files to extract. (0 = audio + video, 1 = video only, 2 = audio only)')
 parser.add_argument('-noconvert', action='store_true', help='Bypasses FFmpeg conversions of the output data.')
 parser.add_argument('-videoformat', type=str, help='FFmpeg (converted) output video format (If -no_convert toggled, this does nothing).')
 parser.add_argument('-audioformat', type=str, help='FFmpeg (converted) output audio format (If -no_convert toggled, this does nothing).')
 parser.add_argument('-audiotracks', type=str, help='List of specific audio tracks to extract from the SFD(s).')
 parser.add_argument('-splitAIX', action='store_true', help='Splits AIX tracks (if found) into individual ADX tracks.')
 parser.add_argument('-extracttofolder', action='store_true', help='Enables extracting each SFD to a separate folder. Recommended for batch & individual SFD files. NOT ENABLED by default (except when using GUI).')
 parser.add_argument('-autooverwrite', action='store_true', help='Automatically overwrites any already existing extraction/conversion files for an SFD. Recommended for batch extractions.')
 parser.add_argument('-disable_done_text', action='store_true', help='Disables the "SFD Extraction Complete" text at the end of the extraction.')
 parser.add_argument('-disable_updater', action='store_true', help='Disables the program update checker from running on the current command.')
 parser.add_argument('-disable_ffmpeg_check', action='store_true', help='Disables the FFmpeg checker. Only use if only extracting video/audio data.')
 args = parser.parse_args()
 
 
 if args.cmdmode:
  disable_gui.set(1)  #Hide GUI if -cmdmode toggled'

 if disable_gui.get() == 1:  #Force the command line arguments to ONLY work if cmdmode is activated, in order to prevent a bug where the GUI would crash when not using CMD commands.
  if args.batch:
   batch_mode.set(1)

  if batch_mode.get() == 1:
    if args.file and os.path.isdir(args.file):
     filePathSFD.set(args.file)
    else:
     tk.messagebox.showerror(title='Input Directory Issue', message="The input directory could not be found/does not exist. Please try to reselect it again, or choose a different one.")
     os._exit(0)
  else:  #Single file extraction
    if args.file and os.path.isfile(args.file):
     filePathSFD.set(args.file)
    else:
     tk.messagebox.showerror(title='No SFD Found', message="The SFD file could not be found. Please try to reselect the SFD file again, or choose a different one.")
     os._exit(0)

  if args.outputfolder and os.path.isdir(args.outputfolder):
    dirPath.set(args.outputfolder)
  else:
    tk.messagebox.showerror(title='Output Directory Error', message="The output directory could not be found. Please try to reselect the directory again, or choose a different one.")
    os._exit(0)
 
  #Load all GUI functions even if cmdmode is active, just to allow the program to get/set the variables it needs to for the extraction.
  advancedoptions()  #Load before main menu GUI to prevent a bug where splitAIXaudio_checkbox would have a NameError, even if globally defined.
  gui_elements_mainmenu()
  if disable_gui.get() == 1:
   master.withdraw()
   extracttofolder.set(0)  #By default, this variable is enabled, so disable it so the user has the choice with the CMD command to enable it or not.

  #Set these below loading the GUI elements so they don't get reset back to their defaults instead of the correct values.
   if args.extractiontype:
     extractiontypeoption.set(args.extractiontype)
   if args.audiotracks:
    audiotracks_to_extract_combobox.current(1)  #Update this to "Custom" so that the "custom_audio_track_extraction_list" function grabs the correct values.
    audiotracks_to_extract_textvariable.set(args.audiotracks)  #Set the correct values after to not be overwritten by the "Custom" text.
   if args.splitAIX:
     if not extractiontypeoption.get() == 1:
      splitAIXaudio_enable_int.set(1)
  if args.noconvert:
    skipfileconversion.set(1)
  if not skipfileconversion.get() == 1:  #Conversion-related settings only, no need to set them if not converting the files.
    if args.videoformat:
      videoextension.set('.' + args.videoformat.lower())
    if args.audioformat:
      audioextension.set('.' + args.audioformat.lower())
  if args.extracttofolder:
   extracttofolder.set(1)
  if args.disable_done_text:
    disable_done_text.set(1)
  if args.disable_updater:
    disable_updater.set(1)
  if args.autooverwrite:
   autooverwritefiles.set(1)

  cleanup_files()
  if not disable_updater.get() == 1:
   updater_exe()
   print("")
  if not skipfileconversion.get() == 1:
   if args.disable_ffmpeg_check:
    pass
   else:
    run_ffmpeg_check()  #Set up FFmpeg location ints
    print("") #Space any FFmpeg text

  #GUI elements that are not set properly unless called here, due to allowing CMD commands to apply to the GUI elements.
  #None of these should overwrite the settings, so load them here so it applies the right option/configs for the right settings.
  enable_extractsfdbutton()
  videoformatbox.update()
  audioformatbox.update()
  custom_audio_track_extraction_list()
  disable_video_and_audio_comboboxes()

  #Run the extractor once everything is set up.
  extraction_buffer_allocated_size.set(50)
  set_up_SFD_ripper_mode()
 
 else:  #For non-CMD command loading of SFDExtractor (ex. just clicking and running the EXE)
  cleanup_files()
  updater_exe()
  print("")
  run_ffmpeg_check()
  print("")
  advancedoptions()
  gui_elements_mainmenu()


optwin.protocol("WM_DELETE_WINDOW", optwinclosing)
atexit.register(cleanup_files)
atexit.register(closeprogram)
master.mainloop()