import os
import tkinter as tk
import requests
import webbrowser
import zipfile
import subprocess
import shutil
from tkinter import messagebox, IntVar, StringVar

def check_for_new_SofdecVideoTools_version():
 current_version = 'V1.0.0'  #Update this for every new release
    
 print("Checking for update...")
 github_api = requests.get("https://api.github.com/repos/firebow59/SofdecVideoTools/releases/latest")

 if github_api.status_code == 200:
  if 'tag_name' not in github_api.text:
   print("Unable to get version tags from Github repo.")
  else:
   get_version_number = github_api.text.split('tag_name')[1]
   get_version_number_split_only_version = get_version_number.strip().split(',')[0]
   get_version_number_split_final = get_version_number_split_only_version.split(':')[1].split('"')[1]  #Change output from ":"X.X.X" to X.X.X
   
   if get_version_number_split_final > current_version:
    programupdate = tk.messagebox.askyesno(title='Program Update', message=f"A new update is available. Would you like to vist the GitHub page to download it?")
    if programupdate == True:
     webbrowser.open_new_tab("https://github.com/Firebow59/SofdecVideoTools/releases/latest")
    else:
     print("Update cancelled.")
   else:
    print(f"Program is on the latest version. ({get_version_number_split_final})")

 else:
  print("Unable to access GitHub repo for SofdecVideoTools.")


if __name__ == "__main__":
 check_for_new_SofdecVideoTools_version()