import torch
from torch.utils.data import Dataset
from torchvision import transforms
import torchvision.transforms.functional as tf

import os
import sys
import linecache
import random
import numpy as np
from PIL import Image
from skimage import io

## siamese-triplet for training
class triTrainDataset(Dataset):
    def __init__(self, txt, pair_num=None, transform=None):
        self.txt = txt
        self.transform = transform

        fr = open(self.txt, 'r')
        self.building_num = len(fr.readlines())
        fr.close()

        if pair_num is not None:
            self.pair_num = pair_num
        else:
            self.pair_num = self.building_num

    def __getitem__(self, index):
        anchor = linecache.getline(self.txt, (index % self.building_num) + 1).strip('\n')
        anchor_folder = os.listdir(anchor)
        anchor_id = random.randint(0, len(anchor_folder)-1)
        anchor_img = anchor + '/' + anchor_folder[anchor_id]
        while True:
            positive_id = random.randint(0, len(anchor_folder)-1)
            if positive_id != anchor_id:
                positive_img = anchor + '/' + anchor_folder[positive_id]
                break

        while True:
            negative = linecache.getline(self.txt, random.randint(1, self.building_num)).strip('\n')
            if negative != anchor:
                negative_folder = os.listdir(negative)
                negative_id = random.randint(0, len(negative_folder)-1)
                negative_img = negative + '/' + negative_folder[negative_id]
                break

        anchor_img = Image.open(anchor_img)
        positive_img = Image.open(positive_img)
        negative_img = Image.open(negative_img)

        if anchor_img.mode != "RGB":
            origin = anchor_img
            anchor_img = Image.new("RGB", origin.size)
            anchor_img.paste(origin)
        if positive_img.mode != "RGB":
            origin = positive_img
            positive_img = Image.new("RGB", origin.size)
            positive_img.paste(origin)
        if negative_img.mode != "RGB":
            origin = negative_img
            negative_img = Image.new("RGB", origin.size)
            negative_img.paste(origin)

        if self.transform is not None:
            anchor_img = self.transform(anchor_img)
            positive_img = self.transform(positive_img)
            negative_img = self.transform(negative_img)

        return anchor_img, positive_img, negative_img

    def __len__(self):
        return self.pair_num

