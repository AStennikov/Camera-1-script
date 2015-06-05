import serial
import sys #operating system library
import os
import time
import cv2
import numpy


print "Camera 1 script"

ser = serial.Serial('/dev/tty.usbserial-FTHAVCC1', 3000000, timeout=1)

#camera is supposed to be ready

#find free filename
file_suffix = 0
while os.path.exists("pics/test%s.png" % str(file_suffix)):
    file_suffix += 1

#set camera parameters
speed = 50
row = 0
column = 0
picture_count = 1 #number of rows that will be made
#1049x1049 is max safe valye
width = 999
height = 999
message = "cmd -nopattern -speed " + str(speed) + " -row " + str(row) + " -column " + str(column) + " -width " + str(width) + " -height " + str(height) + "\n"
print message
ser.write(message)

#now responses come back, read them in. Max 2 lines per every argument
for i in range(0, 30):
    resp = ser.readline()
    if len(resp) > 0:
        print resp[:-2] #don't forget about cutting off line end characters
    else: #quits on first timeout
        break;


#create new opencv image
#image = numpy.zeros(((height+1)/2, picture_count/2, 3), numpy.uint8)


#tell camera to do picture, configure current column as well
message = "cmd -row " + str(0) + " -pic"
print message
ser.write(message + "\n")

#print out responce
timeout = 15;
while True:
    resp = ser.readline()
    if len(resp) > 0:
         print resp[:-2] #don't forget about cutting off line end characters
    else: #quits on first timeout
        timeout = timeout - 1;
        if timeout == 0:
            break;
    if resp[:-2] == "DONE":
        break;
    
#now read picture
print "cmd -getdata"
ser.write("cmd -getdata\n")

#now responses come back, read them in.
resp = ser.readline()   #garbage data
resp = ser.readline()   #garbage data
resp = ser.readline()   #real image size
size = resp[:-2].split(':')
img_width = int(size[1])
img_height = int(size[0])
print size
image = numpy.zeros((img_height, img_width, 3), numpy.uint8)

height_count = 0
width_count = 0
for width_count in range(0, img_width):
    for height_count in range(0, img_height):
    #while True:
        resp = ser.readline()
        if len(resp) > 0:
            #print resp[:-2] #don't forget about cutting off line end characters
            numbers = resp[:-2].split(',')
            #print numbers
            image[height_count, width_count] = (int(numbers[2], 16), int(numbers[1], 16), int(numbers[0], 16))
            #height_count = height_count+1
        else: #quits on first timeout
            break;
    #print height_count, width_count
    percent = width_count*100/height_count
    print str(percent) + "% ready"
    
#save image
cv2.imwrite('pics/test%s.png' % str(file_suffix), image)

#save separate channels as greyscale images as well
b,g,r = cv2.split(image)
cv2.imwrite('pics/test%s_red.png' % str(file_suffix), r)
cv2.imwrite('pics/test%s_green.png' % str(file_suffix), g)
cv2.imwrite('pics/test%s_blue.png' % str(file_suffix), b)


