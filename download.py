import os
import sys
import re
import requests
import tempfile
import shutil
import wget
import winreg
import mviewer.extract_mview as exmview
import mviewer.extract_model as emmodel
import aspose.threed as a3d
from fnmatch import fnmatch
from bs4 import BeautifulSoup


class Downloader:
    def __init__(self):
        self.model_url = ""
        self.name = ""
        self.time = ""
        self.temp_path = ""
        self.downloads_dir = ""

    def download(self, page_url):
        self.get_model_url(page_url.strip())
        self.download_file()
        self.extract_model()
        # dst_path = os.path.join(get_downloads_dir(), f"{name}-{time}")
        # if os.path.exists(dst_path):
        #     dst_path = f"{dst_path}.1"

        # while os.path.exists(dst_path):
        #     [dst_path, i] = dst_path.split(".")
        #     i = int(i) + 1
        #     dst_path = f"{dst_path}.{i}"
        # shutil.copytree(dir, dst_path)

    def merge_glb(self):
        files = [
            os.path.join(self.temp_path, name)
            for name in os.listdir(self.temp_path)
            if fnmatch(name, "*.glb")
        ]
        self.downloads_dir = self.get_downloads_dir()
        dst_name = os.path.join(self.downloads_dir, f"{self.name}-{self.time}")
        if os.path.exists(dst_name + ".glb"):
            dst_name = f"{dst_name}.1"

        while os.path.exists(dst_name + ".glb"):
            [dst_name, i] = dst_name.split(".")
            i = int(i) + 1
            dst_name = f"{dst_name}.{i}"

        if len(files) > 1:
            merged_scene = a3d.Scene()
            scenes = [a3d.Scene.from_file(file) for file in files]
            for scene in scenes:
                merged_scene.root_node.merge(scene.root_node)
            merged_scene.save(dst_name + ".glb")
        else:
            shutil.copy(files[0], dst_name + ".glb")
        return self.downloads_dir

    def convert(self):
        files = [
            name
            for name in os.listdir(self.temp_path)
            if fnmatch(name, "*.obj")
        ]
        for file in files:
            scene = a3d.Scene.from_file(os.path.join(self.temp_path, file))
            file_name = ".".join(file.split(".")[0:-1])
            scene.save(os.path.join(self.temp_path, f"{file_name}.glb"))
        return self.temp_path

    def get_downloads_dir(self):
        reg_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",
        )
        # 查询下载文件夹路径
        downloads_path = winreg.QueryValueEx(
            reg_key, "{374DE290-123F-4565-9164-39C4925E467B}"
        )[0]
        # 关闭注册表键
        winreg.CloseKey(reg_key)
        return downloads_path

    def extract_model(self):
        folder = exmview.main(self.temp_path)
        self.temp_path = os.path.join(self.temp_path, folder)
        folder = emmodel.main(self.temp_path)
        return folder

    def download_file(self):
        path = tempfile.gettempdir()
        wget.download(self.model_url, path)
        file_name = wget.filename_from_url(self.model_url)
        self.temp_path = os.path.join(path, file_name)
        return self.temp_path

    def get_model_url(self, url):
        r = requests.get(
            url,
            timeout=15,
        )
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")
        info = soup.find(class_="pop-dialog")
        self.name = info.find(class_="h20").text
        self.time = info.find(class_="h16").text
        pattern = re.compile(
            r"https://img.dpm.org.cn/Uploads/Mview/\S+(?=')",
            re.MULTILINE | re.DOTALL,
        )
        script = soup.find("script", string=pattern)
        if script:
            self.model_url = pattern.findall(script.text)[0]
            return url
        else:
            raise Exception("未找到模型URL！")


if __name__ == "__main__":
    downloader = Downloader()
    downloader.download(sys.argv[1])
    downloader.convert()
    dst_path = downloader.merge_glb()
    print(f"文件已保存到 {dst_path}")
