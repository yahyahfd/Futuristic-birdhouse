import cv2
import numpy as np
import os


# methode qui extrait l'oiseau à partir d'une seule photo
def extract_bird2(image):
    img = cv2.imread(image)

    # on converti l'image en gris
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # on applique le flou gaussien
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # on detecte les contours
    edged = cv2.Canny(blurred, 30, 150)
    # on recherche des contours
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Recherche du plus grand contour,qui correspond à l'oiseau
    max_contour = max(contours, key=cv2.contourArea)
    # Création d'un masque pour le plus grand contour
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [max_contour], 0, 255, -1)
    # Extraction de l'oiseau
    result = np.zeros_like(img)
    result[mask == 255] = img[mask == 255]
    # Affichage du résultat
    cv2.imwrite("res/resultat.png", result)


# prend deux images, une de fond sans l'oiseau et une avec
# et renvoie l'oiseau seul dans une nouvelle image
def extract_bird(background, bird):
    print(f"extract_bird: bird = {bird}")
    back = cv2.imread(background)
    background_img = cv2.resize(back, (600, 400))
    bir = cv2.imread("res/birds/" + bird)
    bird_img = cv2.resize(bir, (600, 400))
    result = bird_img.copy()
    for i in range(len(bird_img)):
        for j in range(len(bird_img[0])):
            if (bird_img[i][j] == background_img[i][j]).all():
                result[i][j] = (255, 255, 255)
    cv2.imwrite("res/results/Result" + bird.split('.')[0] + ".png", result)


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
def color_count_dict(img,dir):
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


# extrait tout les oiseaux dans le fichier birds
def extract_all():
    directory = "res/birds/"
    # on parcours tout les fichier de birds
    for file in os.listdir(directory):
        # on verifie que le nom correspond à un fichier et que ca ne commence pas par un point
        if os.path.isfile(os.path.join(directory, file)) and not file.startswith('.'):
            extract_bird("res/background/Background.png", file)


# applique color_count pour tout les fichiers dans le dossier results
def color_count_all():
    directory = "res/results/"
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)) and not file.startswith('.'):
            color_count_dict(file,directory)

def main():
    extract_all()
    color_count_all()

if __name__ == "__main__":
    main()
