import serial
import sys  # operating system library
import os
import time
import cv
import cv2
import numpy

class camera:
    serialPort = 0 # serial.Serial('/dev/tty.usbserial-FTHAVCC1', 3000000, timeout=1)

    def __init__(self):
        self.serialPort = serial.Serial('/dev/tty.usbserial-FTHAVCC1', 3000000, timeout=1)

    def test(self):
        self.serialPort.write("cmd -nopattern\n")
        self.printResponse(self)
        print "test complete"

    # prints responses until first timeout
    def printResponse(self):
        while True:
            answer = self.serialPort.readline()
            if len(answer) > 0:
                print answer[:-2]
            else:
                break

    #returns single responce line without [carriage return] and [newline] characters
    def singleResponce(self):
        response = self.serialPort.readline()
        return response[:-2]

    # sets start row. even values only
    def setRow(self, new_value):
        self.serialPort.write("cmd -row " + str(new_value) + "\n")
        self.printResponse()

    # sets start column. even values only
    def setColumn(self, new_value):
        self.serialPort.write("cmd -column " + str(new_value) + "\n")
        self.printResponse()

    # sets image width. odd values only
    def setWidth(self, new_value):
        self.serialPort.write("cmd -width " + str(new_value) + "\n")
        self.printResponse()

    # sets image height. odd values only
    def setHeight(self, new_value):
        self.serialPort.write("cmd -height " + str(new_value) + "\n")
        self.printResponse()

    # sets pixel binning and skip mode. values 0 (no bin&skip), 1 (2x bin&skip), 3 (4x bin&skip) possible
    def setBinning(self, new_value):
        self.serialPort.write("cmd -bin " + str(new_value) + "\n")
        self.printResponse()

    # sets shutterspeed in milliseconds
    def setSpeed(self, new_value):
        self.serialPort.write("cmd -speed " + str(new_value) + "\n")
        self.printResponse()

    # sets vertical monochrome bar pattern
    def setBarPattern(self):
        self.serialPort.write("cmd -barpattern\n")
        self.printResponse()

    # sets red pattern
    def setRedPattern(self):
        self.serialPort.write("cmd -redpattern\n")
        self.printResponse()

    # sets green pattern
    def setGreenPattern(self):
        self.serialPort.write("cmd -greenpattern\n")
        self.printResponse()

    # sets blue pattern
    def setBluePattern(self):
        self.serialPort.write("cmd -bluepattern\n")
        self.printResponse()

    # clear any previous pattern
    def setNoPattern(self):
        self.serialPort.write("cmd -nopattern\n")
        self.printResponse()

    # sets image parameters entered as single string
    def setParametersAsString(self, new_values_string):
        self.serialPort.write(new_values_string + "\n")
        self.printResponse()

    # takes picture with previously defined parameters and returns it as numpy array
    def takePicture(self):
        # tell camera to do picture, configure current column as well
        self.serialPort.write("cmd -pic\n")

        # wait until camera responds with "DONE" message
        timeout = 15;
        while True:
            resp = self.singleResponce()
            if len(resp) > 0:   #prints responce
                print resp
            else:  # quits on first timeout
                timeout -= 1
                if timeout == 0:
                    break;
            if resp == "DONE":
                break;

        #now order camera to transmit picture
        self.serialPort.write("cmd -getdata\n")


        # now responses come back, read them in.
        resp = self.singleResponce()  # garbage data
        resp = self.singleResponce()  # garbage data
        resp = self.singleResponce()  # real image size
        size = resp.split(':')
        # due to binning, incoming picture is actually smaller than we request. This is why real_values are introduced
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
                resp = self.singleResponce()
                if len(resp) > 0:
                    # print resp[:-2] #don't forget about cutting off line end characters
                    numbers = resp.split(',')
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

        return image


# initializes serial port
#def init():
#    ser = serial.Serial('/dev/tty.usbserial-FTHAVCC1', 3000000, timeout=1)

# def setRow(newValue):














