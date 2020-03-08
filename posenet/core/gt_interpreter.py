import json
import os
import numpy as np
import cv2
import math
from utils import packageCoordinateSet, packageCoordinateSetNormalized, circle_equation

pqLastGoodFrame = 0

def read_in_gt(jsonFilename, root="./"):
    with open(os.path.join(root, jsonFilename), 'r') as jsonFile:
        readJSON = jsonFile.read()
        gtJSON = [json.loads(readJSON)]
    
    meta_blocks = []
    for i in range(len(gtJSON)):
        meta_blocks.append(gtJSON[i][0])
        gtJSON[i] = gtJSON[i][1:]

    for z in range(len(gtJSON)):
        for gt in gtJSON[z]:
            for x,y in gt.items():
                gt[x][2][0] = gt[x][2][0]/meta_blocks[z]['meta']['size'][0]
                gt[x][2][1] = gt[x][2][1]/meta_blocks[z]['meta']['size'][1]
    
    return gtJSON, meta_blocks

def average_pose(gt_frame, exercise_name):
    meta_blocks = []
    for i in range(len(gt_frame)):
        meta_blocks.append(gt_frame[i][0])
        gt_frame[i] = gt_frame[i][1:]

    for z in range(len(gt_frame)):
        for gt in gt_frame[z]:
            for x,y in gt.items():
                gt[x][2][0] = gt[x][2][0]/meta_blocks[z]['meta']['size'][0]
                gt[x][2][1] = gt[x][2][1]/meta_blocks[z]['meta']['size'][1]

def evaluate(input_frame, avg_gt):
    # single tolerance for each joint (change later for more specific tolerance load
    tol_rad = 0.1
   
    # pathway of determining correctness in user 
    # run each frame and analyze each joint:
    # determine radius of tolerance for each joint
    # determine whether user joint is within tolerance
    # if majority of joints are in position it is accepted
    # maybe have prioritized joints in some positions (gt have to be modified)
    # assuming input_frame: {jointName: [COORD], jointName2: [COORD], ...}
    for joint in avg_gt.items(): 
        # tolerance computation
        coord = joint[1][2]
        coord_input = input_frame[joint[0]][2]
        distance = math.sqrt(((coord_input[0]-coord[0])**2)+((coord_input[1]-coord[1]))**2)
        if(circle_equation(coord_input[0], coord_input[1], tol_rad, coord[0], coord[1])):
            print("good")
        #print("joint: %s coord: %f %f coord_input: %f %f distance: %f"%(joint[0], coord[0], coord[1], coord_input[0], coord_input[1], distance))
        print("joint: %s distance: %f"%(joint[0], distance))
    return 0

def display_frame(frame, tolerance=0.1, waittime=100):
    # assume tolerance is single digit for right now:
    side = 500
    base_image = np.zeros((side,side), np.uint8)
    for joint in frame.items():
        true_size = (int(joint[1][2][1]*(side/2)), int(joint[1][2][0]*(side/2))+int(side/2))
        cv2.circle(base_image, true_size, 3, (255,255,255))
    cv2.imshow("fasfa", base_image)
    cv2.waitKey(waittime)


def display_compare(frame1, frame2, tolerance=0.1, waittime=100):
    # assume tolerance is single digit for right now:
    side = 500
    base_image = np.zeros((side,side), np.uint8)
    for joint in frame1.items():
        true_size = (int(joint[1][2][1]*(side/2)), int(joint[1][2][0]*(side/2))+int(side/2))
        cv2.circle(base_image, true_size, 3, (255,255,255))
    
    for joint2 in frame2.items():
        true_size = (int(joint2[1][2][1]*(side/2)), int(joint2[1][2][0]*(side/2))+int(side/2))
        cv2.circle(base_image, true_size, 3, (255,255,255))
    cv2.imshow("fasf", base_image)
    cv2.waitKey(waittime)


if __name__ == '__main__':
    # read_in_gt kept in list for future stacking of diff video frames
    # averaging positions too hard due to difference in positions
    # choosing best single GT right now:
    gt_master, meta = read_in_gt('../gt/jumping_jack/jumping_jack_02.json')
    #average_pose(gt_master, 'jumping_jack')
    
    test_infer = cv2.imread('../gt/jumping_jack/01_infer_test.jpg')
    print("Running with shape", test_infer.shape)
    from infer import infer
    _, scores, coord = infer(test_infer)
     
    test = packageCoordinateSetNormalized(scores, coord, (test_infer.shape))
    #evaluate(test, gt_master[0][0])
    #evaluate(test, test)
    # determine total pose range:
    '''
    for gt_f in gt_master:
        for frame in gt_f:
            display_frame(frame)
    '''

    #display_frame(gt_master[0][0], waittime=10000)
    display_compare(gt_master[0][0], test, waittime=10000)
