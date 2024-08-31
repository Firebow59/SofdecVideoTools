import os
import tkinter as tk
import argparse
import zipfile
import subprocess
import shutil
from tkinter import messagebox, IntVar, StringVar

#Required window
root = tk.Tk()
root.withdraw()

#Check for FFmpeg/Update FFmpeg code:
currentdir = os.getcwd()
ffmpeg_exe_path = StringVar()
ffprobe_exe_path = StringVar()
ffplay_exe_path = StringVar()

#FFmpeg location = 0 means its in SofdecVideoTools folder, 1 means its in PATH
ffmpeg_location_int = IntVar()
ffprobe_location_int = IntVar()
ffplay_location_int = IntVar()


def run_ffmpeg_check():
 def download_and_install_ffmpeg():
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
   if os.path.isfile(ffmpeg_exe_newlocation_binfolder + '/ffmpeg.exe'):
     os.remove(ffmpeg_exe_newlocation_binfolder + '/ffmpeg.exe')
   shutil.move(ffmpeg_exe_extractedzip + '/ffmpeg.exe', ffmpeg_exe_newlocation_binfolder + '/ffmpeg.exe')

   if os.path.isfile(ffmpeg_exe_newlocation_binfolder + '/ffprobe.exe'):
     os.remove(ffmpeg_exe_newlocation_binfolder + '/ffprobe.exe')
   shutil.move(ffmpeg_exe_extractedzip + '/ffprobe.exe', ffmpeg_exe_newlocation_binfolder + '/ffprobe.exe')

   if os.path.isfile(ffmpeg_exe_newlocation_binfolder + '/ffplay.exe'):
     os.remove(ffmpeg_exe_newlocation_binfolder + '/ffplay.exe')
   shutil.move(ffmpeg_exe_extractedzip + '/ffplay.exe', ffmpeg_exe_newlocation_binfolder + '/ffplay.exe')
   shutil.rmtree(currentdir + '/resource/bin/ffmpeg/ffmpeg-master-latest-win64-gpl')
  return

 global check_for_ffmpeg
 def check_for_ffmpeg():
  ffmpeg_exe_path.set(currentdir + '/resource/bin/ffmpeg/ffmpeg.exe')
  ffprobe_exe_path.set(currentdir + '/resource/bin/ffmpeg/ffprobe.exe')
  ffplay_exe_path.set(currentdir + '/resource/bin/ffmpeg/ffplay.exe')

  #FFmpeg location = 0 means its in SofdecVideoTools folder, 1 means its in PATH
  #print("Checking for FFmpeg...")

  if os.path.isfile(ffmpeg_exe_path.get()):
   print("FFmpeg.exe found (in SofdecVideoTools' bin folder)")
   ffmpeg_location_int.set(0)

  elif os.path.isfile('ffmpeg.exe'):
   print("FFmpeg.exe found in root folder, moving to bin folder...")
   shutil.move('ffmpeg.exe', ffmpeg_exe_path.get())
   print("FFmpeg.exe is now in the bin folder")
   print("FFmpeg.exe found (in SofdecVideoTools' bin folder)")
   ffmpeg_location_int.set(0)

  elif shutil.which('ffmpeg.exe'):
   print("FFmpeg.exe found (in PATH)")
   ffmpeg_location_int.set(1)
  else:
    print("FFmpeg.exe unable to be found")
    ffmpegmissing_message = tk.messagebox.askyesno('FFprobe.exe missing', "FFmpeg (and related programs such as ffprobe.exe) could not be found. FFmpeg is required to run these programs. Do you want to download FFmpeg? (This is about 400MB)")
    if ffmpegmissing_message:
      download_and_install_ffmpeg()
      print("FFmpeg installed!")
      ffmpeginstallmessage = tk.messagebox.showinfo(title='FFmpeg Installed', message='FFmpeg has been installed!')
    else:
     input("Press any key to exit...")
     os._exit(0)



  if os.path.isfile(ffprobe_exe_path.get()):
   print("FFprobe.exe found (in SofdecVideoTools' bin folder)")
   ffprobe_location_int.set(0)
 
  elif os.path.isfile('ffprobe.exe'):
   print("FFprobe.exe found in root folder, moving to bin folder...")
   shutil.move('ffprobe.exe', ffprobe_exe_path.get())
   print("FFprobe.exe is now in the bin folder")
   print("FFprobe.exe found (in SofdecVideoTools' bin folder)")
   ffprobe_location_int.set(0)
 
  elif shutil.which('ffprobe.exe'):
    print("FFprobe.exe found (in PATH)")
    ffprobe_location_int.set(1)
  else:
    print("FFprobe.exe unable to be found")
    ffmpegmissing_message = tk.messagebox.askyesno('FFprobe.exe missing', "FFmpeg (and related programs such as ffprobe.exe) could not be found. FFmpeg is required to run these programs. Do you want to download FFmpeg? (This is about 400MB)")
    if ffmpegmissing_message:
      download_and_install_ffmpeg()
      print("FFmpeg installed!")
      ffmpeginstallmessage = tk.messagebox.showinfo(title='FFmpeg Installed', message='FFmpeg has been installed!')
    else:
     input("Press any key to exit...")
     os._exit(0)
 
 
  if os.path.isfile(ffplay_exe_path.get()):
   print("FFplay.exe found (in SofdecVideoTools' bin folder)")
   ffplay_location_int.set(0)

  elif os.path.isfile('ffplay.exe'):
   print("FFplay.exe found in root folder, moving to bin folder...")
   shutil.move('ffplay.exe', ffplay_exe_path.get())
   print("FFplay.exe is now in the bin folder")
   print("FFplay.exe found (in SofdecVideoTools' bin folder)")
   ffplay_location_int.set(0)

  elif shutil.which('ffplay.exe'):
   print("FFplay.exe found (in PATH)")
   ffplay_location_int.set(1)
  else:
    print("FFplay.exe unable to be found")
    ffmpegmissing_message = tk.messagebox.askyesno('FFprobe.exe missing', "FFmpeg (and related programs such as ffprobe.exe) could not be found. FFmpeg is required to run these programs. Do you want to download FFmpeg? (This is about 400MB)")
    if ffmpegmissing_message:
      download_and_install_ffmpeg()
      print("FFmpeg installed!")
      ffmpeginstallmessage = tk.messagebox.showinfo(title='FFmpeg Installed', message='FFmpeg has been installed!')
      return
    else:
     input("Press any key to exit...")
     os._exit(0)
  return

 check_for_ffmpeg()
 return 



