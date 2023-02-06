import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler
from PIL import Image

train_labels = []
train_images = np.empty((0,405,500,3))
valide_path = 'images/valides'
invalide_path = 'images/invalides'

def images_training(train_images,train_labels):
    for filename in os.listdir(valide_path):
        foreach_image(valide_path + "/"+filename,1,train_images,train_labels)
    for filename in os.listdir(invalide_path):
        foreach_image(invalide_path + "/"+filename,0)




def foreach_image(filename,lab,train_images,train_labels):
    
    img = Image.open(filename)

    data = np.asarray(img)
    # summarize shape
    print(filename)
    print(data.shape)

    # create Pillow image
    image2 = Image.fromarray(data)
    print(type(image2))

    # summarize image details
    print(image2.mode)
    print(image2.size)
    
    # Transformer l'image en un tenseur (tableau numpy)
    img_tensor = np.expand_dims(img, axis=0)

    # Définir l'étiquette de validation (1 signifie valide, 0 signifie non-valide)
    label = lab

    # Ajouter l'image et son étiquette au jeu de données d'entraînement
    train_images = np.append(train_images, img_tensor, axis=0)
    train_labels = np.append(train_labels, label)


print("Test")

images_training(train_images,train_labels)
# # for i in range (10):
# #     train_labels.append(10) #0 ou 1
# #     train_samples.append(20) # dataset



# # train_labels = np.array(train_labels)
# # train_samples = np.array(train_samples)

# # train_labels, train_samples = shuffle(train_labels,train_samples)

# scaler = MinMaxScaler(feature_range=(0,1))
# scaled_train_samples = scaler.fit_transform(train_samples.reshape(-1,1))

# # Define Sequential model with 3 layers
# model = keras.Sequential(
#     [
#         layers.Dense(2, activation="relu", name="layer1"),
#         layers.Dense(3, activation="relu", name="layer2"),
#         layers.Dense(4, name="layer3"),
#     ]
# )
# # Call model on a test input
# x = tf.ones((3, 3))
# y = model(x)
