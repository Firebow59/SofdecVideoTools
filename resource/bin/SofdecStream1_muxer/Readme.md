# SFD Muxer

[中文](/Readme_cn.md)

Open source CRI Sofdec Muxer.

## Introduction
CRI Sofdec file format (SFD) is a type of video middleware format which developed by CRI Middleware Co., Ltd.

Now(2021), CRI Middleware has stopped supporting this format.

This tool is built as a limited alternative to CRI Sofdec SDK, used for made community localization or community DLC for some classic video games.

## How to Use
Usage:

    SFD_Muxer (-y) [-v [video]]… [-a [audio]]… [-o [output]] (-sfd [sample sfd]) (-s [sofdec stream verson]) (-as [audio offset]) (-l [language])

Option:

    -y:   default overwrite output file.
    -v:   input video filename(mpeg-1 video, less than 16)  
    -a:   input audio filename(SFA/Dolby Digital AC-3/Dobly Digital AIX audio, less than 32)
    -o:   output filename.
    -sfd: sample Sofdec file. Build with this file's parameter. If using this parameter, "-s" and "-as" will be not use.
    -s:   Sofdec stream verson. In the first "private_stream_2" start address + 0x2C, write in ASCII.
    -as:  The start offset value of the audio stream.
          This parameter demonstrate first audio stream's "stream_ID", with +0xC0.
    -l:   language. (e = english[default], c= chinese)
          The code is writing in UTF-8, so must using "chcp 65001" to change terminal codepage when using chinese in windows.

Sample:

    SFD_Muxer -v AT_OP0D.m1v -a AT_OP0D.sfa -a AT_OP0D.ac3 -o AT_OP0D.sfd

## Q&A
1. What is SFA File？

    SFA file is a type of [CRI ADX file](https://wiki.multimedia.cx/index.php/CRI_ADX_file), for the last 6 bytes of padding ("(c)CRI") must in 0x119-0x11F.

2. What is Dobly Digital AIX？

    Dobly Digital AIX is a type of CRI AIX file 。CRI AIX file is a type of Audio containers for multichannel adx.

    Dobly Digital AIX need conformed to constraint conditions below：

    1. Track num = 3 and Phrase num = 1；
    2. All ADX in AIX must be 2 channek and 6 channels of Dolby Digital Surround and tracks within the AIX data correspond as follows:
       | AIX track  | channel       | DoblyDIgital channel          |
       | ---------- | ------------- | ----------------------------- |
       | 1st track  | Left channel  | Front left channel            |
       | 1st track  | Right channel | Front right channel           |
       | 2nd track  | Left channel  | Back left channel             |
       | 2nd track  | Right channel | Back right channel            |
       | 3rd track  | Left channel  | Front center channel          |
       | 3rd track  | Right channel | Low-frequency effects channel |

3. What's the "field"'s mean in "ERROR 2XX" word？

    This field all define in ISO/IEC 11172-1(MPEG-1 Part 1). If need, please read that.

## TODO:
    MPEG-2 video support
    Better SFA/AIX audio surropt
