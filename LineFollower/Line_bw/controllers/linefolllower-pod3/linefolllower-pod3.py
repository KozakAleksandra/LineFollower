from controller import Robot
from controller import Camera
from controller import DistanceSensor, Motor
import time
import cv2
import numpy as np
import sys
from controller import Display

def CountSpeed(CountL, CountR):
    #licz różnice pikseli
    if( CountL + CountR < 2000):
        speed = 3
    elif( CountL + CountR < 10100):
        speed = 7
    else:
        speed = 20
    return speed


def run_robot(robot):
    time_step = 32
    max_speed = 0
    step = -1
    
    #camera
    camera = Camera('camera')
    camera.enable(time_step)
    

    #motors
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)
    
    #irsensors
    left_ir = robot.getDevice('IRL')
    left_ir.enable(time_step)
    
    right_ir = robot.getDevice('IRR')
    right_ir.enable(time_step)            
        
       
    # Step simulation
    while robot.step(time_step) != -1:
    
        left_ir_value = left_ir.getValue()
        right_ir_value = right_ir.getValue()
        
        camera.saveImage("cam.png", 20)
        
        #opencv
        
         # Read image
        icv = cv2.imread("cam.png")
        

 

    # Display cropped image


        imCrop = icv[ 400:640, 150:450]
        
        bw = icv[ 400:640, 150:450]
        
        width, height = 300, 140
        x1, y1 = 150, 0
        x2, y2 = 150, 240
        line_thickness = 2
        cv2.line(bw, (x1, y1), (x2, y2), (0, 255, 0), thickness=line_thickness)
        
        cv2.imwrite( 'cam.png', imCrop) 
  
        (thresh, blackAndWhiteImage) = cv2.threshold(bw, 127, 255, cv2.THRESH_BINARY)
        cv2.imwrite( 'bw.png', blackAndWhiteImage) 
        
        
        bwcount = cv2.imread("bw.png", 0)
        zeros = 72000 - cv2.countNonZero(bwcount)
        print ("liczba czarnych pikseli: ", zeros)
        

        # Cut the image in half
        left1 = bwcount[:, 0:150]
        right1 = bwcount[:, 150:300]
        
        One_left = 36000 - cv2.countNonZero(left1)
        One_right = 36000 - cv2.countNonZero(right1)
        print ("liczba czarnych pikseli po lewej: ", One_left, " po prawej: ", One_right)
 
        
        #display
        display = Display('display')
        display = robot.getDevice('display')
        img = display.imageLoad('bw.png')
        coords = [0, 0, 0, 0]
        frame_xy = [[x1, y1] for x1 in coords
                                  for y1 in coords]
        frames = len(frame_xy)
        frame = step % frames
        pos = frame_xy[frame]
    
        display.imagePaste(img, pos[0], pos[1], False)
          

        max_speed = CountSpeed(One_left, One_right)
        
        
        print("left: {}  right: {} ".format( left_ir_value, right_ir_value))
        
        
        left_speed = max_speed * 0.25
        right_speed = max_speed * 0.25
        
        if (left_ir_value > right_ir_value) and (6 < left_ir_value < 14):
            print("Go left")
            left_speed = -max_speed * 0.25
        elif (right_ir_value > left_ir_value) and (4 < right_ir_value < 14):
            print("Go right")
            right_speed = -max_speed * 0.25
        
        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)
    
    
if __name__ == "__main__":
    
    my_robot = Robot()
    run_robot(my_robot)
