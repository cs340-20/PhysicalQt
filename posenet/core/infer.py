import tensorflow as tf
import cv2
import time
import os
import net as posenet
import utils

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)

try:
    os.getcwd().index('posenet')
    posenet_path = './_models/model-mobilenet_v1_101.pb'
except Exception as e:
    posenet_path = '../posenet/core/_models/model-mobilenet_v1_101.pb'

model_cfg, model_outputs = posenet.simple_load_model(posenet_path, sess)
output_stride = model_cfg['output_stride']

#def infer(imgPath):
def infer(imgMatrix):
    input_image, draw_image, output_scale = posenet.read_imgfile(
            imgMatrix, scale_factor=1.0, output_stride=output_stride)

    heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess.run(
            model_outputs,
            feed_dict={'image:0': input_image}
            )
    
    pose_scores, keypoint_scores, keypoint_coords=posenet.decode_multiple_poses(
            heatmaps_result.squeeze(axis=0),
            offsets_result.squeeze(axis=0),
            displacement_fwd_result.squeeze(axis=0),
            displacement_bwd_result.squeeze(axis=0),
            output_stride = output_stride,
            max_pose_detections = 1,
            min_pose_score = 0.0)
    keypoint_coords *= output_scale

    '''
    draw_image = posenet.draw_skel_and_kp(
            draw_image, pose_scores, keypoint_scores, keypoint_coords,
            min_pose_score=0.0, min_part_score=0.01)
    '''
    #cv2.imwrite(os.path.join("./output", os.path.relpath(imgPath, "./images")), draw_image)
    #cv2.imwrite('./output/demo1.jpg', draw_image)
    #cv2.imshow("fasf", draw_image)
    #cv2.waitKey(10)

    '''
    print("Results for image: %s" % imgPath)
    for pi in range(len(pose_scores)):
        if pose_scores[pi] == 0.:
            break
        print('Pose #%d, score = %f' % (pi, pose_scores[pi]))
        for ki, (s, c) in enumerate(zip(keypoint_scores[pi, :], keypoint_coords[pi, :, :])):
            print('Keypoint %s, score = %f, coord = %s' %
                  (posenet.PART_NAMES[ki], s, c))
    '''
    return (1, keypoint_scores, keypoint_coords)

if __name__ == "__main__":
    #img = cv2.imread('./images/demo1.jpg')
    #infer("./images/demo1.jpg")
    img = cv2.imread("./images/demo1.jpg")
    output = infer(img)
    utils.generateGT(output)
