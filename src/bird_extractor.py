import cv2
import numpy as np


# prend deux images, une de fond sans l'oiseau et une avec
# et renvoie l'oiseau seul dans une nouvelle image
def extract_bird(img1, img2):
    background = cv2.imread(img1)
    bird = cv2.imread(img2)
    result = bird.copy()
    for i in range(len(bird)):
        for j in range(len(bird[0])):
            if (bird[i][j] == background[i][j]).all():
                result[i][j] = (255, 255, 255)
    cv2.imwrite("res/ResultBird.png", result)


# def closest_color(color, color_list):
#    min_distance = np.inf
#    res = None
#    for c in color_list:
#        distance = np.sum(np.abs(c - color))
#        if distance < min_distance:
#            min_distance = distance
#            res = c
#    return res

def closest_color(pixel, color_list):
    min_distance = np.inf
    closest = None
    for color in color_list:
        b, g, r = pixel
        cr, cg, cb = color
        distance = ((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest = color
    return closest


# renvoie la couleur la plus dominante a partir de l'image de l'oiseau
# en considérant deux couleurs proches comme étant la meme couleur
def get_dominant_color(image, colors_list):
    img = cv2.imread(image)
    (h, w, d) = img.shape
    pixels = np.reshape(img, (h * w, d))
    color_counts = {}
    for pixel in pixels:
        if not np.all(pixel == [255, 255, 255]):
            close_color = closest_color(pixel, colors_list)
            color_key = str(close_color)
            if color_key in color_counts:
                color_counts[color_key] += 1
            else:
                color_counts[color_key] = 1
    # return max(color_counts, key=color_counts.get)
    return color_counts


# les différentes couleurs possibles
colors = [np.array([0, 0, 0], dtype=np.int32),  # Noir
          np.array([255, 0, 0], dtype=np.int32),  # Rouge
          np.array([0, 255, 0], dtype=np.int32),  # Vert
          np.array([255, 255, 0], dtype=np.int32),  # Jaune
          np.array([255, 165, 0], dtype=np.int32),  # Orange
          np.array([255, 255, 255], dtype=np.int32),  # Blanc
          np.array([150, 75, 0], dtype=np.int32),  # Marron
          np.array([128, 128, 128], dtype=np.int32),  # Gris
          np.array([0, 0, 255], dtype=np.int32)]  # Bleu

extract_bird("res/Background.png", "res/Rouge.png")
print(get_dominant_color("res/ResultBird.png", colors))
