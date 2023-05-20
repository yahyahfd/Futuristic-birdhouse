import os
import shutil
from src.modules.dimensions import birdRealArea, pixel_area
from src.modules.colors import color_count_dict

valid_images = dict()
percentage_subdirs = dict()
images_to_validate = dict()

# img1 et img2 deux images différentes ou non
# focal et dist comme décrit dans la méthode birdRealArea
# Return un coefficient de similarité entre les deux aires
# On décidera plus tard de ce qu'un coefficient correct vaut
def compare_two_images_Area(img1, img2,dist,focal,dir1,dir2,supornot):
    if supornot:
        dict_to_use = valid_images
    else:
        dict_to_use = images_to_validate

    if(img1 in dict_to_use):       
        c_area_1 = dict_to_use[img1][0]
    else:
        p_area_1 = pixel_area(img1,dir1)
        c_area_1 = birdRealArea(p_area_1,dist,focal)

    if(img2 in dict_to_use):
        c_area_2 = dict_to_use[img2][0]
    else:
        p_area_2 = pixel_area(img2,dir2)
        c_area_2 = birdRealArea(p_area_2,dist,focal)

    max_area = max(c_area_1, c_area_2)
    min_area = min(c_area_1, c_area_2)
    if(max_area == 0):
        if(min_area == 0):
            return 1
        else:
            return 0
    return (min_area/max_area)

# calcul de la médiane après avoir trier le dictionnaire de couleurs
def get_median_color_percentage(color_dict):
    sorted_dict = {k: v for k, v in sorted(color_dict.items(), key=lambda item: item[1])}
    values = list(sorted_dict.values())
    length = len(values)
    if length <= 1:
        return values[0] if length == 1 else 0
    median_index = (length - 1)//2
    if length % 2 == 0:
        median_value = (values[median_index] + values[median_index + 1]) / 2
    else:
        median_value = values[median_index]
    return median_value


# img1 et img2 deux images différentes ou non
# Return un coefficient de similarité entre les deux dictionnaires
# de couleurs (une moyenne entre tous les coeff de couleurs 2 à 2)
# On décidera plus tard de ce qu'un coefficient correct vaut
def compare_two_images_Colors(img1, img2,dir1,dir2,supornot):
    if supornot:
        dict_to_use = valid_images
    else:
        dict_to_use = images_to_validate

    if(img1 in dict_to_use):       
        c_dict_1 = dict_to_use[img1][1]
    else:
        c_dict_1 = color_count_dict(img1,dir1)
    if(img2 in dict_to_use):       
        c_dict_2 = dict_to_use[img2][1]
    else:
        c_dict_2 = color_count_dict(img2,dir2)

    # if not c_dict_1 and not c_dict_2:
    #     # les deux images sont blanches, donc 100% de similarité
    #     # les 2 dicts sont vides
    #     return 1
    
    # On fusionne utilise les clefs des deux dicts pour avoir notre
    # dictionnaire finale
    keys = list(c_dict_1.keys() | c_dict_2.keys())
    result_dict = dict.fromkeys(keys, 0)
    for colors in result_dict.keys():
        if colors in c_dict_1 and colors in c_dict_2:
            color1 = c_dict_1[colors]
            color2 = c_dict_2[colors]
            max_color = max(color1, color2)
            min_color = min(color1, color2)
            result_dict[colors] = min_color / max_color 
        else:
            result_dict[colors] = 0
    threshold = get_median_color_percentage(result_dict)
    total_colors = 0
    count_colors = 0
    count_all = 0
    for val in result_dict.values():
        if val >= threshold:
            total_colors += val
            count_colors += 1
        else:
            count_all += 1
    if count_colors == 0:
        print(0)
        return 0
    else:
        print(total_colors/count_colors)
        return total_colors/count_colors

#fait une comparaison de l'aire et des couleurs de 2 images
def compare_two_images(img1,img2, dist,focal , dir1,dir2,threshold, supornot):
    print(f"Comparing two images: \033[1;34m{img1}\033[0m & \033[1;34m{img2}\033[0m")
    color_similarities = compare_two_images_Colors(img1,img2,dir1,dir2, supornot)
    area_similarities = compare_two_images_Area(img1,img2,dist,focal,dir1,dir2, supornot)
    moyenne = (0.20*area_similarities) + (0.80*color_similarities)
    print(f"couleurs: {color_similarities}")
    print(f"aires: {area_similarities}")
    if(moyenne>threshold):
        print(f"\033[32mmoyenne: {moyenne}\033[0m")
        return True
    else:
        print(f"\033[31mmoyenne: {moyenne}\033[0m")
        return False

#charger les images valides dans valid_images
def load_valid(dist,focal,dirs):
    print("Loading valid images...")
    for file in os.listdir(dirs[1]):
        if os.path.isfile(os.path.join(dirs[1], file)) and not file.startswith('.'):
            p_area = pixel_area(file,dirs[1])
            valid_images[file] = (birdRealArea(p_area,dist,focal), color_count_dict(file,dirs[1]))
            print(f"Loading to model: {file}")

# De base il y a des images dans le dossier model_trainer
# on le rempli d'images plus ou moins similaires à celles
# présentes dans ce dossier à partir du dossier results
def model_train(file,dist,focal,dirs):
        moved = -1
        for paths in valid_images:
            if(compare_two_images(file,paths,dist,focal,dirs[0],dirs[1],0.80)):
                if file not in valid_images:
                    p_area = pixel_area(file,dirs[0])
                    valid_images[file] = (birdRealArea(p_area,dist,focal), color_count_dict(file,dirs[0]))
                    shutil.move(dirs[0]+file, dirs[1])
                    moved = 1
                break
        if(moved == -1):
            shutil.move(dirs[0]+file, dirs[2])

