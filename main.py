import os
from src.modules.modele import load_valid, model_train_from_results;
from src.modules.bird_extractor import extract_all
def main(dist,focal):
    dirs = ["res/results/","res/model_trainer/", "res/invalid_images/","res/birds"]
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)
    extract_all(dirs[3],dirs[0])
    load_valid(dist,focal,dirs)
    model_train_from_results(dist,focal,dirs)

if __name__ == '__main__':
    main(100,1000)
