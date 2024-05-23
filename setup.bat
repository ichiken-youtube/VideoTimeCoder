@echo off

echo Installing ffmpeg...
winget install ffmpeg

echo Installing Libraries...
pip install ffmpeg-python

echo Generating setting file...
if not exist settings.py (
    echo FILESIZE_LIMIT = 95 > settings.py
    echo FRAME_SIZE = ^(1280, 720^) >> settings.py
    echo FPS = 29.97 >> settings.py
    echo TIMECODE_SIZE = 135  >> settings.py
    echo TEXT = ^"YOUR EYES ONLY!! DO NOT POST!!^" >> settings.py
    echo TEXT_SIZE = 70 >> settings.py
) else (
    echo settings.py already exists.
)
pause