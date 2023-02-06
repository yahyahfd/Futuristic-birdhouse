import os
import numpy as np
# import tensorflow as tf
# from tensorflow import keras
# from keras import layers
from PIL import Image

train_labels = []
train_images = []
valide_path = 'images/valides'
invalide_path = 'images/invalides'

def images_training(train_images,train_labels):
    for filename in os.listdir(valide_path):
        train_images, train_labels = foreach_image(valide_path + "/" + filename, 1, train_images, train_labels)
    for filename in os.listdir(invalide_path):
        train_images, train_labels = foreach_image(invalide_path + "/" + filename, 0, train_images, train_labels)
    return train_images, train_labels


def foreach_image(filename, lab, train_images, train_labels):
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

    return train_images, train_labels


print("Test")
train_images, train_labels = images_training(train_images, train_labels)
