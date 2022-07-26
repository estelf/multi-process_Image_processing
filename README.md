# video_splitter
当プログラムはffmpegを使用しているので事前にffmpegのパスを通してください。  
Pythonモジュールとしてcv2 , numpyを使用しています。
マルチプロセス、プラグイン機能に対応した画像一括編集・動画切り出しプログラムです。  
具体的な機能として  
* マルチプロセスで高速な変換
* 動画のフレーム切り出しから画像処理まで一時にできるため、分析や機械学習に最適。  
* 動画だけでなく、画像が入ったフォルダでも処理可能。  
* 画像処理部分はプラグインとして、自由に変更可能、自作も可能。
より詳しい使いかたは`python main2.py -h`でヘルプが出てきます。  
plgから始まるスクリプトがプラグインになっています。  
`plg_face_cutter.py`は`shape_predictor_68_face_landmarks.dat`が必要です。  
