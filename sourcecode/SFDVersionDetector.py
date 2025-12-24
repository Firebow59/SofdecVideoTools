import os
import tkinter as tk
import shutil
import subprocess
from tkinter import IntVar, messagebox, StringVar, Button, filedialog, ttk
import argparse
import sys

#Make sure you have updater.py in the same folder as this PY file, or else the program won't work.
from updater import check_for_new_SofdecVideoTools_version


master = tk.Tk()
master.geometry("300x130"), master.title("SFDVersionDetector V2.1.1"), master.resizable(False, False)

currentdir = os.getcwd()

SFDfilepath = StringVar()
SFDname = StringVar()
output_txt_path = StringVar()
batchmode = IntVar()
writeversion_tofile = IntVar()
printSFDencoder = IntVar()
SFDfile_to_read = StringVar()
onlyprintmuxerinfo = IntVar()
disable_done_text = IntVar()
disable_gui = IntVar()
disable_updater = IntVar()


def gui_elements():
 def selectvideo():
  if batchmode.get() == 1:
   SFDfile = filedialog.askdirectory(title="Select a folder containing SFD files.")
  else:
   SFDfile = filedialog.askopenfilename(title="Select A SFD File", filetypes=[("SFD file", ".sfd")])
  SFDfilepath.set(SFDfile)
  togglerunbutton()

 def opendocspdf():
  sfdversiondetector_docs = os.getcwd() + '/resource/docs/documentation.pdf'
  os.startfile(sfdversiondetector_docs)

 def togglerunbutton_when_mode_changed():
  SFDfilepath.set('')
  togglerunbutton()

 batchmodecheck = ttk.Checkbutton(text='Enable batch mode', variable=batchmode, command=togglerunbutton_when_mode_changed, onvalue=1, offvalue=0)
 batchmodecheck.place(x=10, y=8.1)
 batchmodecheck.bind('w', togglerunbutton_when_mode_changed)

 chooseSFD = Button(text="Browse", command=selectvideo, padx=45, pady=5)
 chooseSFD.place(x=10, y=55)
 playSFD = Button(text="Find SFD Version", command=findversion, state=tk.DISABLED, padx=18, pady=5)
 playSFD.place(x=155, y=55) #leave seperate to fix issue with "None"
 opendocs = Button(text="Documentation", command=opendocspdf, padx=93).place(x=10, y=95)


 def togglerunbutton():
  if SFDfilepath.get() == '':
   playSFD.config(state=tk.DISABLED)
  else:
   playSFD.config(state=tk.NORMAL)
 chooseSFD.bind('w', togglerunbutton)

 writeversion_tofile_check = ttk.Checkbutton(text="Write version details to text file", variable=writeversion_tofile, onvalue=1, offvalue=0)
 #writeversion_tofile_check.place(x=10, y=27)



