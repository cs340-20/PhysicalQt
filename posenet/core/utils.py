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

def compare():
    return 0
