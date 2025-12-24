import os
import tkinter as tk
import subprocess
import atexit
from tkinter import IntVar, messagebox, StringVar, Frame, LabelFrame, Label, Button, Toplevel, filedialog, ttk
from PIL import Image, ImageTk

#Make sure you have check_for_ffmpeg.py and updater.py in the same folder as this PY file, or else the program won't work.
from check_for_ffmpeg import ffmpeg_location_int, ffprobe_location_int, run_ffmpeg_check, update_ffmpeg, ffplay_location_int
from updater import check_for_new_SofdecVideoTools_version

master = tk.Tk()
master.geometry("300x130"), master.title("SFDPlayer V2.1.1"), master.resizable(False, False)#, master.iconbitmap("resource/icon/sfdplayer.ico")

SFDfilepath = StringVar()
SFDname = StringVar()
programresolution = StringVar()
aspectratio = StringVar()
disableaudio = IntVar()
only_extract_certain_audio_tracks_int = IntVar()

programresolution.set('-x 1280 -y 720') #Set FFplay box size
#aspectratio.set('-aspect 4:3')

helphint_image = ImageTk.PhotoImage(Image.open(os.getcwd() + '/resource/img/questionmark.png').resize((10, 13)))


def gui_elements():
 global show_help_hint
 def show_help_hint(helpmenu_message_index):
  help_message_textbox_title = [
  'Play Audio Tracks',
  ]

  help_messages = [
  '"All Tracks" will play every audio track present in the SFD.\n\n"Custom" will allow you to play only certain audio tracks from an SFD, starting at 0 (the first audio track in the file) and going up to 31. (ex. To only play tracks 1 (the 2nd track in the SFD file) and 3 (the 4th track in the SFD file), you would enter "1, 4", without the quotes.)',
  ]

  help_message_textbox = tk.messagebox.showinfo(title=f'{help_message_textbox_title[helpmenu_message_index]}', message=f'{help_messages[helpmenu_message_index]}')


 
 def selectvideo():
  SFDfile = filedialog.askopenfilename(title="Select A SFD File", filetypes=[("SFD file", ".sfd")])
  SFDfilepath.set(SFDfile)
  SFDname.set(os.path.basename(SFDfilepath.get()))
  toggleplaybutton()

 def opendocspdf():
  sfdplayerdocs = os.getcwd() + '/resource/docs/documentation.pdf'
  os.startfile(sfdplayerdocs)

 chooseSFD = Button(text="Browse", command=selectvideo, padx=45, pady=5).place(x=10, y=55)
 playSFD = Button(text="Play SFD", command=playvideo, state=tk.DISABLED, padx=40, pady=5)
 playSFD.place(x=155, y=55) #leave seperate to fix issue with "None"
 opendocs = Button(text="Documentation", command=opendocspdf, padx=93).place(x=10, y=95) #padx=22

 def toggleplaybutton():
  if SFDfilepath.get() == '':
   playSFD.config(state=tk.DISABLED)
  else:
   playSFD.config(state=tk.NORMAL)

 vbitrate = StringVar()
 vidbitrateselect = Label(text="Video Bitrate:", font = ("Arial Bold", 8)).place(x=4700, y=87)
 videobitrateentry = ttk.Entry(textvariable=vbitrate, width=15)
 videobitrateentry.place(x=5000, y=105)
 vbitratevalue = f'-b:a {vbitrate.get()}'

 global custom_audio_track_extraction_list
 def custom_audio_track_extraction_list(*args):
   if not audiotracks_to_extract_combobox.get() == 'All Tracks':
    only_extract_certain_audio_tracks_int.set(1)
    for audio_track_number in audiotracks_to_extract_textvariable.get().split(','):
     if not audio_track_number.strip() in list_of_audio_tracks_to_extract and audio_track_number.strip().isdigit():
      list_of_audio_tracks_to_extract.append(audio_track_number.strip())
      master.focus_set()  #Force program to unselect the audioformatbox, updating it's variables.


      global string_of_audio_tracks_to_extract_for_command
      string_of_audio_tracks_to_extract_for_command = StringVar()
      for numbers_of_audio_tracks in list_of_audio_tracks_to_extract:
       if not numbers_of_audio_tracks in string_of_audio_tracks_to_extract_for_command.get():
        string_of_audio_tracks_to_extract_for_command.set(string_of_audio_tracks_to_extract_for_command.get() + numbers_of_audio_tracks + ',')
      #After every track to extract is added to the list:
      string_of_audio_tracks_to_extract_for_command.set(string_of_audio_tracks_to_extract_for_command.get().strip()[:-1]) #[:-1] to remove the last extra " ," on the last number in the string.
      list_of_audio_tracks_to_extract.clear()


     elif not audio_track_number.strip().isdigit() and not audio_track_number.strip() == '':
      #Message box instead displayed once the user clicks "Play SFD", to prevent the box from showing up twice in a row.
      only_extract_certain_audio_tracks_int.set(0)
      return
   else:
    only_extract_certain_audio_tracks_int.set(0)

 audtrackselect = Label(text="Use Audio Track:", font = ("Arial Bold", 8)).place(x=179, y=8)
 global list_of_audio_tracks_to_extract
 global audiotracks_to_extract_combobox
 list_of_audio_tracks_to_extract = []
 OPTIONS_audiotracktype = ["All Tracks", "Custom"]
 audiotracks_to_extract_textvariable = StringVar()
 audiotracks_to_extract_combobox = ttk.Combobox(master, value=OPTIONS_audiotracktype, textvariable=audiotracks_to_extract_textvariable, width=14)
 audiotracks_to_extract_combobox.place(x=182, y=25)
 audiotracks_to_extract_combobox.current(0)

 audiotracks_to_extract_helphint_label = Label(image=helphint_image)
 audiotracks_to_extract_helphint_label.image = helphint_image
 audiotracks_to_extract_helphint_label.place(x=277, y=8)  #Leave .place seperate to avoid error with bind
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


 def toggleaudiotrackselector():
  if disableaudio.get() == 1:
   audiotracks_to_extract_combobox.config(state=tk.DISABLED)
  else:
   audiotracks_to_extract_combobox.config(state=tk.NORMAL)
   audiotracks_to_extract_combobox.current(0)

 disableaudiocheck = ttk.Checkbutton(text='Disable audio', variable=disableaudio, command=toggleaudiotrackselector, onvalue=1, offvalue=0).place(x=10, y=10)

 def changeffplayresolution():
  if playatoriginalresolution.get() == 1:
   programresolution.set('')
  else:
   programresolution.set('-x 640 -y 400')

 playatoriginalresolution = IntVar()
 playatoriginalresolutioncheck = ttk.Checkbutton(text="Play at original resolution", variable=playatoriginalresolution, command=changeffplayresolution, onvalue=1, offvalue=0).place(x=10, y=27)




