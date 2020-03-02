import json
import os
import numpy as np
import cv2

def read_in_gt(root="./"):
    gt_collection = []
    for _, _, files in os.walk(root):
        for f in files:
            if len(f) >= 5:
                if f[-5:] == '.json':
                    with open(f,'r') as jsonFile:
                        readJSON = jsonFile.read()
                        gtJSON = json.loads(readJSON)
                        gt_collection.append(gtJSON)
    return gt_collection

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
    
    #averaged_poses = []


    # determine total pose range:
    for gt_f in gt_frame:
        for frame in gt_f:
            display_frame(frame)
    

def evaluate(input_frame, avg_gt):
    # single tolerance for each joint (change later for more specific tolerance load
    tolerance = 0.1
   
    # pathway of determining correctness in user 

    return 0

def display_frame(frame, tolerance=0.1):
    # assume tolerance is single digit for right now:
    side = 100
    base_image = np.zeros((side,side), np.uint8)
    for joint in frame.items():
        true_size = (int(joint[1][2][1]*(side/2)), int(joint[1][2][0]*(side/2))+int(side/2))
        cv2.circle(base_image, true_size, 3, (255,255,255))
    cv2.imshow("fasfa", base_image)
    cv2.waitKey(100)

if __name__ == '__main__':
    gt_master = read_in_gt()
    average_pose(gt_master, 'jupming_jack')
