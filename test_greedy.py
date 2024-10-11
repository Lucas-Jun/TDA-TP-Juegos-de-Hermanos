import unittest
import greedy
import set_files
import os

class TestGreegy(unittest.TestCase):

    
    def setUp(self) -> None:
        self.cur_path = os.path.dirname(__file__)

    def test_20_elementos(self):
        new_path = self.cur_path + '\\test-juegodehermanos\\parte1-test\\20.txt'
        self.lista = set_files.set_coins(new_path)
        res_s, _ = greedy.main(self.lista)
        self.assertEqual(res_s, 7165)

    def test_25_elementos(self):
        new_path = self.cur_path + '\\test-juegodehermanos\\parte1-test\\25.txt'
        self.lista = set_files.set_coins(new_path)
        res_s, _ = greedy.main(self.lista)
        self.assertEqual(res_s, 9635)
    
    def test_50_elementos(self):
        new_path = self.cur_path + '\\test-juegodehermanos\\parte1-test\\50.txt'
        self.lista = set_files.set_coins(new_path)
        res_s, _ = greedy.main(self.lista)
        self.assertEqual(res_s, 17750)
    
    def test_100_elementos(self):
        new_path = self.cur_path + '\\test-juegodehermanos\\parte1-test\\100.txt'
        self.lista = set_files.set_coins(new_path)    
        res_s, _ = greedy.main(self.lista)
        self.assertEqual(res_s, 35009)
    
    def test_1000_elementos(self):
        new_path = self.cur_path + '\\test-juegodehermanos\\parte1-test\\1000.txt'
        self.lista = set_files.set_coins(new_path)     
        res_s, _ = greedy.main(self.lista)
        self.assertEqual(res_s, 357814)
    
    def test_10000_elementos(self):
        new_path = self.cur_path + '\\test-juegodehermanos\\parte1-test\\10000.txt'
        self.lista = set_files.set_coins(new_path)    
        res_s, _ = greedy.main(self.lista)
        self.assertEqual(res_s, 3550307)
    
    def test_20000_elementos(self):
        new_path = self.cur_path + '\\test-juegodehermanos\\parte1-test\\20000.txt'
        self.lista = set_files.set_coins(new_path)      
        res_s, _ = greedy.main(self.lista)
        self.assertEqual(res_s, 7139357)
    

if __name__ == '__main__':
    unittest.main()


