import json
import os
import numpy as np
import cv2
import math
from utils import packageCoordinateSet, packageCoordinateSetNormalized, circle_equation, gen_bounding_box, normalization_fix, bind_pose_loc, scale_pose
from net import constants

pqLastGoodFrame = 0
pqSeekingFrame = 10 # look last 10 frames to determine evaluation

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
                gt[x][2][0] = gt[x][2][0]/meta_blocks[z]['meta']['size'][1]
                gt[x][2][1] = gt[x][2][1]/meta_blocks[z]['meta']['size'][0]
    
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

def evaluate(input_frame, avg_gt, threshold=len(constants.PART_NAMES)-5):
    # single tolerance for each joint (change later for more specific tolerance load
    tol_rad = 0.02
    total_score = 0
    total_parts = len(constants.PART_NAMES)
    achieve_score = threshold/total_parts

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
        distance = math.sqrt(((coord_input[0]-coord[0])**2)+((coord_input[1]-coord[1])**2))
        #print(distance)
        #if(circle_equation(coord_input[0], coord_input[1], tol_rad, coord[0], coord[1], name=joint[0])):
        if distance <= tol_rad:
            total_score += 1 

    #print("total joint score: ", total_score)
    if total_score/total_parts > achieve_score:
        return 1
    else:
        return 0

def display_frame(frame, tolerance=0.025, waittime=100):
    # assume tolerance is single digit for right now:
    side = 500
    base_image = np.zeros((side,side, 3))
    for joint in frame.items():
        true_size = normalization_fix(joint[1][2], side, side) 
        cv2.circle(base_image, true_size, 3, (255,255,255)) 
        cv2.circle(base_image, true_size, int(side*tolerance), (0,255,0), 1)
    bbox = gen_bounding_box(frame, ratio_w=1, ratio_h=1)
    cv2.rectangle(base_image, normalization_fix(bbox[0], side, side), normalization_fix(bbox[1], side, side), (0,0,255), 1)
    cv2.imshow("fasfa", base_image)
    cv2.waitKey(waittime)

def display_compare(frame1, frame2, tolerance=0.025, waittime=1000):
    # assume tolerance is single digit for right now:
    side = 500
    base_image = np.zeros((side,side,3))
    for joint in frame1.items():
        true_size = normalization_fix(joint[1][2], side, side) 
        cv2.circle(base_image, true_size, 3, (255,255,255), -1)
    print("-------")

    for joint2 in frame2.items():
        true_size = normalization_fix(joint2[1][2], side, side)
        cv2.circle(base_image, true_size, 3, (0,0,255), -1)
        cv2.circle(base_image, true_size, int(side*tolerance), (0,255,0), 1)    

    bbox = gen_bounding_box(frame2, ratio_w=1, ratio_h=1)
    cv2.rectangle(base_image, normalization_fix(bbox[0], side, side), normalization_fix(bbox[1], side, side), (0,0,255), 1)
    cv2.imshow("fasf", base_image)
    cv2.waitKey(waittime)


if __name__ == '__main__':
    # read_in_gt kept in list for future stacking of diff video frames
    # averaging positions too hard due to difference in positions
    # choosing best single GT right now:
    gt_master, meta = read_in_gt('../gt/jumping_jack/jumping_jack_02.json')
    gt_master2, meta2 = read_in_gt('../gt/jumping_jack/jumping_jack_img_03.json')
    
    '''
    for i in range(len(gt_master[0])):
        print('output result (0 - reject; 1 - accept):', evaluate(gt_master[0][0], gt_master[0][i]))
    '''
    display_compare(gt_master[0][0], gt_master2[0][0], waittime=-1)
    #display_frame(gt_master2[0][0], waittime=-1)
    #display_frame(gt_master[0][0], waittime=-1)
    
    scale_pose(gen_bounding_box(gt_master[0][0]), gen_bounding_box(gt_master2[0][0]), gt_master[0][0], gt_master2[0][0])
    _out = bind_pose_loc(gt_master[0][0],gt_master2[0][0])
    
    #display_frame(_out, waittime=-1)
    display_compare(gt_master[0][0], _out, waittime=-1)
    display_compare(gt_master[0][0], gt_master2[0][0], waittime=-1)
    # determine total pose range:
    '''
    for gt_f in gt_master:
        for frame in gt_f:
            display_frame(frame)
    '''
