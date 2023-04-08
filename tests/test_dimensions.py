import unittest
import cv2
import numpy as np
import os
from src.modules.dimensions import pixel_area

class TestDimensions(unittest.TestCase):
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


        # Image remplie de couleurs aléatoires
        self.img3 = np.zeros((400, 600, 3), dtype=np.uint8)
        self.img3[:200, :200, 0] = 255  # rouge
        self.img3[200:, :200, 1] = 255  # vert
        self.img3[0:, 200:, 2] = 255  # bleu
        # Enregistrer les images dans le dossier img
        cv2.imwrite("test_img/img1.png", self.img1)
        cv2.imwrite("test_img/img2.png", self.img2)
        cv2.imwrite("test_img/img3.png", self.img3)


    def test_pixel_area(self):
        self.assertEqual(0, pixel_area("img1.png","test_img/"))
        self.assertEqual(600*200, pixel_area("img2.png","test_img/"))
        self.assertEqual(600*400, pixel_area("img3.png","test_img/"))

if __name__ == '__main__':
    unittest.main()
