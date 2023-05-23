import os
import unittest

import cv2
import numpy as np
from src.modules.bird_extractor import extract_bird

class TestBirdExtractor(unittest.TestCase):
    def setUp(self):
        os.makedirs("test_img", exist_ok=True)
        os.makedirs("test_img/Result", exist_ok=True)

        # création d'une image avec un "oiseau brun" sur fond blanc
        self.brown_bird_on_white = np.zeros((400, 600, 3), dtype=np.uint8)
        self.brown_bird_on_white[:, :, :] = 255
        self.brown_bird_on_white[50:150, 200:400, 0] = 100
        self.brown_bird_on_white[50:150, 200:400, 1] = 50
        self.brown_bird_on_white[50:150, 200:400, 2] = 0
        self.brown_bird_on_white[100:150, 300:400, 0] = 150
        self.brown_bird_on_white[100:150, 300:400, 1] = 100
        self.brown_bird_on_white[100:150, 300:400, 2] = 50

        # création d'une image avec un oiseau brun sur fond vert
        self.brown_bird_on_green = np.zeros((400, 600, 3), dtype=np.uint8)
        self.brown_bird_on_green[:, :, 1] = 255
        self.brown_bird_on_green[50:150, 200:400, 0] = 100
        self.brown_bird_on_green[50:150, 200:400, 1] = 50
        self.brown_bird_on_green[50:150, 200:400, 2] = 0
        self.brown_bird_on_green[100:150, 300:400, 0] = 150
        self.brown_bird_on_green[100:150, 300:400, 1] = 100
        self.brown_bird_on_green[100:150, 300:400, 2] = 50

        cv2.imwrite("test_img/brown_bird_on_white.png", self.brown_bird_on_white)
        cv2.imwrite("test_img/brown_bird_on_green.png", self.brown_bird_on_green)
    
    def test_extract_bird(self):
        bird_on_bg = "brown_bird_on_green.png"
        bird_alone = "brown_bird_on_white.png"
        extract_bird(bird_on_bg,"test_img/"+bird_on_bg,"test_img/Result/")
        # Vérifier si l'image extraite existe
        assert os.path.isfile("test_img/Result/"+bird_on_bg)
        
        # Charger l'image de sortie et l'image attendue
        output_img = cv2.imread("test_img/Result/"+bird_on_bg) # oiseau extrait (meme nom)
        expected_img = cv2.imread("test_img/"+bird_alone) # oiseau isolé au début pour vérifier

        # Vérifier si les deux images ont la même taille
        assert output_img.shape == expected_img.shape

        # Vérifier si les deux images sont identiques
        difference = cv2.subtract(output_img, expected_img)
        b, g, r = cv2.split(difference)
        assert cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0

if __name__ == '__main__':
    unittest.main()
