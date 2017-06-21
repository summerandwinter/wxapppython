import sys
sys.path.insert(0, "..")

from haishoku.haishoku import Haishoku
import requests
from io import BytesIO
from PIL import Image

def main():
    url = "https://y.gtimg.cn/music/photo_new/T002R300x300M000000mbhaG00NiAJ.jpg"
    r = requests.get(url)
    path = BytesIO(r.content)

    image  = Image.open(path)
    p = image.getpalette();
    print(p)
    # getPalette api
    palette = Haishoku.getPalette(path)
    print(palette)

    # getDominant api
    dominant = Haishoku.getDominant(path)
    print(dominant)

    # showPalette api
    Haishoku.showPalette(path)

    # showDominant api
    Haishoku.showDominant(path)

    # Haishoku object
    h = Haishoku.loadHaishoku(path)
    print(h.palette)
    print(h.dominant)

if __name__ == "__main__":
    main()