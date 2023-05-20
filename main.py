import os
from src.modules.modele import load_valid, model_train_from_results, unsupervised_model, load_to_validate
from src.modules.bird_extractor import extract_all
from src.modules.colors import color_count_all

def main(dist,focal):
    res = "resources/"
    dirs = [res+"accepted_birds/",res+"model_trainer/", res+"birds_to_validate/",res+"extracted_birds_to_validate/",res+"results/"]
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)
    # extract_all(dirs[0],dirs[1])
    # extract_all(dirs[2],dirs[3])
    load_to_validate(dist,focal,dirs)
    # load_valid(dist,focal,dirs)
    input("Appuyez sur Entrée pour lancer le modèle non supervisé...")
    unsupervised_model(dist,focal,dirs)
    input("Appuyez sur Entrée pour lancer le modèle supervisé...")
    model_train_from_results(dist,focal,dirs)

if __name__ == '__main__':
    main(100,1000)
