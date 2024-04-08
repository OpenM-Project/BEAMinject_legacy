# Windows only for now
import os
import sys
import requests
import argparse
import zipfile
import shutil


parser = argparse.ArgumentParser()
parser.add_argument("asset_type", type=str, default="win64",
                        help="Asset type for release. Default is win64.")
parser.add_argument("download_directory", type=str, default=".", nargs='?',
                        help="Directory to copy upx.exe to. Default is current directory.")
parser.add_argument('-nf', '--nofail', help="Returns exit code 0 on error.", action='store_true')
args = parser.parse_args()
asset_type = args.asset_type
exit_code = 1 - args.nofail
download_dir = args.download_directory

class Unbuffered(object):
   def __init__(self, stream):
        self.stream = stream
   def write(self, data):
        self.stream.write(data)
        self.stream.flush()
   def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()
   def __getattr__(self, attr):
        return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)
print("UPX downloader script")
print("=====================")
try:
    print("= Getting latest release...", end=" ")
    release_data = requests.get("https://api.github.com/repos/upx/upx/releases/latest").json()
    tag_name = release_data["tag_name"]
    assets = release_data["assets"]
    print(f"found UPX {tag_name}!")

    print(f"= Finding {asset_type} asset...", end=" ")
    upx_asset = None
    for asset in assets:
        if asset["name"].endswith(f"-{asset_type}.zip"):
            upx_asset = asset

    if upx_asset:
        upx_rel = os.path.splitext(upx_asset["name"])[0]
        print(f"found {upx_rel}!")
        temp_dir = "temp_upx"
        os.makedirs(temp_dir, exist_ok=True)

        print(f"= Downloading {upx_rel}...", end=" ")
        upx_url = upx_asset["browser_download_url"]
        response = requests.get(upx_url)
        with open(os.path.join(temp_dir, "upx.zip"), "wb") as f:
            f.write(response.content)
        print(f"download done, {len(response.content)} bytes written")

        print("= Extracting UPX release...", end=" ")
        with zipfile.ZipFile(os.path.join(temp_dir, "upx.zip"), "r") as zip_ref:
            zip_ref.extractall(temp_dir)
        print(f"done.")

        upx_exe_path = os.path.join(temp_dir, upx_rel, "upx.exe")
        destination_path = os.path.join(download_dir, "upx.exe")
        shutil.copy(upx_exe_path, destination_path)

        print(f"= UPX executable copied to {os.path.abspath(destination_path)}")
        print("= Cleaning up")
        shutil.rmtree("temp_upx")
    else:
        print(f"\n! No {asset_type} release was found, exiting")
        sys.exit(1)
except Exception as e:
    print(f"\n! Caught exception {e} while processing release, exiting")
    sys.exit(1)
