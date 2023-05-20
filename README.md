# meziane-hafid-plong-2022

## Comment lancer l'application

1. Aller à la racine du projet
2. Lancer ./program.sh; ce script se charge :
    *   d'**installer toutes les dépendances nécessaires** pour le bon fonctionnement du projet
    *   de lancer les **tests unitaires**
    *   de lancer le **main.py** qui permet de faire tourner le programme en **classifiant les oiseaux** dans le bon dossier
    
## Réinitialiser la disposition des images pour re-tester:
1. Aller à la racine du projet
2. Lancer ./reset.sh; ce script se charge :
    *   de remettre chaque **image** présente dans chaque **sous-dossier** de 'resources/results/' dans le **dossier initial** 'resources/extracted_birds_to_validate/'
    *   de supprimer les **sous-dossiers créés dans le dossier** 'resources/results/'
    