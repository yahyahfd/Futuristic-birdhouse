import cv2

# On imagine qu'on n'a que des images d'oiseaux avec fond transparent
# distance_from_objective est en millimètres, focal_length en pixels²
# apparent_size en pixel et le resultat en millimètre²


def birdRealArea(apparent_area, distance_from_objective, focal_length):
    return (apparent_area * (distance_from_objective**2))/(focal_length**2)


def pixel_area(image_path, dir):
    # Charger l'image
    img = cv2.imread(dir + image_path)

    # Convertir l'image en niveau de gris
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Appliquer un seuil pour séparer les pixels non blancs des pixels blancs
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # Calculer l'aire totale en pixels des pixels non blancs
    total_area = cv2.countNonZero(binary)

    return total_area


# Code trouvé sur internet afin d'obtenir la focale de la caméra en pixels (à adapter)
# # Load the camera matrix
# camera_matrix = cv2.load("camera_matrix.npy")

# # Extract the focal length in pixels
# focal_length_x = camera_matrix[0][0]
# focal_length_y = camera_matrix[1][1]

def main():
    print("yes")
    p_area = pixel_area("Resultmerle3.png", "res/results/")
    print("L'aire totale de l'objet est de {} pixels²".format(p_area))

    # 1000 pixels pour la focale et 100 millimètres pour la distance de la caméra
    c_area = birdRealArea(p_area, 100, 1000)
    print("L'aire totale réelle de l'objet est de {} millimètres²".format(c_area))


if __name__ == "__main__":
    main()
