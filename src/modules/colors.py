import cv2
import numpy as np
import os

def closest_color(pixel, color_list):
    min_distance = np.inf
    closest = None
    for color in color_list:
        distance = np.sum(np.abs(color - pixel))
        if distance < min_distance:
            min_distance = distance
            closest = color
    return closest


# renvoie la couleur la plus dominante a partir de l'image de l'oiseau
# en considérant deux couleurs proches comme étant la meme couleur
def get_dominant_color(image, colors_list):
    img = cv2.imread("res/results/" + image)
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

# sert à convertir une couleur rgb en hsv
def rgb_to_hsv(color):
    return cv2.cvtColor(color, cv2.COLOR_RGB2HSV)

# compte le nombre de pixels de chaque couleur en rgb
# puis converti le tout en hsv avant de regrouper
# les couleurs par leur hue (teinte)
def old_color_count_dict(img,dir):
    # print(f"color_count_dict: file = {img}")
    image = cv2.imread(dir + img)
    resized_img = cv2.resize(image, (300, 200))
    total_pixels = 0
    color_counts = {}
    for i in range(len(resized_img)):
        for j in range(len(resized_img[0])):
            rgb_color = resized_img[i][j]
            if not np.all(rgb_color == [255, 255, 255]):
                total_pixels +=1
                hsv_color = cv2.cvtColor(np.uint8([[rgb_color]]), cv2.COLOR_RGB2HSV)[0][0]
                hue = hsv_color[0]
                if(hue in color_counts):
                    color_counts[hue] +=1
                else:
                    color_counts[hue] = 1
    # max = 0
    for color, count in color_counts.items():
        color_counts[color] = round((count / total_pixels) * 100, 2)
        # print(f"{color}: {round((count / total_pixels) * 100, 2)}")
        # if(color_counts[color]>max):
            # max = color_counts[color]
    # print(max)
    return color_counts


# def color_count(img, colors_list,dir):
#     color_count_dict(img,dir)
#     print(f"color_count: file = {img}")
#     image = cv2.imread(dir + img)
#     resized_img = cv2.resize(image, (300, 200))
#     color_counts = {color: 0 for color in colors_list.keys()}
#     total_pixels = 0
#     for i in range(len(resized_img)):
#         for j in range(len(resized_img[0])):
#             if not np.all(resized_img[i][j] == [255, 255, 255]):
#                 closest = closest_color(resized_img[i][j], colors_list.values())
#                 for color, value in colors_list.items():
#                     if np.array_equal(value, closest):
#                         color_counts[color] += 1
#                         total_pixels += 1
#     # print(f"area: {total_pixels} pixels")
#     for color, count in color_counts.items():
#         color_counts[color] = round((count / total_pixels) * 100, 2)
#         # print(f"{color}: {round((count / total_pixels) * 100, 2)}")
#     return color_counts

# les différentes couleurs possibles
# colors = {"Noir": np.array([0, 0, 0], dtype=np.int32),
#           "Rouge": np.array([255, 0, 0], dtype=np.int32),
#           "Vert": np.array([0, 255, 0], dtype=np.int32),
#           "Jaune": np.array([255, 255, 0], dtype=np.int32),
#           "Blanc": np.array([255, 255, 255], dtype=np.int32),
#           "Bleu": np.array([0, 0, 255], dtype=np.int32),
#           "Marron": np.array([150, 75, 255], dtype=np.int32),
#           "Cyan": np.array([0, 255, 255], dtype=np.int32)}


# compte le nombre de pixels de chaque couleur en rgb
# puis converti le tout en hsv avant de regrouper
# les couleurs par leur hue (teinte)
def color_count_dict(img,dir):
    # print(f"color_count_dict: file = {img}")
    image = cv2.imread(dir + img, cv2.IMREAD_UNCHANGED)
    total_pixels = 0
    color_counts = {}
    for i in range(len(image)):
        for j in range(len(image[0])):
            rgba_color = image[i][j]
            # transparence
            alpha = rgba_color[3]
            if alpha != 0: # Si non transparent
                total_pixels +=1 
                rgb_color = rgba_color[:3] # rgb sans canal alpha (sans la transparence)
                # conversion en hsv
                hsv_color = cv2.cvtColor(np.uint8([[rgb_color]]), cv2.COLOR_RGB2HSV)[0][0]
                # On récupére la teinte
                hue = hsv_color[0]
                if(hue in color_counts):
                    color_counts[hue] +=1
                else:
                    color_counts[hue] = 1

    colors_to_remove = []
    # On converti tout ce comptage en pourcentage de présence de chaque couleur (groupé par teinte)
    for color, count in color_counts.items():
        color_counts[color] = round((count / total_pixels) * 100, 3)
        if(color_counts[color] == 0.0):
            # On stocke dans une liste pour éviter de modifier le dict en pleine itération
            colors_to_remove.append(color)
        
    # Si on a 0.0, on supprime de notre dictionnaire car négligeable (3 chiffres après la virgule et on a 0.0...)
    for color in colors_to_remove:
        color_counts.pop(color)
    return color_counts

# applique color_count pour tout les fichiers dans le dossier results
def color_count_all(dir):
    for file in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, file)) and not file.startswith('.'):
            color_count_dict(file,dir)

def main():
    color_count_all("res/results/")

if __name__ == "__main__":
    main()
