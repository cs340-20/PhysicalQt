from infer import infer
import cv2
import net as posenet

def video_parse(videoPath):
    cap = cv2.VideoCapture(videoPath)
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            pose_scores, key_coor, key_conf = infer(frame)
            #print(pose_scores.shape, key_coor.shape, key_conf.shape)
            #draw_image = posenet.draw_skel_and_kp(frame, pose_scores, key_conf, key_coor, min_pose_score=0.0, min_part_score=0.0)
            #cv2.imshow("faf", draw_image)
            #cv2.waitKey(100)
        else:
            break

if __name__ == '__main__':
    video_parse('../gt/jumping_jack/01edit.mp4')
    video_parse('../gt/jumping_jack/02edit.mp4')
