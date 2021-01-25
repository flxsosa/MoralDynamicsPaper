import pygame
import cv2
import numpy as np
import glob
import os

pygame.init()

def make_video(screen):
    img_num = 0
    while True:
        img_num += 1
        str_num = "00"+str(img_num)
        file_name = "image"+str_num[-3:]+".jpg"
        pygame.image.save(screen,file_name)
        yield

def vid_from_img(name="sim",dir="*.jpg"):
    img_dic = {}
    img_str = []
    size = 0,0
    for filename in glob.glob(dir):
        img = cv2.imread(filename)
        h,w,l =img.shape
        size = (w,h)
        img_str.append(filename)
        img_dic[filename] = img

    out = cv2.VideoWriter(name+'.mp4', cv2.VideoWriter_fourcc(*'DIVX'),60, size)
    img_str.sort()

    for i in img_str:
        out.write(img_dic[i])
    out.release()
    os.system("rm *.jpg")
