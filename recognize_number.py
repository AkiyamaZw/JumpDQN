import tensorflow as tf
import numpy as np
import cv2
import os
from sklearn.externals import joblib
from sklearn import svm

def getdata_svm():
    path = "./game/number_data/crop_"
    y = [0,1,2,3,4,5,6,7,8,9]
    x = []
    for i in y:
        paths = path+str(i)+"_gray.jpg"
        img = cv2.imread(paths,-1)
        img = np.reshape(img,[8*10])
        x.append(img)
    return x,y

def svm_lm():
    clf = svm.SVC()
    x,y = getdata_svm()
    x = np.array(x).astype(np.float32)
    x = np.reshape(x,(10,8*10))
    clf.fit(x,y)
    print("learned")
    save_model(clf)
    for i in range(10):
        result = clf.predict(x[i].reshape((1,8*10)))
        print(result)

def is_white(im):
    h,w =im.shape
    for a in range( h):
        for b in range(w):
            if im[a,b]!= 255:
                return False
    return True

def save_model(clf):
    save_path = "./game/svm_model/model.pkl"
    joblib.dump(clf,save_path)

def get_reward(img_list):
    result = []
    model_path = "./game/svm_model/model.pkl"
    clf = joblib.load(model_path)
    for img in img_list:
        #cv2.imshow("goal part",img)
        #cv2.waitKey(0)

        if is_white(img):
            result.append(-1)
            #print("null")
        else:
            x = clf.predict(img.reshape(1,img.shape[0]*img.shape[1]))
            result.append(x)
            #print(x)
        #print(result)
    final_point = 0
    for i in range(3,-1,-1):# from 3 to 0, -1 would not be among it
        mi = 1
        if result[i]!=-1:
            final_point += result[i]*(mi)
            mi *= 10

    #print(final_point)
    return final_point




def test(num):
    model_path = "./game/svm_model/model.pkl"
    clf = joblib.load(model_path)
    x, y = getdata_svm()
    cv2.imshow("s",x[num].reshape((10,8)))
    if is_white(x[num].reshape((10,8))):
        print(x[num].reshape((10,8)))
        print("null")
    else:
        re = clf.predict(x[num].reshape(1, 10*8))
        print(re)
    cv2.waitKey(0)
if __name__ == "__main__":
    test(2)

