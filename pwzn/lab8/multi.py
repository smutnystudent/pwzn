import requests
import os
from PIL import Image
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor

def save_png(name):
    src = "http://if.pw.edu.pl/~mrow/dyd/wdprir/" + name
    rec_img = requests.get(src).content
    with open(name, 'wb') as handler:
        handler.write(rec_img)
    img = Image.open(name)
    bnw = img.convert('L')
    bnw.save(name)

if __name__=='__main__':
    req = requests.get('http://if.pw.edu.pl/~mrow/dyd/wdprir/')
    soup = BeautifulSoup(req.text, 'html.parser')
    alist = soup.find_all('a')
    pool = ProcessPoolExecutor(max_workers=10)
    tasks = []
    for item in alist:
        if ".png" in item.get_text():
            tasks.append(pool.submit(save_png, (item.get_text())))
