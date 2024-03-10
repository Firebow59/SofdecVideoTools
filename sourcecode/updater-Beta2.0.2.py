import requests
from requests import get
import webbrowser
from webbrowser import open_new_tab
from tkinter import messagebox
import tkinter as tk

def check_for_new_version(owner, repo, current_version):
    url = f"https://github.com/{owner}/{repo}/releases/latest"
    response = requests.get(url)

    if response.status_code == 200:
        if f"/{current_version}" not in response.text:
            programupdate = tk.messagebox.askyesno(title='Program Update', message=f"A new update is available. Would you like to vist the GitHub page to download it?")
            if programupdate == True:
             webbrowser.open_new_tab(url)
            else:
             pass

def main():
    owner = "Firebow59"
    repo = "SofdecVideoTools"
    current_version = "2.0.2"

    check_for_new_version(owner, repo, current_version)

if __name__ == "__main__":
    main()