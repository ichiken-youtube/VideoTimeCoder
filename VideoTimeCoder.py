import ffmpeg
import settings
import sys

#音声ビットレート[kbps]
AUDIO_BITRATE = 320
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

def add_timecode(input_path, output_path, fps,size,videoBitrate):
    stream = ffmpeg.input(input_path)
    audio_stream = stream.audio
    (
        stream
        .filter('scale', size[0], size[1])
        .drawtext(timecode='00:00:00:00',timecode_rate=fps,fontfile="C:/Windows/Fonts/msgothic.ttc",fontsize=135, y=100, x=size[1]-500,fontcolor='white',alpha=0.7,borderw=10,bordercolor='#404040')
        .drawtext(text='文字起こし用\n　投稿禁止',fontfile="C:/Windows/Fonts/msgothic.ttc",fontsize=135, y=280, x=size[1]-500,fontcolor='white',alpha=0.7,borderw=10,bordercolor='#404040')
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

    add_timecode(input_path, output_path, fps=settings.FPS, size=settings.SIZE, videoBitrate=bitrate)