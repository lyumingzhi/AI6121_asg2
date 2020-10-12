import numpy as np
from PIL import Image
import cv2 
def Median_filtering(image,window_size):   #image为传入灰度图像，window_size为滤波窗口大小
    high, wide = image.shape
    img = image.copy()
    mid = (window_size-1) // 2
    med_arry = []
    for i in range(high-window_size):
        for j in range(wide-window_size):
            for m1 in range(window_size):
                for m2 in range(window_size):
                    med_arry.append(int(image[i+m1,j+m2]))

            # for n in range(len(med_arry)-1,-1,-1):
            med_arry.sort()   				#对窗口像素点排序
            # print(med_arry)
            img[i+mid,j+mid] = med_arry[(len(med_arry)+1) // 2]        #将滤波窗口的中值赋给滤波窗口中间的像素点
            del med_arry[:]
    # print("结束")
    Image.fromarray(np.asarray(img)).save('tmp.png')
imgl=Image.open('disparity_map_l.jpg').convert('L')
Median_filtering(np.asarray(imgl),3)