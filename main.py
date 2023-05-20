import os
from src.modules.modele import load_valid, model_train_from_results;
from src.modules.bird_extractor import extract_all
def main(dist,focal):

    res = "resources/"
    # os.makedirs("accepted_birds/", exist_ok=True)
    # os.makedirs("model_trainer/", exist_ok=True)
    # os.makedirs("birds_to_validate/", exist_ok=True)
    # os.makedirs("extracted_birds_to_validate/", exist_ok=True)
    # extract_all(res+"accepted_birds/",res+"model_trainer/")
    # extract_all(res+"birds_to_validate/",res+"extracted_birds_to_validate/")
    dirs = [res+"accepted_birds/",res+"model_trainer/", res+"birds_to_validate/",res+"extracted_birds_to_validate/"]
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)
    # extract_all(dirs[0],dirs[1])
    extract_all(dirs[2],dirs[3])
    # load_valid(dist,focal,dirs)
    # model_train_from_results(dist,focal,dirs)

if __name__ == '__main__':
    main(100,1000)
