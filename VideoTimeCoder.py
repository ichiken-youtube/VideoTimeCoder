import ffmpeg
import settings

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
    input_path = "C0032.MP4"    # 入力動画ファイル名
    output_path = "output_ff.mp4"  # 出力動画ファイル名
    size = (1280, 720)  # 出力する動画のサイズ（幅、高さ）
    fps = 29.97  # フレームレート
    add_timecode(input_path, output_path, fps, size)