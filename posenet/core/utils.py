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

def gen_bounding_box(frame):
    # find (highest x, lowest y)
    # find (lowest x, highest y)
    h_x, h_y, l_x, l_y = 0,0,1000,1000
    for joint in frame.items():
        coord = joint[1][2]
        if(coord[0] >= h_x):
            h_x = coord[0]
        if(coord[0] <= l_x):
            l_x = coord[0]
        if(coord[1] >= h_y):
            h_y = coord[1]
        if(coord[1] <= l_y):
            l_y = coord[1]

    return [(h_x,l_y),(l_x,h_y)]

def circle_equation(x,y,radius, x_offset, y_offset, name=""):
    output_val = ((x-x_offset)**2)+((y-y_offset)**2)
    print("try radius: ", name, output_val, radius**2, output_val <= radius**2)
    if(output_val <= (radius**2)):
        return True
    else:
        return False


