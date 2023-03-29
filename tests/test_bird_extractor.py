import unittest

class TestBirdExtractor(unittest.TestCase):
    # img 1 =Image d'oiseau tout seul
    # img 2 = Image de background tout seul
    # img 3 =image de l'oiseau sur le backgroud
    # Vérifier que extraire oiseau de img3 = img2
    # def setUp(self):
        # Dossier avec les images d'oiseaux isolés
        # self.bird_images = 
        # self.background = 'res/background/Background.png'
        # self.combined_images = 

        #Inspire toi de ça 
    # def test_extract_bird2(self):
    #     extract_bird2(self.image)
    #     result_path = 'res/resultat.png'
    #     self.assertTrue(os.path.isfile(result_path))
        
    # def test_extract_bird(self):
    #     extract_bird(self.background, self.bird)
    #     result_path = 'res/results/Resulttest.png'
    #     self.assertTrue(os.path.isfile(result_path))
        
    # def test_extract_all(self):
    #     extract_all()
    #     for file in os.listdir('res/results/'):
    #         if file.startswith('Result'):
    #             result_path = 'res/results/' + file
    #             self.assertTrue(os.path.isfile(result_path))
    pass

if __name__ == '__main__':
    unittest.main()
