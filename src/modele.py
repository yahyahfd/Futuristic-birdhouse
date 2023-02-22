import os
import shutil
from dimensions import birdRealArea, pixel_area
from bird_extractor import color_count, colors

# img1 et img2 deux images différentes ou non
# focal et dist comme décrit dans la méthode birdRealArea
# Return un coefficient de similarité entre les deux aires
# On décidera plus tard de ce qu'un coefficient correct vaut
def compare_two_images_Area(img1, img2,focal,dist,dir1,dir2):
    p_area_1 = pixel_area(img1,dir1)
    c_area_1 = birdRealArea(p_area_1,dist,focal)
    p_area_2 = pixel_area(img2,dir2)
    c_area_2 = birdRealArea(p_area_2,dist,focal)
    max_area = max(c_area_1, c_area_2)
    min_area = min(c_area_1, c_area_2)
    if(max_area == 0):
        if(min_area == 0):
            return 1
        else:
            return 0
    return min_area/max_area

# img1 et img2 deux images différentes ou non
# Return un coefficient de similarité entre les deux disctionnaires
# de couleurs (une moyenne entre tous les coeff de couleurs 2 à 2)
# On décidera plus tard de ce qu'un coefficient correct vaut
def compare_two_images_Colors(img1, img2,dir1,dir2):
    c_dict_1 = color_count(img1,colors,dir1)
    c_dict_2 = color_count(img2,colors,dir2)
    color_percentage = {color: 0 for color in colors.keys()}
    for color, _ in color_percentage.items():
        color1 = c_dict_1[color]
        color2 = c_dict_2[color]
        max_color = max(color1, color2)
        min_color = min(color1, color2)
        if(max_color == 0):
            if(min_color == 0):
                color_percentage[color] = 1
            else:
                color_percentage[color] = 0
        else:
            color_percentage[color] = min_color / max_color 
    moyenne = 0
    for col_per in color_percentage.values():
        moyenne += col_per
    moyenne = moyenne / len(color_percentage)
    return moyenne

#fait une comparaison de l'aire et des couleurs de 2 images
def compare_two_images(img1,img2, focal, dist, dir1,dir2):
    color_similarities = compare_two_images_Colors(img1,img2,dir1,dir2)
    area_similarities = compare_two_images_Area(img1,img2,focal,dist,dir1,dir2)
    return min(area_similarities,color_similarities)/max(area_similarities,color_similarities)

valid_images = []
#charger les images valides dans valid_images
def load_valid():
    directory = "res/model_trainer/"
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)) and not file.startswith('.'):
            valid_images.append(file)

# De base il y a des images dans le dossier model_trainer
# on le rempli d'images plus ou moins similaires à celles
# présentes dans ce dossier à partir du dossier results
def model_train(file):
        dir1 = "res/results/"
        dir2 = "res/model_trainer/"
        if(len(valid_images) == 0):
            valid_images.append(file)
            shutil.move(file, "res/model_trainer/")
            print("first image of the model added (could be problematic and not intended)")
        else:
            moved = -1
            for paths in valid_images:
                if(compare_two_images(file,paths,1000,100,dir1,dir2)>0.80):
                    valid_images.append(file)
                    shutil.move(dir1+file, "res/model_trainer/")
                    moved = 1
                    break
            if(moved == -1):
                shutil.move(dir1+file, "res/invalid_images/")


def model_train_from_results():
    directory = "res/results"
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)) and not file.startswith('.'):
            model_train(file)

def main():
    # img1 = "Resultcorbeau.png"
    # img2 = "Resultpigeon.png"
    # print(compare_two_images(img1,img2,1000,100))
    load_valid()
    model_train_from_results()

if __name__ == "__main__":
    main()
