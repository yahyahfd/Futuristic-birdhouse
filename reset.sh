#!/bin/bash

echo "Réinitialisation du projet"
mkdir -p res/results # crée le dossier res/results s'il n'existe pas

# Exclusion list
exclude_list=(Resultmerle.png Resultmerle2.png Resultmesange.png Resultmesange2.png Resultmoineau.png Resultmoineau2.png Resultrougegorge.png Resultrougegorge2.png)

# Déplace les images valides de model_trainer
if [ -n "$(ls -A res/invalid_images 2>/dev/null)" ]; then
    mv res/invalid_images/*.png res/results/
fi

# Déplace les images de invalid_images sauf celles de l'exclusion list
for file in res/model_trainer/*
do
    if [[ ! " ${exclude_list[@]} " =~ " $(basename $file) " ]]; then
        mv "$file" res/results/
    fi
done

echo "Projet réinitialisé. Tout les fichiers ont été redéplacé dans leur dossier initial"