def update_ffmpeg():
 ffmpeg_exe_newlocation_binfolder = currentdir + '/resource/bin/ffmpeg'

 #Get location of FFmpeg, FFprobe and FFplay if it's on the user's PATH/System Environment Variables
 ffmpeg_environment_variable_location = shutil.which('ffmpeg.exe')
 if not ffmpeg_environment_variable_location == None:
  ffmpeg_location_int.set(1)
  ffmpeg_exe_path.set(os.path.dirname(shutil.which('ffmpeg.exe')))
 elif os.path.exists(ffmpeg_exe_newlocation_binfolder + '/ffmpeg.exe'):
  ffmpeg_location_int.set(0)
  ffmpeg_exe_path.set(ffmpeg_exe_newlocation_binfolder)
 else:
   print("FFmpeg unable to be found. Please re-download it in the following messagebox.")
   check_for_ffmpeg()


 ffprobe_environment_variable_location = shutil.which('ffprobe.exe')
 if not ffprobe_environment_variable_location == None:
  ffprobe_location_int.set(1)
  ffprobe_exe_path.set(os.path.dirname(shutil.which('ffprobe.exe')))
 elif os.path.exists(ffmpeg_exe_newlocation_binfolder + '/ffprobe.exe'):
  ffprobe_location_int.set(0)
  ffprobe_exe_path.set(ffmpeg_exe_newlocation_binfolder)
 else:
   print("FFprobe unable to be found. Please re-download it in the following messagebox.")
   check_for_ffmpeg()
   

 ffplay_environment_variable_location = shutil.which('ffplay.exe')
 if not ffplay_environment_variable_location == None:
  ffplay_location_int.set(1)
  ffplay_exe_path.set(os.path.dirname(shutil.which('ffplay.exe')))
 elif os.path.exists(ffmpeg_exe_newlocation_binfolder + '/ffplay.exe'):
  ffplay_location_int.set(0)
  ffplay_exe_path.set(ffmpeg_exe_newlocation_binfolder)
 else:
   print("FFplay unable to be found. Please re-download it in the following messagebox.")
   check_for_ffmpeg()

 if ffmpeg_location_int.get() == 1 or ffprobe_location_int.get() == 1 or ffplay_location_int.get() == 1:
  ffmpegPATH_check_message = tk.messagebox.askyesno('FFmpeg Location', "FFmpeg was found on your PATH/System Environment Variables. Updating FFmpeg will replace it for other programs that use either FFmpeg.exe, FFprobe.exe, or FFplay.exe from your PATH as well.\n\nDo you want to update FFmpeg?\n(If no is selected, you'll have the option to install it just to SofdecVideoTools' folder.)")
  if ffmpegPATH_check_message:
    pass
  else:
   ffmpeg_move_to_BIN_folder_check_message = tk.messagebox.askyesno('FFmpeg Location', "Would you like to download the latest FFmpeg update to SofdecVideoTools' folder instead? (This will prevent it from replacing the version of FFmpeg on your PATH.)")
   if ffmpeg_move_to_BIN_folder_check_message:
    ffmpeg_location_int.set(0)
    ffprobe_location_int.set(0)
    ffplay_location_int.set(0)
    ffmpeg_exe_path.set(ffmpeg_exe_newlocation_binfolder)
    ffprobe_exe_path.set(ffmpeg_exe_newlocation_binfolder)
    ffplay_exe_path.set(ffmpeg_exe_newlocation_binfolder)
   else:
     print("FFmpeg will not be updated.")
     os._exit(0)



 #Download latest version of FFmpeg, update EXE files
 if os.path.isfile('ffmpeg.zip'):
   os.remove('ffmpeg.zip')
 if os.path.isfile('ffmpeg-master-latest-win64-gpl.zip'):
   os.remove('ffmpeg-master-latest-win64-gpl.zip')
 wget_location = os.getcwd() + '/resource/bin/wget.exe'
 downloadffmpeg=f'"{wget_location}" https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip'
 print("Downloading the latest FFmpeg update... (This may take a bit)")
 subprocess.run(downloadffmpeg, stderr=subprocess.STDOUT, shell=True) #creationflags=subprocess.CREATE_NO_WINDOW
 os.rename('ffmpeg-master-latest-win64-gpl.zip', 'ffmpeg.zip')
   
 with zipfile.ZipFile('ffmpeg.zip', 'r') as ffmpeg_zip:
   ffmpeg_zip.extractall(currentdir + '/resource/bin/ffmpeg')
   ffmpeg_zip.close()
   os.remove('ffmpeg.zip')
   ffmpeg_exe_extractedzip = currentdir + '/resource/bin/ffmpeg/ffmpeg-master-latest-win64-gpl/bin'

   if ffmpeg_location_int.get() == 0:
    if os.path.isfile(ffmpeg_exe_newlocation_binfolder + '/ffmpeg.exe'):
      os.remove(ffmpeg_exe_newlocation_binfolder + '/ffmpeg.exe')
    shutil.move(ffmpeg_exe_extractedzip + '/ffmpeg.exe', ffmpeg_exe_newlocation_binfolder + '/ffmpeg.exe')
   if ffmpeg_location_int.get() == 1:
     if os.path.isfile(ffmpeg_exe_path.get() + '/ffmpeg.exe'):
      os.remove(ffmpeg_exe_path.get() + '/ffmpeg.exe')
     shutil.move(ffmpeg_exe_extractedzip + '/ffmpeg.exe', ffmpeg_exe_path.get())


   if ffprobe_location_int.get() == 0:
    if os.path.isfile(ffmpeg_exe_newlocation_binfolder + '/ffprobe.exe'):
     os.remove(ffmpeg_exe_newlocation_binfolder + '/ffprobe.exe')
    shutil.move(ffmpeg_exe_extractedzip + '/ffprobe.exe', ffmpeg_exe_newlocation_binfolder + '/ffprobe.exe')
   if ffprobe_location_int.get() == 1:
     if os.path.isfile(ffprobe_exe_path.get() + '/ffprobe.exe'):
      os.remove(ffprobe_exe_path.get() + '/ffprobe.exe')
     shutil.move(ffmpeg_exe_extractedzip + '/ffprobe.exe', ffmpeg_exe_path.get())


   if ffplay_location_int.get() == 0:
    if os.path.isfile(ffmpeg_exe_newlocation_binfolder + '/ffplay.exe'):
     os.remove(ffmpeg_exe_newlocation_binfolder + '/ffplay.exe')
    shutil.move(ffmpeg_exe_extractedzip + '/ffplay.exe', ffmpeg_exe_newlocation_binfolder + '/ffplay.exe')
   if ffplay_location_int.get() == 1:
     if os.path.isfile(ffplay_exe_path.get() + '/ffplay.exe'):
      os.remove(ffplay_exe_path.get() + '/ffplay.exe')
     shutil.move(ffmpeg_exe_extractedzip + '/ffplay.exe', ffmpeg_exe_path.get())
   
   #Delete old ZIP folder
   shutil.rmtree(currentdir + '/resource/bin/ffmpeg/ffmpeg-master-latest-win64-gpl')
   print("FFmpeg has been updated.")
   ffmpeginstallmessage = tk.messagebox.showinfo(title='FFmpeg Updated', message='FFmpeg has been successfully updated!')
   check_for_ffmpeg()
   return



root.update()  #Required to prevent error
root.destroy()