## randomRotate-triplet for training
class triRotTrainDataset(Dataset):
    def __init__(self, txt, pair_num=None, transform=None):
        self.txt = txt
        self.transform = transform

        fr = open(self.txt, 'r')
        self.building_num = len(fr.readlines())
        fr.close()

        if pair_num is not None:
            self.pair_num = pair_num
        else:
            self.pair_num = self.building_num

    def __getitem__(self, index):
        anchor = linecache.getline(self.txt, (index % self.building_num) + 1).strip('\n')
        anchor_folder = os.listdir(anchor)
        anchor_id = random.randint(0, len(anchor_folder)-1)
        anchor_img = anchor + '/' + anchor_folder[anchor_id]
        while True:
            positive_id = random.randint(0, len(anchor_folder)-1)
            if positive_id != anchor_id:
                positive_img = anchor + '/' + anchor_folder[positive_id]
                break

        while True:
            negative = linecache.getline(self.txt, random.randint(1, self.building_num)).strip('\n')
            if negative != anchor:
                negative_folder = os.listdir(negative)
                negative_id = random.randint(0, len(negative_folder)-1)
                negative_img = negative + '/' + negative_folder[negative_id]
                break

        anchor_img = Image.open(anchor_img)
        positive_img = Image.open(positive_img)
        negative_img = Image.open(negative_img)

        if anchor_img.mode != "RGB":
            origin = anchor_img
            anchor_img = Image.new("RGB", origin.size)
            anchor_img.paste(origin)
        if positive_img.mode != "RGB":
            origin = positive_img
            positive_img = Image.new("RGB", origin.size)
            positive_img.paste(origin)
        if negative_img.mode != "RGB":
            origin = negative_img
            negative_img = Image.new("RGB", origin.size)
            negative_img.paste(origin)

        affine = transforms.RandomRotation((-60, 60))
        # affine = transforms.RandomAffine(degrees=60, translate=(0.1, 0.1), shear=30)

        # anchor_img_1 = affine(anchor_img)
        # positive_img_1 = affine(positive_img)
        # negative_img_1 = affine(negative_img)
        anchor_img_1 = anchor_img
        positive_img_1 = positive_img
        negative_img_1 = negative_img

        anchor_img_2 = affine(anchor_img)
        positive_img_2 = affine(positive_img)
        negative_img_2 = affine(negative_img)

        # angle_1 = random.uniform(-30, 30)
        # angle_2 = random.uniform(-30, 30)
        # translate_1 = random.uniform(-20, 20)
        # translate_2 = random.uniform(-20, 20)
        # shear_1 = random.uniform(-30, 30)
        # shear_2 = random.uniform(-30, 30)

        # anchor_img_1 = tf.affine(anchor_img, angle=angle_1, translate=(translate_1, translate_1), scale=1.0, shear=shear_1)
        # positive_img_1 = tf.affine(positive_img, angle=angle_1, translate=(translate_1, translate_1), scale=1.0, shear=shear_1)
        # negative_img_1 = tf.affine(negative_img, angle=angle_1, translate=(translate_1, translate_1), scale=1.0, shear=shear_1)

        # anchor_img_2 = tf.affine(anchor_img, angle=angle_2, translate=(translate_2, translate_2), scale=1.0, shear=shear_2)
        # positive_img_2 = tf.affine(positive_img, angle=angle_2, translate=(translate_2, translate_2), scale=1.0, shear=shear_2)
        # negative_img_2 = tf.affine(negative_img, angle=angle_2, translate=(translate_2, translate_2), scale=1.0, shear=shear_2)

        if self.transform is not None:
            anchor_img_1 = self.transform(anchor_img_1)
            positive_img_1 = self.transform(positive_img_1)
            negative_img_1 = self.transform(negative_img_1)
            anchor_img_2 = self.transform(anchor_img_2)
            positive_img_2 = self.transform(positive_img_2)
            negative_img_2 = self.transform(negative_img_2)

        return anchor_img_1, positive_img_1, negative_img_1, anchor_img_2, positive_img_2, negative_img_2

    def __len__(self):
        return self.pair_num

## siamese-triplet for training, label
class triTrainDataset2(Dataset):
    def __init__(self, txt, pair_num=None, transform=None):
        self.txt = txt
        self.transform = transform

        fr = open(self.txt, 'r')
        self.building_num = len(fr.readlines())
        fr.close()

        if pair_num is not None:
            self.pair_num = pair_num
        else:
            self.pair_num = self.building_num

    def __getitem__(self, index):
        anchor = linecache.getline(self.txt, (index % self.building_num) + 1).strip('\n')
        anchor_folder = os.listdir(anchor)
        anchor_id = random.randint(0, len(anchor_folder)-1)
        anchor_img = anchor + '/' + anchor_folder[anchor_id]
        while True:
            positive_id = random.randint(0, len(anchor_folder)-1)
            if positive_id != anchor_id:
                positive_img = anchor + '/' + anchor_folder[positive_id]
                break

        r = random.randint(0, 9)
        if r <= 7:
            label = torch.FloatTensor([1.0])
            while True:
                candidate = linecache.getline(self.txt, random.randint(1, self.building_num)).strip('\n')
                if candidate != anchor:
                    candidate_folder = os.listdir(candidate)
                    candidate_id = random.randint(0, len(candidate_folder)-1)
                    candidate_img = candidate + '/' + candidate_folder[candidate_id]
                    break
        else:
            label = torch.FloatTensor([0.5])
            while True:
                candidate_id = random.randint(0, len(anchor_folder)-1)
                if candidate_id != anchor_id and candidate_id != positive_id:
                    candidate_img = anchor + '/' + anchor_folder[candidate_id]
                    break

        anchor_img = Image.open(anchor_img)
        positive_img = Image.open(positive_img)
        candidate_img = Image.open(candidate_img)

        if self.transform is not None:
            anchor_img = self.transform(anchor_img)
            positive_img = self.transform(positive_img)
            candidate_img = self.transform(candidate_img)

        return anchor_img, positive_img, candidate_img, label

    def __len__(self):
        return self.pair_num

