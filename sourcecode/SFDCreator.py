import tkinter as tk
import os
import shutil
import webbrowser
import atexit
import subprocess
from PIL import Image, ImageTk
from tkinter import filedialog, ttk, messagebox, Frame, LabelFrame, Label, StringVar, Button, Toplevel, IntVar

#Make sure you have check_for_ffmpeg.py in the same folder as this PY file, or else the program won't work.
from check_for_ffmpeg import ffmpeg_location_int, ffprobe_location_int, run_ffmpeg_check, update_ffmpeg


#GUI Main Menu Window/Frames
master = tk.Tk()
master.geometry("600x450"), master.title("SFDCreator V1.0.0"), master.resizable(False, False)#, master.iconbitmap("resource/icon/sfdextractor.ico")
dirframe = LabelFrame(master, text="Input Files")
dirframe.place(relx=0.010, rely=0.0, relheight=0.365, relwidth=0.980) #leave this .place seperate from the "dirframe =" to avoid position issue.
outputdirframe = LabelFrame(master, text="Output File").place(relx=0.010, rely=0.37, relheight=0.368, relwidth=0.980)
otherframe = LabelFrame(master, text="Other").place(relx=0.010, rely=0.745, relheight=0.250, relwidth=0.550)


#GUI Vars
currentdir = os.getcwd()
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
sofdecstreamtype = StringVar()
vbitrate = StringVar()
abitrate = StringVar()
aHz = StringVar()
audiochannel = StringVar()
resolution = StringVar()
resolution_4by3 = StringVar()
vratio = StringVar()
framerate = StringVar()
cancelcreation = IntVar()


