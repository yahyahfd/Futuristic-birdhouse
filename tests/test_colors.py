import unittest
from src.modules.colors import *


class TestColors(unittest.TestCase):
    def setUp(self):
        os.makedirs("test_img", exist_ok=True)

        # image avec 100% de pixels rouges
        img1 = np.zeros((100, 100, 4))
        img1[:, :] = (0,0 , 255, 255)
        cv2.imwrite("test_img/red_100.png", img1)

        # image avec 40% de pixels rouges et 60% de pixels bleus
        img2 = np.zeros((100, 100, 4), dtype=np.uint8)
        img2[:, :] = (255, 255, 0, 255)
        img2[:, int(img2.shape[1] * 0.6):] = (0, 255, 255, 255)
        cv2.imwrite("test_img/cyan_60_yellow_40.png", img2)

        # image avec 80% de pixels verts et 20% de pixels rouges
        img3 = np.zeros((100, 100, 4), dtype=np.uint8)
        img3[:, :] = (0, 0, 255, 255)
        img3[:, :int(img3.shape[1] * 0.2)] = (0, 255, 0, 255)
        cv2.imwrite("test_img/green_80_rouge_20.png", img3)

    def test_rgb_to_hsv(self):
        red = np.array([[[255, 0, 0]]], dtype=np.uint8)
        hsv = rgb_to_hsv(red)
        expected_hsv = np.array([[[0, 255, 255]]], dtype=np.uint8)
        self.assertTrue(np.array_equal(hsv, expected_hsv))

        green = np.array([[[0, 255, 0]]], dtype=np.uint8)
        hsv = rgb_to_hsv(green)
        expected_hsv = np.array([[[60, 255, 255]]], dtype=np.uint8)
        self.assertTrue(np.array_equal(hsv, expected_hsv))

        blue = np.array([[[0, 0, 255]]], dtype=np.uint8)
        hsv = rgb_to_hsv(blue)
        expected_hsv = np.array([[[120, 255, 255]]], dtype=np.uint8)
        self.assertTrue(np.array_equal(hsv, expected_hsv))

    def test_color_count_dict(self):
        directory = "test_img/"
        expected1 = {'Rouge': 100.0}
        expected2 = {'Jaune': 40.0, 'Cyan': 60.0}
        expected3 = {'Vert': 20.0, 'Rouge': 80.0}
        actual1 = color_count_dict("red_100.png", directory)
        actual2 = color_count_dict("cyan_60_yellow_40.png", directory)
        actual3 = color_count_dict("green_80_rouge_20.png", directory)

        self.assertEqual(expected1, actual1)
        self.assertEqual(expected2, actual2)
        self.assertEqual(expected3, actual3)

    if __name__ == '__main__':
        unittest.main()
