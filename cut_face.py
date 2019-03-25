# -*- coding: utf-8 -*-

import os
import sys
import cv2
import face_recognition

# 设置递归深度
sys.setrecursionlimit(1000000)


def get_face(filepath):
    img = cv2.imread(filepath)

    face_locations = face_recognition.face_locations(img)

    if len(face_locations) == 1:
        # 只处理拥有一个人脸的图片
        (top, right, bottom, left) = face_locations[0]
        # dst = cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 255), 1)

        # 左上坐标：(1,2)	右下坐标：(3,4) face = img[2:4,1:3]
        face = cv2.resize(img[top: bottom, left: right], (128, 128))
        print(''.join(filepath.split('.')[:-1]) + '.png')
        save_face(face, ''.join(filepath.split('.')[:-1]) + '.png')


def show_face(face):
    cv2.imshow('', face)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def save_face(face, filename):
    cv2.imwrite(filename=filename, img=face)


def list_dir(rootdir):
    """遍历目录"""
    files = []
    child_list = os.listdir(rootdir)
    for i in range(len(child_list)):
        path = os.path.join(rootdir, child_list[i])
        if os.path.isdir(path):
            files.extend(list_dir(rootdir))
        if os.path.isfile(path):
            files.append(path.replace('\\', '/'))
    return files


if __name__ == '__main__':
    # for file in list_dir('faces'):
    #     print(file)
    #     get_face(file)
    get_face('faces/4.jpg')