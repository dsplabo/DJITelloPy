#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from djitellopy import Tello    # DJITelloPyのTelloクラスをインポート
import time                     # time.sleepを使いたいので
import cv2                      # OpenCVを使うため

# メイン関数
def main():
    ### ここにドローンのSSIDを入力
    drone1_ip = ""
    drone2_ip = ""

    # 初期化部
    # Telloクラスを使って，tellというインスタンス(実体)を作る
    tello1 = Tello(drone1_ip, retry_count=1)    # 応答が来ないときのリトライ回数は1(デフォルトは3)
    tello2 = Tello(drone2_ip, retry_count=1)    # 応答が来ないときのリトライ回数は1(デフォルトは3)
    tello1.RESPONSE_TIMEOUT = 0.01   # コマンド応答のタイムアウトは短くした(デフォルトは7)
    tello2.RESPONSE_TIMEOUT = 0.01   # コマンド応答のタイムアウトは短くした(デフォルトは7)

    # Telloへ接続
    tello1.connect()
    time.sleep(0.1)
    tello2.connect()

    current_time = time.time()  # 現在時刻の保存変数
    pre_time = current_time     # 5秒ごとの'command'送信のための時刻変数

    # SDKバージョンを問い合わせ
    sdk_ver = tello1.query_sdk_version()

    # モータとカメラの切替フラグ
    motor_on = False                    # モータON/OFFのフラグ
    camera_dir = Tello.CAMERA_FORWARD   # 前方/下方カメラの方向のフラグ
    
    # 前回強制終了して下方カメラかもしれないので
    if sdk_ver == '30':                                     # SDK 3.0に対応しているか？ 
        tello1.set_video_direction(Tello.CAMERA_FORWARD)     # カメラは前方に
        tello2.set_video_direction(Tello.CAMERA_FORWARD)     # カメラは前方に

    # 画像転送を有効にする
    # tello1.streamoff()   # 誤動作防止の為、最初にOFFする
    # tello2.streamoff()   # 誤動作防止の為、最初にOFFする
    # tello1.streamon()    # 画像転送をONに
    # tello2.streamon()    # 画像転送をONに
    
    # frame_read1 = tello1.get_frame_read()     # 画像フレームを取得するBackgroundFrameReadクラスのインスタンスを作る
    # frame_read2 = tello2.get_frame_read()     # 画像フレームを取得するBackgroundFrameReadクラスのインスタンスを作る

    current_time = time.time()  # 現在時刻の保存変数
    pre_time = current_time     # 5秒ごとの'command'送信のための時刻変数

    # SDKバージョンを問い合わせ
    sdk_ver = tello1.query_sdk_version()

    # モータとカメラの切替フラグ
    motor_on = False                    # モータON/OFFのフラグ
    camera_dir = Tello.CAMERA_FORWARD   # 前方/下方カメラの方向のフラグ
    
    # 前回強制終了して下方カメラかもしれないので
    if sdk_ver == '30':                                     # SDK 3.0に対応しているか？ 
        tello1.set_video_direction(Tello.CAMERA_FORWARD)     # カメラは前方に
        tello2.set_video_direction(Tello.CAMERA_FORWARD)     # カメラは前方に

    time.sleep(0.5)     # 通信が安定するまでちょっと待つ
    
    image = cv2.imread("./white_image.png")

    # ループ部
    # Ctrl+cが押されるまでループ
    try:
        # 永久ループで繰り返す
        while True:

            # (1) 画像取得
            # image1 = frame_read1.frame    # 映像を1フレーム取得しimage変数に格納
            # image2 = frame_read2.frame    # 映像を1フレーム取得しimage変数に格納

            # (2) 画像サイズ変更と、カメラ方向による回転
            # small_image1 = cv2.resize(image1, dsize=(480,360) )   # 画像サイズを半分に変更
            # small_image2 = cv2.resize(image2, dsize=(480,360) )   # 画像サイズを半分に変更

            # if camera_dir == Tello.CAMERA_DOWNWARD:     # 下向きカメラは画像の向きが90度ずれている
                # small_image1 = cv2.rotate(small_image1, cv2.ROTATE_90_CLOCKWISE)      # 90度回転して、画像の上を前方にする
                # small_image2 = cv2.rotate(small_image2, cv2.ROTATE_90_CLOCKWISE)      # 90度回転して、画像の上を前方にする
            # (3) ここから画像処理

            # (4) ウィンドウに表示
            cv2.imshow('OpenCV Window', image)    # ウィンドウに表示するイメージを変えれば色々表示できる
            # cv2.imshow('OpenCV Window', small_image2)    # ウィンドウに表示するイメージを変えれば色々表示できる

            # (5) OpenCVウィンドウでキー入力を1ms待つ
            key = cv2.waitKey(1) & 0xFF
            if key == 27:                   # key が27(ESC)だったらwhileループを脱出，プログラム終了
                break
            elif key == ord('t'):           # 離陸
                tello1.takeoff()
                time.sleep(0.1)
                tello2.takeoff()
            elif key == ord('l'):           # 着陸
                tello1.land()
                time.sleep(0.1)
                tello2.land()
            elif key == ord('w'):           # 前進 30cm
                tello1.move_forward(30)
                time.sleep(0.1)
                tello2.move_forward(30)
            elif key == ord('s'):           # 後進 30cm
                tello1.move_back(30)
                time.sleep(0.1)
                tello2.move_back(30)
            elif key == ord('a'):           # 左移動 30cm
                tello1.move_left(30)
                time.sleep(0.1)
                tello2.move_left(30)
            elif key == ord('d'):           # 右移動 30cm
                tello1.move_right(30)
                time.sleep(0.1)
                tello2.move_right(30)
            elif key == ord('e'):           # 旋回-時計回り 30度
                tello1.rotate_clockwise(30)
                time.sleep(0.1)
                tello2.rotate_clockwise(30)
            elif key == ord('q'):           # 旋回-反時計回り 30度
                tello1.rotate_counter_clockwise(30)
                time.sleep(0.1)
                tello2.rotate_counter_clockwise(30)
            elif key == ord('r'):           # 上昇 30cm
                tello1.move_up(30)
                time.sleep(0.1)
                tello2.move_up(30)
            elif key == ord('f'):           # 下降 30cm
                tello1.move_down(30)
                time.sleep(0.1)
                tello2.move_down(30)
            elif key == ord('p'):           # ステータスをprintする
                print("drone1 : " + tello1.get_current_state())
                time.sleep(0.1)
                print("drone2 : " + tello2.get_current_state())
            elif key == ord('m'):           # モータ始動/停止を切り替え
                if sdk_ver == '30':         # SDK 3.0に対応しているか？
                    if motor_on == False:       # 停止中なら始動 
                        tello1.turn_motor_on()
                        tello2.turn_motor_on()
                        motor_on = True
                    else:                       # 回転中なら停止
                        tello1.turn_motor_off()
                        tello2.turn_motor_off()
                        motor_on = False

            # (6) 10秒おきに'command'を送って、死活チェックを通す
            current_time = time.time()                          # 現在時刻を取得
            if current_time - pre_time > 10.0 :                 # 前回時刻から10秒以上経過しているか？
                tello1.send_command_without_return('command')    # 'command'送信
                time.sleep(0.1)
                tello2.send_command_without_return('command')    # 'command'送信
                pre_time = current_time                         # 前回時刻を更新

    except( KeyboardInterrupt, SystemExit):    # Ctrl+cが押されたらループ脱出
        print( "Ctrl+c を検知" )

    
    if sdk_ver == '30':                                 # SDK 3.0に対応しているか？
        tello1.set_video_direction(Tello.CAMERA_FORWARD) # カメラは前方に戻しておく
        tello2.set_video_direction(Tello.CAMERA_FORWARD) # カメラは前方に戻しておく

    # tello1.streamoff()                                   # 画像転送を終了(熱暴走防止)
    # tello2.streamoff()                                   # 画像転送を終了(熱暴走防止)
    # frame_read1.stop()                                   # 画像受信スレッドを止める
    # frame_read2.stop()                                   # 画像受信スレッドを止める

    # del tello1.background_frame_read                     # フレーム受信のインスタンスを削除    
    # del tello2.background_frame_read                     # フレーム受信のインスタンスを削除   
    del tello1                                           # telloインスタンスを削除
    del tello2                                           # telloインスタンスを削除


# "python3 main_core.py"として実行された時だけ動く様にするおまじない処理
if __name__ == "__main__":      # importされると__name_に"__main__"は入らないので，pyファイルが実行されたのかimportされたのかを判断できる．
    main()    # メイン関数を実行