## siamese-triplet + softmax for training
class triSoftTrainDataset(Dataset):
    def __init__(self, txt, pair_num=None, transform=None):
        self.txt = txt
        self.transform = transform

        fr = open(self.txt, 'r')
        self.building_num = len(fr.readlines())
        fr.close()

        if pair_num is not None:
            self.pair_num = pair_num
        else:
            self.pair_num = self.building_num

    def __getitem__(self, index):
        anchor_label = index % self.building_num
        anchor = linecache.getline(self.txt, anchor_label + 1).strip('\n')
        anchor_folder = os.listdir(anchor)
        anchor_id = random.randint(0, len(anchor_folder)-1)
        anchor_img = anchor + '/' + anchor_folder[anchor_id]
        while True:
            positive_id = random.randint(0, len(anchor_folder)-1)
            if positive_id != anchor_id:
                positive_img = anchor + '/' + anchor_folder[positive_id]
                break

        positive_label = anchor_label

        while True:
            negative_label = random.randint(0, self.building_num - 1)
            negative = linecache.getline(self.txt, negative_label + 1).strip('\n')
            if negative != anchor:
                negative_folder = os.listdir(negative)
                negative_id = random.randint(0, len(negative_folder)-1)
                negative_img = negative + '/' + negative_folder[negative_id]
                break

        anchor_img = Image.open(anchor_img)
        positive_img = Image.open(positive_img)
        negative_img = Image.open(negative_img)

        if anchor_img.mode != "RGB":
            origin = anchor_img
            anchor_img = Image.new("RGB", origin.size)
            anchor_img.paste(origin)
        if positive_img.mode != "RGB":
            origin = positive_img
            positive_img = Image.new("RGB", origin.size)
            positive_img.paste(origin)
        if negative_img.mode != "RGB":
            origin = negative_img
            negative_img = Image.new("RGB", origin.size)
            negative_img.paste(origin)

        if self.transform is not None:
            anchor_img = self.transform(anchor_img)
            positive_img = self.transform(positive_img)
            negative_img = self.transform(negative_img)

        return anchor_img, positive_img, negative_img, \
            torch.from_numpy(np.array([anchor_label])),\
            torch.from_numpy(np.array([positive_label])),\
            torch.from_numpy(np.array([negative_label]))

    def __len__(self):
        return self.pair_num

## siamese-contrastive for training
class contrasTrainDataset(Dataset):
    def __init__(self, txt, pair_num=None, transform=None):
        self.txt = txt
        self.transform = transform

        fr = open(self.txt, 'r')
        self.building_num = len(fr.readlines())
        fr.close()

        if pair_num is not None:
            self.pair_num = pair_num
        else:
            self.pair_num = self.building_num

    def __getitem__(self, index):
        label_1 = (index % self.building_num)
        img0 = linecache.getline(self.txt, label_1 + 1).strip('\n')
        img0_folder = os.listdir(img0)
        img0_id = random.randint(0, len(img0_folder)-1)
        img0_img = img0 + '/' + img0_folder[img0_id]

        label = random.randint(0, 1)
        if label==1:
            label_2 = label_1
            while True:
                img1_id = random.randint(0, len(img0_folder)-1)
                if img1_id != img0_id:
                    img1_img = img0 + '/' + img0_folder[img1_id]
                    break
        else:
            while True:
                label_2 = random.randint(0, self.building_num - 1)
                img1 = linecache.getline(self.txt, label_2 + 1).strip('\n')
                if img1 != img0:
                    img1_folder = os.listdir(img1)
                    img1_id = random.randint(0, len(img1_folder)-1)
                    img1_img = img1 + '/' + img1_folder[img1_id]
                    break

        img0_img = Image.open(img0_img)
        img1_img = Image.open(img1_img)

        if img0_img.mode != "RGB":
            origin = img0_img
            img0_img = Image.new("RGB", origin.size)
            img0_img.paste(origin)
        if img1_img.mode != "RGB":
            origin = img1_img
            img1_img = Image.new("RGB", origin.size)
            img1_img.paste(origin)

        if self.transform is not None:
            img0_img = self.transform(img0_img)
            img1_img = self.transform(img1_img)

        return torch.from_numpy(np.array([label])),\
             torch.from_numpy(np.array([label_1])),\
             torch.from_numpy(np.array([label_2])),\
             img0_img, img1_img

    def __len__(self):
        return self.pair_num

