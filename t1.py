import numpy as np
import cv2
import time

imgLena = cv2.imread('lena.jpg',cv2.IMREAD_GRAYSCALE)#以灰度的方式读取lena.jpg
imgNbe = cv2.imread('nbe.jpg')#不支持读中文，所以将诺贝尔.jpg改成nbe.jpg
h = imgLena.shape[0]#获得图片的高度
w = imgLena.shape[1]#获得图片的宽度

cv2.namedWindow('image', cv2.WINDOW_NORMAL)#将要展示图片的窗口命名为image

cv2.imshow('image',imgNbe)#展示图片nbe.jpg
cv2.imshow('image',imgLena)#展示图片lena.jpg，实际上不起作用

imgMixed = imgNbe#因为实在nbe.jpg的基础上改变图片，所以先把nbe.jpg赋值给混合图片

#判断现在所在的圆圈范围
def isInCircle(x,y,r):
	if(x-w//2)**2+(y-h//2)**2 < r**2:
		return 1
	else:
		return 0

r = 0
#250长度随便给的，可以给h/2的与根号2的乘积，应该是正好
while r<250:
	r+=10#每帧半径变大10
	for i in range(0,h-1):
		for j in range(0,w-1):
			if(isInCircle(i,j,r) == 1):
				imgMixed[i,j] = imgLena[i,j]#如果在圆圈范围内，就把lena.jpg的像素值赋值给混合图片

	cv2.imshow('image',imgMixed)#打印混合图片
	if(cv2.waitKey(1) == 27):#如果是waitKey(0)的话，任意按键结束，waitKey(1)指定按键结束，27代表ESC
		break

cv2.destroyAllWindows()#关闭所有窗口