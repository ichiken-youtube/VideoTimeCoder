# VideoTimeCorder

# セットアップ
```setup.bat```を実行してください。  
## 手動で実行する場合は
```
winget install ffmpeg
pip install ffmpeg-python
```
を実行し、設定ファイルsettings.pyを作成してください。  

## 設定ファイル
settings.pyに以下の内容が書き込まれている必要があります。
```
FILESIZE_LIMIT = 95 #動画のファイルサイズ上限[MB]
SIZE = (1280, 720) #動画の画面サイズ
FPS = 29.97 #動画のフレームレート
TEXT = "YOUR EYES ONLY!! DO NOT POST!!" #タイムコードの他に任意の文字列を入れられます。
```

# 実行
動画ファイルをバッチファイルにドラッグ&ドロップしてください。  
```output.mp4```というファイルを生成します。  
動画は基本的に3Mbpsでエンコードされます。  
予想ファイルサイズが設定値を超える場合は、映像ビットレートを自動で下げて調整します。  
音声のビットレートは320kbps固定です。