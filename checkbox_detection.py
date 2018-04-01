
# coding: utf-8

# In[1]:


import cv2
from PIL import Image
import numpy as np

im = cv2.imread('Page1.jpg')
small = cv2.resize(im, (0,0), fx=0.5, fy=0.5) 

imgray = cv2.cvtColor(small,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

print("total contours detected")
print(len(contours))

#print(contours[1497])
#print(contours[1000])   #prints the coordinates of contour

square_contours=[]
filled_square_contours=[]
checked_square_contours=[]

for c in range(1,1560):
	# approximate the contour
	peri = cv2.arcLength(contours[c], True)
	approx = cv2.approxPolyDP(contours[c], 0.02 * peri, True)

	# if our approximated contour has four points, then its a perfect square
    # if our approximated contour has more than four points, then its a distorted square including the ticked ones
	if len(approx) >= 4:
		(x, y, w, h) = cv2.boundingRect(approx)
		ar = w / float(h)      #aspect ratio i.e ration of length and width
		res1 = cv2.rectangle(small.copy(), (x,y),(x+w,y+h), (0,0,255),2)
		res2 = small[y:y+h,x:x+w]
		cv2.imwrite("result2.png", res2)  #image inside the contours[c] stored separately
		res2=Image.open("result2.png")
		basewidth=400
		wpercent = (basewidth/float(res2.size[0]))
		hsize = int((float(res2.size[1])*float(wpercent)))
		res2 = res2.resize((basewidth,hsize), Image.ANTIALIAS)  #image has been resized for further working on it
		res2.save('resized.jpg') 
		res2=cv2.imread("resized.jpg")
		count=0
		black_point=[0,0,0]
		for i in range(hsize):
		    for j in range(basewidth):
        		k = res2[i,j]      #k is the pixel values of image
        		#print k
        		if(all(x <= 100 for x in k)):  #those images with some k having rgb close to black, are not pure white
                                               #i.e. they are either checked or filled with some value. they are nt empty images
					count+=1
		#extrema = res2.convert("L").getextrema()  #extrema checks if the image is complete white or complete black
# a square will have an aspect ratio that is approximately equal to one, otherwise, the shape is a rectangle
		if (ar >= 0.75 and ar <= 1.25):
			#y=contours[c][:, 0]
			if(cv2.contourArea(contours[c])>130 and cv2.contourArea(contours[c])<350):   #Area enclosed within checkboxes lie in (130,350)           
				if(len(approx)>4):  
					checked_square_contours.append(c)
				if count<20:
					square_contours.append(c)
				else:
					square_contours.append(c)
					filled_square_contours.append(c)
                    
#checking if contours[1000] is filled or not
res1 = cv2.rectangle(small.copy(), (64,377),(80,391), (0,0,255),2)
res2 = small[64:80,377:391]
cv2.imwrite("result2.png", res2)
# cnt=contours[1497]
# mask = np.zeros(res2.shape[:2],np.uint8)
# mean = cv2.mean(res2,mask)
# print(mean)
res2=Image.open("result2.png")
basewidth=400
wpercent = (basewidth/float(res2.size[0]))
hsize = int((float(res2.size[1])*float(wpercent)))
res2 = res2.resize((basewidth,hsize), Image.ANTIALIAS)
res2.save('resized.jpg') 
res2=cv2.imread("resized.jpg")
# TotalNumberOfPixels = basewidth * hsize;
# ZeroPixels = TotalNumberOfPixels - cv2.CountNonZero(cv2.imread("resized.jpg"));
# print("number of zero pixels in contour 1000:", ZeroPixels)
count=0
black_point=[0,0,0]
for i in range(hsize):
    for j in range(basewidth):
        k = res2[i,j]
        #print k
        if(all(x <= 100 for x in k)):
            count+=1
if count>2:
    print("filled")

print("total square_contours detected:",len(square_contours))
print(square_contours)
print("\n")
print("total filled_square_contours detected:",len(filled_square_contours))
print(filled_square_contours)
print("\n")
print("total checked_square_contours detected:",len(checked_square_contours))
print(checked_square_contours)
           
# area0 = cv2.contourArea(contours[1000])
# area1 = cv2.contourArea(contours[1497])
# area2 = cv2.contourArea(contours[8])
# print(area0,area1,area2)

