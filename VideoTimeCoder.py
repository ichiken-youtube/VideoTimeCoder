import ffmpeg
import settings
import sys

#音声ビットレート[kbps]
AUDIO_BITRATE = 320
#標準動画ビットレート[kbps]
VIDEO_BITRATE_LIMIT = 3000

def calc_bitrate(input_path):
    meta = ffmpeg.probe(input_path)
    duration = float(meta['format']['duration'])
    print(type(duration))
    print('Duration : '+str(duration)+'[s]')
    audioSize = AUDIO_BITRATE/8.0*duration
    print('AudioSize : '+str(audioSize)+'[KB]')
    videoSize = settings.FILESIZE_LIMIT*1024 - audioSize
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
    warn_text=settings.TEXT
    warn_fontSize=settings.TEXT_SIZE
    tc_text = '00:00:00:00'
    tc_fontSize = settings.TIMECODE_SIZE
    stream = ffmpeg.input(input_path)
    audio_stream = stream.audio
    (
        stream
        .filter('scale', size[0], size[1])
        .drawtext(timecode=tc_text,timecode_rate=fps,fontfile="C:/Windows/Fonts/msgothic.ttc",fontsize=tc_fontSize, y=100, x=(size[0]-getTextWidth(tc_fontSize,tc_text))/2,fontcolor='white',alpha=0.8,borderw=10,bordercolor='#404040')
        .drawtext(text=warn_text,fontfile="C:/Windows/Fonts/msgothic.ttc",fontsize=warn_fontSize, y=280, x=(size[0]-getTextWidth(warn_fontSize,warn_text))/2,fontcolor='white',alpha=0.8,borderw=10,bordercolor='#404040')
        .output(audio_stream,output_path,**{'b:v': str(videoBitrate)+'k'},**{'b:a': str(AUDIO_BITRATE)+'k'})# crfは標準20くらい。大きいほど画質が悪い。
        .run()  
    )

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('ファイルが指定されていません。このファイルを直接起動しないでください。')
        exit(1)

    input_path = sys.argv[1]    # 入力動画ファイル名
    output_path = "output.mp4"  # 出力動画ファイル名
    bitrate = calc_bitrate(input_path)

    add_timecode(input_path, output_path, fps=settings.FPS, size=settings.FRAME_SIZE, videoBitrate=bitrate)