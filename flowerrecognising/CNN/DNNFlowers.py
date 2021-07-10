import tensorflow as tf
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os

for dirname, _, filenames in os.walk('/../input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

import matplotlib.pyplot as plt
import seaborn as sns
import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout, MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from keras.applications import VGG19, resnet
import cv2
import os
import random
import requests
from PIL import Image
from io import BytesIO

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

categories=['Dandelion', 'Daisy', 'Tulip','Sunflower', 'Rose','Cactus','Lily','Orchid','Violet']
img_size = 224




model = keras.models.load_model("flowerrecognising/CNN/model4.h5")


def process_image(img):
    '''
    Function is used before prediction to prepare image
    :param img: image in jpg format
    :return: normalizated and resized image
    '''

    # grayscale and normalization
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.IMREAD_COLOR)
    img = img / 255.0
    # resizing
    img = cv2.resize(img, (224, 224))
    img = np.expand_dims(img, axis=0)
    # making it model ready
    return img



def scientific_to_fine_percent(var,biggest):

    x= 87/float(scientific_to_real(biggest))
    print(x)
    print(float("{:.25f}".format(float(var))))
    return int((float("{:.25f}".format(float(var))))* x)



def scientific_to_real(var):
    return float("{:.25f}".format(float(var)))

def predict(img):
    '''
    Predict name of plant by using CNN model
    :param img: image in jpg format
    :return: Name of plant
    '''
    img = process_image(img)
    label = model.predict(img)
    predictions =[]

    print(label)

    for x in range(5):
        final_1 = np.argmax(label, axis=1)[0]
        print(final_1)
        #label = np.delete(label, final_1, axis=1)

        print(categories[final_1])
        print(scientific_to_real(label[0][final_1]))
        sublist=[]
        sublist.append(categories[final_1])
        sublist.append(label[0][final_1])
        predictions.append(sublist)
        label[0, final_1] = 0



    return predictions
