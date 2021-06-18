import tensorflow as tf
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

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
from keras.layers import Dense, Conv2D , MaxPool2D , Flatten , Dropout , MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from keras.applications import VGG19, resnet
import cv2
import os
import random

import requests
from PIL import Image
from io import BytesIO

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
labels = ['dandelion', 'daisy','tulip','sunflower','rose']
categories=['Dandelion', 'Daisy', 'Tulip','Sunflower', 'Rose']
img_size = 224

# def get_data(data_dir):
#     data = []
#     for label in labels:
#         path = os.path.join(data_dir, label)
#         class_num = labels.index(label)
#         for img in os.listdir(path):
#             try:
#                 img_arr = cv2.imread(os.path.join(path, img), cv2.IMREAD_COLOR)
#                 resized_arr = cv2.resize(img_arr, (img_size, img_size)) # Reshaping images to preferred size
#                 data.append([resized_arr, class_num])
#             except Exception as e:
#                 print(e)
#     return np.array(data)
#
# data = get_data("../input/flowers/flowers/")
#
# x = []
# y = []
#
# for feature, label in data:
#     x.append(feature)
#     y.append(label)
#
# x = np.array(x) / 255
# x = x.reshape(-1, img_size, img_size, 3)
# y = np.array(y)
#
# from sklearn.preprocessing import LabelBinarizer
# label_binarizer = LabelBinarizer()
# y = label_binarizer.fit_transform(y)
#
# x_train,x_test,y_train,y_test = train_test_split(x , y , test_size = 0.2 , stratify = y , random_state = 0)
#
# del x,y,data
#
# strategy = tf.distribute.get_strategy()
#
# with strategy.scope():
#     pre_trained_model = VGG19(input_shape=(224,224,3), include_top=False, weights="imagenet")
#
#     for layer in pre_trained_model.layers[:19]:
#         layer.trainable = False
#
#     model = Sequential([
#         pre_trained_model,
#         MaxPool2D((2,2) , strides = 2),
#         Flatten(),
#         Dense(5 , activation='softmax')])
#     model.compile(optimizer = "adam" , loss = 'categorical_crossentropy' , metrics = ['accuracy'])
#
# from keras.callbacks import ReduceLROnPlateau
# learning_rate_reduction = ReduceLROnPlateau(monitor='val_accuracy', patience = 2, verbose=1,factor=0.3, min_lr=0.000001)
#
# history = model.fit(x_train,y_train, batch_size = 64 , epochs = 12 , validation_data = (x_test, y_test),callbacks = [learning_rate_reduction])
# model.save("model3.h5")
#


# model = keras.models.load_model("flowerrecognising/CNN/model3.h5")


def process_image(img):


    # grayscale and normalization
    img = np.array(img)

    img = cv2.cvtColor(img, cv2.IMREAD_COLOR)
    img = img / 255.0

    # resizing
    img = cv2.resize(img, (224, 224))


    img = np.expand_dims(img, axis=0)
    # making it model ready

    return img


def predict(url):
    img = process_image(url)
    label = model.predict(img)
    final_1 = np.argmax(label, axis=1)[0]
    print(final_1)
    return categories[final_1]
