import imageio
import numpy as np
from scipy import ndimage
#from scipy.misc import imresize
import torchvision.transforms.functional as functional
import torchvision.transforms as transforms
import torch
import os

def load_images():
    #
    path = '/Users/eddie/Desktop/Semester_Project/demo_test/test_images'
    #img_index = [ img_index.append() for item in os.listdir(path)]
    img_index = []
    frame_time = []
    frame_dicts = []
    imgs = os.listdir(path) #os.listdir will mess up the order, hence the following sort function
    imgs.sort(key=lambda x: float(x[4:-4]))

    for item in imgs:
        img_index.append(item)
        time = float(item[4:-4])
        frame_time.append(time)

    files = [os.path.join(path, '{}'.format(item)) for item in img_index]
    frames = [imageio.imread(file) for file in files]

    for i in range(len(frames)):
        frame_dict = {'image' : frames[i], 'frame_time' : frame_time[i]}
        frame_dicts.append(frame_dict)

    return frames, frame_time, frame_dicts

def load_keys():
    keys = []
    path = '/Users/eddie/Desktop/Semester_Project/demo_test/keyboard_logs'
    file_name = os.listdir(path)
    path = path +'/'+ file_name[1]  #1 refers to the test.txt

    with open(path, 'r') as f:
        data = f.readlines()
        for line in data:
            key = line.split(",")
            keys.append(key)
    return keys

def valid_keys(keys):
    key_dicts = []
    for key in keys:
        key[2] = float(key[2])
        key_dict = {'action' : key[0], 'ID' : key[1] , 'keyboard_time' : key[2]}
        key_dicts.append(key_dict)
    return key_dicts

# def time_interval_check(key_pairs):
#     for key_pair in key_pairs:
#
#         key_pair[1]

def find_PRESS_key(key_dicts):
    press_time = []
    for key_dict in key_dicts:
        if (key_dict['action'] == 'PRESS'):
            press_time.append(key_dict['keyboard_time'])

    return press_time


def time_alignment(frame_time,press_time):
    time_pool = []
    #time_flag = 0.0
    start_time = []
    k = 0
    for time1 in press_time:
        for time2 in frame_time[k:]:   #[k:] seems to be useless, it doesn't work in this way, but how to optimize here?
            if (time1 - time2 > 0):
                time_pool.append(time2)
                k += 1
        start_time.append(max(time_pool))
        #time_flag = start_time

    return start_time

def crop_videos(start_time,frame_dicts): # 8 frames per press
    croped_frames_for_all = []
    for time in start_time:
        croped_frames = []
        for i in range(len(frame_dicts)): #same here, we need to optimize this part in order to save time, otherwise soo time consuming.
            if (time == frame_dicts[i]['frame_time']):
                for j in range(8):
                    croped_frames.append(frame_dicts[i+j]['image'])

        croped_frames_for_all.append(croped_frames)

    return croped_frames_for_all

# def alignment(key_pairs,frames):
#
#     for key_pair in key_pairs:
#         # id = key_pair['ID']
#         # action = key_pair['action']
#         # time = key_pair['time']
#         if key_pair['action'] == 'PRESS':
#
#     return


# keys = load_keys()
# print(len(keys))
# # frames = load_images(path)
# # print(len(frames))
# print(keys[0][3])

def save_as_gif(gif_name,croped_frames_for_all,duration = 0.5):
    frames = []
    for i in range(len(croped_frames_for_all[1])):
        frames.append(imageio.imread(croped_frames_for_all[1][i]))
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)

    return

frames, frame_time, frame_dicts = load_images()
keys = load_keys()
key_dicts = valid_keys(keys)
press_time = find_PRESS_key(key_dicts)
start_time = time_alignment(frame_time,press_time)

croped_frames_for_all = crop_videos(start_time,frame_dicts)
print(start_time)
#print(len(result))


imageio.mimsave('gif_test.gif', croped_frames_for_all[3], 'GIF', duration=0.2)