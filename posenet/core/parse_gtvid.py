from infer import infer
import cv2
import net as posenet
import utils

def video_parse(videoPath, exerciseName, idName):
    cap = cv2.VideoCapture(videoPath)
    vidData = []
    fps = cap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    framecounter = 0
    duration = frame_count/fps
    vidMeta = {'total_frames': frame_count, 'length': duration, 'size': (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}
    print(vidMeta) 
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            _, key_coor, key_conf = infer(frame)
            vidData.append((framecounter, key_coor, key_conf))
            framecounter += 1
            print("%s/%s"%(framecounter, frame_count))
        else:
            break
    utils.generateGT(vidData, exerciseName, idName, meta=vidMeta)

def image_parse(imagePath, exerciseName, idName):
    img = cv2.imread(imagePath)
    imgData = []
    frame_count = 1
    duration = 1
    imgMeta = {'total_frames': frame_count, 'length': duration, 'size': (img.shape[1], img.shape[0])}
    print(imgMeta) 
    _, key_coor, key_conf = infer(img)
    imgData.append((1, key_coor, key_conf))
    utils.generateGT(imgData, "%s_img"%exerciseName, idName, meta=imgMeta)


if __name__ == '__main__':
    #video_parse('../gt/jumping_jack/01edit.mp4', 'jumping_jack', '01')
    #video_parse('../gt/jumping_jack/02edit.mp4', 'jumping_jack', '02')
    #image_parse('../gt/jumping_jack/02_infer_test.jpg', 'jumping_jack', '02')
    image_parse('../gt/jumping_jack/03_infer_test.jpg', 'jumping_jack', '03')
