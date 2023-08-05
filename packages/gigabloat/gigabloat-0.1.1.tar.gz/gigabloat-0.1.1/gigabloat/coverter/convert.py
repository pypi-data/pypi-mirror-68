import glob
import os
import ntpath
from PIL import Image


class Converter:
    def __init__(self, path):
        self.path = path

    def setup(self, format_from, format_to):
        print(f"Convert files in {self.path} from {format_from} to {format_to}")

    def webpToJpeg(self):
        for file in glob.glob(self.path + "*.webp"):
            try:
                name = ntpath.basename(file).split(".")[0]
                im = Image.open(file).convert("RGB")
                im.save(self.path + name + ".jpg", "jpeg")
                print(file)
                os.rename(file, self.path + "webp/" + name + ".webp")
            except Exception as e:  # pylint: disable=W0703
                print("Something went wrong while converting " + file)
                print(e)
