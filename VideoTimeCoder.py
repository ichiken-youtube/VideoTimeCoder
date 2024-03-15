import ffmpeg
import settings
import sys

def add_timecode(input_path, output_path, fps,size):
    stream = ffmpeg.input(input_path)
    audio_stream = stream.audio
    (
        stream
        .filter('scale', size[0], size[1])
        .drawtext(timecode='00:00:00:00',timecode_rate=fps,fontfile="C:/Windows/Fonts/msgothic.ttc",fontsize=128, y=100, x=size[1]-500,fontcolor='white',alpha=0.8,borderw=10,bordercolor='#404040')
        .drawtext(text='文字起こし用\n 投稿禁止',fontfile="C:/Windows/Fonts/msgothic.ttc",fontsize=128, y=220, x=size[1]-500,fontcolor='white',alpha=0.8,borderw=10,bordercolor='#404040')
        .output(audio_stream,output_path,**{'b:v': '3000k'},**{'b:a': '320k'})# crfは標準20くらい。大きいほど画質が悪い。
        .run()  
    )

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('ファイルが指定されていません。このファイルを直接起動しないでください。')
        exit(1)

    input_path = sys.argv[1]    # 入力動画ファイル名
    output_path = "output.mp4"  # 出力動画ファイル名
    add_timecode(input_path, output_path, fps=settings.FPS, size=settings.SIZE)