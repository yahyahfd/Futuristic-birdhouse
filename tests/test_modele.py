import os
import unittest
import cv2

import numpy as np
from src.modules.modele import compare_two_images

class TestCompareTwoImages(unittest.TestCase):
    def setUp(self): 
        # Créer dossier test_img si nécessaire
        os.makedirs("test_img", exist_ok=True)
        self.focal = 1000
        self.distance = 100
        # Image vide
        self.img1 = np.full((400, 600, 3), 255, dtype=np.uint8)
        # Image initialement vide, puis remplie à 50% de rouge
        self.img2 = np.full((400, 600, 3), 255, dtype=np.uint8)
        indices = np.random.choice(range(600*400), size=600*400//2, replace=False)
        for i in indices:
            x, y = i % 600, i // 600
            self.img2[y, x] = [0, 0, 255]

        # Même image que img2 mais avec une autre génération pour comparer
        self.img2_bis = np.full((400, 600, 3), 255, dtype=np.uint8)
        indices = np.random.choice(range(600*400), size=600*400//2, replace=False)
        for i in indices:
            x, y = i % 600, i // 600
            self.img2_bis[y, x] = [0, 0, 255]


        # Image remplie de couleurs aléatoires
        self.img3 = np.zeros((400, 600, 3), dtype=np.uint8)
        self.img3[:200, :200, 0] = 255  # rouge
        self.img3[200:, :200, 1] = 255  # vert
        self.img3[0:, 200:, 2] = 255  # bleu

        # Image mirroir de img3 (même couleurs dans mêmes proportions)
        self.img3_bis = np.zeros((400, 600, 3), dtype=np.uint8)
        self.img3_bis[:200, 400:, 0] = 255  # rouge
        self.img3_bis[200:, 400:, 1] = 255  # vert
        self.img3_bis[0:, :400, 2] = 255  # bleu


        # Enregistrer les images dans le dossier img
        cv2.imwrite("test_img/img1.png", self.img1)
        cv2.imwrite("test_img/img2.png", self.img2)
        cv2.imwrite("test_img/img2_bis.png", self.img2_bis)
        cv2.imwrite("test_img/img3.png", self.img3)
        cv2.imwrite("test_img/img3_bis.png", self.img3_bis)
        
    def test_compare_two_images(self):
        # Les images test1.jpg et test2.jpg sont identiques
        dir1 = "test_img/"
        dist = 500
        focal = 200
        threshold = 0.9
        # Images identiques: img1 blanche, img2 et img3 même image
        self.assertTrue(compare_two_images("img1.png", "img1.png", dist, focal, dir1, dir1, threshold))
        self.assertTrue(compare_two_images("img2.png", "img2.png", dist, focal, dir1, dir1, threshold))
        self.assertTrue(compare_two_images("img3.png", "img3.png", dist, focal, dir1, dir1, threshold))

        self.assertFalse(compare_two_images("img1.png", "img2.png", dist, focal, dir1, dir1, threshold))
        self.assertFalse(compare_two_images("img1.png", "img3.png", dist, focal, dir1, dir1, threshold))
        self.assertFalse(compare_two_images("img2.png", "img3.png", dist, focal, dir1, dir1, threshold))

        self.assertTrue(compare_two_images("img3.png", "img3_bis.png", dist, focal, dir1, dir1, threshold))
        self.assertTrue(compare_two_images("img2.png", "img2_bis.png", dist, focal, dir1, dir1, threshold))
        

if __name__ == '__main__':
    unittest.main()
