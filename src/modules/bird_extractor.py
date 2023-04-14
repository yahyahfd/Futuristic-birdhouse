import cv2
import numpy as np
import os
from rembg import remove

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
def extract_bird3(background, bird,dir1,dir2):
    print(f"extract_bird: \033[1;34m{bird}\033[m")
    back = cv2.imread(background)
    background_img = cv2.resize(back, (600, 400))
    bir = cv2.imread(dir1 + bird)
    bird_img = cv2.resize(bir, (600, 400))
    result = bird_img.copy()
    for i in range(len(bird_img)):
        for j in range(len(bird_img[0])):
            if (bird_img[i][j] == background_img[i][j]).all():
                result[i][j] = (255, 255, 255)
    cv2.imwrite(dir2+ bird.split('.')[0] + ".png", result)


# Methode avec la library RemBG
def extract_bird(filename,img_path,output_path):
    print(f"extract_bird: \033[1;34m{filename}\033[m")
    input = cv2.imread(img_path)
    output = remove(input)
    cv2.imwrite(output_path+filename, output)

# extrait tout les oiseaux dans le dossier birds vers le dossiers Results
def extract_all(input_dir,output_dir):
    print("\nBird extracting...")
    # on parcours tout les fichier de birds
    for file in os.listdir(input_dir):
        input_file = os.path.join(input_dir, file)
        # on verifie que le nom correspond à un fichier et que ca ne commence pas par un point
        if os.path.isfile(input_file) and not file.startswith('.'):
            extract_bird(file,input_file,output_dir)

def main():
    os.makedirs("res/birds/", exist_ok=True)
    os.makedirs("res/results/", exist_ok=True)
    extract_all("res/birds/","res/results/")

if __name__ == "__main__":
    main()
