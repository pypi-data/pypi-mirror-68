import cv2
import numpy as np
import urllib.request
import os
import time

def download(url,path):
    """The image in the above URl will be downloaded to the path.\nPath should include name\nex : C/User/pc/Desktop/img.png"""
    imglink=urllib.request.urlopen(url)
    imgNp=np.array(bytearray(imglink.read()))
    img = cv2.imdecode(imgNp,-1)
    cv2.imwrite(path,img)
    
def download_bulk(txt_file,folder = "default"):
    if folder == "default":
        folder = os.getcwd()+"images/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(txt_file) as file:
        for url in file:
            download(url,folder+"/"+str(time.time())+".png")
