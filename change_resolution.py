# change_resolution.py
# change the resolution of videos of different actions in different folders

import cv2, os
import shutil
from tqdm import tqdm

# input path, output path and output video type

'''
directory structure:
input_path
├── action1
│   ├── video1_1.mp4
│   ├── video1_2.mp4
│   ├── ...
├── action2
│   ├── video2_1.mp4
│   ├── video2_2.mp4
│   ├── ...
├── ......
'''
# configuration
input_path = '/mnt/data/testing/ISCN_20220708_v2/7' # input directory path
output_path = '/mnt/data/testing/ISCN_20220708_v2/1080/7' # output directory path
output_type = '.avi' # output file type

# list all action directories in the input path
dirs = os.listdir(input_path) 

# every directory in the directory list
for dir in dirs:
    dir_path = input_path + "/" + str(dir) # whole path of a action directory
    videos = os.listdir(dir_path) # all videos of the action
    out = output_path + '/' + dir # output folders
    if not os.path.exists(out):
        os.makedirs(out)
    
    # every file in folders
    for file in videos:
        file_dir_e = dir_path + "/" + str(file)
        print('input: ', file_dir_e)
        file_n = os.path.splitext(file_dir_e)[0]
        filename = file_n.split('/')
        output = out + '/' + filename[-1] + output_type
        print('output: ', output)
        
        # video property 
        cap = cv2.VideoCapture(file_dir_e)
        fps = int(round(cap.get(cv2.CAP_PROP_FPS)))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        #duration = frame_count / fps
        print(
            'fps:', fps, '\n'
            'height*width:', height, '*', width, '\n'
            'frame_count:', frame_count, '\n'
            #'duration:', duration
            )

        if height == 1080:
            shutil.move(file_dir_e, output)
        else: 
            # convert video
            success, _ = cap.read()
            if output_type == '.mp4':
                fourcc = cv2.VideoWriter_fourcc('M','P','4','V')
            else:
                fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
            videowriter = cv2.VideoWriter(output, fourcc, 30, (1080,1920)) # 2k: 2048x1080 1080: 1920x1080 720p: 1280x720
            print('resizing ', file_n)
            with tqdm() as pbar:
                while success:
                    pbar.update()
                    success, img1 = cap.read()
                    try:
                        img1 = cv2.flip(img1, 0)
                        img1 = cv2.flip(img1, 180)
                        img = cv2.resize(img1, (1080,1920), interpolation=cv2.INTER_LINEAR) 
                        videowriter.write(img)
                    except:
                        break
            
            
    
