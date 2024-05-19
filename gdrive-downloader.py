import os
import time
from argparse import ArgumentParser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from anti_useragent import UserAgent
from selenium.webdriver.common.by import By

download_dir = os.getcwd()

# set downloaded chromedriver path
# driver_path = bin_dir + '/chromedriver-linux64/chromedriver'
# service = Service(executable_path=driver_path)
# if using pip install chromedriver_binary
import chromedriver_binary
service = Service()

# ------ ChromeDriver Options ------
options = Options()
# downloaded chrome binary
options.binary_location = '/usr/bin/google-chrome-stable'
# local
# options.binary_location = '/Applications/Chromium.app/Contents/MacOS/Chromium'
options.add_argument('--single-process')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
# options.add_argument("--blink-settings=imagesEnabled=false")                                 # 画像を非表示にする。
options.add_argument("--disable-background-networking")                                      # 拡張機能の更新、セーフブラウジングサービス、アップグレード検出、翻訳、UMAを含む様々なバックグラウンドネットワークサービスを無効にする。
options.add_argument("--disable-blink-features=AutomationControlled")                        # navigator.webdriver=false となる設定。確認⇒　driver.execute_script("return navigator.webdriver")
options.add_argument("--disable-default-apps")                                               # デフォルトアプリのインストールを無効にする。
options.add_argument("--disable-dev-shm-usage")                                              # ディスクのメモリスペースを使う。DockerやGcloudのメモリ対策でよく使われる。
options.add_argument("--disable-extensions")                                                 # 拡張機能をすべて無効にする。
# options.add_argument("--disable-features=DownloadBubble")                                    # ダウンロードが完了したときの通知を吹き出しから下部表示(従来の挙動)にする。
options.add_argument('--disable-features=DownloadBubbleV2')                                  # `--incognito`を使うとき、ダイアログ(名前を付けて保存)を非表示にする。
options.add_argument("--disable-features=Translate")                                         # Chromeの翻訳を無効にする。右クリック・アドレスバーから翻訳の項目が消える。
# options.add_argument("--disable-popup-blocking")                                             # ポップアップブロックを無効にする。
options.add_argument("--headless=new")                                                       # ヘッドレスモードで起動する。
options.add_argument("--hide-scrollbars")                                                    # スクロールバーを隠す。
options.add_argument("--ignore-certificate-errors")                                          # SSL認証(この接続ではプライバシーが保護されません)を無効
# options.add_argument("--incognito")                                                          # シークレットモードで起動する。
options.add_argument("--mute-audio")                                                         # すべてのオーディオをミュートする。
options.add_argument("--no-default-browser-check")                                           # アドレスバー下に表示される「既定のブラウザとして設定」を無効にする。
options.add_argument("--propagate-iph-for-testing")                                          # Chromeに表示される青いヒント(？)を非表示にする。
# options.add_argument("--start-maximized")                                                    # ウィンドウの初期サイズを最大化。--window-position, --window-sizeの2つとは併用不可
# options.add_argument("--test-type=gpu")                                                      # アドレスバー下に表示される「Chrome for Testing~~」を非表示にする。
options.add_argument("--user-agent=" + UserAgent("windows").chrome)                          # ユーザーエージェントの指定。
options.add_argument("--window-size=1280,960")                                              # ウィンドウの初期サイズを設定する。--start-maximizedとは併用不可
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])  # Chromeは自動テスト ソフトウェア~~ ｜ コンソールに表示されるエラー　を非表示
# options.set_capability("browserVersion", "117")                                              # `--headless=new`を使うとき、コンソールに表示されるエラーを非表示にするための必須オプション
prefs = {
    "credentials_enable_service": False,                                                     # パスワード保存のポップアップを無効
    "savefile.default_directory": download_dir,                                              # ダイアログ(名前を付けて保存)の初期ディレクトリを指定
    "download.default_directory": download_dir,                                              # ダウンロード先を指定
    "download_bubble.partial_view_enabled": False,                                           # ダウンロードが完了したときの通知(吹き出し/下部表示)を無効にする。
    "plugins.always_open_pdf_externally": True,                                              # Chromeの内部PDFビューアを使わない(＝URLにアクセスすると直接ダウンロードされる)
}
options.add_experimental_option("prefs", prefs)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--id', required=True, type=str)
    return parser.parse_args()

def wait_for_downloads():
    while any([filename.endswith(".crdownload") for filename in 
               os.listdir(download_dir)]):
        time.sleep(2)
        print(".", end="")


def download_function():
    args = parse_args()
    driver = webdriver.Chrome(service=service, options=options)

    driver.command_executor._commands["send_command"] = (
        "POST",
        '/session/$sessionId/chromium/send_command'
    )
    params = {
        'cmd': 'Page.setDownloadBehavior',
        'params': {
            'behavior': 'allow',
            'downloadPath': download_dir
        }
    }
    driver.execute("send_command", params=params)

    driver.get(f'https://drive.usercontent.google.com/download?id={args.id}&export=download')
    # source = driver.page_source
    if len(driver.find_elements(By.ID, 'uc-download-link')) != 0:
        print("Waiting for downloads", end="")
        driver.find_element(By.ID, 'uc-download-link').click()
        time.sleep(4)
        # not required in headless mode
        wait_for_downloads()
        print("done!")
    else:
        print(driver.page_source)

    driver.quit()

if __name__ == '__main__':
    download_function()


