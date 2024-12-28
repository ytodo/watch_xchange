import subprocess
import requests
import time

# WEBサーバーにアクセスしてhtmlコードを取得する
def fetch_html_from_server(port):

    # 監視するURLを構成する
    url = 'http://127.0.0.1' + ':' + port

    try:
        # requestsを送信して200(リクエスト成功)が返ったらその内容を取得
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            return html_content

        # もしエラーが返ったらその内容を表示（コンソールで起動している時のみ）
        else:
            print(f"サーバーからのレスポンスコードがエラーです: {response.status_code}")
            return None
    except:
        print("Get nothing..")
        return None

# 取得したhtmlコード内にターゲットの文字が有るかチェックする
def check_status(fetched_html, target_string):

    # もし文字列が存在したらrpi-xchangeをリスタート
    if target_string in fetched_html:

        if (os_id == "debian"):
            msg_mlt = "rpi-multi_forward をリスタートします。"
            msg_xch = "rpi-xchange をリスタートします。"
            cmd_mlt = 'sudo systemctl restart rpi-multi_forward.service'
            cmd_xch = 'sudo systemctl restart rpi-xchange.service'
        else:
            msg_mlt = "multi_forward をリスタートします。"
            msg_xch = "xchange をリスタートします。"
            cmd_mlt = 'sudo systemctl restart multi_forward.service'
            cmd_xch = 'sudo systemctl restart xchange.service'

        print(msg_mlt)
        subprocess.run(cmd_mlt, shell=True)
        time.sleep(5)

        print(msg_xch)
        subprocess.run(cmd_xch, shell=True)

# OSの種類を取得
def get_os_id():

    # OS変数の初期化
    os_id = None

    # OSの種類を取得してos_idに代入する
    try:
        with open('/etc/os-release', 'r') as file:
            for line in file:
                if line.startswith('ID='):
                    os_id = line.strip().split('=')[1].strip('"')
                    break
    # OS種類が取得できない時
    except FileNotFoundError:
        os_id = "Unknown"

    return os_id

if __name__ == "__main__":

    # OSを取得
    os_id = get_os_id()

    # OS特有のポートを代入（独自のポートを設定した時は変更する）
    if (os_id == "debian"):
        port = '20202'                   # 監視するポート番号
    else:
        port = '20202'                   # ポートはブログどおりに設定した場合Alma:8081

    # WEB表示を監視したい文字列
    target_string = "Not Running"
    count = 0

    # 監視開始(シャットダウン・リブート又は[Ctrl] + [c]でのみ終了
    print("ポート:", port, "を監視しています。")

    while True:

        # 取得したhtmlを変数に代入
        fetched_html = fetch_html_from_server(port)

        # 変数が空で無ければ
        if fetched_html:

            # 内容を検査
            check_status(fetched_html, target_string)

        # リクエスト送信の間隔を設定する。(10sec)
        time.sleep(10)
