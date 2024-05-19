# TL;DR
Google Drive Public File Downloader Alternative using Selenium
```bash
python gdrive-downloader.py --id {file_id}
```

# INSTALL Chrome binary For Ubuntu Server(x86_64)

```bash
apt update

curl -Lo "/tmp/google-chrome-stable_current_amd64.deb"  https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb & dpkg -i /tmp/google-chrome-stable_current_amd64.deb

apt install -f 

/usr/bin/google-chrome-stable --version
```


# Installation
Change the chromedriver-binary version to match the Chrome binary version in requirements.txt.

Then, run:
```bash
pip install -r requirements.txt
```
current version (chromedriver-binary==125.0.6422.60.0)
# RUN
```bash
python gdrive-downloader.py --id {file_id}
```
{file_id} from google drive url:https://drive.usercontent.google.com/download?id={file_id}&export=download