def findversion():
 if SFDfilepath.get() == '':
  tk.messagebox.showerror('File Error', "No SFD/directory was provided, or the directory/file chosen was invalid. Please try again.")
  return

 #Check if file/path exists 
 if os.path.isfile(SFDfilepath.get()):
  pass
 elif os.path.exists(SFDfilepath.get()):
  pass
 
 
 def determine_SFD_version():
  with open(SFDfile_to_read.get(), 'rb') as SFD_file_openfile:
   SFD_file_openfile.seek(0x0)
   SFD_file_binarydata = SFD_file_openfile.read(0x3000) #Most SFDs headers are between 0x1000 and 0x2000, but set to 0x3000 just in case a SFD header is a bit lower down.

   try:
    #Check if V2 SFD
    if b'\x53\x6F\x66\x64\x65\x63\x53\x74\x72\x65\x61\x6D\x32' in SFD_file_binarydata:  #"SofdecStream2" in hex
     print("")
     if onlyprintmuxerinfo.get() == 1:
      sys.stdout.write(f"{SFDname.get()}: V2\n")
     else:
      sys.stdout.write(f'"{SFDname.get()}" is a V2 SFD.\n')
     SFD_file_openfile.close()


    #Check if V1 SFD
    #Look for "SofdecStream"/"Sofdec Stream" (V1.01b uses spaced version) in hex
    elif b'\x53\x6F\x66\x64\x65\x63\x53\x74\x72\x65\x61\x6D' in SFD_file_binarydata or b'\x53\x6F\x66\x64\x65\x63\x20\x53\x74\x72\x65\x61\x6D' in SFD_file_binarydata:
     #Check for SFD version ("SFDMUX" text)
     if b'\x53\x46\x44\x4D\x55\x58' in SFD_file_binarydata:
      offset_of_SFDMUX_text = SFD_file_binarydata.find(b'\x53\x46\x44\x4D\x55\x58')
      offset_of_SFDMUX_int = int(hex(offset_of_SFDMUX_text), 16)
      SFD_file_openfile.seek(offset_of_SFDMUX_int)
      readSFDmux_version = SFD_file_openfile.read(0x10)
      SFDmux_version_textconversion = readSFDmux_version.decode('utf-8').split('Ver')[1].strip()
      SFDmux_version_correctedtext = SFDmux_version_textconversion[1:]  #Remove extra characters after "Ver" until it reaches the version number
      print("")
      if onlyprintmuxerinfo.get() == 1:
       sys.stdout.write(f"{SFDname.get()}: V{SFDmux_version_correctedtext}\n")
      else:
       sys.stdout.write(f'"{SFDname.get()}" is a V1 SFD, created with the V{SFDmux_version_correctedtext} muxer.\n')
      SFD_file_openfile.close()
     else:
      #"CRAFT" or "CRITAGS" in hex, all of which are used in CRAFT SFDs
      #"CRI_SFM" is used in some non-CRAFT SFDs, so don't search for it for CRAFT SFDs. (ex: Phantasy Star Online's "Tentou-you Demo Movie" disc)
      if b'\x43\x52\x41\x46\x54' in SFD_file_binarydata or b'\x43\x52\x49\x54\x41\x47\x53' in SFD_file_binarydata:
       offset_of_muxer_version_CRAFT = SFD_file_binarydata.find(b'\x56\x65\x72')  #Find "Ver" in SFD
       offset_of_muxer_version_CRAFT_int = int(hex(offset_of_muxer_version_CRAFT), 16)
       SFD_file_openfile.seek(offset_of_muxer_version_CRAFT_int)
       readCRAFTmuxer_version = SFD_file_openfile.read(0x8)
       CRAFTmuxer_version_textconversion = readCRAFTmuxer_version.decode('utf-8').split('Ver')[1].strip()
       CRAFTmuxer_version_correctedtext = CRAFTmuxer_version_textconversion[1:].strip()
       print("")
       if onlyprintmuxerinfo.get() == 1:
        sys.stdout.write(f"{SFDname.get()}: CRAFT, V{CRAFTmuxer_version_correctedtext}\n")
       else:
        sys.stdout.write(f'"{SFDname.get()}" is a V1 SFD, created with the CRAFT (V{CRAFTmuxer_version_correctedtext}) muxer.\n')
       SFD_file_openfile.close()

      elif b'\x43\x52\x49\x5F\x53\x46\x4D' in SFD_file_binarydata:  #CRI_SFM - can either be V1.0.7(?) (Phantasy Star Online's "Tentou-you Demo Movie" disc) or CRAFT
       print("")
       if onlyprintmuxerinfo.get() == 1:
        sys.stdout.write(f"{SFDname.get()}: V1.0.7 or CRAFT (CRI_SFM)\n")
       else:
        sys.stdout.write(f'"{SFDname.get()}" is a V1 SFD, and could be either a V1.0.7 or CRAFT SFD muxer (CRAFT being the most likely one, since it has "CRI_SFM" in the file).\n')


    else:  #No "SofdecStream"/SFDMUX header = V1.0.0
     #Since (what I assume are) V1.0.0 files (the original muxer doesn't add any data headers onto the file data) seem to always have their header removed, 
     #attempt to check for (c)CRI string at 0x1938 and 0x1138.
     #0x1938 was found in some DC games such as "Pen Pen Triicelon", "July", and "Godzilla Generations".
     #0x1138 was found in the Dreamcast version of "Sonic Adventure". (ex. "SA1_600.SFD")
     
     print("")
     if onlyprintmuxerinfo.get() == 1:
      pass
     else:
      if onlyprintmuxerinfo.get() == 1:
       pass
      else:
       print(f"Unable to find SofdecStream/SFDMUX header for {SFDname.get()}, checking if {SFDname.get()} is a V1.0.0 SFD...")
    
     
     #Check for the first segment of video/audio data (at 0x180F/0x100F)
     SFD_file_openfile.seek(0x180F)
     check_if_section_equals_video_or_audio = SFD_file_openfile.read(0x1)
     if check_if_section_equals_video_or_audio == ((b'\xc0' or b'\xe0' or b'\xd0')):
      #Check 0x1938 for (c)CRI tag - if a SFD file didn't have any audio, this would appear though, hence the previous check.
      SFD_file_openfile.seek(0x1938)
      readSFDmux_version = SFD_file_openfile.read(0x06)
      if readSFDmux_version == b'\x28\x63\x29\x43\x52\x49':  # "(c)CRI" (SFA/ADX audio tag) in hex
       if onlyprintmuxerinfo.get() == 1:
         sys.stdout.write(f"{SFDname.get()}: V1.0.0\n")
       else:
         sys.stdout.write(f'"{SFDname.get()}" is a V1.0.0 SFD.\n')
      else:
       if onlyprintmuxerinfo.get() == 1:
         sys.stdout.write(f"{SFDname.get()}: V1.0.0\n")
       else:
         sys.stdout.write(f'"{SFDname.get()}" is (likely) a V1.0.0 SFD (as it contains a correct section header at 0x1938).\n')
     else:
      #Check for 0x1138 offset.
      SFD_file_openfile.seek(0x100F)
      check_if_section_equals_video_or_audio = SFD_file_openfile.read(0x1)
      if check_if_section_equals_video_or_audio == ((b'\xc0' or b'\xe0' or b'\xd0')):
       #Check 0x1138 for (c)CRI tag - if a SFD file didn't have any audio, this would appear though, hence the previous check.
       SFD_file_openfile.seek(0x1138)
       readSFDmux_version = SFD_file_openfile.read(0x06)
       if readSFDmux_version == b'\x28\x63\x29\x43\x52\x49': # "(c)CRI" (SFA/ADX audio tag) in hex
         if onlyprintmuxerinfo.get() == 1:
          sys.stdout.write(f"{SFDname.get()}: V1.0.0\n")
         else:
          sys.stdout.write(f'"{SFDname.get()}" is a V1.0.0 SFD.\n')
       else:
         if onlyprintmuxerinfo.get() == 1:
          sys.stdout.write(f"{SFDname.get()}: V1.0.0\n")
         else:
          sys.stdout.write(f'"{SFDname.get()}" is (likely) a V1.0.0 SFD (as it contains a correct section header at 0x100F).\n')
 
      else:
       if onlyprintmuxerinfo.get() == 1:
        sys.stdout.write(f"{SFDname.get()}: SFD version unable to be determined. It may possibly not be an SFD file, despite the extension, or may be an earlier SEGA Saturn SFD.\n")
        #Mana Khemia 2 Portable Plus is an example of a game that uses .SFD but is actually a different format (PSMF), for whatever reason.
       else:
        sys.stdout.write(f"{SFDname.get()}: SFD version unable to be determined. It may possibly not be an SFD file, despite the extension, or may be an earlier SEGA Saturn SFD.\n")
     SFD_file_openfile.close()
   

   except Exception as error_readforversion:
     sys.stderr.write(f"The following error occurred:, {error_readforversion}\n")
     SFD_file_openfile.close()
   sys.stdout.flush()


 if batchmode.get() == 1:  #Loop if batchmode.get() == 1
  for root, dirs, files in os.walk(SFDfilepath.get()):
   for SFD_file_batchmode in files:
    if SFD_file_batchmode.endswith('.sfd') or SFD_file_batchmode.endswith('.SFD'):
     SFDname.set(SFD_file_batchmode)
     SFDfile_to_read.set(root + '/' + SFD_file_batchmode)
     determine_SFD_version()
    else:
     continue
 elif batchmode.get() == 0:
  SFDname.set(os.path.basename(SFDfilepath.get()))
  SFDfile_to_read.set(SFDfilepath.get())
  determine_SFD_version()

 if disable_done_text.get() == 1:
  pass
 else:
  input("\n\nDone, press any key to exit...")


