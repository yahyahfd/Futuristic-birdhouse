import cv2
import numpy as np


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
    background_img = cv2.imread("res/background/"+background)
    bird_img = cv2.imread("res/birds/"+bird)
    result = bird_img.copy()
    for i in range(len(bird_img)):
        for j in range(len(bird_img[0])):
            if (bird_img[i][j] == background_img[i][j]).all():
                result[i][j] = (255, 255, 255)
    cv2.imwrite("res/results/Result"+bird, result)


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
          np.array([255, 255, 255], dtype=np.int32),  # Blanc
          np.array([0, 0, 255], dtype=np.int32),  # Bleu
          np.array([0, 255, 255], dtype=np.int32)]  # Cyan

# extract_bird("Background.png", "corbeau.png")
# extract_bird("Background.png", "corbeau2.png")
# extract_bird("Background.png", "corbeau3.png")
# extract_bird("Background.png", "corbeau4.png")
# extract_bird("Background.png", "moineau.png")
# extract_bird("Background.png", "moineau2.png")
# extract_bird("Background.png", "moineau3.png")
extract_bird2("res/birds/moineau3.png")
# print(get_dominant_color("res/ResultBird.png", colors))
