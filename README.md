# SofdecVideoTools
**A set of GUI programs for processes related to Sofdec video files, designed for Windows.**

These programs are intended to be more user-friendly alternatives and/or replacements to older SFD programs, such as SEGA Dreamcast Movie Creator.

Instructions and explanations of options in the programs can be found in the included documentation found in the program(s), or in the Downloads + Documentation section below.

Support for .usm files and/or some audio types (AIX audio, MP2 audio) used in some SFDs is not currently supported in these programs.

## Downloads + Documentation

The latest version of the programs can be downloaded [here](https://github.com/Firebow59/SofdecVideoTools/releases/latest).

Documentation for the programs can be found [here.](https://github.com/Firebow59/oldalpha-SofdecVideoTools/blob/main/resource/docs/documentation.pdf)


## Requirements
- A x64/64-bit Windows PC
- FFmpeg (if you don't have this, a prompt will come up and the program will automatically install it for you!)

## Programs Included

- **SFDCreator** - Allows you to create your own SFD files for use in various games.
- **SFDExtractor** - Extracts the contents of SFD files (and converts them to modern formats by default).
- **SFDPlayer** - Plays SFD files (without re-encoding the video)

## Other
Got suggestions and/or found a bug? [Leave it here!](https://github.com/Firebow59/SofdecVideoTools/issues) (In the case that it's a bug, make sure to specify which program, and how to replicate it if possible)

For developers, feel free to use the code in this repo for your own projects, EXCEPT in this case of use for malicious purposes, such as viruses, fake installers, spyware and/or adware, etc.

## O&A
**Q:** How big are the programs when extracted?

**A:** They are about 30MB if you already have FFmpeg installed on your system. Otherwise, it's closer to 450MB.


**Q:** A prompt comes up saying "Windows protect your PC". What is this, and what do I do to bypass it?

**A:** This happens with programs not recognized by the Windows software database. To bypass it, click on "More info", then on "Run Anyway". The programs should boot after that.

## Credits + Other Infomation
FFmpeg is licensed under the [GNU Lesser General Public License (LGPL) version 2.1 or later](https://www.gnu.org/licenses old-licenses/lgpl-2.1.html).
For more details, please see [this page](https://www.ffmpeg.org/legal.html)
Copyright (c) [2000-2023] FFmpeg developers

SFDmux (used in SFDCreator and part of [CryTools](https://github.com/ThisKwasior/CryTools)) is created by [ThisKwasior](https://github.com/ThisKwasior). The license for it can be found [here.](https://github.com/ThisKwasior/CryTools/blob/master/LICENSE) 

[SFD_Muxer](https://github.com/nebulas-star/SFD_Muxer) is created by [nebulas-star](https://github.com/nebulas-star). The license for it can be found [here.](https://github.com/nebulas-star/SFD_Muxer/blob/main/LICENSE)

SFDMUX 1.07 is from the SEGA Dreamcast Katana SDK.

legaladx is taken from [video2dreamcastdisc](https://github.com/alex-free/video2dreamcastdisc/), and is licensed under the BSD 3-Clause License. It's license can be found [here.](https://github.com/alex-free/video2dreamcastdisc/blob/master/licenses/legaladx.txt)

wget is licensed under the GNU General Public License Version 3.0, which can be found [here](https://www.gnu.org/licenses/gpl-3.0.txt). More info on wget can be found [here.](https://www.gnu.org/software/wget/)

Thanks to [kTeo-0](https://github.com/kTeo-0) for their suggestions regarding QoL settings.
