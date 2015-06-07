import serial
import sys  # operating system library
import os
import time
import cv
import cv2
import numpy
import camera

print "Camera 1 script"

# find free filename
file_suffix = 0
while os.path.exists("pics/test%s.png" % str(file_suffix)):
    file_suffix += 1

imageWidth = 40
imageHeight = 2000

cam = camera.camera()
cam.setParametersAsString("cmd -row 0 -column 0 -width 39 -height 1999 -speed 2 -bin 0 -rshift 2 -nopattern")
'''cam.setRow(0)
cam.setColumn(0)
cam.setWidth(19)
cam.setHeight(1999)
cam.setSpeed(10)
cam.setBinning(0)
cam.setBarPattern()'''
# image = cam.takePicture()

#take several pictures and merge them together
numberOfImages = 66
image = numpy.zeros(((imageHeight)/2, imageWidth/2*numberOfImages, 3), numpy.uint8)

for i in range(0, numberOfImages):
    cam.setColumn(imageWidth*i)
    print "Image " + str(i+1) + " of " + str(numberOfImages)
    smallImage = cam.takePicture()
    image[0:imageHeight/2, imageWidth/2*i:imageWidth/2*(i+1)] = smallImage

    # image = numpy.concatenate((image, smallImage), axis=1)

# that should rotate image 180 degrees. NOT TESTED
# numpy.rot90(image, 2)

# save image
cv2.imwrite('pics/test%s.png' % str(file_suffix), image)

# save separate channels as greyscale images as well
b, g, r = cv2.split(image)
cv2.imwrite('pics/test%s_red.png' % str(file_suffix), r)
cv2.imwrite('pics/test%s_green.png' % str(file_suffix), g)
cv2.imwrite('pics/test%s_blue.png' % str(file_suffix), b)


'''# camera.init()
ser = serial.Serial('/dev/tty.usbserial-FTHAVCC1', 3000000, timeout=1)

# camera is supposed to be ready

# find free filename
file_suffix = 0
while os.path.exists("pics/test%s.png" % str(file_suffix)):
    file_suffix += 1

# set camera parameters. These will be requested from camera. Actual width and height will be different due to binning.
speed = 50
row = 0
column = 0
binning = 3
# 1999x1249 is max safe value
width = 99 # 1999
height = 99 #1249
message = "cmd -nopattern -bin " + str(binning) + " -speed " + str(speed) + " -row " + str(row) + " -column " + str(
    column) + " -width " + str(width) + " -height " + str(height) + "\n"
# message = "cmd -nopattern -speed " + str(speed) + " -row " + str(row) + " -column " + str(column) + " -width " + str(width) + " -height " + str(height) + "\n"
print message
ser.write(message)

# now responses come back, read them in. Max 2 lines per every argument
for i in range(0, 30):
    resp = ser.readline()
    if len(resp) > 0:
        print resp[:-2]  # don't forget about cutting off line end characters
    else:  # quits on first timeout
        break;


# create new opencv image
# image = numpy.zeros(((height+1)/2, picture_count/2, 3), numpy.uint8)


# tell camera to do picture, configure current column as well
message = "cmd -row " + str(0) + " -pic"
print message
ser.write(message + "\n")

# print out responce
timeout = 15;
while True:
    resp = ser.readline()
    if len(resp) > 0:
        print resp[:-2]  # don't forget about cutting off line end characters
    else:  # quits on first timeout
        timeout -= 1
        if timeout == 0:
            break;
    if resp[:-2] == "DONE":
        break;

# now read picture
print "cmd -getdata"
ser.write("cmd -getdata\n")

# now responses come back, read them in.
resp = ser.readline()  # garbage data
resp = ser.readline()  # garbage data
resp = ser.readline()  # real image size
size = resp[:-2].split(':')
# due to binning, incoming picture is actually smaller than we request. This is why real_ values are introduced
real_width = int(size[0])
real_height = int(size[1])
real_data_length = int(size[2])
print size
image = numpy.zeros((real_height, real_width, 3), numpy.uint8)
print real_width, real_height, real_data_length
print image.shape

height_count = 0
width_count = 0
percent = 0
for height_count in range(0, real_height):
    for width_count in range(0, real_width):
        # while True:
        resp = ser.readline()
        if len(resp) > 0:
            # print resp[:-2] #don't forget about cutting off line end characters
            numbers = resp[:-2].split(',')
            # print numbers
            image[height_count, width_count] = (
                int(numbers[3], 16), (int(numbers[2], 16) + int(numbers[1], 16)) / 2, int(numbers[0], 16))
        else:  # quits on first timeout
            break;
            # print width_count, height_count

    # prints percent transferred only when it changes by more than 5%
    if percent + 5 <= height_count * 100 / real_height:
        percent = height_count * 100 / real_height
        print str(percent) + "% ready"

# save image
cv2.imwrite('pics/test%s.png' % str(file_suffix), image)

# save separate channels as greyscale images as well
b, g, r = cv2.split(image)
cv2.imwrite('pics/test%s_red.png' % str(file_suffix), r)
cv2.imwrite('pics/test%s_green.png' % str(file_suffix), g)
cv2.imwrite('pics/test%s_blue.png' % str(file_suffix), b)'''




