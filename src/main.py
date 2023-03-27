from modules.modele import load_valid, model_train_from_results;

def main(dist,focal):
    # code pour comparer les oiseaux
    load_valid(dist,focal)
    model_train_from_results(dist,focal)

if __name__ == '__main__':
    main(100,1000)