def updater_exe():
 check_for_new_SofdecVideoTools_version()

gui_elements()

if __name__ == "__main__":
 parser = argparse.ArgumentParser(description='Detects the version of a V1 or V2 Sofdec file') #\nExample Command: SFDVersionDetector.exe -files "C:\example_FILES"')
 parser.add_argument('-file', type=str, help='Input file/directory.')
 parser.add_argument('-no_gui', action='store_true', help='Disables the GUI.')
 parser.add_argument('-version_only', action='store_true', help='Only prints the version type and name of SFD, in the format NAME: VERSION.')
 parser.add_argument('-disable_done_text', action='store_true', help='Only prints the version type and name of SFD, in the format NAME: VERSION.')
 parser.add_argument('-disable_updater', action='store_true', help='Disables the program update checker from running on the current command.')
 args = parser.parse_args()

 if disable_updater.get() == 1:  #Check if updater should run or not
   pass
 else:
   updater_exe()
   print("")


 #Check if any commands are given - if not, run GUI, otherwise disable the GUI.
 if args.no_gui:
  disable_gui.set(1)

 if disable_gui.get() == 1:
  SFDfilepath.set(args.file)
  if args.version_only:
   onlyprintmuxerinfo.set(1)
  if args.disable_done_text:
   disable_done_text.set(1)
  if args.disable_updater:
   disable_updater.set(1)

  master.withdraw()  #Hide GUI if running via command line

  if SFDfilepath.get() == '':
   input('No file was provided. Please provide a file with the -file flag, and try again.')
   os._exit(0)
  if os.path.isdir(SFDfilepath.get()):
   batchmode.set(1)
  elif os.path.isfile(SFDfilepath.get()):
   batchmode.set(0)
  else:
   input('\nThe given file/folder could not be found. Please ensure the folder exists and the path is correct, and try again.\nPress any key to exit.\n')
   os._exit(0)

  findversion()
  os._exit(0)
 else:  #Enable GUI
  disable_done_text.set(1)
  pass


master.mainloop()