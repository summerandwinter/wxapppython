import sys
sys.path.insert(0, "..")

from haishoku.haishoku import Haishoku
import requests
from io import BytesIO

def main():
    url = "https://img3.doubanio.com/lpic/s27028282.jpg"
    r = requests.get(url)
    path = BytesIO(r.content)

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