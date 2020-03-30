import numpy as np
import csv
from net import constants
import json

def generateGT(poseMasterObj, exerciseName, exerciseID, meta=None):
    masterOut = []
    with open("%s_%s.json"%(exerciseName, exerciseID), 'w') as jsonFile:
        if(meta != None):
            trueMeta = {'meta': meta}
            masterOut.append(trueMeta)
        else:
            print("Warning! You are creating an exercise without metadata. There might be problems later on when you are parsing this exercise!")

        for poseObj in poseMasterObj:
            frame, keypoint_scores, keypoint_coords = poseObj
            setmate = {}
            for part in range(len(constants.PART_NAMES)):
                setmate[constants.PART_NAMES[part]] = (frame, keypoint_scores[0,part],list(keypoint_coords[0, part, :]))
            masterOut.append(setmate)

        jsonOutput = json.dumps(masterOut, indent=4)
        jsonFile.write(jsonOutput) 

def packageCoordinateSet(rawCoordScores, rawCoordPoints):
    setmate = {}
    for part in range(len(constants.PART_NAMES)):
        setmate[constants.PART_NAMES[part]] = (rawCoordScores[0,part], rawCoordPoints[0, part, :])
    return setmate

def packageCoordinateSetNormalized(rawCoordScores, rawCoordPoints, image_size):
    #image_size = (width, height)
    width, height = image_size[0], image_size[1]
    setmate = packageCoordinateSet(rawCoordScores, rawCoordPoints)
    newmate = {}
    for part in setmate.items():
        newmate[part[0]] = (-1, part[1][0], [part[1][1][0]/width, part[1][1][1]/height])
    return newmate

def gen_bounding_box(frame, ratio_w=1, ratio_h=1):
    l_x, l_y, s_x, s_y = 0,0,1_000_000, 1_000_000
    
    for joint in frame.items():
        print(joint)
        coord = joint[1][2]
        print(coord)
        if l_x < coord[0]:
            l_x = coord[0]
        if l_y < coord[1]:
            l_y = coord[1]
        if s_x > coord[0]:
            s_x = coord[0]
        if s_y > coord[1]:
            s_y = coord[1]

    print(s_x, l_x, s_y, l_y)
    return [(s_x*ratio_w, s_y*ratio_h), (l_x*ratio_w, l_y*ratio_h)]
    
def circle_equation(x,y,radius, x_offset, y_offset, name=""):
    output_val = ((x-x_offset)**2)+((y-y_offset)**2)
    print("try radius: ", name, output_val, radius**2, output_val <= radius**2)
    if(output_val <= (radius**2)):
        return True
    else:
        return False

def normalization_shift(coordinate, side_x, side_y):
    return (int(coordinate[1]*(side_x/1.5)), int(coordinate[0]*(side_y/1.5))+int(side_y/1.5))

def normalization_fix(coordinate, side_x, side_y):
    return (int(coordinate[1]*(side_x/2)), int(coordinate[0]*(side_y/2))+int(side_y/2))

# use with gen_bounding_box:
def get_bbx_size(coord_box):
    l_x, l_y = coord_box[0]
    h_x, h_y = coord_box[1]
    # (w,h)
    return (int(h_x-l_x), int(h_y-l_y))

# fix the scaling issue based on bounding box:
def fix_pose(bbox1, bbox2, pose):
    # bbox1 -> box 
    return 0

def bind_pose_loc(pose1, pose2):
    # transformation of pose2 to anchor at pose1's [tbd joint]
    # i'm thinking left ankle
    p1_left_ankle = pose1['leftAnkle']
    p2_left_ankle = pose2['leftAnkle']
    init_dist_x = p1_left_ankle[2][0] - p2_left_ankle[2][0]
    init_dist_y = p1_left_ankle[2][1] - p2_left_ankle[2][1]

    # get offsets based on p2_left_ankle
    # offset - {'joint_name': [x_offset, y_offset]}
    offsets = {joint[0]:[p2_left_ankle[2][0]-joint[1][2][0], p2_left_ankle[2][1]-joint[1][2][1]] for joint in pose2.items()}
    
    # change joints based on offsets:
    # set pose2's left ankle to pose1's
    #pose2['leftAnkle'][2] = pose1['leftAnkle'][2]

    export_pose2 = dict()

    for offset in offsets.items():
        #print(offset)
        #print(pose2[offset[0]][0], pose2[offset[0]][1], p1_left_ankle[2][0])
        export_pose2[offset[0]] = [
                    pose2[offset[0]][0],
                    pose2[offset[0]][1],
                    [
                        p1_left_ankle[2][0]-offset[1][0],
                        p1_left_ankle[2][1]-offset[1][1]
                    ]
                ]

    print(export_pose2)
    return export_pose2