def gui_elements_mainmenu():
 global entryvid
 global entryaud1
 global entryaud2
 global entryDir
 global comboboxframerate
 global OPTIONS_streamtype
 global comboboxstreamtype
 global updatemenu_for_streamtype1
 global streamtypebox
 global updatevratio_streamtype1

 #The following elements are global for the purpose of preset options.
 global updatevres
 global updatevratio
 global updateframerate
 global updatevres_streamtype1
 global update_streamtype
 global comboboxvres
 global comboboxvres_streamtype1


 #Functions (for GUI buttons)
 def GetVideo():
  video = filedialog.askopenfilename(title="Select A Video File", filetypes=[("Video files", ".mpeg .mpg .mp4 .avi .wmv .mkv .mov .m1v .m2v")])
  filePathvideo.set(video)
  if autoinputvideoaudio.get() == 1:
   filePathaudt1.set(filePathvideo.get())
   filePathaudt2.set(filePathvideo.get())
   master.focus_set()  #Set focus off of entry box, onto the main window
  videoaudio()  #Update videoaudio() and copyaudio() to reflect new video/audio changes
  copyaudio()
  if not addaudiotracks.get() == 1:  #If additional audio tracks is disabled, set the file paths for track 3 and 4 to be blank
   filePathaudt3.set('')
   filePathaudt4.set('')
  if setSFDfilenametovideofilename.get() == 1:
   UsevideonameforSFD()
  if setoutputdirectorytovideodirectory.get() == 1:
   setdirectorytovideodirectory()
  master.focus_set()

 
 def GetAud1():
  audt1 = filedialog.askopenfilename(title="Select A Audio File for Track 1", filetypes=[("Audio files", ".wav .mp3 .flac .mp2 .adx .ogg .mpeg .mpg .mp4 .avi .mkv .mov")])
  filePathaudt1.set(audt1)
  master.focus_set()
  if not addaudiotracks.get() == 1:  #If additional audio tracks is disabled, set the file paths for track 3 and 4 to be blank
   filePathaudt3.set('')
   filePathaudt4.set('')


 global GetAud2 #Global so that this function works since the button for browseaud2 is in the options menu (due to Add Additional Audio tracks option)
 def GetAud2():
  audt2 = filedialog.askopenfilename(title="Select A Audio File for Track 2", filetypes=[("Audio files", ".wav .mp3 .flac .mp2 .adx .ogg .mpeg .mpg .mp4 .avi .mkv .mov")])
  filePathaudt2.set(audt2)
  master.focus_set()
  if not addaudiotracks.get() == 1:  #If additional audio tracks is disabled, set the file paths for track 3 and 4 to be blank
   filePathaudt3.set('')
   filePathaudt4.set('')

 global videoaudio #Same reason as why GetAud2 is global, only difference being since it's controlled by a checkbox on the main menu.
 def videoaudio():
  if UseVideoAudio.get() == 1:
   filePathaudt1.set(filePathvideo.get())
   master.focus_set()
   if UseTrack1forTrack2.get() == 1:
    filePathaudt2.set(filePathvideo.get())
    master.focus_set()
  if UseVideoAudio.get() == 0:
   filePathaudt1.set("")
   if UseTrack1forTrack2.get() == 1:
    UseTrack1forTrack2.set(0)
    filePathaudt2.set("")
    master.focus_set()


 global copyaudio
 def copyaudio(): #Same reason as why GetAud2 is global, only difference being since it's controlled by a checkbox on the main menu.
  if UseTrack1forTrack2.get() == 1:
   filePathaudt2.set(filePathaudt1.get())
   master.focus_set()
  if UseTrack1forTrack2.get() == 0:
   filePathaudt2.set("")



 #Open GitHub/About Program functions
 def opengithubrepo():
  webbrowser.open("https://github.com/Firebow59/SofdecVideoTools")
 def openissuespage():
  webbrowser.open("https://github.com/Firebow59/SofdecVideoTools/issues")
 def aboutprogram():
  link = 'This tool is intended for creating Sofdec video files (or SFD files for short) for use in various games. Developed by Firebow59.'
  aboutprogramwindow = tk.messagebox.showinfo(title='About Program', message=link)
 def docs():
  sfdcreatordocs = os.getcwd() + '/resource/docs/documentation.pdf'
  os.startfile(sfdcreatordocs)


 #GUI Labels
 videoreslabel = Label(outputdirframe, text="Video Resolution:", font = ("Arial Bold", 8)).place(x=10, y=240)
 videoframeratelabel = Label(outputdirframe, text="Video Framerate:", font = ("Arial Bold", 8)).place(x=169, y=240)
 vidbitrateselect = Label(outputdirframe, text="Video Bitrate:", font = ("Arial Bold", 8)).place(x=332, y=240)
 encodeasstreamselect = Label(outputdirframe, text="SFD Version/Muxer:", font = ("Arial Bold", 8)).place(x=417, y=285)
 videoratiooptions = Label(outputdirframe, text="Scale/Crop Settings:", font = ("Arial Bold", 8)).place(x=448, y=240)
 vidselect = Label(dirframe, text="Video File:", font = ("Arial Bold", 8)).place(x=3, y=-1)
 aud1select = Label(dirframe, text="Audio for Track 1:", font = ("Arial Bold", 8)).place(x=3, y=39)
 outputdirselect = Label(outputdirframe, text="Output Directory:", font = ("Arial Bold", 8)).place(x=127, y=184)
 outputsfdnameselect = Label(outputdirframe, text="SFD Filename:", font = ("Arial Bold", 8)).place(x=9, y=184)
 

 #SFD Version Detector help menu
 global helpinfo_sfdversion_window
 helpinfo_sfdversion_window = tk.Tk()  #Draw menu on boot to prevent "Doesn't exist" errors
 helpinfo_sfdversion_window.withdraw()
 def help_determine_sfd_version_functions():
  global show_help_determine_sfd_version
  def show_help_determine_sfd_version(*args):
   #Set up window, find X and Y values where window should be placed - relative to the question mark icon next to the SFD Version/Muxer text.
   #Add 30 to X value to push it to the right side of the question mark
   questionmark_sfd_muxer_help_label_find_x_value = questionmark_sfd_muxer_help_label.winfo_rootx() + 30
   questionmark_sfd_muxer_help_label_find_y_value = questionmark_sfd_muxer_help_label.winfo_rooty()
   helpinfo_sfdversion_window.geometry(f'232x55+{questionmark_sfd_muxer_help_label_find_x_value}+{questionmark_sfd_muxer_help_label_find_y_value}') #Last 2 values on geometry = X/Y placement of window
  
   helpinfo_sfdversion_window.resizable(False, False)
   helpinfo_sfdversion_window.overrideredirect(True)  #Hide top bar of window
   find_SFD_version_label = Label(helpinfo_sfdversion_window, text="Unsure which muxer to use? Click here:", font=("Arial Bold", 8))
   find_SFD_version_open_findversion_window = Button(helpinfo_sfdversion_window, text="Determine SFD Version", command=find_sfd_version_main_window).place(x=50, y=22.5)
   find_SFD_version_label.place(x=2, y=2)  #Leave .place seperate to avoid error with bind
   helpinfo_sfdversion_window.deiconify()  #Reshow help window, do last to prevent flashing

  global close_help_determine_sfd_version
  def close_help_determine_sfd_version(*args):
   helpinfo_sfdversion_window.withdraw()
   master.focus_set()


 global helpmenu_find_sfd_version_window
 helpmenu_find_sfd_version_window = tk.Tk()
 helpmenu_find_sfd_version_window.withdraw()
 def find_sfd_version_main_window(*args):
   helpinfo_sfdversion_window.withdraw()  #Hide the info window when main Version Detector window is opened
   helpmenu_find_sfd_version_window = tk.Tk()
   helpmenu_find_sfd_version_window.geometry('520x280'), helpmenu_find_sfd_version_window.title('Find SFD Version'), helpmenu_find_sfd_version_window.resizable(False, False)
   helpmenu_find_sfd_version_window.tkraise()  #Set focus to helpmenu window/make it appear on top

   filePath_version_detect_sample_sfd = StringVar()
   unable_to_get_muxer_info = IntVar()
   def get_example_sfd():
    version_detect_sample_sfd_select = filedialog.askopenfilename(title="Select A SFD File", filetypes=[("SFD files", ".sfd")])
    if os.path.exists(version_detect_sample_sfd_select):
     filePath_version_detect_sample_sfd.set(version_detect_sample_sfd_select)
     launch_version_detector_button.config(state=tk.NORMAL)
    else:
     print("The given SFD was unable to be found. Please try again.")
     filePath_version_detect_sample_sfd.set('')
     launch_version_detector_button.config(state=tk.DISABLED)
    helpmenu_find_sfd_version_window.tkraise()  #Make helpmenu appear on top

   def get_SFD_version_and_video_details(*args):
    #Reset labels
    helpmenu_find_sfd_version_output_sfdname_text.config(text="", font=("Arial", 9))
    helpmenu_find_sfd_version_output_muxertype_text.config(text="", font=("Arial", 9))
    helpmenu_find_sfd_version_output_videoresolution_text.config(text="", font=("Arial", 9))
    helpmenu_find_sfd_version_output_videoframerate_text.config(text="", font=("Arial", 9))

    versiondetector_path = f'"{os.getcwd() + '/SFDVersionDetector.exe'}"'
    #versiondetector_path = 'python SFDVersionDetector.py'  #Debug path
    versiondetector_cmd = f'{versiondetector_path} -file "{filePath_version_detect_sample_sfd.get()}" -no_gui -version_only -disable_done_text -disable_updater'
    if os.path.exists(versiondetector_path):  #Disable if trying to use .py file
     versiondetector_runcommand_subprocess = subprocess.run(versiondetector_cmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
     output_SFD_version_version_detector_stdout = versiondetector_runcommand_subprocess.stdout
     if "SFD version unable to be determined" in output_SFD_version_version_detector_stdout:
      unable_to_get_muxer_info.set(1)
      print("Unable to determine SFD version.")

      version_detector_unable_to_detect_error_message = (
      f"{os.path.basename(filePath_version_detect_sample_sfd.get())}'s "
      "muxer/version was unable to be determined.\n\nIt may be a V1.0.0 SFD file, or a "
      "earlier Saturn SFD file (which SofdecVideoTools does not currently support)."
      "\n\nIf possible, please head to SofdecVideoTools' GitHub page, and make a issue with the following infomation:"
      "\n- Name of game the SFD came from"
      "\n- The filename of the SFD file"
      "\n- Any other info regarding the file that may be useful."
      )
    
      tk.messagebox.showerror(title='SFD Version Detector Error', message=f"{version_detector_unable_to_detect_error_message}")
      if unable_to_get_muxer_info.get() == 1:
       output_SFD_version_version_detector_stdout_fixed = 'Unable to be determined.'
     else:
      output_SFD_version_version_detector_stdout_fixed = versiondetector_runcommand_subprocess.stdout.strip().split(':')[1]
    else:
     print("SFDVersionDetector.exe could not be found.")
     tk.messagebox.showerror(title='SFD Version Detector Error', message=f"SFDVersionDetector.exe could not be found. Please check that the file exists in the same folder as SFDCreator.exe. If it doesn't exist in the same folder, re-download SofdecVideoTools.")
     helpmenu_find_sfd_version_window.tkraise()
     return


    #Set FFprobe location based on where it's located (PATH or SofdecVideoTools' folder)
    global ffprobe_exe_path
    if ffprobe_location_int.get() == 1:
     ffprobe_exe_path = 'ffprobe.exe'
    else:
     ffprobe_exe_path = currentdir + '/resource/bin/ffmpeg/ffprobe.exe'

    get_framerate_FFprobe_command = f'"{ffprobe_exe_path}" -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate "{filePath_version_detect_sample_sfd.get()}"'
    get_framerate_FFprobe_runcommand = subprocess.run(get_framerate_FFprobe_command, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
    version_detect_sample_sfd_framerate = get_framerate_FFprobe_runcommand.stdout.strip()
    #Since the resolution is written like X/Y (ex. 60/1, 6000/100), fix it to be written just as a rounded value.
    version_detect_sample_sfd_framerate_split = version_detect_sample_sfd_framerate.split('/')
    version_detect_sample_sfd_framerate_fixed = round(int(version_detect_sample_sfd_framerate_split[0]) / int(version_detect_sample_sfd_framerate_split[1]))
   
    get_resolution_FFprobe_command = f'"{ffprobe_exe_path}" -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "{filePath_version_detect_sample_sfd.get()}"'
    get_resolution_FFprobe_runcommand = subprocess.run(get_resolution_FFprobe_command, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
    version_detect_sample_sfd_resolution = get_resolution_FFprobe_runcommand.stdout.strip()

    #Update labels with info
    #[:-1] on resolution to remove the x after the height
    helpmenu_find_sfd_version_output_sfdname_text.config(text=f"- SFD filename: {os.path.basename(filePath_version_detect_sample_sfd.get())}", font=("Arial", 9))
    helpmenu_find_sfd_version_output_muxertype_text.config(text=f"- Muxer Type: {output_SFD_version_version_detector_stdout_fixed.strip()}", font=("Arial", 9))
    helpmenu_find_sfd_version_output_videoresolution_text.config(text=f"- Video Resolution: {version_detect_sample_sfd_resolution[:-1]}", font=("Arial", 9))
    helpmenu_find_sfd_version_output_videoframerate_text.config(text=f"- Video Framerate: {version_detect_sample_sfd_framerate_fixed}", font=("Arial", 9))
    helpmenu_find_sfd_version_window.tkraise()  #Make helpmenu appear on top


   #Buttons and labels
   helpmenu_find_sfd_version_find_sample_sfd = Button(helpmenu_find_sfd_version_window, text="Browse", command=get_example_sfd, padx=45, pady=5).place(x=32, y=22.5)
   launch_version_detector_button = Button(helpmenu_find_sfd_version_window, text="Determine SFD Version", command=get_SFD_version_and_video_details, padx=4, pady=5)
   launch_version_detector_button.place(x=32, y=92.5)
   launch_version_detector_button.config(state=tk.DISABLED)

   helpmenu_find_sfd_version_how_to_use_frame = ttk.LabelFrame(helpmenu_find_sfd_version_window, borderwidth=2).place(relx=0.38, rely=0.01, relheight=0.54, relwidth=0.61)
   helpmenu_find_sfd_version_how_to_use_text = Label(helpmenu_find_sfd_version_window, text="How to Use:", font=("Arial Bold", 9)).place(x=200, y=14)
   helpmenu_find_sfd_version_select_sfd_text = Label(helpmenu_find_sfd_version_window, text="- Select a SFD from the game you want to create an SFD", font=("Arial", 9)).place(x=200, y=34)
   helpmenu_find_sfd_version_select_sfd_text = Label(helpmenu_find_sfd_version_window, text="for by clicking the Browse button.", font=("Arial", 9)).place(x=200, y=51)
   helpmenu_find_sfd_version_select_sfd_text = Label(helpmenu_find_sfd_version_window, text='- Once you have an SFD file selected, click "Determine', font=("Arial", 9)).place(x=200, y=74)
   helpmenu_find_sfd_version_select_sfd_text = Label(helpmenu_find_sfd_version_window, text='SFD Version".', font=("Arial", 9)).place(x=200, y=91)
   helpmenu_find_sfd_version_select_sfd_text = Label(helpmenu_find_sfd_version_window, text='- The SFD muxer needed will then be determined, and', font=("Arial", 9)).place(x=200, y=114)
   helpmenu_find_sfd_version_select_sfd_text = Label(helpmenu_find_sfd_version_window, text='printed into the "Output" box below.', font=("Arial", 9)).place(x=200, y=129)

   helpmenu_find_sfd_version_output_frame = ttk.LabelFrame(helpmenu_find_sfd_version_window, borderwidth=2).place(relx=0.01, rely=0.55, relheight=0.44, relwidth=0.98)
   helpmenu_find_sfd_version_output_text = Label(helpmenu_find_sfd_version_window, text="Output:", font=("Arial Bold", 9)).place(x=8, y=164)
   helpmenu_find_sfd_version_output_sfdname_text = Label(helpmenu_find_sfd_version_window, text="- SFD filename:", font=("Arial", 9))
   helpmenu_find_sfd_version_output_sfdname_text.place(x=8, y=184)  #Keep these .place's seperate to avoid NoneType error
   helpmenu_find_sfd_version_output_muxertype_text = Label(helpmenu_find_sfd_version_window, text="- Muxer Type:", font=("Arial", 9))
   helpmenu_find_sfd_version_output_muxertype_text.place(x=8, y=204)
   helpmenu_find_sfd_version_output_videoresolution_text = Label(helpmenu_find_sfd_version_window, text="- Video Resolution:", font=("Arial", 9))
   helpmenu_find_sfd_version_output_videoresolution_text.place(x=8, y=224)
   helpmenu_find_sfd_version_output_videoframerate_text = Label(helpmenu_find_sfd_version_window, text="- Video Framerate:", font=("Arial", 9))
   helpmenu_find_sfd_version_output_videoframerate_text.place(x=8, y=244)
 help_determine_sfd_version_functions()


 questionmark_sfd_muxer_help_image = ImageTk.PhotoImage(Image.open(os.getcwd() + '/resource/img/questionmark.png').resize((10, 13)))
 questionmark_sfd_muxer_help_label = Label(outputdirframe, image=questionmark_sfd_muxer_help_image)
 questionmark_sfd_muxer_help_label.image = questionmark_sfd_muxer_help_image
 questionmark_sfd_muxer_help_label.place(x=565, y=285)  #Leave .place seperate to avoid error with bind
 helpinfo_sfdversion_window.focus_set()  #Set focus to help window so it displays on top
 
 questionmark_sfd_muxer_help_label.bind("<Enter>", show_help_determine_sfd_version)  #If user enters the area of the question mark icon, run the help window
 questionmark_sfd_muxer_help_label.bind("<Button-1>", close_help_determine_sfd_version)  #If user left clicks on the question mark icon, close the help window


 #GUI buttons/checkboxes
 SFDmuxerbtn = Button(text="Create the SFD!", command=createSFD, padx=80, pady=15)
 #Change .place in change_SFDmuxerbtn_batch() for change to occur too
 SFDmuxerbtn.place(x=345, y=363)     #.place(x=345, y=363) #Keep seperate so change_SFDmuxerbtn_batch() works
 extraoptions = Button(text="Extra Options", command=show_extraoptionswindow, padx=36.3, pady=1).place(x=12, y=354)
 opengithubrepobtn = Button(text="Open GitHub Repo", command=opengithubrepo, padx=23, pady=1).place(x=173, y=354)
 aboutcreator = Button(text="About Program", command=aboutprogram, padx=30.4, pady=1).place(x=12, y=384)
 programdocuments = Button(text="Documentation", command=docs, padx=30.3, pady=1).place(x=12, y=414)
 #presetbtn = Button(text="Save/Load Preset", command=openpresetwindow, padx=28, pady=1).place(x=173, y=384)

 global UseVideoAudio
 global UseTrack1forTrack2
 UseVideoAudio = IntVar()
 videoaudiocheck = ttk.Checkbutton(text='Use Audio from Input Video', variable=UseVideoAudio, command=videoaudio, onvalue=1, offvalue=0).place(x=12, y=137)
 UseTrack1forTrack2 = IntVar()
 track1fortrack2check = ttk.Checkbutton(text='Use Track 1 Audio for Track 2', variable=UseTrack1forTrack2, command=copyaudio, onvalue=1, offvalue=0).place(x=192, y=137)


 batchmode = IntVar()
 def change_SFDmuxerbtn_batch(*args):
  if batchmode.get() == 1:
   SFDmuxerbtn.config(text="Add to List!", command=write_batchmode_info_tofile, padx=25)
  else:
   SFDmuxerbtn.config(text="Create the SFD!", command=createSFD)
  SFDmuxerbtn.place(x=345, y=363)
 batchmode.trace('w', change_SFDmuxerbtn_batch)
 change_SFDmuxerbtn_batch() #Run on boot so that SFD button exists
 #batchmodecheck = ttk.Checkbutton(text='Enable Batch Mode', variable=batchmode, command=change_SFDmuxerbtn_batch, onvalue=1, offvalue=0).place(x=405, y=410)




 #GUI Entry/Combobox Widgets
 entryvid = ttk.Entry(dirframe, textvariable=filePathvideo, width=72)
 entryvid.insert(0, "")
 entryvid.place(x=5, y=15)
 browsevid = Button(text="Browse", command=GetVideo, padx=40, pady=5).place(x=455, y=25)


 def ChooseExportDir():
  exportpath = filedialog.askdirectory(title="Choose An Output Directory")
  dirPath.set(exportpath)
  if not os.path.exists(dirPath.get()):
   tk.messagebox.showerror(title='Directory Error', message="Can't find the directory selected. Try again, or select a different directory.")
  entryDir.focus()
  entryDir.xview_moveto(1)
  master.focus_set()  #Set focus off of output directory entry


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

 videobitrateentry = ttk.Entry(outputdirframe, textvariable=vbitrate, width=15)
 vbitrate.set('80M')
 videobitrateentry.place(x=335, y=257)


 #Video Options
 OPTIONS_VRes = ["Same as Video", "320/426 x 240 (240p)", "480/640 x 360 (360p)", "640/848 x 480 (480p)", "960/1280 x 720 (720p)", "1440/1920 x 1080 (1080p)"]
 comboboxvres = StringVar()
 vres = ttk.Combobox(master, value=OPTIONS_VRes)
 vres.place(x=12, y=257)
 vres.current(0)
 
 def updatevres(event):
  selected_vresvalue = vres.get()
  global get4by3_resolution
  def get4by3_resolution(event=None):
   if comboboxvres.get() == OPTIONS_VRes[1]:
    resolution_4by3.set('320:240')
   elif comboboxvres.get() == OPTIONS_VRes[2]:
    resolution_4by3.set('480:360')
   elif comboboxvres.get() == OPTIONS_VRes[3]:
    resolution_4by3.set('640:480')
   elif comboboxvres.get() == OPTIONS_VRes[4]:
    resolution_4by3.set('960:720')
   elif comboboxvres.get() == OPTIONS_VRes[5]:
    resolution_4by3.set('1440:1080')
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
     resolution.set(f'{width}:{height}')
     comboboxvres.set(selected_vresvalue)
     vres.selection_clear()
    except ValueError:
     pass
  
  if selected_vresvalue == "Same As Video":
   comboboxvres.set(OPTIONS_VRes[0])
   resolution.set("")
   enable_video_scale_options()  #Lock vratio box again if re-selected
   vres.selection_clear()
  elif selected_vresvalue in OPTIONS_VRes[1:]:
   index = OPTIONS_VRes.index(selected_vresvalue)
   comboboxvres.set(OPTIONS_VRes[index])
   height = int(OPTIONS_VRes[index].split(" ")[-1][1:-2])
   resolution.set(f'-2:{height}')
   vres.selection_clear()
  elif selected_vresvalue == "320/426 x 240 (240p)":
   comboboxvres.set(OPTIONS_VRes[1])
   resolution.set('426:240')
   vres.selection_clear()
  elif selected_vresvalue == "480/640 x 360 (360p)":
   comboboxvres.set(OPTIONS_VRes[2])
   resolution.set('640:360')
   vres.selection_clear()
  elif selected_vresvalue == "640/848 x 480 (480p)":
   comboboxvres.set(OPTIONS_VRes[3])
   resolution.set('848:480')
   vres.selection_clear()
  elif selected_vresvalue == "960/1280 x 720 (720p)":
   comboboxvres.set(OPTIONS_VRes[4])
   resolution.set('1280:720')
   vres.selection_clear()
  elif selected_vresvalue == "1440/1920 x 1080 (1080p)":
   comboboxvres.set(OPTIONS_VRes[5])
   resolution.set('1920:1080')
   vres.selection_clear()
  get4by3_resolution()
  enable_video_scale_options()
  updatevratio(event=None)  #Update video crop/scale settings with new resolution
 vres.bind("<<ComboboxSelected>>", updatevres)
 vres.bind("<KeyRelease>", updatevres)
 comboboxvres.set(OPTIONS_VRes[0])  #Set to "Same as Video" on program boot

 def enable_video_scale_options(*args):
   if vres.get() == 'Same as Video' or resolution.get() == "":
    vratiobox.config(state=tk.DISABLED)
    vratio.set('')
   else:
    vratiobox.config(state=tk.NORMAL)
 vres.bind("w", enable_video_scale_options)


 OPTIONS_VRatio = ["None", "Crop (16:9 to 4:3)", "Scale (16:9 to 4:3)", "Squish (16:9 to 4:3)", "Stretch (4:3 to 16:9)"] #, "Scale (4:3 to 16:9)"]
 comboboxvratio = StringVar()
 vratiobox = ttk.Combobox(master, value=OPTIONS_VRatio, textvariable=comboboxvratio, width=18)
 vratiobox.place(x=451, y=257)
 vratiobox.current(0)
 vratiobox.state(["readonly"])

 def updatevratio(event):
  selected_vratiovalue = comboboxvratio.get()
  if resolution.get() == '':
   pass
  else:
   if selected_vratiovalue == "None":
    comboboxvratio.set(OPTIONS_VRatio[0])
    vratio.set('')
    vratiobox.selection_clear()
   elif selected_vratiovalue == "Crop (16:9 to 4:3)":
    comboboxvratio.set(OPTIONS_VRatio[1])
    vratio.set(f'-vf "scale={resolution.get()},crop=(ih*4/3):ih"')
    vratiobox.selection_clear()
   elif selected_vratiovalue == "Scale (16:9 to 4:3)":
    comboboxvratio.set(OPTIONS_VRatio[2])
    vratio.set(f'-vf "scale={resolution.get()},pad=iw:iw*3/4:(ow-iw)/2:(oh-ih)/2"')
    vratiobox.selection_clear()
   elif selected_vratiovalue == "Squish (16:9 to 4:3)":
    comboboxvratio.set(OPTIONS_VRatio[3])
    vratio.set(f'-vf "scale=iw*sar:ih, scale={resolution_4by3.get()}, setsar=1"')
    vratiobox.selection_clear()
   elif selected_vratiovalue == "Stretch (4:3 to 16:9)":
    comboboxvratio.set(OPTIONS_VRatio[4])
    vratio.set(f'-vf "scale={resolution.get()},crop=(ih*16/9):ih"')
    vratiobox.selection_clear()
   elif selected_vratiovalue == "Scale (4:3 to 16:9)":
    comboboxvratio.set(OPTIONS_VRatio[5])
    vratio.set('')
    vratiobox.selection_clear()
  #print(f'vratio: {vratio.get()}')
 vratiobox.bind("<<ComboboxSelected>>", updatevratio)


 OPTIONS_VFrame = ["Same as Video", "24", "29.97", "30", "59.97", "60"]
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
 vframerate.bind("<<ComboboxSelected>>", updateframerate)
 vframerate.bind("<KeyRelease>", update_customframerate)
 
 #Audio Options - now in Extra Options menu




 #Update options for V1 SFDs
 V1_enabled_int_vratio = IntVar()
 def updatemenu_for_streamtype1(*args):
   if sofdecstreamtype.get() == '1' or sofdecstreamtype.get() == '2' or sofdecstreamtype.get() == '3' or sofdecstreamtype.get() == '5':
    V1_enabled_int_vratio.set(1)
    vres_streamtype1.place(x=12, y=257)
    vratiobox_streamtype1.place(x=451, y=257)
    if sofdecstreamtype.get() == '5':
      vres_streamtype1.current(7)  #Set to 480p if CRAFT muxer is selected by default
    if sofdecstreamtype.get() == '1' or sofdecstreamtype.get() == '2' or sofdecstreamtype.get() == '3':
      vres_streamtype1.current(3)  #Set to 240p for V1.0.0, V1.0.1b and V1.07 muxers by default
   else:
    V1_enabled_int_vratio.set(0)
    vratiobox.current(0)
    vratio.set('')  #Clear vratio var
    vres_streamtype1.place_forget()
    vratiobox_streamtype1.place_forget()
 sofdecstreamtype.trace_add("write", updatemenu_for_streamtype1)




 #Stream Type 1 Options
 OPTIONS_VRes_streamtype1 = ["Same as Video", "128 x 128", "160 x 128", "320 x 240", "256 x 256", "480 x 336", "320 x 480", "640 x 480"]
 comboboxvres_streamtype1 = StringVar()
 vres_streamtype1 = ttk.Combobox(master, value=OPTIONS_VRes_streamtype1)

 def updatevres_streamtype1(*args):
  selected_vresvalue = vres_streamtype1.get()
  if "x" in selected_vresvalue:
    custom_resolution = selected_vresvalue.split("x")
    if len(custom_resolution) == 2:
     try:
      #V1 SFDs require resolutions that have heights and widths that are multiples of 16 - check custom resolutions to ensure they will work.
      width = int(custom_resolution[0])
      height = int(custom_resolution[1])
      incorrect_width_V1_custom_resolution = IntVar()
      incorrect_height_V1_custom_resolution = IntVar()
      #V1 SFDs require resolutions that are multiples of 16 - check custom resolutions to ensure they will work.
     
      if width % 16 == 0:  #Check if the remainder of the width divided by 16 = 0
       incorrect_height_V1_custom_resolution.set(0)
      else:
       incorrect_width_V1_custom_resolution.set(1)
      
      if height % 16 == 0:  #Check if the remainder of the height divided by 16 = 0
       incorrect_height_V1_custom_resolution.set(0)
      else:
       incorrect_height_V1_custom_resolution.set(1)
    

      if incorrect_width_V1_custom_resolution.get() == 1 and incorrect_height_V1_custom_resolution.get() == 1:
       tk.messagebox.showerror(title='Custom Resolution Error', message="The given height and width are not multiples of 16. V1 muxers (aside from nebulas-star's muxer) require the width and height to both be multiples of 16. Please change the width and height to be both multiples of 16.")
       resolution.set('')
       SFDmuxerbtn.config(state=tk.DISABLED)
       return
      if incorrect_width_V1_custom_resolution.get() == 0 and incorrect_height_V1_custom_resolution.get() == 1:
       tk.messagebox.showerror(title='Custom Resolution Error', message="The given height is not a multiple of 16. V1 muxers (aside from nebulas-star's muxer) require both the width and height to be multiples of 16. Please change the height to be a multiple of 16.")
       resolution.set('')
       SFDmuxerbtn.config(state=tk.DISABLED)
       return
      if incorrect_width_V1_custom_resolution.get() == 1 and incorrect_height_V1_custom_resolution.get() == 0:
       tk.messagebox.showerror(title='Custom Resolution Error', message="The given width is not a multiple of 16. V1 muxers (aside from nebulas-star's muxer) require both the width and height to be multiples of 16. Please change the width to be a multiple of 16.")
       resolution.set('')
       SFDmuxerbtn.config(state=tk.DISABLED)
       return
      else:
       SFDmuxerbtn.config(state=tk.NORMAL)
      
      resolution.set(f'{width}:{height}')
      comboboxvres_streamtype1.set(selected_vresvalue)
      master.focus_set()
      vres_streamtype1.selection_clear()
     except ValueError:
      pass


  if selected_vresvalue == "Same As Video":
   comboboxvres_streamtype1.set(OPTIONS_VRes_streamtype1[0])
   comboboxvres_streamtype1.set("Same As Video")
   resolution.set("")
   vres_streamtype1.selection_clear()
  elif selected_vresvalue == "128 x 128":
   comboboxvres_streamtype1.set(OPTIONS_VRes_streamtype1[1])
   resolution.set('128:128')
   vres_streamtype1.selection_clear()
  elif selected_vresvalue == "160 x 128":
   comboboxvres_streamtype1.set(OPTIONS_VRes_streamtype1[2])
   resolution.set('160:128')
   vres_streamtype1.selection_clear()
  elif selected_vresvalue == "320 x 240":
   comboboxvres_streamtype1.set(OPTIONS_VRes_streamtype1[3])
   resolution.set('320:240')
   vres_streamtype1.selection_clear()
  elif selected_vresvalue == "256 x 256":
   comboboxvres_streamtype1.set(OPTIONS_VRes_streamtype1[3])
   resolution.set('256:256')
   vres_streamtype1.selection_clear()
  elif selected_vresvalue == "480 x 336":
   comboboxvres_streamtype1.set(OPTIONS_VRes_streamtype1[4])
   resolution.set('480:336')
   vres_streamtype1.selection_clear()
  elif selected_vresvalue == "320 x 480":
   comboboxvres_streamtype1.set(OPTIONS_VRes_streamtype1[5])
   resolution.set('320:480')
   vres_streamtype1.selection_clear()
  elif selected_vresvalue == "640 x 480":
   comboboxvres_streamtype1.set(OPTIONS_VRes_streamtype1[6])
   resolution.set('640:480')
   vres_streamtype1.selection_clear()
 vres_streamtype1.bind("<<ComboboxSelected>>", updatevres_streamtype1)
 vres_streamtype1.bind("<Leave>", updatevres_streamtype1)  #<Leave> will make it so when the combobox is unfocused/user is clicked off of it (master.focus_set() used above), it will run the update command
 #vres_streamtype1.bind("<KeyRelease>", master.after(2000, updatevres_streamtype1))  #Delay updating the command so that user has time to enter a custom resolution


 OPTIONS_VRatio_streamtype1 = ["Crop to Resolution", "Squish to Resolution", "Scale to Resolution"]
 comboboxvratio_streamtype1 = StringVar()
 vratiobox_streamtype1 = ttk.Combobox(master, value=OPTIONS_VRatio_streamtype1, textvariable=comboboxvratio_streamtype1, width=18)
 vratiobox_streamtype1.place(x=451, y=257)
 vratiobox_streamtype1.current(1)
 vratiobox_streamtype1.state(["readonly"])

 def updatevratio_streamtype1(*args):
  selected_vratiovalue_streamtype1 = comboboxvratio_streamtype1.get()
  updatevres_streamtype1() #Run this to get most updated resolution value selected in the Video Resolution combobox
  global output_resolutionwidth
  output_resolutionwidth = resolution.get().split(":")[0]

  if selected_vratiovalue_streamtype1 == "Crop to Resolution" and V1_enabled_int_vratio.get() == 1:
   comboboxvratio_streamtype1.set(OPTIONS_VRatio_streamtype1[0])
   vratio.set(f'-vf "crop={resolution.get()}"')
   vratiobox_streamtype1.selection_clear()
  elif selected_vratiovalue_streamtype1 == "Squish to Resolution" and V1_enabled_int_vratio.get() == 1:
   comboboxvratio_streamtype1.set(OPTIONS_VRatio_streamtype1[1])
   vratio.set(f'-vf "scale={resolution.get()},setsar=1/2"')
   vratiobox_streamtype1.selection_clear()
  elif selected_vratiovalue_streamtype1 == "Scale to Resolution" and V1_enabled_int_vratio.get() == 1:
   comboboxvratio_streamtype1.set(OPTIONS_VRatio_streamtype1[2])
   vratio.set(f'-vf "scale={output_resolutionwidth}:-1,pad={resolution.get()}:(ow-iw)/2:(oh-ih)/2"')
   vratiobox_streamtype1.selection_clear()
 vratiobox_streamtype1.bind("<<ComboboxSelected>>", updatevratio_streamtype1)
 vratiobox_streamtype1.bind("<KeyRelease>", updatevratio_streamtype1)






 #Muxer Selector
 OPTIONS_streamtype = ["Select a muxer:", "V1 (SFDMUX V1.0.0)", "V1 (SFDMUX V1.0.1b)", "V1 (SFDMUX V1.07)", "V1 (nebulas-star's muxer)", "V1 (CRAFT, V2.98)", "V2 (muxer by ThisKwasior)"]
 #OPTIONS_streamtype = ["No muxer (create converted files)", "V1 (SFDMUX V1.0.0)", "V1 (SFDMUX V1.0.1b)", "V1 (SFDMUX V1.07)", "V1 (nebulas-star's muxer)", "V1 (CRAFT, V2.98)", "V2", "Use External Muxer"]
 comboboxstreamtype = StringVar()
 streamtypebox = ttk.Combobox(master, value=OPTIONS_streamtype, textvariable=comboboxstreamtype, width=23)
 streamtypebox.place(x=421, y=302)
 streamtypebox.current(0)
 streamtypebox.state(["readonly"])

 def update_streamtype(*args):
  selected_streamtypevalue = comboboxstreamtype.get()
  #if selected_streamtypevalue == "No muxer (only create converted files)":
  if selected_streamtypevalue == "Select a muxer:":
   comboboxstreamtype.set(OPTIONS_streamtype[0])
   sofdecstreamtype.set("0")
   streamtypebox.selection_clear()
  elif selected_streamtypevalue == "V1 (SFDMUX V1.0.0)":
   comboboxstreamtype.set(OPTIONS_streamtype[1])
   sofdecstreamtype.set("1")
   streamtypebox.selection_clear()
  elif selected_streamtypevalue == "V1 (SFDMUX V1.0.1b)":
   comboboxstreamtype.set(OPTIONS_streamtype[2])
   sofdecstreamtype.set("2")
   streamtypebox.selection_clear()
  if selected_streamtypevalue == "V1 (SFDMUX V1.07)":
   comboboxstreamtype.set(OPTIONS_streamtype[3])
   sofdecstreamtype.set("3")
   updatemenu_for_streamtype1()
   streamtypebox.selection_clear()
  elif selected_streamtypevalue == "V1 (nebulas-star's muxer)":
   comboboxstreamtype.set(OPTIONS_streamtype[4])
   sofdecstreamtype.set("4")
   streamtypebox.selection_clear()
  elif selected_streamtypevalue == "V1 (CRAFT, V2.98)":
   comboboxstreamtype.set(OPTIONS_streamtype[5])
   sofdecstreamtype.set("5")
   updatemenu_for_streamtype1()
   streamtypebox.selection_clear()
  if selected_streamtypevalue == "V2 (muxer by ThisKwasior)":
   comboboxstreamtype.set(OPTIONS_streamtype[6])
   sofdecstreamtype.set("6")
   streamtypebox.selection_clear()
  if selected_streamtypevalue == "Use External Muxer":
   comboboxstreamtype.set(OPTIONS_streamtype[7])
   sofdecstreamtype.set("7")
   show_externalSFDmuxerwin()
   streamtypebox.selection_clear()
 streamtypebox.bind("<<ComboboxSelected>>", update_streamtype)
 sofdecstreamtype.set('0')


 def update_menu_when_muxer_selected(*args):
  selected_streamtypevalue = comboboxstreamtype.get()
  if selected_streamtypevalue == "Select a muxer:":
   vratiobox.config(state=tk.DISABLED)
   vres.config(state=tk.DISABLED)
   videobitrateentry.config(state=tk.DISABLED)
   vframerate.config(state=tk.DISABLED)
   sofdecstreamtype.set('0')
   update_streamtype()
   updatemenu_for_streamtype1()
  else:
   update_streamtype()
   updatemenu_for_streamtype1()  #Call to update the menu to V1 settings if V1 option selected
   vratiobox.config(state=tk.NORMAL)
   vres.config(state=tk.NORMAL)
   videobitrateentry.config(state=tk.NORMAL)
   vframerate.config(state=tk.NORMAL)
   enable_video_scale_options()
 streamtypebox.bind("<<ComboboxSelected>>", update_menu_when_muxer_selected)
 update_menu_when_muxer_selected()  #Run intially



def useexternalSFDmuxer():
 global externalSFDmuxer_window
 externalSFDmuxer_window = Toplevel(master)
 externalSFDmuxer_window.geometry("250x355"), externalSFDmuxer_window.title("External SFD Muxer Window"), externalSFDmuxer_window.resizable(False, False)
 #externalSFDmuxer_window.geometry("250x375")
 
 externalcustommuxer_file_list = StringVar()
 def choosemuxer_files():
  muxer_selected_files_list = []
  global external_sfdmuxer
  external_sfdmuxer = filedialog.askopenfilenames(title='Choose an SFD muxer (+ any other files it requires)')
  for files in external_sfdmuxer:
   files_name = os.path.basename(files)
   muxer_selected_files_list.append(files_name)
  externalcustommuxer_file_list.set(", ".join(muxer_selected_files_list))
  print(f"Files selected (for external muxer): {externalcustommuxer_file_list.get()}")
  print("")
  externalSFDmuxer_window.focus()


 global useexternalsfdmuxer
 useexternalsfdmuxer = IntVar()
 choosemuxer_filesbtn = Button(externalSFDmuxer_window, text="Choose Muxer Files", command=choosemuxer_files, padx=37, pady=2)
 choosemuxer_filesbtn.place(x=32.5, y=32)

 custommuxer_videoformatlabel = Label(externalSFDmuxer_window, text="Video Format:", font=("Arial Bold", 8)).place(x=27, y=75)
 OPTIONS_externalmuxer_videoformat = ["MPEG", "M1V", "Other (please specify)"]
 externalmuxer_videoformat = StringVar()
 externalmuxer_videoformatcombobox = ttk.Combobox(externalSFDmuxer_window, value=OPTIONS_externalmuxer_videoformat, textvariable=externalmuxer_videoformat, width=20)
 externalmuxer_videoformatcombobox.place(x=30, y=93)

 custommuxer_audioformatlabel = Label(externalSFDmuxer_window, text="Audio Format:", font=("Arial Bold", 8)).place(x=27, y=125)
 OPTIONS_externalmuxer_audioformat = ["ADX", "SFA", "Other (please specify)"]
 externalmuxer_audioformat = StringVar()
 externalmuxer_audioformatcombobox = ttk.Combobox(externalSFDmuxer_window, value=OPTIONS_externalmuxer_audioformat, textvariable=externalmuxer_audioformat, width=20)
 externalmuxer_audioformatcombobox.place(x=30, y=143)

 custommuxer_commandlabel = Label(externalSFDmuxer_window, text="Muxer Command:", font=("Arial Bold", 8)).place(x=27, y=175)
 externalmuxer_command = StringVar()
 externalmuxer_command_combobox = ttk.Entry(externalSFDmuxer_window, textvariable=externalmuxer_command, width=30)
 externalmuxer_command_combobox.place(x=30, y=193)

 def enable_chosemuxer_filesbtn(*args):
  if useexternalsfdmuxer.get() == 1:
    choosemuxer_filesbtn.config(state=tk.NORMAL)
    externalmuxer_audioformatcombobox.config(state=tk.NORMAL)
    externalmuxer_videoformatcombobox.config(state=tk.NORMAL)
    externalmuxer_command_combobox.config(state=tk.NORMAL)
    comboboxstreamtype.set('External Muxer Enabled')
    comboboxstreamtype.set(OPTIONS_streamtype[7])
    streamtypebox.config(state=tk.DISABLED)
    sofdecstreamtype.set('7')
    updatemenu_for_streamtype1()
  if useexternalsfdmuxer.get() == 0:
    choosemuxer_filesbtn.config(state=tk.DISABLED)
    externalmuxer_audioformatcombobox.config(state=tk.DISABLED)
    externalmuxer_videoformatcombobox.config(state=tk.DISABLED)
    externalmuxer_command_combobox.config(state=tk.DISABLED)
    
    #Reset back to "Select a muxer:" (default)
    sofdecstreamtype.set('0')
    comboboxstreamtype.set(OPTIONS_streamtype[0])
    streamtypebox.config(state=tk.NORMAL)
    updatemenu_for_streamtype1()
    externalcustommuxer_file_list.set("") #Reset muxer files list
 useexternalsfdmuxer.trace('w', enable_chosemuxer_filesbtn)


 enable_externalSFDmuxer_check = ttk.Checkbutton(externalSFDmuxer_window, text='Enable external SFD muxer', command=enable_chosemuxer_filesbtn(), variable=useexternalsfdmuxer, onvalue=1, offvalue=0)
 enable_externalSFDmuxer_check.place(x=40, y=6)
 enable_externalSFDmuxer_check.bind("<<CheckboxSelected>>", enable_chosemuxer_filesbtn)
 enable_externalSFDmuxer_check.bind("<<CheckboxDeselected>>", enable_chosemuxer_filesbtn)

 custommuxer_note1label = Label(externalSFDmuxer_window, text="Note: In the muxer command section, use the following values/names for the video, audio, and SFD filenames:", wraplength=240, font = ("Arial Bold", 8)).place(x=5, y=225)
 custommuxer_note1blabel = Label(externalSFDmuxer_window, text="Video = newvideo (+ extension selected above)", wraplength=250, font=("Arial", 8)).place(x=5, y=275)
 custommuxer_note1clabel = Label(externalSFDmuxer_window, text="Audio = trackX (where X is a number between 1 and 4, + extension selected above)", wraplength=250, font=("Arial", 8)).place(x=5, y=295)
 custommuxer_note1clabel = Label(externalSFDmuxer_window, text="Output SFD name = file.sfd", wraplength=250, font=("Arial", 8)).place(x=5, y=330)


 externalSFDmuxer_window.withdraw() #Hide window on boot


def usecustomFFmpegcommands():
 global usecustomFFmpegcommandswin
 usecustomFFmpegcommandswin = Toplevel(master)
 usecustomFFmpegcommandswin.geometry("550x355"), usecustomFFmpegcommandswin.title("Custom FFmpeg Command Window"), usecustomFFmpegcommandswin.resizable(False, False)
 #externalSFDmuxer_window.geometry("250x375")


 usecustomFFmpegcommandswin.withdraw() #Hide window on boot


def advancedopt():
  global optwin
  global crfvalue
  crfvalue = StringVar()
  global usebitexact
  usebitexact = IntVar()
  
  optwin = Toplevel(master)
  optwin.geometry("600x400"), optwin.title("Extra Options"), optwin.resizable(False, False)
  ffmpegsettingsframe = LabelFrame(optwin, text="Additional FFmpeg Settings").place(relx=0.010, rely=0.005, relheight=0.460, relwidth=0.983)
  qualitysettings = LabelFrame(optwin, text="QoL Settings").place(relx=0.010, rely=0.485, relheight=0.225, relwidth=0.41)
  miscprogramsettingsframe = LabelFrame(optwin, text="Misc. Program Settings").place(relx=0.43, rely=0.485, relheight=0.225, relwidth=0.561)
  keepframe = LabelFrame(optwin, text="Keep File(s)").place(relx=0.010, rely=0.73, relheight=0.26, relwidth=0.41)


  def keepfiles_options_extraoptionswindow():
   AVI = ttk.Checkbutton(optwin, text='Keep converted AVI file', variable=keepAVI, onvalue=1, offvalue=0).place(x=11, y=310)
   MPEG = ttk.Checkbutton(optwin, text='Keep converted MPEG file', variable=keepMPEG, onvalue=1, offvalue=0).place(x=11, y=330)
   ADX = ttk.Checkbutton(optwin, text='Keep converted ADX/SFA file(s)', variable=keepADX, onvalue=1, offvalue=0).place(x=11, y=350)
   log = ttk.Checkbutton(optwin, text='Keep sfdmux log file', variable=keepsfdmuxlog, onvalue=1, offvalue=0).place(x=11, y=370)



  def FFmpegsettings_extraoptionswindow():
   crfentry = ttk.Entry(optwin, textvariable=crfvalue, width=12)
   crfentry.insert(0, "")
   crfentry.place(x=11, y=41)
   crflbl = Label(optwin, text="CRF Value:", font=("Arial Bold", 8)).place(x=8, y=21)
   if crfentry.get() == '':
    crfentry.insert(0, "01")

   
   #Checkbox toggles
   useidenticalcustomdurations = IntVar()
   useidenticalcustomdurations_check = ttk.Checkbutton(optwin, text='Use custom video duration for audio', variable=useidenticalcustomdurations, onvalue=1, offvalue=0)
   useidenticalcustomdurations_check.place(x=11, y=70)

   bitexactcheck = ttk.Checkbutton(optwin, text='Use -bitexact for audio', variable=usebitexact, onvalue=1, offvalue=0).place(x=11, y=90)

   global enableKVCD_int   #Set as global to prevent auto enabled issue
   enableKVCD_int = IntVar()
   enableKVCDcheck = ttk.Checkbutton(optwin, text='Enable KVCD quantization', variable=enableKVCD_int, onvalue=1, offvalue=0).place(x=11, y=110)

   global useHQM1Vcommands_int
   useHQM1Vcommands_int = IntVar()
   #useHQ_m1v_commandscheck = ttk.Checkbutton(optwin, text='Enable HQ M1V video commands', variable=useHQM1Vcommands_int, onvalue=1, offvalue=0).place(x=11, y=130)

   global enable2PassEncoding_int  #Set as global to prevent auto enabled issue
   enable2PassEncoding_int = IntVar()
   #enable2PassEncodingcheck = ttk.Checkbutton(optwin, text='Enable 2-pass encoding', variable=enable2PassEncoding_int, onvalue=1, offvalue=0).place(x=11, y=150)



 
   #Audio options
   audbitrateselect = Label(optwin, text="Audio Bitrate:", font = ("Arial Bold", 8)).place(x=244, y=90)
   audiobitrateentry = ttk.Entry(optwin, textvariable=abitrate, width=12)
   audiobitrateentry.insert(0, "320k")
   audiobitrateentry.place(x=245, y=110)

   audhzselect = Label(optwin, text="Audio Sample Rate:", font = ("Arial Bold", 8)).place(x=337, y=90)
   audiohzentry = ttk.Entry(optwin, textvariable=aHz, width=17)
   audiohzentry.insert(0, "44100")
   audiohzentry.place(x=340, y=110)

   audchannelselect = Label(optwin, text="# of Audio Channels:", font = ("Arial Bold", 8)).place(x=457, y=90)
   OPTIONS_AChannel = ["Stereo (2 Channels)", "Mono (1 Channel)"]
   comboboxchannel = StringVar()
   achannelbox = ttk.Combobox(optwin, value=OPTIONS_AChannel, textvariable=comboboxchannel, width=17)
   achannelbox.place(x=460, y=110)
   achannelbox.current(0)
   achannelbox.state(["readonly"])

   def update_achannel(event):
    selected_achannelvalue = comboboxchannel.get()
    if selected_achannelvalue == "Stereo (2 Channels)":
     comboboxchannel.set(OPTIONS_AChannel[0])
     audiochannel.set("-ac 2")
     achannelbox.selection_clear()
    elif selected_achannelvalue == "Mono (1 Channel)":
     comboboxchannel.set(OPTIONS_AChannel[1])
     audiochannel.set("-ac 1")
     achannelbox.selection_clear()
   achannelbox.bind("<<ComboboxSelected>>", update_achannel)



   #Video/Audio duration settings
   def toggledurationentriesstate():
    if enablevideoffmpegduration.get() == 1:
     videostarttimeentry.config(state=tk.NORMAL)
     videoendtimeentry.config(state=tk.NORMAL)
    else:
     videostarttimeentry.config(state=tk.DISABLED)
     videoendtimeentry.config(state=tk.DISABLED)

   global enablevideoffmpegduration
   enablevideoffmpegduration = IntVar()
   enablecustomdurationcheck = ttk.Checkbutton(optwin, text='Use custom video duration', variable=enablevideoffmpegduration, command=toggledurationentriesstate, onvalue=1, offvalue=0)
   enablecustomdurationcheck.place(x=244, y=18)

   durationstarttimelbl = Label(optwin, text="Start Time:", font=("Arial Bold", 8)).place(x=242, y=40)
   durationendtimelbl = Label(optwin, text="Clip Length:", font=("Arial Bold", 8)).place(x=326, y=40)

   global videostarttimedurationvalue
   global videoendtimedurationvalue
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

   global enableaudioffmpegduration
   global audiostarttimedurationvalue
   global audioendtimedurationvalue
   enableaudioffmpegduration = IntVar()
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

   #def enable_same_custom_duration_checkbox(*args):
    #if enableaudioffmpegduration.get() == 1 and enablevideoffmpegduration.get() == 1:
     #useidenticalcustomdurations_check.config(state=tk.NORMAL)
    #else:
     #useidenticalcustomdurations_check.config(state=tk.DISABLED)
   #enableaudiocustomdurationcheck.bind("w", enable_same_custom_duration_checkbox)
   #enable_same_custom_duration_checkbox()  #Call on boot

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



  def QoL_settings_extraoptionswindow():
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
   autoinput_audiofromvideo.place(x=11, y=215)

   global setoutputdirectorytovideodirectory
   setoutputdirectorytovideodirectory = IntVar()
   setoutputdirectorytovideodirectorycheck = ttk.Checkbutton(optwin, text='Use video directory for output directory', variable=setoutputdirectorytovideodirectory, onvalue=1, offvalue=0)
   setoutputdirectorytovideodirectorycheck.place(x=11, y=235)

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
   setSFDfilenametovideofilenamecheck.place(x=11, y=255)

   global UsevideonameforSFD
   def UsevideonameforSFD(*args): 
    if setSFDfilenametovideofilename.get() == 1:
     videofilename = os.path.basename(filePathvideo.get())
     videofilename_noextension = os.path.splitext(videofilename)[0]
     SFDfilename.set(videofilename_noextension)
    if setSFDfilenametovideofilename.get() == 0:
     SFDfilename.set('')
   setSFDfilenametovideofilename.trace('w', UsevideonameforSFD)

   #global createsfdtofolder
   #createsfdtofolder = IntVar()
   #createsfdtofoldercheck = ttk.Checkbutton(optwin, text='Create SFD to folder', variable=createsfdtofolder, onvalue=1, offvalue=0)
   #createsfdtofoldercheck.place(x=11, y=275)



  def misc_program_options_extraoptionswindow():
   global enableaudiopadding
   enableaudiopadding = IntVar()
   enableaudiopaddingcheck = ttk.Checkbutton(optwin, text='Enable audio padding for: ', variable=enableaudiopadding, onvalue=1, offvalue=0)
   enableaudiopaddingcheck.place(x=264, y=215)

   def enable_tracks_to_fill_combobox(*args):
    if enableaudiopadding.get() == 1:
     paddingaudio_tracks_to_fill_comboxbox.config(state=tk.NORMAL)
    else:
     paddingaudio_tracks_to_fill_comboxbox.config(state=tk.DISABLED)
   enableaudiopadding.trace("w", enable_tracks_to_fill_combobox)

   global paddingaudio_tracks_to_fill_comboxbox
   OPTIONS_audiopadding_tracks_to_fill = ["All tracks w/out audio", "Track 1", "Track 2", "Track 3", "Track 4", "Track 1 + 2", "Track 1 + 3", "Track 1 + 4", "Track 2 + 3", "Track 2 + 4", "Track 3 + 4"]
   paddingaudio_tracks_to_fill_comboxbox = ttk.Combobox(optwin, value=OPTIONS_audiopadding_tracks_to_fill, width=20)
   paddingaudio_tracks_to_fill_comboxbox.place(x=427, y=214)
   paddingaudio_tracks_to_fill_comboxbox.config(state=tk.DISABLED)  #Disabled until enableaudiopadding == 1
   paddingaudio_tracks_to_fill_comboxbox.current(0)

   global addaudiotracks
   addaudiotracks = IntVar()

   global aud2select
   aud2select = Label(dirframe, text="Audio for Track 2:", font = ("Arial Bold", 8))

   global moreaudiotracks
   moreaudiotracks = Button(text="Additional Audio Tracks", command=show_extraaudiotrackswin, padx=10, pady=3)

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

   if addaudiotracks.get() == 0:  #set place positions on program boot
    entryaud2.place(x=5, y=95.8)
    aud2select.place(x=3, y=76.499999999999992)
    moreaudiotracks.place_forget()
    browseaud2.place(x=455, y=105)


   addaudiotrackscheck = ttk.Checkbutton(optwin, text='Enable additional audio tracks', variable=addaudiotracks, command=showaudiotracksbutton, onvalue=1, offvalue=0)
   addaudiotrackscheck.place(x=264, y=235)

   global showffmpegcommands
   showffmpegcommands = IntVar()
   showffmpegcommandscheck = ttk.Checkbutton(optwin, text='Print program output to CMD window', variable=showffmpegcommands, onvalue=1, offvalue=0)
   showffmpegcommandscheck.place(x=264, y=255)
   showffmpegcommands.set(0)


   #Misc Other Options/Settings
   #useexternalsfdmuxerbtn = Button(optwin, text="Use external SFD muxer", command=show_externalSFDmuxerwin, padx=24.35, pady=1).place(x=263, y=295)
   #customffmpegcommandsbtn = Button(optwin, text="Use custom FFmpeg commands", command=show_customFFmpegcommandwin, padx=1, pady=1).place(x=263, y=325)


  #Load settings
  keepfiles_options_extraoptionswindow()
  FFmpegsettings_extraoptionswindow()
  QoL_settings_extraoptionswindow()
  misc_program_options_extraoptionswindow()
  optwin.withdraw() #Hide window on boot


def openpresetwindow():
 global presetwindow
 presetwindow = Toplevel(master)
 presetwindow.geometry("360x100"), presetwindow.title("Preset Window"), presetwindow.resizable(False, False)

 def update_filePathpreset(*args):
  filePathpreset.set(currentdir + '/preset/' + presetselector.get())

 filePathpreset = StringVar()
 presetfolder = os.getcwd() + '/preset'
 presetfiles_list = [file for file in os.listdir(presetfolder) if file.endswith('.txt')]
 presetselector = ttk.Combobox(presetwindow, values=presetfiles_list, width=30)
 presetselector.place(x=5, y=15)  #Keep seperate to avoid NoneType error
 presetselector.bind("<<ComboboxSelected>>", update_filePathpreset)
 
 
 def openpreset():
  preset = filedialog.askopenfilename(title="Select A Preset File", filetypes=[("Preset files", ".txt")], initialdir=presetfolder)
  filePathpreset.set(preset)
  presetselector.set(os.path.basename(preset))
  presetwindow.focus() #Bring window to front after the filedialog is done
  presetwindow.focus_set()


 def applypreset():
  if not filePathpreset.get():
   print("Error: No/Invalid file path provided for preset file.")
   return
  else:
   try:
    with open(filePathpreset.get(), 'r') as presetfile:
     presetfile_lines = presetfile.readlines()

     #Remember to minus 1 off of each number compared to preset file, since this starts at 0.

     #Get SFD muxer first to determine which settings (V2 or V1 settings) to use
     sfdmuxer_readpreset = presetfile_lines[11].split('=')[1]
     if sfdmuxer_readpreset == 'N/A':
       pass
     else:
      #Update menu for V1 encoding if SFDmuxer equals 2 or 4
      if int(sfdmuxer_readpreset) == 2:  #Call as int or otherwise doesn't work.
        streamtypebox.set("V1 (SFDMUX V1.07)")
      elif int(sfdmuxer_readpreset) == 4:
        streamtypebox.set("V1 (V1.01b w/header patch)")
      update_streamtype()

     #Get SFD muxer first to determine which settings (V2 or V1 settings) to use
     videoresolution_readpreset = presetfile_lines[1].split('=')[1]
     if videoresolution_readpreset == 'N/A':
       pass
     else:
      if int(sfdmuxer_readpreset) == 2 or int(sfdmuxer_readpreset) == 4:  #Check if V1 file to bring up the correct options
       comboboxvres_streamtype1.set(str(videoresolution_readpreset))
       input(f'videoresolution_readpreset: {str(videoresolution_readpreset)}')
       updatevres_streamtype1()
      else:
       videoresolution_list = ["Same as Video", "320x240", "426x240", "480x360", "640x360", "640x480", "848x480", "960x720", "1280x720", "1920x1080", "1440x1080"]
       if not videoresolution_readpreset in videoresolution_list:
        print('s')
       else:
        print('y')


   except Exception as e:
     print("An error occurred:", e)
     

 def createpreset():
  print('makepreset')

 openpresetbtn = Button(presetwindow, text="Open File", command=openpreset, padx=37, pady=2).place(x=220, y=12)
 applypresetbtn = Button(presetwindow, text="Apply Preset", command=applypreset, padx=40, pady=2).place(x=5, y=65)
 createpresetbtn = Button(presetwindow, text="Create New Preset", command=createpreset, padx=38, pady=2).place(x=175, y=65)


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


 extraaudiotrackswin.withdraw() #Hide window on boot


def createSFD():
   cancelcreation.set(0)  #Reset cancelcreation int
   global ffprobe_exe_path #Fix for FFprobe EXE error when not on user's path
   global ffmpeg_location_int
   global ffprobe_location_int
   createSFD_with_noaudio = IntVar()
   FFmpeg_onlyprinterrors_cmd = StringVar()
   videofile = filePathvideo.get()
   audio1_origaudiopath = StringVar()
   audio2_origaudiopath = StringVar()
   audio3_origaudiopath = StringVar()
   audio4_origaudiopath = StringVar()
   audio1_adx = StringVar()
   audio2_adx = StringVar()
   audio3_adx = StringVar()
   audio4_adx = StringVar()
   audio1_sfa = StringVar()
   audio2_sfa = StringVar()
   audio3_sfa = StringVar()
   audio4_sfa = StringVar()
   audio1_sfa_muxercmd = StringVar()
   audio2_sfa_muxercmd = StringVar()
   audio3_sfa_muxercmd = StringVar()
   audio4_sfa_muxercmd = StringVar()

   #Set up audio1_origaudiopath variables
   audio1_origaudiopath.set(filePathaudt1.get())
   audio2_origaudiopath.set(filePathaudt2.get())
   audio3_origaudiopath.set(filePathaudt3.get())
   audio4_origaudiopath.set(filePathaudt4.get())

   if cancelcreation.get() == 1:
    return
     
   if not addaudiotracks.get() == 1 and enableaudiopadding.get() == 0:  #If additional audio tracks is disabled, set the file paths for track 3 and 4 to be blank
    filePathaudt3.set('')
    filePathaudt4.set('')

   def check_foranyerrors_before_SFDcreation_and_set_padding_audio_tracks():
    #Errors
    if SFDfilename.get() == '':
      filenamemissing = tk.messagebox.showerror(title='File Error', message='No filename was inputted for the SFD file. Please go back and input a name for the output SFD file.')
      cleanup_files()
      cancelcreation.set(1)
    if sofdecstreamtype.get() == '0':
      nomuxerselected_error = tk.messagebox.showerror(title='Setting Error', message='No muxer was selected for making the SFD file. Please select a muxer under the "Encode As" menu to continue.')
      cleanup_files()
      cancelcreation.set(1)
    if not enableaudiopadding.get() == 1 and filePathaudt1.get() == '' and filePathaudt2.get() == '' and filePathaudt3.get() == '' and filePathaudt4.get() == '':
      audiorequired = tk.messagebox.showerror(title='No audio tracks selected', message='No audio files were provided for any audio track. Please select at least one audio track, or toggle "Enable audio padding" for a blank/silent track.')
      cleanup_files()
      cancelcreation.set(1)
      
      #Old code for creating SFDs without audio, currently broken
      #audiorequired = tk.messagebox.askyesno(title='No audio tracks selected', message='No audio file(s) were provided for any track. Do you want to create the SFD without any audio?')
      #if audiorequired:
       #createSFD_with_noaudio.set(1)
       #pass
      #else:
       #return
    

    #Check if previous audio tracks are missing audio, print error if so (if enableaudiopadding isn't enabled).
    #First, set up blank/padding files based on the options selected:
    
    #Padding track option numbers, + what int values enableaudiopadding_tracks_to_fill_comboxbox.current() fits for each track
    #["All tracks w/out audio",  0
    #"Track 1",                  1
    #"Track 2",                  2
    #"Track 3",                  3
    #"Track 4",                  4
    #"Track 1 + 2",              5
    #"Track 1 + 3",              6
    #"Track 1 + 4",              7
    #"Track 2 + 3",              8
    #"Track 2 + 4",              9
    #"Track 3 + 4"]              10

    #Track 1 - 0, 1, 5, 6, 7
    #Track 2 - 0, 2, 5, 8, 9
    #Track 3 - 0, 3, 6, 8, 10
    #Track 4 - 0, 4, 7, 9, 10

    #paddingaudio_tracks_to_fill_int = IntVar()
    def set_paddingaudio_tracks_to_fill_int():
     if enableaudiopadding.get() == 1:
      #Track 1
      if paddingaudio_tracks_to_fill_comboxbox.current() == 0 and audio1_origaudiopath.get() == '':
         audio1_origaudiopath.set('blank.adx')
      elif paddingaudio_tracks_to_fill_comboxbox.current() in [1, 5, 6, 7]:
        if not filePathaudt1.get() == '':
         filePathaudt1_already_has_file_fill_with_paddingaudio_question = tk.messagebox.askyesno('File Error', f'Track 1 already has an audio file. The audio padding settings currently selected will result in overwriting this track. Do you want to replace it with padding audio?')
         if filePathaudt1_already_has_file_fill_with_paddingaudio_question == True:
           audio1_origaudiopath.set('blank.adx')
        else:
          audio1_origaudiopath.set('blank.adx')
    

      #Track 2
      if paddingaudio_tracks_to_fill_comboxbox.current() == 0 and audio2_origaudiopath.get() == '':
         audio2_origaudiopath.set('blank.adx')
      elif paddingaudio_tracks_to_fill_comboxbox.current() in [2, 5, 8, 9]:
        if not filePathaudt2.get() == '':
         filePathaudt2_already_has_file_fill_with_paddingaudio_question = tk.messagebox.askyesno('File Error', f'Track 2 already has an audio file. The audio padding settings currently selected will result in overwriting this track. Do you want to replace it with padding audio?')
         if filePathaudt2_already_has_file_fill_with_paddingaudio_question == True:
           audio2_origaudiopath.set('blank.adx')
        else:
          audio2_origaudiopath.set('blank.adx')
    

      #Track 3
      if paddingaudio_tracks_to_fill_comboxbox.current() == 0 and audio3_origaudiopath.get() == '':
         audio3_origaudiopath.set('blank.adx')
      elif paddingaudio_tracks_to_fill_comboxbox.current() in [3, 6, 8, 10]:
        if not filePathaudt3.get() == '':
         filePathaudt3_already_has_file_fill_with_paddingaudio_question = tk.messagebox.askyesno('File Error', f'Track 3 already has an audio file. The audio padding settings currently selected will result in overwriting this track. Do you want to replace it with padding audio?')
         if filePathaudt3_already_has_file_fill_with_paddingaudio_question == True:
           audio3_origaudiopath.set('blank.adx')
        else:
          audio3_origaudiopath.set('blank.adx')
    

      #Track 4
      if paddingaudio_tracks_to_fill_comboxbox.current() == 0 and audio4_origaudiopath.get() == '':
         audio4_origaudiopath.set('blank.adx')
      elif paddingaudio_tracks_to_fill_comboxbox.current() in [4, 7, 9, 10]:
        if not filePathaudt4.get() == '':
         filePathaudt4_already_has_file_fill_with_paddingaudio_question = tk.messagebox.askyesno('File Error', f'Track 4 already has an audio file. The audio padding settings currently selected will result in overwriting this track. Do you want to replace it with padding audio?')
         if filePathaudt4_already_has_file_fill_with_paddingaudio_question == True:
           audio4_origaudiopath.set('blank.adx')
        else:
          audio4_origaudiopath.set('blank.adx')

      #Print which tracks have padding audio enabled, just in case an error occurs
      if audio1_origaudiopath.get() == 'blank.adx':
       print("Track 1 set to padding audio.")

      if audio2_origaudiopath.get() == 'blank.adx':
       print("Track 2 set to padding audio.")

      if audio3_origaudiopath.get() == 'blank.adx':
       print("Track 3 set to padding audio.")

      if audio4_origaudiopath.get() == 'blank.adx':
       print("Track 4 set to padding audio.")

   

    if cancelcreation.get() == 1:
     return
    set_paddingaudio_tracks_to_fill_int()  #Run this to get the padding audio tracks set up
    if cancelcreation.get() == 1:
     return


    #If padding audio is NOT enabled, and track is empty, set to empty string
    if not enableaudiopadding.get() == 1 and filePathaudt1.get() == '':
     audio1_origaudiopath.set('')
    if not enableaudiopadding.get() == 1 and filePathaudt2.get() == '':
     audio2_origaudiopath.set('')
    if not enableaudiopadding.get() == 1 and filePathaudt3.get() == '':
     audio3_origaudiopath.set('')
    if not enableaudiopadding.get() == 1 and filePathaudt4.get() == '':
     audio4_origaudiopath.set('')



    print_missingaudiotrack_error_int = IntVar()
    missingtrack_errornote = StringVar()

    def print_missing_track_error_function():
      if print_missingaudiotrack_error_int.get() == 1:
       filenamemissing = tk.messagebox.showerror(title='Audio Track Error', message=f'{missingtrack_errornote.get()}')
       cleanup_files()
       cancelcreation.set(1)
       return
      else:
       pass

    #No track 1 check, since if the only audio is in track 1, it's fine.
    #Check + write error for previous tracks in Track 2
    if not audio2_origaudiopath.get() == '' and audio1_origaudiopath.get() == '':
      missingtrack_errornote.set('No audio file is present in track 1, but audio is present in track 2.\n\nPlease either move the audio in track 2 to track 1, or toggle "Enable audio padding" in the Extra Options menu to fill any empty tracks with blank audio.')
      print_missingaudiotrack_error_int.set(1)


    #Check + write error for previous tracks in Track 3
    if not audio3_origaudiopath.get() == '':
       if audio1_origaudiopath.get() == '' and audio2_origaudiopath.get() == '':
        missingtrack_errornote.set('No audio files are present in track 1 or 2, but audio is present in track 3.\n\nPlease either move the audio in track 3 to track 1, or toggle "Enable audio padding" in the Extra Options menu to fill any empty tracks with blank audio.')
        print_missingaudiotrack_error_int.set(1)

       elif audio2_origaudiopath.get() == '':
        missingtrack_errornote.set('No audio file is present in track 2, but audio is present in track 1 and 3.\n\nPlease either move the audio in track 3 to track 2, or toggle "Enable audio padding" in the Extra Options menu to fill any empty tracks with blank audio.')
        print_missingaudiotrack_error_int.set(1)
       elif audio1_origaudiopath.get() == '':
        missingtrack_errornote.set('No audio file is present in track 1, but audio is present in track 2 and 3.\n\nPlease either move all the audio up one track, or toggle "Enable audio padding" in the Extra Options menu to fill any empty tracks with blank audio.')
        print_missingaudiotrack_error_int.set(1)


    #Check + write error for previous tracks in Track 4
    if not audio4_origaudiopath.get() == '':
       #Missing track 1, 2 and 3
       if audio3_origaudiopath.get() == '' and audio2_origaudiopath.get() == '' and audio1_origaudiopath.get() == '':
        missingtrack_errornote.set('No audio files are present in track 1, 2, or 3, but audio is present in track 4.\n\nPlease either move the audio in track 4 to track 1, or toggle "Enable audio padding" in the Extra Options menu to fill any empty tracks with blank audio.')
        print_missingaudiotrack_error_int.set(1)

       #Missing track 2 and 3
       if audio3_origaudiopath.get() == '' and audio2_origaudiopath.get() == '':
        missingtrack_errornote.set('No audio files are present in track 2 or 3, but audio is present in track 1 and 4.\n\nPlease either move the audio in track 2 to track 1, or toggle "Enable audio padding" in the Extra Options menu to fill any empty tracks with blank audio.')
        print_missingaudiotrack_error_int.set(1)

       #Missing track 1 and 3
       if audio3_origaudiopath.get() == '' and audio1_origaudiopath.get() == '':
        missingtrack_errornote.set('No audio files are present in track 1 or 3, but audio is present in track 2 and 4.\n\nPlease either move all the audio tracks up one slot, or toggle "Enable audio padding" in the Extra Options menu to fill any empty tracks with blank audio, in the case you need audio in specific tracks.')
        print_missingaudiotrack_error_int.set(1)

       #Missing track 1 + 2
       elif audio1_origaudiopath.get() == '' and audio2_origaudiopath.get() == '':
        missingtrack_errornote.set('No audio files are present in track 1 or 2, but audio is present in track 3 and 4.\n\nPlease either move the audio in track 3 and 4 to track 1 and 2, or toggle "Enable audio padding" in the Extra Options menu to fill any empty tracks with blank audio.')
        print_missingaudiotrack_error_int.set(1)
       
       #Missing only track 3
       elif audio3_origaudiopath.get() == '':
        missingtrack_errornote.set('No audio file is present in track 3, but audio is present in track 1, 2, and 4.\n\nPlease either move the audio in track 4 to track 3, or toggle "Enable audio padding" in the Extra Options menu to fill any empty tracks with blank audio.')
        print_missingaudiotrack_error_int.set(1)
       
       #Missing only track 2
       elif audio2_origaudiopath.get() == '':
         missingtrack_errornote.set('No audio file is present in track 2, but audio is present in track 1, 3, and 4.\n\nPlease either move the audio in track 4 to track 3, or toggle "Enable audio padding" in the Extra Options menu to fill any empty tracks with blank audio.')
         print_missingaudiotrack_error_int.set(1)
       
       #Missing only track 1
       elif audio1_origaudiopath.get() == '':
        missingtrack_errornote.set('No audio file is present in track 1, but audio is present in track 2, 3, and 4.\n\nPlease either move all the audio up one track, or toggle "Enable audio padding" in the Extra Options menu to fill any empty tracks with blank audio.')
        print_missingaudiotrack_error_int.set(1)

    if print_missingaudiotrack_error_int.get() == 1:
      print_missing_track_error_function()
      return


    if os.path.isfile(dirPath.get() + '/' + SFDfilename.get() + '.sfd'):
     sfdalreadyexists_messagebox = tk.messagebox.askyesno(title='File Error', message='An SFD file with the same name already exists in the output directory. Do you want to overwrite it?')
     if sfdalreadyexists_messagebox:
      os.remove(dirPath.get() + '/' + SFDfilename.get() + '.sfd')
      pass
     else:
      print("SFD creation cancelled, SFD will not be overwritten.")
      cleanup_files()
      cancelcreation.set(1)
    
    videofile = filePathvideo.get()
    if not os.path.exists(StringVar.get(filePathvideo)):
      videomissing = tk.messagebox.showerror(title='File Error', message="No video file was selected, or the file doesn't exist in the given path. Please select a video file to continue.")
      cleanup_files()
      cancelcreation.set(1)
    if not os.path.exists(dirPath.get()):
      tk.messagebox.showerror(title='Directory Error', message="Can't find the directory selected. Try again, or select a different directory.")
      cleanup_files()
      cancelcreation.set(1)
   
    if enablevideoffmpegduration.get() == 1 and videostarttimedurationvalue.get() == '':
      tk.messagebox.showerror(title='FFmpeg Duration Error', message="To use a custom video duration, you must input both the length of the clip and the start time of the clip into their respective boxes. Please enter the time you want the video to start in the first box to continue, or disable the custom duration checkbox.")
      cleanup_files()
      cancelcreation.set(1)
    if enablevideoffmpegduration.get() == 1 and videoendtimedurationvalue.get() == '':
      tk.messagebox.showerror(title='FFmpeg Duration Error', message="To use a custom video duration, you must input both the length of the clip and the start time of the clip into their respective boxes. Please enter the length you want the video in the second box to be to continue, or disable the custom duration checkbox.")
      cleanup_files()
      cancelcreation.set(1)
    if enablevideoffmpegduration.get() == 1 and videostarttimedurationvalue.get() == '' and videoendtimedurationvalue.get() == '':
      tk.messagebox.showerror(title='FFmpeg Duration Error', message="No values were inputed for a custom duration. Please disable the custom duration checkbox to continue, or input values into the proper boxes.")
      cleanup_files()
      cancelcreation.set(1)

   if cancelcreation.get() == 1:
     return
   check_foranyerrors_before_SFDcreation_and_set_padding_audio_tracks()
   if cancelcreation.get() == 1:
    return


   HQM1Vcommands = StringVar()
   KVCD_cmd = StringVar()
   def setupforSFDcreation():
    #remove ".sfd" if it was included on SFDfilename
    if SFDfilename.get().endswith(".sfd"):
      SFDfilename.set(SFDfilename.get()[:-4])

    #Set ffmpeg command properly if it's on the user's PATH
    global ffmpeg_exe_path
    global ffprobe_exe_path
    if ffmpeg_location_int.get() == 1:
      ffmpeg_exe_path = 'ffmpeg.exe'
    else:
      ffmpeg_exe_path = currentdir + '/resource/bin/ffmpeg/ffmpeg.exe'
    if ffprobe_location_int.get() == 1:
      ffprobe_exe_path = 'ffprobe.exe'
    else:
      ffprobe_exe_path = currentdir + '/resource/bin/ffmpeg/ffprobe.exe'


    #Fix framerate if it's set to Same as Video
    if framerate.get() == 'Same as Video':
      framerate.set('')
    if comboboxframerate.get() == 'Same as Video':
      framerate.set('')
    if comboboxframerate.get() == '-r Same as Video':
      framerate.set('')
    if framerate.get() == '-r Same as Video':
      framerate.set('')

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

    if useHQM1Vcommands_int.get() == 1:
     HQM1Vcommands.set('-bf 0 -g 1 -b:v')
    else:
     HQM1Vcommands.set('')

    if enableKVCD_int.get() == 1:
     KVCD_cmd.set('-intra_matrix "8,16,19,22,26,27,29,34,16,16,22,24,27,29,34,37,19,22,26,27,29,34,34,38,22,22,26,27,29,34,37,40,22,26,27,29,32,35,40,48,26,27,29,32,35,40,48,58,26,27,29,34,38,46,56,69,27,29,35,38,46,56,69,83" -inter_matrix "16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16"')


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


    global subprocessoptions
    subprocess_runcommand = StringVar()
    if showffmpegcommands.get() == 1:
     subprocess_runcommand.set('{"stderr": subprocess.STDOUT, "shell": True}')
    else:
     subprocess_runcommand.set('{"creationflags": subprocess.CREATE_NO_WINDOW, "shell": True, "capture_output": True, "text": True}')
    subprocessoptions = eval(subprocess_runcommand.get())
   
   if cancelcreation.get() == 1:
    return
   setupforSFDcreation()


   def use_and_run_externalmuxer():
    global muxer_files
    muxer_files = []
    for files in external_sfdmuxer:
     files_name = os.path.basename(files)
     muxer_files_tempfolder = currentdir + '/MUXER'
     if not os.path.exists(muxer_files_tempfolder):
      os.mkdir(muxer_files_tempfolder)
     externalmuxer_copypath = os.path.join(muxer_files_tempfolder, files_name)
     shutil.copy(files, externalmuxer_copypath)
     muxer_files.append(externalmuxer_copypath)
   if useexternalsfdmuxer == 1:
    use_and_run_externalmuxer()




   if showffmpegcommands.get() == 0:
    FFmpeg_onlyprinterrors_cmd.set('-v error')  #Set FFmpeg to only print errors if showffmpegcommands == 0
   else:
    FFmpeg_onlyprinterrors_cmd.set('')



   def convertfiles_for_SFDmuxing():
    global outputmpegextension
    outputmpegextension = StringVar()
    if sofdecstreamtype.get() == '1' or sofdecstreamtype.get() == '2' or sofdecstreamtype.get() == '3' or sofdecstreamtype.get() == '4' or sofdecstreamtype.get() == '5':
     outputmpegextension.set('m1v')
    if sofdecstreamtype.get() == '6':
     outputmpegextension.set('mpeg')

    if sofdecstreamtype.get() == '1' or sofdecstreamtype.get() == '2' or sofdecstreamtype.get() == '3' and resolution.get() == '':
     resolution.set('320:240')
    elif sofdecstreamtype.get() == '5' and resolution.get() == '':  #Set CRAFT muxer's default to 480p
     resolution.set('640:480')
    updatevratio_streamtype1()

    if cancelcreation.get() == 1:
     return

    print("Converting video to AVI...")
    convert_avi_cmd=f'"{ffmpeg_exe_path}" {FFmpeg_onlyprinterrors_cmd.get()} -y -i "{filePathvideo.get()}" -crf {crfvalue.get()} -b:v 300M {framerate.get()} {vratio.get()} {videostarttimedurationvalue.get()} {videoendtimedurationvalue.get()} AVIconvert.avi'
    convert_avi_cmd_runcommand = subprocess.run(convert_avi_cmd, **subprocessoptions)
    if not convert_avi_cmd_runcommand.returncode == 0:
      cancelcreation.set(1)
      print("AVI video conversion failed, canceling SFD creation...")
      if showffmpegcommands.get() == 1:
       cleanup_files()
       error_messagebox = tk.messagebox.showerror('FFmpeg Error', f"AVIconvert.avi could not be created. The error can be found on the CMD window.")
      else:
       avi_conversion_error_message = convert_avi_cmd_runcommand.stderr or convert_avi_cmd_runcommand.stdout or "An unknown error occurred."
       cleanup_files()
       error_messagebox = tk.messagebox.showerror('FFmpeg Error', f"AVIconvert.avi could not be created, and FFmpeg gave the following error:\n\n{avi_conversion_error_message}")
      return


    #Prior to Beta 3.0.0 - vratio for V1 SFDs was set to the resolution variable, now vratio is used for both V1 and V2 SFDs.
    if cancelcreation.get() == 1:
     return
   
    print("Converting video to MPEG...")
    if enable2PassEncoding_int.get() == 1:
      convert_mpeg_pass_1_cmd=f'"{ffmpeg_exe_path}" {FFmpeg_onlyprinterrors_cmd.get()} -y -i AVIconvert.avi -crf {crfvalue.get()} {framerate.get()} {vratio.get()} {ffmpegstartdurationcmd.get()} {HQM1Vcommands.get()} -b:v {vbitrate.get()} {KVCD_cmd.get()} -c:v mpeg1video -pass 1 -f null /dev/null && /'
      convert_mpeg_pass_2_cmd=f'"{ffmpeg_exe_path}" {FFmpeg_onlyprinterrors_cmd.get()} -y -i AVIconvert.avi -crf {crfvalue.get()} {framerate.get()} {vratio.get()} {ffmpegstartdurationcmd.get()} {HQM1Vcommands.get()} -b:v {vbitrate.get()} {KVCD_cmd.get()} -c:v mpeg1video -pass 2 newvideo.{outputmpegextension.get()}'
      #Share same run command name so that errors are caught.
      convert_mpeg_cmd_runcommand = subprocess.run(convert_mpeg_pass_1_cmd, **subprocessoptions)
      convert_mpeg_cmd_runcommand = subprocess.run(convert_mpeg_pass_2_cmd, **subprocessoptions)
    else:
     convert_mpeg_cmd=f'"{ffmpeg_exe_path}" {FFmpeg_onlyprinterrors_cmd.get()} -y -i AVIconvert.avi -crf {crfvalue.get()} {framerate.get()} {vratio.get()} {ffmpegstartdurationcmd.get()} {HQM1Vcommands.get()} -b:v {vbitrate.get()} {KVCD_cmd.get()} -c:v mpeg1video newvideo.{outputmpegextension.get()}'
     convert_mpeg_cmd_runcommand = subprocess.run(convert_mpeg_cmd, **subprocessoptions)
    if not convert_mpeg_cmd_runcommand.returncode == 0:
      cancelcreation.set(1)
      print("MPEG video conversion failed, canceling SFD creation...")
      if showffmpegcommands.get() == 1:
       cleanup_files()
       error_messagebox = tk.messagebox.showerror('FFmpeg Error', f"newvideo.{outputmpegextension.get()} could not be created. The error can be found on the CMD window.")
      else:
       mpeg_conversion_error_message = convert_mpeg_cmd_runcommand.stderr or convert_mpeg_cmd_runcommand.stdout or "An unknown error occurred."
       cleanup_files()
       error_messagebox = tk.messagebox.showerror('FFmpeg Error', f"newvideo.{outputmpegextension.get()} could not be created, and FFmpeg gave the following error:\n\n{mpeg_conversion_error_message}")
      return



   def createaudiopadding():
    if cancelcreation.get() == 1:
     return
    
    if enableaudiopadding.get() == 1:
     print("Enable padding audio turned on, creating padding audio...")
     ffprobe_cmd = f'"{ffprobe_exe_path}" -i "{videofile}" -show_entries format=duration -v quiet -of csv="p=0"'
     duration = float(os.popen(ffprobe_cmd).read().strip())
     if os.path.isfile('blank.adx'):
      os.remove('blank.adx')
     if os.path.isfile('blank.sfa'):
      os.remove('blank.sfa')
     ffmpeg_blankaudio_cmd = f'"{ffmpeg_exe_path}" {FFmpeg_onlyprinterrors_cmd.get()} -y -f lavfi -i anullsrc=channel_layout=mono:sample_rate=8000 -t {duration} -b:a 1k -shortest blank.adx'
     
     #Set command to ALWAYS not show FFmpeg output, to be able to check for the Encoder error.
     ffmpeg_blankaudio_cmd_runcommand = subprocess.run(ffmpeg_blankaudio_cmd, shell=True, capture_output=True, text=True)
     if not ffmpeg_blankaudio_cmd_runcommand.returncode == 0:
      print("Padding audio creation failed, canceling SFD creation...")
      if showffmpegcommands.get() == 1:
       cleanup_files()
       error_messagebox = tk.messagebox.showerror('FFmpeg Error', f"blank.adx could not be created. The error can be found on the CMD window.")
      else:
       blankaudio_error_message = ffmpeg_blankaudio_cmd_runcommand.stderr or ffmpeg_blankaudio_cmd_runcommand.stdout or "An unknown error occurred."
       cleanup_files()
       error_messagebox = tk.messagebox.showerror('FFmpeg Error', f"blank.adx could not be created, and FFmpeg gave the following error:\n\n{blankaudio_error_message}")
      return

   if cancelcreation.get() == 1:
     return
   if enableaudiopadding.get() == 1:
    createaudiopadding()


   if cancelcreation.get() == 1:
     return

   if audio1_origaudiopath.get() == '':
      audio1_adx.set('')
   elif audio1_origaudiopath.get() == 'blank.adx': #Pass if blank audio, since already ADX
      audio1_adx.set('blank.adx')
   else:
     audio1_adx.set('track1.adx')
     convert_audio1_cmd=f'"{ffmpeg_exe_path}" {FFmpeg_onlyprinterrors_cmd.get()} -y -i "{audio1_origaudiopath.get()}" -b:a {abitrate.get()} {bitexactcmd.get()} -ar {aHz.get()} {audiochannel.get()} {ffmpegstartdurationcmd.get()} {audiostarttimedurationvalue.get()} {ffmpegenddurationcmd.get()} {audioendtimedurationvalue.get()} {audio1_adx.get()}'
     print(f"Converting audio track 1 to ADX...")
     convert_audio1_cmd_runcommand = subprocess.run(convert_audio1_cmd, **subprocessoptions)
     if not convert_audio1_cmd_runcommand.returncode == 0:
      cancelcreation.set(1)
      print("Track 1 ADX conversion failed, canceling SFD creation...")
      if showffmpegcommands.get() == 1:
       cleanup_files()
       error_messagebox = tk.messagebox.showerror('FFmpeg Error', f"track1.adx could not be created. The error can be found on the CMD window.")
      else:
       convert_audio1_error_message = convert_audio1_cmd_runcommand.stderr or convert_audio1_cmd_runcommand.stdout or "An unknown error occurred."
       cleanup_files()
       error_messagebox = tk.messagebox.showerror('FFmpeg Error', f"track1.adx could not be created, and FFmpeg gave the following error:\n\n{convert_audio1_error_message}")
      return


   if cancelcreation.get() == 1:
     return
   
   if audio2_origaudiopath.get() == '':
      audio2_adx.set('')
   elif audio2_origaudiopath.get() == 'blank.adx':
      audio2_adx.set('blank.adx')
   else:
     audio2_adx.set('track2.adx')
     convert_audio2_cmd=f'"{ffmpeg_exe_path}" {FFmpeg_onlyprinterrors_cmd.get()} -y -i "{audio2_origaudiopath.get()}" -b:a {abitrate.get()} {bitexactcmd.get()} -ar {aHz.get()} {audiochannel.get()} {ffmpegstartdurationcmd.get()} {audiostarttimedurationvalue.get()} {ffmpegenddurationcmd.get()} {audioendtimedurationvalue.get()} {audio2_adx.get()}'
     print(f"Converting audio track 2 to ADX...")
     convert_audio2_cmd_runcommand = subprocess.run(convert_audio2_cmd, **subprocessoptions)
     if not convert_audio2_cmd_runcommand.returncode == 0:
      cancelcreation.set(1)
      print("Track 2 ADX conversion failed, canceling SFD creation...")
      if showffmpegcommands.get() == 1:
       cleanup_files()
       error_messagebox = tk.messagebox.showerror('FFmpeg Error', f"track2.adx could not be created. The error can be found on the CMD window.")
      else:
       convert_audio2_error_message = convert_audio2_cmd_runcommand.stderr or convert_audio2_cmd_runcommand.stdout or "An unknown error occurred."
       cleanup_files()
       error_messagebox = tk.messagebox.showerror('FFmpeg Error', f"track2.adx could not be created, and FFmpeg gave the following error:\n\n{convert_audio2_error_message}")
      return


   if cancelcreation.get() == 1:
     return

   if audio3_origaudiopath.get() == '':
      audio3_adx.set('')
   elif audio3_origaudiopath.get() == 'blank.adx':
      audio3_adx.set('blank.adx')
   else:
      audio3_adx.set('track3.adx')
      convert_audio3_cmd=f'"{ffmpeg_exe_path}" {FFmpeg_onlyprinterrors_cmd.get()} -y -i "{audio3_origaudiopath.get()}" -b:a {abitrate.get()} {bitexactcmd.get()} -ar {aHz.get()} {audiochannel.get()} {ffmpegstartdurationcmd.get()} {audiostarttimedurationvalue.get()} {ffmpegenddurationcmd.get()} {audioendtimedurationvalue.get()} {audio3_adx.get()}'
      print(f"Converting audio track 3 to ADX...")
      convert_audio3_cmd_runcommand = subprocess.run(convert_audio3_cmd, **subprocessoptions)
      if not convert_audio3_cmd_runcommand.returncode == 0:
       cancelcreation.set(1)
       print("Track 3 ADX conversion failed, canceling SFD creation...")
       if showffmpegcommands.get() == 1:
        cleanup_files()
        error_messagebox = tk.messagebox.showerror('FFmpeg Error', f"track3.adx could not be created. The error can be found on the CMD window.")
       else:
        convert_audio3_error_message = convert_audio3_cmd_runcommand.stderr or convert_audio3_cmd_runcommand.stdout or "An unknown error occurred."
        cleanup_files()
        error_messagebox = tk.messagebox.showerror('FFmpeg Error', f"track3.adx could not be created, and FFmpeg gave the following error:\n\n{convert_audio3_error_message}")
       return


   if cancelcreation.get() == 1:
     return

   if audio4_origaudiopath.get() == '':
      audio4_adx.set('')
   elif audio4_origaudiopath.get() == 'blank.adx':
      audio4_adx.set('blank.adx')
   else:
      audio4_adx.set('track4.adx')
      convert_audio4_cmd=f'"{ffmpeg_exe_path}" {FFmpeg_onlyprinterrors_cmd.get()} -y -i "{audio4_origaudiopath.get()}" -b:a {abitrate.get()} {bitexactcmd.get()} -ar {aHz.get()} {audiochannel.get()} {ffmpegstartdurationcmd.get()} {audiostarttimedurationvalue.get()} {ffmpegenddurationcmd.get()} {audioendtimedurationvalue.get()} {audio4_adx.get()}'
      print(f"Converting audio track 4 to ADX...")
      convert_audio4_cmd_runcommand = subprocess.run(convert_audio4_cmd, **subprocessoptions)
      if not convert_audio4_cmd_runcommand.returncode == 0:
       cancelcreation.set(1)
       print("Track 4 ADX conversion failed, canceling SFD creation...")
       if showffmpegcommands.get() == 1:
        cleanup_files()
        error_messagebox = tk.messagebox.showerror('FFmpeg Error', f"track4.adx could not be created. The error can be found on the CMD window.")
       else:
        convert_audio4_error_message = convert_audio4_cmd_runcommand.stderr or convert_audio4_cmd_runcommand.stdout or "An unknown error occurred."
        cleanup_files()
        error_messagebox = tk.messagebox.showerror('FFmpeg Error', f"track4.adx could not be created, and FFmpeg gave the following error:\n\n{convert_audio4_error_message}")
       return


   if cancelcreation.get() == 1:
     return
   
   if sofdecstreamtype.get() == '1' or sofdecstreamtype.get() == '2' or sofdecstreamtype.get() == '3' or sofdecstreamtype.get() == '4' or sofdecstreamtype.get() == '5':
     adx_to_sfa_converter = os.getcwd() + '/resource/bin/legaladx/legaladx.exe'

     #Always check audioX_adx, not just audioX (since audioX = original path for files)
     if audio1_adx.get() == 'blank.adx':
      audio1_sfa.set('blank.sfa')
     elif not audio1_adx.get() == '':
      audio1_sfa.set('track1.sfa')
     elif audio1_adx.get() == '':  #If no audio for track X, skip file by setting audio1_sfa to nothing
      audio1_sfa.set('')

     if audio2_adx.get() == 'blank.adx':
      audio2_sfa.set('blank.sfa')
     elif not audio2_adx.get() == '':
      audio2_sfa.set('track2.sfa')
     elif audio2_adx.get() == '':
      audio2_sfa.set('')

     if audio3_adx.get() == 'blank.adx':
      audio3_sfa.set('blank.sfa')
     elif not audio3_adx.get() == '':
      audio3_sfa.set('track3.sfa')
     elif audio3_adx.get() == '':
      audio3_sfa.set('')

     if audio4_adx.get() == 'blank.adx':
      audio4_sfa.set('blank.sfa')
     elif not audio4_adx.get() == '':
      audio4_sfa.set('track4.sfa')
     elif audio4_adx.get() == '':
      audio4_sfa.set('')


     def convertadx_to_sfa():
      if cancelcreation.get() == 1:
       return
      
      if enableaudiopadding.get() == 1 and os.path.isfile('blank.adx'):
        legaladxcmd_blankaudio = f'"{adx_to_sfa_converter}" blank.adx blank.sfa'
        convert_blank_audio_to_SFA_runcommand = subprocess.run(legaladxcmd_blankaudio, **subprocessoptions)
        if not convert_blank_audio_to_SFA_runcommand.returncode == 0:
         cancelcreation.set(1)
         print("Padding audio SFA conversion failed, canceling SFD creation...")
         if showffmpegcommands.get() == 1:
          cleanup_files()
          error_messagebox = tk.messagebox.showerror('LegalADX Error', f"blank.sfa could not be created. The error can be found on the CMD window.")
         else:
          convert_blank_audio_to_SFA_error_message = convert_blank_audio_to_SFA_runcommand.stderr or convert_blank_audio_to_SFA_runcommand.stdout
          cleanup_files()
          #[35:] used to remove the "LegalADX v1.0 By Alex Free (C)2022" header that's always printed.
          error_messagebox = tk.messagebox.showerror('LegalADX Error', f"blank.sfa could not be created. LegalADX.exe gave the following error:\n\n{convert_blank_audio_to_SFA_error_message[35:]}")
         return


      if cancelcreation.get() == 1:
       return

      if audio1_sfa.get() == '' or audio1_sfa.get() == 'blank.sfa':
        pass
      else:
        if os.path.isfile('track1.adx'):
         legaladxcmd_track1 = f'"{adx_to_sfa_converter}" {audio1_adx.get()} {audio1_sfa.get()}'
         convert_track1_to_SFA_runcommand = subprocess.run(legaladxcmd_track1, **subprocessoptions)
         if not convert_track1_to_SFA_runcommand.returncode == 0:
          cancelcreation.set(1)
          print("Track 1 SFA conversion failed, canceling SFD creation...")
          if showffmpegcommands.get() == 1:
           cleanup_files()
           error_messagebox = tk.messagebox.showerror('LegalADX Error', f"track1.sfa could not be created. The error can be found on the CMD window.")
          else:
           convert_track1_to_SFA_error_message = convert_track1_to_SFA_runcommand.stderr or convert_track1_to_SFA_runcommand.stdout
           cleanup_files()
           error_messagebox = tk.messagebox.showerror('LegalADX Error', f"track1.sfa could not be created, and LegalADX gave the following error:\n\n{convert_track1_to_SFA_error_message[35:]}")
          return
      

      if cancelcreation.get() == 1:
       return

      if audio2_sfa.get() == '' or audio2_sfa.get() == 'blank.sfa':
        pass
      else:
        if os.path.isfile('track2.adx'):
         legaladxcmd_track2 = f'"{adx_to_sfa_converter}" {audio2_adx.get()} {audio2_sfa.get()}'
         convert_track2_to_SFA_runcommand = subprocess.run(legaladxcmd_track2, **subprocessoptions)
         if not convert_track2_to_SFA_runcommand.returncode == 0:
          cancelcreation.set(1)
          print("Track 2 SFA conversion failed, canceling SFD creation...")
          if showffmpegcommands.get() == 1:
           cleanup_files()
           error_messagebox = tk.messagebox.showerror('LegalADX Error', f"track2.sfa could not be created. The error can be found on the CMD window.")
          else:
           convert_track2_to_SFA_error_message = convert_track2_to_SFA_runcommand.stderr or convert_track2_to_SFA_runcommand.stdout
           cleanup_files()
           error_messagebox = tk.messagebox.showerror('LegalADX Error', f"track2.sfa could not be created, and LegalADX gave the following error:\n\n{convert_track2_to_SFA_error_message[35:]}")
          return
     

      if cancelcreation.get() == 1:
       return

      if audio3_sfa.get() == '' or audio3_sfa.get() == 'blank.sfa':
        pass
      else:
        if os.path.isfile('track3.adx'):
         legaladxcmd_track3 = f'"{adx_to_sfa_converter}" {audio3_adx.get()} {audio3_sfa.get()}'
         convert_track3_to_SFA_runcommand = subprocess.run(legaladxcmd_track3, **subprocessoptions)
         if not convert_track3_to_SFA_runcommand.returncode == 0:
          cancelcreation.set(1)
          print("Track 3 SFA conversion failed, canceling SFD creation...")
          if showffmpegcommands.get() == 1:
           cleanup_files()
           error_messagebox = tk.messagebox.showerror('LegalADX Error', f"track3.sfa could not be created. The error can be found on the CMD window.")
          else:
           convert_track3_to_SFA_error_message = convert_track3_to_SFA_runcommand.stderr or convert_track3_to_SFA_runcommand.stdout
           cleanup_files()
           error_messagebox = tk.messagebox.showerror('LegalADX Error', f"track3.sfa could not be created, and LegalADX gave the following error:\n\n{convert_track3_to_SFA_error_message[35:]}")
          return
    

      if cancelcreation.get() == 1:
       return

      if audio4_sfa.get() == '' or audio4_sfa.get() == 'blank.sfa':
        pass
      else:
        if os.path.isfile('track4.adx'):
         legaladxcmd_track4 = f'"{adx_to_sfa_converter}" {audio4_adx.get()} {audio4_sfa.get()}'
         convert_track4_to_SFA_runcommand = subprocess.run(legaladxcmd_track4, **subprocessoptions)
         if not convert_track4_to_SFA_runcommand.returncode == 0:
          cancelcreation.set(1)
          print("Track 4 SFA conversion failed, canceling SFD creation...")
          if showffmpegcommands.get() == 1:
           cleanup_files()
           error_messagebox = tk.messagebox.showerror('LegalADX Error', f"track4.sfa could not be created. The error can be found on the CMD window.")
          else:
           convert_track4_to_SFA_error_message = convert_track4_to_SFA_runcommand.stderr or convert_track4_to_SFA_runcommand.stdout
           cleanup_files()
           error_messagebox = tk.messagebox.showerror('LegalADX Error', f"track4.sfa could not be created, and LegalADX gave the following error:\n\n{convert_track4_to_SFA_error_message[35:]}")
          return
     
     if cancelcreation.get() == 1:
      return
     convertadx_to_sfa()
     
   if cancelcreation.get() == 1:
     return
   convertfiles_for_SFDmuxing()


   def mux_SFD():
    if cancelcreation.get() == 1:
      return
    
    print("Creating SFD...")

    #Set up audio file commands for V1 SFD muxers

    #V1.00/V1.01b/V1.07 muxers
    if sofdecstreamtype.get() == '1' or sofdecstreamtype.get() == '2' or sofdecstreamtype.get() == '3':
     if not audio1_sfa.get() == '':
      audio1_sfa_muxercmd.set(f'-a={audio1_sfa.get()[:-4]}')  #-4 off of end of filename to remove ".SFA" extension
     if not audio2_sfa.get() == '':
      audio2_sfa_muxercmd.set(f'-a={audio2_sfa.get()[:-4]}')
     if not audio3_sfa.get() == '':
      audio3_sfa_muxercmd.set(f'-a={audio3_sfa.get()[:-4]}')
     if not audio4_sfa.get() == '':
      audio4_sfa_muxercmd.set(f'-a={audio4_sfa.get()[:-4]}')
     
    #Alt V1 muxer
    if sofdecstreamtype.get() == '4':
      if not audio1_sfa.get() == '':
       audio1_sfa_muxercmd.set(f'-a {audio1_sfa.get()}')
      if not audio2_sfa.get() == '':
       audio2_sfa_muxercmd.set(f'-a {audio2_sfa.get()}')
      if not audio3_sfa.get() == '':
       audio3_sfa_muxercmd.set(f'-a {audio3_sfa.get()}')
      if not audio4_sfa.get() == '':
       audio4_sfa_muxercmd.set(f'-a {audio4_sfa.get()}')

    #CRAFT muxer
    if sofdecstreamtype.get() == '5':
      if not audio1_sfa.get() == '':
       audio1_sfa_muxercmd.set(f'-a="{audio1_sfa.get()}"')
      if not audio2_sfa.get() == '':
       audio2_sfa_muxercmd.set(f'-ach01="{audio2_sfa.get()}"')
      if not audio3_sfa.get() == '':
       audio3_sfa_muxercmd.set(f'-ach02="{audio3_sfa.get()}"')
      if not audio4_sfa.get() == '':
       audio4_sfa_muxercmd.set(f'-ach03="{audio4_sfa.get()}"')


    if cancelcreation.get() == 1:
      return

    #V1.00, V1.01b OR V1.07
    if sofdecstreamtype.get() == '1' or sofdecstreamtype.get() == '2' or sofdecstreamtype.get() == '3':
     #Since V1.00 and V1.01b muxers are broken, use V1.07 muxer, and modify output SFD to fit the V1.00/V1.01b file requirements
     sfdmux_streamtype1_1999muxer_location = os.getcwd() + '/resource/bin/SFDmuxers/SFDmux_V1.07/SFDmux.exe'
     sfdmux_V107_cmd=f'"{sfdmux_streamtype1_1999muxer_location}" -v=newvideo {audio1_sfa_muxercmd.get()} {audio2_sfa_muxercmd.get()} {audio3_sfa_muxercmd.get()} {audio4_sfa_muxercmd.get()} -s=file'
     sfdmux_V107_cmd_runcommand = subprocess.run(sfdmux_V107_cmd, **subprocessoptions)
     if not sfdmux_V107_cmd_runcommand.returncode == 0:
      cancelcreation.set(1)
      print("SFD muxing failed, canceling SFD creation...")
      if showffmpegcommands.get() == 1:
       cleanup_files()
       error_messagebox = tk.messagebox.showerror('SFDmux Error', f"{SFDfilename.get()}.sfd could not created. The error can be found on the CMD window.")
      else:
       sfdmux_V107_error_message = sfdmux_V107_cmd_runcommand.stderr or sfdmux_V107_cmd_runcommand.stdout
       cleanup_files()
       #[97:] used to remove the SFDmux header that would be otherwise present, + the spaces until it hits the error message
       error_messagebox = tk.messagebox.showerror('SFDmux Error', f"{SFDfilename.get()}.sfd could not created, and the SFD muxer gave the following error:\n{sfdmux_V107_error_message[97:]}")
      return

     #V1.07 -> V1.00 conversion
     #Tested in the following Dreamcast games: AeroWings, Sonic Adventure
     if sofdecstreamtype.get() == '1':
      print("Applying V1.07 -> V1.0.0 conversion...")
      with open('file.sfd', 'rb+') as V100_SFD_conversion:
       V100_SFD_conversion.seek(0x0)
       V100_SFD_conversion_data_preheader = V100_SFD_conversion.read(0x1000)  #Stop reading SFD file at 0x1000 (where V1.07 header starts)
       V100_SFD_conversion.seek(0x1800)
       V100_SFD_conversion_data_postheader = V100_SFD_conversion.read()
       V100_fixed_SFD_data = V100_SFD_conversion_data_preheader + V100_SFD_conversion_data_postheader
       
       with open('file2.sfd', 'wb') as V100_new_SFD:
        V100_new_SFD.write(V100_fixed_SFD_data)
       V100_SFD_conversion.close()    

       #Make converted SFD replace pre-converted SFD
       if os.path.isfile('file.sfd'):
        os.remove('file.sfd')
       if os.path.isfile('file2.sfd'):
        os.rename('file2.sfd', 'file.sfd')
       print("Done!")


     #V1.07 -> V1.01b conversion
     if sofdecstreamtype.get() == '2':
      print("Applying V1.07 -> V1.0.1b conversion...")
      with open('file.sfd', 'rb+') as V101b_SFD_conversion:
       #V1.01b header is in this format: Sofdec Stream header segments -> Pre-Sofdec Stream header -> rest of SFD
       #V1.07 SFD has the first two swapped, and less blank data between the Sofdec Stream header segments:
       #Tested on the following Dreamcast games: Evolution - The World of Sacred Device, Dynamite Deka 2
       #Do note that Evolution only has one SFD that is actually a V1.01b SFD, but it does support V1.01b SFDs where V1.07 SFDs are normally used.
       
       #Read data before and after Sofdec Stream header data
       V101b_SFD_conversion.seek(0x0)
       V101b_SFD_conversion_data_preheader = V101b_SFD_conversion.read(0x1000) #Exclude last 0x20 before "SofdecStream" text, since not needed.
       V101b_SFD_conversion.seek(0x1800)
       V101b_SFD_conversion_data_postheader = V101b_SFD_conversion.read()

       #Read Sofdec Stream header info from V1.07 file
       #Exclude "SofdecStream" header, since V1.01b SFD uses version with space ("Sofdec Stream")
       V101b_SFD_conversion.seek(0x1040)
       V101b_SFD_conversion_data_header_SFDfileinfo = V101b_SFD_conversion.read(0x20)
       #Exclude SFD muxer version header, since it's replaced later with the V1.01b muxer header
       V101b_SFD_conversion.seek(0x1180)
       V101b_SFD_conversion_data_header_inputvideoinfo = V101b_SFD_conversion.read(0x20)
       V101b_SFD_conversion.seek(0x11C0)
       V101b_SFD_conversion_data_header_inputaudio1info = V101b_SFD_conversion.read(0x20)
       V101b_SFD_conversion.seek(0x1200)
       V101b_SFD_conversion_data_header_inputaudio2info = V101b_SFD_conversion.read(0x20)
       V101b_SFD_conversion.seek(0x1240)
       V101b_SFD_conversion_data_header_inputaudio3info = V101b_SFD_conversion.read(0x20)
       V101b_SFD_conversion.seek(0x1280)
       V101b_SFD_conversion_data_header_inputaudio4info = V101b_SFD_conversion.read(0x20)
       V101b_SFD_conversion.close()
       
       #Modfiy V1.07 SFD to fit V1.01b requirements
       with open('file2.sfd', 'wb') as V107_convertSFD_to_V101b:
        V107_convertSFD_to_V101b.seek(0x0)
        #"Sofdec Stream" that V1.01b uses, instead of V1.0.7's "SofdecStream" (+ padding until 0x20)
        V107_convertSFD_to_V101b.write(b'\x53\x6F\x66\x64\x65\x63\x20\x53\x74\x72\x65\x61\x6D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        V107_convertSFD_to_V101b.write(b'\x00' * 0x80)
        V107_convertSFD_to_V101b.write(V101b_SFD_conversion_data_header_SFDfileinfo)
        V107_convertSFD_to_V101b.write(b'\x00' * 0x1E0)
        #The next line is "SFDMUX Ver.1.01b 1998-11-20 Copyright(c) 1998 CRI" converted to hex.
        V107_convertSFD_to_V101b.write(b'\x53\x46\x44\x4D\x55\x58\x20\x56\x65\x72\x2E\x31\x2E\x30\x31\x62\x20\x31\x39\x39\x38\x2D\x31\x31\x2D\x32\x30\x20\x43\x6F\x70\x79\x72\x69\x67\x68\x74\x28\x63\x29\x20\x31\x39\x39\x38\x20\x43\x52\x49')
        V107_convertSFD_to_V101b.write(b'\x00' * 0x10F)  #Not 110 b/c the "I" in the "1998 CRI" part of the header goes into next line, so removing one to compensate.
        #If any audio tracks are empty, then they just show as 0x20 of blank 0's.
        V107_convertSFD_to_V101b.write(V101b_SFD_conversion_data_header_inputaudio1info)
        V107_convertSFD_to_V101b.write(b'\x00' * 0x70)
        V107_convertSFD_to_V101b.write(V101b_SFD_conversion_data_header_inputaudio2info)
        V107_convertSFD_to_V101b.write(b'\x00' * 0x70)
        V107_convertSFD_to_V101b.write(V101b_SFD_conversion_data_header_inputaudio3info)
        V107_convertSFD_to_V101b.write(b'\x00' * 0x70)
        V107_convertSFD_to_V101b.write(V101b_SFD_conversion_data_header_inputaudio4info)
        V107_convertSFD_to_V101b.write(b'\x00' * 0x1040)
        V107_convertSFD_to_V101b.write(V101b_SFD_conversion_data_header_inputvideoinfo)
        V107_convertSFD_to_V101b.write(b'\x00' * 0x9F0)
        V107_convertSFD_to_V101b.write(V101b_SFD_conversion_data_preheader)
        V107_convertSFD_to_V101b.write(V101b_SFD_conversion_data_postheader)
        V107_convertSFD_to_V101b.close()
  
      if os.path.isfile('file.sfd'):
        os.remove('file.sfd')
      if os.path.isfile('file2.sfd'):
        os.rename('file2.sfd', 'file.sfd')
      print("Done!")


    #V1 (nebulas-star) muxer
    if cancelcreation.get() == 1:
      return

    if sofdecstreamtype.get() == '4':
     sfdmux_streamtype1_location = os.getcwd() + '/resource/bin/SFDmuxers/SofdecStream1_muxer/SFD_Muxer.exe'
     sfdmux_V1_ALT_cmd=f'"{sfdmux_streamtype1_location}" -v newvideo.m1v {audio1_sfa_muxercmd.get()} {audio2_sfa_muxercmd.get()} {audio3_sfa_muxercmd.get()} {audio4_sfa_muxercmd.get()} -s 1 -o file.sfd'
     sfdmux_V1_ALT_cmd_runcommand = subprocess.run(sfdmux_V1_ALT_cmd, **subprocessoptions)
     if not os.path.isfile('file.sfd'):  #Since using returncode causes program to hang (since it always = 0), check if SFD was made instead.
      cancelcreation.set(1)
      print("")  #Extra print to make sure that the error message and the next print.
      print("SFD muxing failed, canceling SFD creation...")
      if showffmpegcommands.get() == 1:
       cleanup_files()
       error_messagebox = tk.messagebox.showerror('SFDmux Error', f"{SFDfilename.get()}.sfd could not created. The error can be found on the CMD window.")
      else:
       sfdmux_ALT_error_message = sfdmux_V1_ALT_cmd_runcommand.stderr or sfdmux_V1_ALT_cmd_runcommand.stdout
       cleanup_files()
       error_messagebox = tk.messagebox.showerror('SFDmux Error', f"{SFDfilename.get()}.sfd could not created, and the SFD muxer gave the following error:\n\n{sfdmux_ALT_error_message}")
      return
  

    #CRAFT muxer
    if cancelcreation.get() == 1:
      return

    if sofdecstreamtype.get() == '5':
     sfdcrfc_CRAFT_location = os.getcwd() + '/resource/bin/SFDmuxers/CRAFTmuxer_V2.98/sfdcrfc.exe'
     sfdcrfc_CRAFT_cmd=f'"{sfdcrfc_CRAFT_location}" -exe=m -v="newvideo.m1v" {audio1_sfa_muxercmd.get()} {audio2_sfa_muxercmd.get()} {audio3_sfa_muxercmd.get()} {audio4_sfa_muxercmd.get()} -s="file.sfd"'
     sfdcrfc_CRAFT_cmd_runcommand = subprocess.run(sfdcrfc_CRAFT_cmd, **subprocessoptions)
     if not sfdcrfc_CRAFT_cmd_runcommand.returncode == 0:
      cancelcreation.set(1)
      print("SFD muxing failed, canceling SFD creation...")
      if showffmpegcommands.get() == 1:
       cleanup_files()
       error_messagebox = tk.messagebox.showerror('SFDcrfc Error', f"{SFDfilename.get()}.sfd could not created. The error can be found on the CMD window.")
      else:
       sfdcrfc_CRAFT_error_message = sfdcrfc_CRAFT_cmd_runcommand.stderr or sfdcrfc_CRAFT_cmd_runcommand.stdout
       cleanup_files()
       error_messagebox = tk.messagebox.showerror('SFDcrfc Error', f"{SFDfilename.get()}.sfd could not created, and the CRAFT muxer gave the following error:\n\n{sfdcrfc_CRAFT_error_message}")
      return


    #V2 muxer
    if cancelcreation.get() == 1:
      return     

    if sofdecstreamtype.get() == '6':
     sfdmuxlocation = os.getcwd() + '/resource/bin/SFDmuxers/CryTools_V2_muxer/sfdmux.exe'
     sfdmux_V2SFD_cmd=f'"{sfdmuxlocation}" file.sfd newvideo.{outputmpegextension.get()} {audio1_adx.get()} {audio2_adx.get()} {audio3_adx.get()} {audio4_adx.get()}'
     sfdmux_V2SFD_cmd_runcommand = subprocess.run(sfdmux_V2SFD_cmd, **subprocessoptions)
     if not os.path.exists('file.sfd'):  #Check for if SFD file was created, since returncode doesn't work.
      cancelcreation.set(1)
      print("SFD muxing failed, canceling SFD creation...")
      if showffmpegcommands.get() == 1:
       cleanup_files()
       error_messagebox = tk.messagebox.showerror('SFDmux Error', f"{SFDfilename.get()}.sfd could not created. The error can be found on the CMD window.")
      else:
       sfdmux_V2_error_message = sfdmux_V2SFD_cmd_runcommand.stdout  #sfdmux_V2SFD_cmd_runcommand.stderr prints nothing, so can't use it
       cleanup_files()
       error_messagebox = tk.messagebox.showerror('SFDmux Error', f"{SFDfilename.get()}.sfd could not created, and the SFD muxer gave the following error:\n\n{sfdmux_V2_error_message}")
      return

   mux_SFD()
   if cancelcreation.get() == 1:
    return


   def cleanup_and_finish_SFD():
    if os.path.isfile('file.sfd'): #Clean up files if SFD can't be created
      pass
    else:
      cleanup_files()
      return


    def keepfiles_function():
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
      elif audio1_adx.get() == 'blank.adx':
       if os.path.exists(os.path.join(currentdir, 'blank.adx')):
        shutil.copy(os.path.join(currentdir, 'blank.adx'), os.path.join(dirPath.get(), 'track1.adx')) 
      else:
       print(f"track1.adx not found, unable to move to destination directory.")
      
      if os.path.exists(os.path.join(currentdir, 'track2.adx')):
       shutil.move(os.path.join(currentdir, 'track2.adx'), os.path.join(dirPath.get(), 'track2.adx'))
      elif audio2_adx.get() == 'blank.adx':
       if os.path.exists(os.path.join(currentdir, 'blank.adx')):
        shutil.copy(os.path.join(currentdir, 'blank.adx'), os.path.join(dirPath.get(), 'track2.adx')) 
      else:
       print(f"track2.adx not found, unable to move to destination directory.")


     #Keep Track 3 and 4 ADXs
     if IntVar.get(keepADX) == 1 and addaudiotracks.get() == 1:
      if os.path.exists(os.path.join(currentdir, 'track3.adx')):
       shutil.move(os.path.join(currentdir, 'track3.adx'), os.path.join(dirPath.get(), 'track3.adx'))
      elif audio3_adx.get() == 'blank.adx':
       if os.path.exists(os.path.join(currentdir, 'blank.adx')):
        shutil.copy(os.path.join(currentdir, 'blank.adx'), os.path.join(dirPath.get(), 'track3.adx')) 
      else:
       print(f"track3.adx not found, unable to move to destination directory.")
      
      if os.path.exists(os.path.join(currentdir, 'track4.adx')):
       shutil.move(os.path.join(currentdir, 'track4.adx'), os.path.join(dirPath.get(), 'track4.adx'))
      elif audio4_adx.get() == 'blank.adx':
       if os.path.exists(os.path.join(currentdir, 'blank.adx')):
        shutil.copy(os.path.join(currentdir, 'blank.adx'), os.path.join(dirPath.get(), 'track4.adx')) 
      else:
       print(f"track4.adx not found, unable to move to destination directory.")



     #Keep Track 1 and 2 SFA files
     if IntVar.get(keepADX) == 1:
      if os.path.exists(os.path.join(currentdir, 'track1.sfa')):
       shutil.move(os.path.join(currentdir, 'track1.sfa'), os.path.join(dirPath.get(), 'track1.sfa'))
      elif audio1_sfa.get() == 'blank.sfa':  #Copy blank file if the track used padding audio, and keep files is selected.
       if os.path.exists(os.path.join(currentdir, 'blank.sfa')):
        shutil.copy(os.path.join(currentdir, 'blank.sfa'), os.path.join(dirPath.get(), 'track1.sfa')) 
      else:
       print(f"track1.sfa not found, unable to move to destination directory.")
      
      if os.path.exists(os.path.join(currentdir, 'track2.sfa')):
       shutil.move(os.path.join(currentdir, 'track2.sfa'), os.path.join(dirPath.get(), 'track2.sfa'))
      elif audio2_sfa.get() == 'blank.sfa':
       if os.path.exists(os.path.join(currentdir, 'blank.sfa')):
        shutil.copy(os.path.join(currentdir, 'blank.sfa'), os.path.join(dirPath.get(), 'track2.sfa')) 
      else:
       print(f"track2.sfa not found, unable to move to destination directory.")


     #Keep Track 3 and 4 SFA files
     if IntVar.get(keepADX) == 1 and addaudiotracks.get() == 1:
      if os.path.exists(os.path.join(currentdir, 'track3.sfa')):
       shutil.move(os.path.join(currentdir, 'track3.sfa'), os.path.join(dirPath.get(), 'track3.sfa'))
      elif audio3_sfa.get() == 'blank.sfa':
       if os.path.exists(os.path.join(currentdir, 'blank.sfa')):
        shutil.copy(os.path.join(currentdir, 'blank.sfa'), os.path.join(dirPath.get(), 'track3.sfa')) 
      else:
       print(f"track3.sfa not found, unable to move to destination directory.")
      
      if os.path.exists(os.path.join(currentdir, 'track4.sfa')):
       shutil.move(os.path.join(currentdir, 'track4.sfa'), os.path.join(dirPath.get(), 'track4.sfa'))
      elif audio4_sfa.get() == 'blank.sfa':
       if os.path.exists(os.path.join(currentdir, 'blank.sfa')):
        shutil.copy(os.path.join(currentdir, 'blank.sfa'), os.path.join(dirPath.get(), 'track4.sfa')) 
      else:
       print(f"track4.sfa not found, unable to move to destination directory.")


    SFDname_withextension = StringVar()
    SFDname_withextension = SFDfilename.get() + '.sfd'
    min_file_size = 50
    file_size_kb = os.path.getsize('file.sfd') // 50
    print("Checking SFD file...")
    if file_size_kb < min_file_size:
      cancelcreation.set(1)
      SFDfilesizeerror = tk.messagebox.showerror('SFD Error', f"{SFDname_withextension} couldn't be properly created. Try creating the file again.")
      if os.path.isfile(SFDname_withextension):
       os.remove(SFDname_withextension)
      cleanup_files()
    else:
      videocheckcommand = f'"{ffprobe_exe_path}" -v error -show_entries stream=codec_type -of default=noprint_wrappers=1 file.sfd -select_streams v:0'
      videocheckcmd_output = subprocess.run(videocheckcommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      if videocheckcmd_output.returncode == 0:
        os.rename('file.sfd', SFDname_withextension)
        keepfiles_function()
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

   cleanup_and_finish_SFD()
   cancelcreation.set(0)
   if cancelcreation.get() == 1:
    return

   print("")
   #return


def write_batchmode_info_tofile():
  batch_txtfile = os.path.join(currentdir, 'resource/batch/batch.txt')
  batchmode_firstrun_int = IntVar()

  #Delete old batch txt file if it exists, and create the new txt file.
  if os.path.isfile(batch_txtfile):
   if batchmode_firstrun_int.get() == 1:
    pass
   else:
    os.remove(batch_txtfile)
    batchmode_firstrun_int.set(1)
   with open(batch_txtfile, "w") as batchfile:
    batchfile.close()

  if os.path.isfile(batch_txtfile):
   with open(batch_txtfile, "a") as batchfile:
    batchfile.write(f"videofilepath={filePathvideo.get()}\n")
    batchfile.write(f"track1filepath={filePathaudt1.get()}\n")
    batchfile.write(f"track2filepath={filePathaudt2.get()}\n")
    batchfile.write(f"track3filepath={filePathaudt3.get()}\n")
    batchfile.write(f"track4filepath={filePathaudt4.get()}\n")
    batchfile.write(f"outputdirectory={dirPath.get()}\n")
    batchfile.write(f"sofdecmuxer={sofdecstreamtype.get()}\n")
    batchfile.write(f"sfdfilename={SFDfilename.get()}\n")
  else:
   print("Error: batch.txt does not exist.")
   return


#Hide/Show/Load GUI sub-windows
def show_extraoptionswindow():
 optwin.deiconify()

def show_extraaudiotrackswin():
  extraaudiotrackswin.deiconify()

def show_externalSFDmuxerwin():
  externalSFDmuxer_window.deiconify()

def show_customFFmpegcommandwin():
 usecustomFFmpegcommandswin.deiconify()

def hide_subwindows(): #Hide window(s) so that sub-windows can't be opened different multiple times.
 extraaudiotrackswin.withdraw()
 externalSFDmuxer_window.withdraw()
 usecustomFFmpegcommandswin.withdraw()
 optwin.withdraw()


gui_elements_mainmenu() #Load GUI elements (for main menu)
advancedopt()
extraaudiotracks()
useexternalSFDmuxer()
usecustomFFmpegcommands()
externalSFDmuxer_window.protocol("WM_DELETE_WINDOW", hide_subwindows) #Hide window (until if opened later)
optwin.protocol("WM_DELETE_WINDOW", hide_subwindows)
extraaudiotrackswin.protocol("WM_DELETE_WINDOW", hide_subwindows)
usecustomFFmpegcommandswin.protocol("WM_DELETE_WINDOW", hide_subwindows)

def close_helpmenu_windows_and_exit(*args):
 if helpmenu_find_sfd_version_window.winfo_exists():
  helpmenu_find_sfd_version_window.destroy()

 if helpinfo_sfdversion_window.winfo_exists():
  helpinfo_sfdversion_window.destroy()
 
 #master.after(200)
 os._exit(0)
master.protocol("WM_DELETE_WINDOW", close_helpmenu_windows_and_exit)


#Check for program updates, check for FFmpeg programs, and set up FFmpeg/FFprobe EXE paths.
def updater_exe():
 updaterlocation = os.getcwd() + '/updater.exe'
 if os.path.isfile(updaterlocation):
  runupdater = f'"{updaterlocation}"'
  runupdater_subprocess_cmd = subprocess.run(runupdater, shell=True, capture_output=True, text=True)
 else:
  print("Unable to find updater.exe, program will not be able to update.")
  pass
updater_exe()  #Run on boot

run_ffmpeg_check()  #Set up ffmpeg_location_int and ffprobe_location_int on boot
print("")


def cleanup_files():
 if os.path.isfile('file.sfd'):
  os.remove('file.sfd')
 if os.path.isfile('file2.sfd'):
  os.remove('file2.sfd')
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
 if os.path.exists('blank.adx'):
  os.remove('blank.adx')
 if os.path.exists('blank.sfa'):
  os.remove('blank.sfa')
 if os.path.isfile('AVIconvert.avi'):
  os.remove('AVIconvert.avi')
 if os.path.isfile(f'newvideo.mpeg'):
  os.remove(f'newvideo.mpeg')
 if os.path.isfile(f'newvideo.m1v'):
  os.remove(f'newvideo.m1v')
 cancelcreation.set(0)
 return


#def checkfiles():
 #cleanup_files()
 #if useexternalsfdmuxer.get() == 1:
  #os.remove(muxer_files)

#def closeprogram():
 #killffmpeg = 'taskkill /F /IM ffmpeg.exe'
 #os.system(killffmpeg)
 #os._exit(0)

atexit.register(cleanup_files)
#atexit.register(closeprogram)
cleanup_files() #Run on boot to clean up any files if any where missed due to crash, program closing, etc.
master.mainloop()