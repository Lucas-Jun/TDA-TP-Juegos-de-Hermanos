import unittest
import p_dinamica
import set_files
import os

class TestGreegy(unittest.TestCase):
    
    def setUp(self) -> None:
        self.cur_path = os.path.dirname(__file__)

    def test_5_elementos(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte2-tests\\5.txt'
        self.lista = set_files.set_coins(new_path)
        _, res = p_dinamica.solucion_dinamica(self.lista)
        self.assertEqual(res, 1483)

    def test_10_elementos(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte2-tests\\10.txt'
        self.lista = set_files.set_coins(new_path)
        _, res = p_dinamica.solucion_dinamica(self.lista)
        self.assertEqual(res, 2338)

    def test_20_elementos(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte2-tests\\20.txt'
        self.lista = set_files.set_coins(new_path)
        _, res = p_dinamica.solucion_dinamica(self.lista)
        self.assertEqual(res, 5234)

    def test_25_elementos(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte2-tests\\25.txt'
        self.lista = set_files.set_coins(new_path)
        _, res = p_dinamica.solucion_dinamica(self.lista)
        self.assertEqual(res, 7491)
    
    def test_50_elementos(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte2-tests\\50.txt'
        self.lista = set_files.set_coins(new_path)
        _, res = p_dinamica.solucion_dinamica(self.lista)
        self.assertEqual(res, 14976)
    
    def test_100_elementos(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte2-tests\\100.txt'
        self.lista = set_files.set_coins(new_path)    
        _, res = p_dinamica.solucion_dinamica(self.lista)
        self.assertEqual(res, 28844)
    
    def test_1000_elementos(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte2-tests\\1000.txt'
        self.lista = set_files.set_coins(new_path)     
        _, res = p_dinamica.solucion_dinamica(self.lista)
        self.assertEqual(res, 1401590)
    
    def test_2000_elementos(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte2-tests\\2000.txt'
        self.lista = set_files.set_coins(new_path)     
        _, res = p_dinamica.solucion_dinamica(self.lista)
        self.assertEqual(res, 2869340)

    def test_5000_elementos(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte2-tests\\5000.txt'
        self.lista = set_files.set_coins(new_path)     
        _, res = p_dinamica.solucion_dinamica(self.lista)
        self.assertEqual(res, 9939221)

    def test_10000_elementos(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte2-tests\\10000.txt'
        self.lista = set_files.set_coins(new_path)    
        _, res = p_dinamica.solucion_dinamica(self.lista)
        self.assertEqual(res, 34107537)
    

if __name__ == '__main__':
    unittest.main()