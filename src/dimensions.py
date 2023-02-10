import cv2

# On imagine qu'on n'a que des images d'oiseaux avec fond transparent
# distance_from_objective est en millimètres, focal_length en pixels²
# apparent_size en pixel et le resultat en millimètre²
def birdRealArea(apparent_area, distance_from_objective, focal_length):
    return (apparent_area * (distance_from_objective**2))/(focal_length**2)


# Méthode afin de calculer l'aire totale de l'oiseau en pixel
def pixel_area(image_path):
    # On charge l'image en niveau de gris pour faciliter le "filtrage"
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # On applique un seuil afin de séparer l'oiseau du fond blanc
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # On cherche maintenant les contours de l'objet...
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # ... et on fait la somme des aires des contours afin d'obtenir l'aire totale
    total_area = 0
    for contour in contours:
        total_area += cv2.contourArea(contour)
    
    return total_area


p_area = pixel_area("../res/ResultBird.png")
print("L'aire totale de l'objet est de {} pixels²".format(p_area))

# 1000 pixels pour la focale et 100 millimètres pour la distance de la caméra
c_area = birdRealArea(p_area,100,1000)
print("L'aire totale réelle de l'objet est de {} millimètres²".format(c_area))

# Code trouvé sur internet afin d'obtenir la focale de la caméra en pixels (à adapter)
# # Load the camera matrix
# camera_matrix = cv2.load("camera_matrix.npy")

# # Extract the focal length in pixels
# focal_length_x = camera_matrix[0][0]
# focal_length_y = camera_matrix[1][1]
