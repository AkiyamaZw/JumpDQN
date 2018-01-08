import matplotlib
import os
import cv2
import numpy as np
import time
import recognize_number as rn

def test():
    #jump(1000)# out of windows
    #jump(100)# a little move
    #jump(1)
    #jump(20)
    #jump(800)
    #jump(900)
    # time ={100,900}
    pass

def main_process(action,last_reward,terminate=False):
    # process action
    if terminate:
        tap_to_start()
        terminate=False

    jump(action)
    time.sleep(2.6)
    # get observer
    observer_path = screencrop()
    observer,goal_crop_path = observer_preprocess(observer_path)
    #cv2.imshow("observer",observer)
    #cv2.waitKey(0)
    #process rewards
    # cut pictureto four part 0,0,0,0
    num = cut_process(goal_crop_path)
    reward=0
    if num[0] == -1:
        reward=last_reward
        terminate = True
        observer = -1
    else:
        reward_now = rn.get_reward(num[1:])
        reward = reward_now - last_reward
    print(reward,terminate)
    return reward, observer,terminate




## cmd
def tap_to_start():
    os.system("adb shell input tap 570 1570")


def jump(time):
    os.system("adb shell input swipe 19 19 19 19 %s" % time)


def screencrop():
    paths = os.getcwd()
    save_path = os.path.join(paths,"test_pic/autojump.png")
    os.system("adb shell screencap -p /sdcard/autojump.png")
    os.system("adb pull /sdcard/autojump.png "+save_path)
    return save_path

## image process
def is_end(img):
    h,w = img.shape
    for i in range(int(h/4)):
        for j in range(int(w/4)):
            if img[i,j] != 0:
                return False
    return True

def cut_process(goal_pic_path):
    img = cv2.imread(goal_pic_path,-1)
    #print(img.shape)
    #print(img)
    if is_end(img):
        return -1,0,0,0,0
    else:
        div = 8
        return 1,img[:,:div],img[:,div:2*div],img[:,2*div:3*div],img[:,3*div:4*div]

def observer_preprocess(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (108, 192))

    img_crop = img[20:30, 11:43]
    img_crop = cv2.cvtColor(img_crop,cv2.COLOR_BGR2GRAY)
    img_crop = black_white(img_crop)

    #cv2.imshow("imgs", img_crop)
    paths = os.getcwd()
    save_path = os.path.join(paths, "test_pic/goal_crop.jpg")
    cv2.imwrite(save_path,img_crop)
    return img,save_path

def black_white(img):
    h,w = img.shape
    for i in range(h):
        for j in range(w):
            if img[i,j] > 128:
                img[i,j] = 255
            else:
                img[i,j] = 0
    return img

def recognizeGoal(path):
    # this part is used to recognizing goal and return the reward
    pass

def recognizeEnd(path):
    # this function is used to recognizing whether game is over
    pass

def jumpgame(action):
    # this function is used to play the game with the "action",and
    # return the terminate, observer, reward
    # reword: num
    # observer: a image
    # terminate: a bool value
    observer = 0
    terminate = 0
    reward = 0
    return reward, observer,terminate
def get_image(filename):
    path = screencrop()
    img = cv2.imread(path)
    img = cv2.resize(img, (108, 192))

    img_crop = img[20:30, 11:19]
    img_crop = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
    img_crop = black_white(img_crop)

    #cv2.imshow("imgs", img_crop)
    #cv2.waitKey(0)
    paths = os.getcwd()
    save_path = os.path.join(paths, "./game/number_data/crop_"+str(filename)+"_gray.jpg")
    cv2.imwrite(save_path, img_crop)

if __name__ == "__main__":
    #screencrop()
    #cropimage()
    #collectnumber("6.png")
    #test()
    #transfer_gray()
    #analaysis()
    main_process(800,terminate=False,last_reward=0)
    #get_image(6)