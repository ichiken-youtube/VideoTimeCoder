import ffmpeg
import sys
import os
try:
    import settings
except ImportError:
    print("settings.py not found. Using default values.")

#音声ビットレート[kbps]
AUDIO_BITRATE = 320
#標準動画ビットレート[kbps]
VIDEO_BITRATE_LIMIT = 3000

#デフォルト設定
FILESIZE_LIMIT = 95 
FRAME_SIZE = (1280, 720) 
FPS = 29.97 
TIMECODE_SIZE = 135
TIMECODE_Y = 100
TEXT = "" 
TEXT_SIZE = 70
TEXT_Y = 280
OUTPUT_DIRECTORY=""
OUTPUT_FILENAME = "output.mp4"

def calc_bitrate(input_path):
    meta = ffmpeg.probe(input_path)
    duration = float(meta['format']['duration'])
    print('Duration : '+str(duration)+'[s]')
    audioSize = AUDIO_BITRATE/8.0*duration
    print('AudioSize : '+str(audioSize)+'[KB]')
    videoSize = FILESIZE_LIMIT*1024 - audioSize
    print('VideoSize : '+str(videoSize)+'[kB]')
    videoBitrate = int(videoSize/duration*8)
    if videoBitrate > VIDEO_BITRATE_LIMIT:
        videoBitrate = VIDEO_BITRATE_LIMIT
    print('VideoBitrate : '+str(videoBitrate)+'[kbps]')
    return videoBitrate

def getTextWidth(font_size,text):
    w=0
    for char in text:
        if ord(char) <= 0x7f:
            # ASCII (半角)
            w += font_size/2
        else:
            # 非ASCII（全角）
            w += font_size
    return w


def add_timecode(input_path, output_path, fps,size,videoBitrate):
    warn_text=TEXT
    warn_fontSize=TEXT_SIZE
    tc_text = '00:00:00:00'
    tc_fontSize = TIMECODE_SIZE
    stream = ffmpeg.input(input_path)
    audio_stream = stream.audio
    (
        stream
        .filter('scale', size[0], size[1])
        .drawtext(timecode=tc_text,timecode_rate=fps,fontfile="C:/Windows/Fonts/msgothic.ttc",fontsize=tc_fontSize, y=TIMECODE_Y, x=(size[0]-getTextWidth(tc_fontSize,tc_text))/2,fontcolor='white',alpha=0.8,borderw=10,bordercolor='#404040')
        .drawtext(text=warn_text,fontfile="C:/Windows/Fonts/msgothic.ttc",fontsize=warn_fontSize, y=TEXT_Y, x=(size[0]-getTextWidth(warn_fontSize,warn_text))/2,fontcolor='white',alpha=0.8,borderw=10,bordercolor='#404040')
        .output(audio_stream,output_path,**{'b:v': str(videoBitrate)+'k'},**{'b:a': str(AUDIO_BITRATE)+'k'})# crfは標準20くらい。大きいほど画質が悪い。
        .run()  
    )

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('ファイルが指定されていません。このファイルを直接起動しないでください。')
        exit(1)
    
    input_path = sys.argv[1]    # 入力動画ファイル名

    try:
        AUDIO_BITRATE = settings.AUDIO_BITRATE
        print('AUDIO_BITRATE='+str(AUDIO_BITRATE))
    except:
        print('AUDIO_BITRATE='+str(AUDIO_BITRATE)+'(Default)')

    try:
        FILESIZE_LIMIT = settings.FILESIZE_LIMIT
        print('FILESIZE_LIMIT='+str(FILESIZE_LIMIT))
    except:
        print('FILESIZE_LIMIT='+str(FILESIZE_LIMIT)+'(Default)')

    try:
        FRAME_SIZE = settings.FRAME_SIZE
        print('FRAME_SIZE='+str(FRAME_SIZE))
    except:
        print('FRAME_SIZE='+str(FRAME_SIZE)+'(Default)')

    try:
        FPS = settings.FPS
        print('FPS='+str(FPS))
    except:
        print('FPS='+str(FPS)+'(Default)')

    try:
        TIMECODE_SIZE = settings.TIMECODE_SIZE
        print('TIMECODE_SIZE='+str(TIMECODE_SIZE))
    except:
        print('TIMECODE_SIZE='+str(TIMECODE_SIZE)+'(Default)')
    
    try:
        TIMECODE_Y = settings.TIMECODE_Y
        print('TIMECODE_Y='+str(TIMECODE_Y))
    except:
        print('TIMECODE_Y='+str(TIMECODE_Y)+'(Default)')

    try:
        TEXT = settings.TEXT
        print('TEXT='+str(TEXT))
    except:
        print('TEXT=""')

    try:
        TEXT_SIZE = settings.TEXT_SIZE
        print('TEXT_SIZE='+str(TEXT_SIZE))
    except:
        print('TEXT_SIZE='+str(TEXT_SIZE)+'(Default)')

    try:
        TEXT_Y = settings.TEXT_Y
        print('TEXT_Y='+str(TEXT_Y))
    except:
        print('TEXT_Y='+str(TEXT_Y)+'(Default)')

    try:
        OUTPUT_DIRECTORY = settings.OUTPUT_DIRECTORY
        print('OUTPUT_DIRECTORY='+str(OUTPUT_DIRECTORY))
    except:
        OUTPUT_DIRECTORY = os.path.dirname(input_path)
        print('OUTPUT_DIRECTORY='+str(OUTPUT_DIRECTORY))
    
    try:
        OUTPUT_FILENAME = settings.OUTPUT_FILENAME
        print('OUTPUT_FILENAME='+str(OUTPUT_FILENAME))
    except:
        orig_filename = os.path.basename(input_path)
        OUTPUT_FILENAME = os.path.splitext(orig_filename)[0]+"_timecoded.mp4"
        print('OUTPUT_FILENAME='+OUTPUT_FILENAME)

    output_path = OUTPUT_DIRECTORY+"/"+OUTPUT_FILENAME  # 出力動画ファイル名
    bitrate = calc_bitrate(input_path)

    if bitrate < 0:
        print('目標サイズでのエンコードができません。')
        exit(1)
    elif bitrate < 250:
        print('動画ビットレートが極端に低くなります。続行しますか？[Y/N]')
        ans = input()
        if 'Y' in ans or 'y' in ans:
            pass
        else:
            exit(1)


    add_timecode(input_path, output_path, fps=FPS, size=FRAME_SIZE, videoBitrate=bitrate)