def model_train_from_results(dist,focal,dirs):
    print("\nModel training...")
    for file in os.listdir(dirs[0]):
        if os.path.isfile(os.path.join(dirs[0], file)) and not file.startswith('.'):
            model_train(file,dist,focal,dirs)
    print("\nModel training finished.")
    
def percentage_in_sub_dir(sub_dir):
    if(sub_dir in percentage_subdirs):
        print(percentage_subdirs[sub_dir])
    else:       
        png_files = []
        for root,dirs,files in os.walk(sub_dir):
            for file in files:
                if file.endswith(".png"):
                    file_path = os.path.join(root,file)
                    png_files.append(file_path)
        total_similarity = 0
        count = 0
        for i in range(len(png_files)):
            for j in range(i+1, len(png_files)):
                dir_i = os.path.dirname(png_files[i])
                filename_i = os.path.basename(png_files[i])
                dir_j = os.path.dirname(png_files[j])
                filename_j = os.path.basename(png_files[j])
                similarity_percentage = compare_two_images_Colors(filename_i,filename_j,dir_i+"/",dir_j+"/")
                total_similarity += similarity_percentage
                count += 1
        average_similarity = total_similarity / count
        percentage_subdirs[sub_dir] = average_similarity
        print("Average similarity: ", average_similarity)

# NOT USED
def percentages_in_dir(dirs):
    subdirectories = [os.path.join(dirs[4], sub_dir) for sub_dir in os.listdir(dirs[4]) if os.path.isdir(os.path.join(dirs[4], sub_dir))]
    for subdirectory in subdirectories:
        print(subdirectory)
        percentage_in_sub_dir(subdirectory)

#charger les images valides dans valid_images
def load_to_validate(dist,focal,dirs):
    print("Loading images to validate...")
    for file in os.listdir(dirs[3]):
        if os.path.isfile(os.path.join(dirs[3], file)) and not file.startswith('.'):
            p_area = pixel_area(file,dirs[3])
            images_to_validate[file] = (birdRealArea(p_area,dist,focal), color_count_dict(file,dirs[3]))
            print(f"Loading to unsupervised model: {file}")

def unsupervised_model(dist,focal,dirs):
    print("\nUnsupervised training...")
    # On commence par regrouper toutes les images à 80% similaires présentes dans extracted_bird_to_validate
    bird_list = []
    for file in os.listdir(dirs[3]):
        if os.path.isfile(os.path.join(dirs[3], file)) and not file.startswith('.') and file.endswith(".png"):
            # On commence par mettre toutes les images dans une même liste
            bird_list.append(file)
    
    while len(bird_list) > 0:
        # On fait une nouvelle liste à manipuler
        copy_bird_list = bird_list[1:]
        pivot = bird_list[0]

        # On retire de copy_bird_list tout oiseau avec un taux de similitude >=80% avec notre pivot qu'on déplacera donc dans un dossier avec le nom du pivot
        for bird in bird_list[1:]:
            if not compare_two_images(pivot,bird,dist,focal,dirs[3],dirs[3],0.80,False):
                copy_bird_list.remove(bird)
        
        # On se retrouve dans copy_bird_list avec uniquement les oiseaux similaires à notre pivot
        # On déplace tout le contenu de copy_bird_list ainsi que notre pivot dans un nouveau sous-dossier du même nom que notre pivot
        pivot_name, extension = os.path.splitext(os.path.basename(pivot))
        folder = dirs[4]+pivot_name+"/"
        if not os.path.exists(folder):
            os.makedirs(folder)
        shutil.move(dirs[3]+pivot,folder)
        bird_list.remove(pivot)
        for bird in copy_bird_list:
            shutil.move(dirs[3]+bird, folder)
            bird_list.remove(bird)
    print("\nUnsupervised training completed.")

#  ANCIENS AJOUTS DANS UNSUPERVISED MODEL
# On doit maintenant comparer le pivot avec chaque sous-dossier présent dans results (et les sous-sous-dossiers)
# Si on trouve un taux de similitudes à 80% avec un groupe d'oiseaux (un sous-dossier entier y compris ses sous-sous-dossiers)
# on le marque comme max: à la fin de toutes les comparaisons, si on retrouve un max > 80% -> on déplace les images de 
# copy_bird_list vers ce sous_dossier, sinon on crée un nouveau sous-dossier
# max = 0
# folder = ""
# for file,percentage in percentage_subdirs:
#     if max < percentage:
#         max = percentage
#         folder = file
# on vérifie si max >80%, si c'est le cas, on rajoute nos copy birds à folder et on update le pourcentage
# sinon, on crée un nouveau dossier et on y met nos oiseaux

def main():
    dirs = ["res/results/","res/model_trainer/", "res/invalid_images/"]
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)
    # img1 = "Resultcorbeau.png"
    # img2 = "Resultpigeon.png"
    # print(compare_two_images(img1,img2,100,1000))
    load_valid(100,1000,dirs)
    model_train_from_results(100,1000,dirs)
    # print(compare_two_images_Colors("Resultpigeon4.png","Resultpigeon3.png","res/results/","res/results/"))
    # compare_two_images_Area("Resultpigeon4.png","Resultpigeon3.png",100,1000,"res/results/","res/results/")

if __name__ == "__main__":
    main()