def playvideo():
 custom_audio_track_extraction_list()  #Run this to update it in case the user went directly from the audio tracks combobox to playing the SFD, in which case the combobox and thus variable wouldn't have been updated.
 if only_extract_certain_audio_tracks_int.get() == 0 and not audiotracks_to_extract_combobox.get() == "All Tracks":
  tk.messagebox.showerror(title='Invalid Input for Custom Audio Extraction', message="The input provided for custom audio track extraction was invalid.\n\nPlease ensure only numbers are present in the box, and that it's written in the format 'A, B, C, ...' (ex. 1, 12, 4, 5, 2)")
  return


 if SFDfilepath.get() == '':
  tk.messagebox.showerror('File Error', "No SFD was provided. Please provide an SFD to continue.")
  return

 #Set ffmpeg command properly if it's on the user's PATH
 if ffmpeg_location_int.get() == 1:
  ffmpeg_exe_path = 'ffmpeg.exe'
 else:
  ffmpeg_exe_path = os.getcwd() + '/resource/bin/ffmpeg/ffmpeg.exe'
 if ffplay_location_int.get() == 1:
   ffplay_exe_path = 'ffplay.exe'
 else:
  ffplay_exe_path = os.getcwd() + '/resource/bin/ffmpeg/ffplay.exe'


 SFD_extractor_EXE_path = os.getcwd() + '/SFDExtractor.exe'
 if os.path.isfile(SFD_extractor_EXE_path):
  print("Extracting SFD data...")
  if only_extract_certain_audio_tracks_int.get() == 1:
   only_extract_certain_audio_tracks_command = f'-audiotracks {string_of_audio_tracks_to_extract_for_command.get()}'
  else:
   only_extract_certain_audio_tracks_command = ''

  #Extraction type = 0 (Video/Audio), or 1 (Video only), so if disable audio = 1, it works to enable only video extraction
  try:
   extract_SFD_data=f'"{SFD_extractor_EXE_path}" -cmdmode -disable_done_text -disable_updater -disable_ffmpeg_check -autooverwrite -noconvert -extractiontype {disableaudio.get()} {only_extract_certain_audio_tracks_command} -file "{SFDfilepath.get()}" -outputfolder "{os.getcwd()}"'
   subprocess.run(extract_SFD_data)
  except IOError as extraction_error:
   cleanup_files()
   extraction_error_message = extract_SFD_data.stderr or extract_SFD_data.stdout or "An unknown error occurred."
   tk.messagebox.showerror('SFDExtractor Error', f"{os.path.basename(SFDfilepath.get())} could not be extracted. Please try again. If the issue persists, reach out either on SofdecVideoTool's GitHub or GameBanana page with details on the error, file being used, etc.")
 else:
  tk.messagebox.showerror(title='File Missing Error', message="SFDExtractor.exe could not be found. If it is missing from the folder containing SFDPlayer.exe, reinstall SofdecVideoTools.")
  return
 
 #Convert video/audio data to MPG/MP2
 print("Converting video/audio data...", end='\r')
 for extracted_SFD_files in os.listdir(os.getcwd()):
  if extracted_SFD_files.lower().endswith(('.m1v', '.m2v')):
   if extracted_SFD_files.lower().endswith(('videotrack_e0.m1v', 'videotrack_e0.m2v')):
    os.rename((os.getcwd() + '/' + extracted_SFD_files), 'video.mpg')
  if extracted_SFD_files.lower().endswith(('.sfa', '.adx', '.aix', '.ac3')):
   try:
    convert_audio_data=f'"{ffmpeg_exe_path}" -hide_banner -loglevel error -i "{os.getcwd() + f'/{extracted_SFD_files}'}" -c:a mp2 -b:a 320k -bitexact {extracted_SFD_files}.mp2'
    subprocess.run(convert_audio_data, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
   except IOError as audio_conversion_error:
    cleanup_files()
    audio_conversion_error_message = convert_audio_data.stderr or convert_audio_data.stdout or "An unknown error occurred."
    tk.messagebox.showerror('FFmpeg Error', f"{os.path.basename(SFDfilepath.get())} could not be extracted, and FFmpeg gave the following error:\n\n{audio_conversion_error_message}")
 print("Converting video/audio data... DONE!", end='\n')
   
 #Combine extracted audio tracks into one file.
 if not disableaudio.get() == 1:
  print("Combining audio tracks into one file...", end='\r')
  list_of_converted_MP2_files_to_combine = []
  for converted_MP2_audio_files in os.listdir(os.getcwd()):
   if converted_MP2_audio_files.lower().endswith('.mp2'):
    list_of_converted_MP2_files_to_combine.append(converted_MP2_audio_files)
  converted_MP2_audio_files = ''

  number_of_MP2_files_to_combine = IntVar()
  ffmpeg_list_of_MP2_files = StringVar()
  for converted_MP2_audio_files in list_of_converted_MP2_files_to_combine:
   ffmpeg_list_of_MP2_files.set(ffmpeg_list_of_MP2_files.get() + f'-i "{converted_MP2_audio_files}" ')
   number_of_MP2_files_to_combine.set(number_of_MP2_files_to_combine.get() + 1)

  #Get the average RMS of all audio tracks, divide it by the total # of audio tracks to get an average RMS, to later correct the combined audio file's volume to.
  RMS_of_all_extracted_audio_combined = IntVar()
  RMS_average_of_all_extracted_audio = IntVar()
  RMS_average_of_all_extracted_audio.set('0')  #Set to 0 so that when RMS_of_all_extracted_audio_combined.set() runs the first time, it doesn't give an error since it equals ''.
  for converted_MP2_audio_files in list_of_converted_MP2_files_to_combine:  #Create a new loop so total # of MP2 files is set to it's final value.
   try: 
    get_RMS_of_audio = f'"{ffmpeg_exe_path}" -hide_banner -loglevel error -i "{os.getcwd() + '/' + converted_MP2_audio_files}" -loglevel info -hide_banner -nostats -filter:a volumedetect -f null NUL'
    get_RMS_of_audio_run_command = subprocess.run(get_RMS_of_audio, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
   except IOError as audio_RMS_find_error:
    cleanup_files()
    audio_conversion_error_message = get_RMS_of_audio.stderr or get_RMS_of_audio.stdout or "An unknown error occurred."
    tk.messagebox.showerror('FFmpeg Error', f"{os.path.basename(SFDfilepath.get())} could not be extracted, and FFmpeg gave the following error:\n\n{audio_conversion_error_message}")
   
   get_RMS_of_audio_find_RMS_volume_info = int(round(float(((get_RMS_of_audio_run_command.stderr.split('mean_volume: ')[1]).split('dB')[0]).strip())))  #Convert to float, then round before converting to int, to prevent a ValueError
   RMS_of_all_extracted_audio_combined.set(RMS_average_of_all_extracted_audio.get() + get_RMS_of_audio_find_RMS_volume_info)
  RMS_average_of_all_extracted_audio.set(RMS_of_all_extracted_audio_combined.get() / number_of_MP2_files_to_combine.get())
  
  combine_audio_to_one_file=f'"{ffmpeg_exe_path}" {ffmpeg_list_of_MP2_files.get().strip()} -b:a 320k -bitexact -filter_complex "amix=inputs={number_of_MP2_files_to_combine.get()}:duration=longest:normalize=1" allaudio.mp2'
  subprocess.run(combine_audio_to_one_file, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
  print("Combining audio tracks into one file... DONE!", end='\n')


 print("Combining video and audio to one file...", end='\r')
 #Combine the now-single audio track into the video.
 if disableaudio.get() == 1:
  os.rename((os.getcwd() + f'/video.mpg'), 'SFD.mpg')
 else:
  try:
   combine_video_and_audio=f'"{ffmpeg_exe_path}" -hide_banner -loglevel error -i video.mpg -i allaudio.mp2 -c:v copy -c:a copy SFD.mpg'
   subprocess.run(combine_video_and_audio, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
  except IOError as video_audio_combine_error:
    cleanup_files()
    video_and_audio_combine_error_message = combine_video_and_audio.stderr or combine_video_and_audio.stdout or "An unknown error occurred."
    tk.messagebox.showerror('FFmpeg Error', f"{os.path.basename(SFDfilepath.get())} could not be extracted, and FFmpeg gave the following error:\n\n{video_and_audio_combine_error_message}")
 print("Combining video and audio to one file... DONE!", end='\n')


 print("Doing final cleanups...", end='\r')
 #Remove old files that aren't the new .MPG file
 for conversion_files in os.listdir(os.getcwd()):
  if conversion_files.lower().endswith(('.mpg', '.mp2', '.aix', '.adx', '.sfa', '.ac3', '.m1v', '.m2v')):
   if not conversion_files.lower() == 'sfd.mpg':
    os.remove(conversion_files)
 print("Doing final cleanups... DONE!", end='\n')

 try:
  ffplaycmd=f'"{ffplay_exe_path}" {programresolution.get()} {aspectratio.get()} SFD.mpg'
  subprocess.run(ffplaycmd, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
 except IOError as FFplay_error:
    cleanup_files()
    video_and_audio_playback_error_message = ffplaycmd.stderr or ffplaycmd.stdout or "An unknown error occurred."
    tk.messagebox.showerror('FFplay Error', f"{os.path.basename(SFDfilepath.get())} could not be played, and FFplay gave the following error:\n\n{video_and_audio_playback_error_message}")
 print("")

 string_of_audio_tracks_to_extract_for_command.set('')  #Reset this to fix a bug where it would just keep adding the numbers to the string, even if user has removed them from the combobox.
 cleanup_files()
 return


def cleanup_files():
 for conversion_files in os.listdir(os.getcwd()):
  if conversion_files.lower().endswith(('.mpg', '.mp2', '.aix', '.adx', '.sfa', '.ac3', '.m1v', '.m2v')):
   os.remove(conversion_files)

def closeprogram():
  if "taskkill /f /im ffplay.exe" == True:
   os.system("taskkill /f /im ffplay.exe")
  os._exit(0)

def updater_exe():
 check_for_new_SofdecVideoTools_version()
 
cleanup_files() #Delete any files that are left over on program boot, moreso in case program crashes and doesn't clean up files.
updater_exe()
print("")
run_ffmpeg_check()  #Set up FFmpeg location ints
print("")
gui_elements()

atexit.register(cleanup_files)
atexit.register(closeprogram)

master.mainloop()