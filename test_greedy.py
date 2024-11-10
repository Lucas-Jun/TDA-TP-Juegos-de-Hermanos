import unittest
import greedy
import set_files
import os

class TestGreegy(unittest.TestCase):

    def setUp(self) -> None:
        self.cur_path = os.path.dirname(__file__)

    def test_20_elementos(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte1-tests\\20.txt'
        self.lista = set_files.set_coins(new_path)
        res_s, _, _ = greedy.solucion_greedy(self.lista)
        self.assertEqual(res_s, 7165)

    def test_25_elementos(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte1-tests\\25.txt'
        self.lista = set_files.set_coins(new_path)
        res_s, _, _ = greedy.solucion_greedy(self.lista)
        self.assertEqual(res_s, 9635)
    
    def test_50_elementos(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte1-tests\\50.txt'
        self.lista = set_files.set_coins(new_path)
        res_s, _, _ = greedy.solucion_greedy(self.lista)
        self.assertEqual(res_s, 17750)
    
    def test_100_elementos(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte1-tests\\100.txt'
        self.lista = set_files.set_coins(new_path)    
        res_s, _, _ = greedy.solucion_greedy(self.lista)
        self.assertEqual(res_s, 35009)
    
    def test_1000_elementos(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte1-tests\\1000.txt'
        self.lista = set_files.set_coins(new_path)     
        res_s, _, _ = greedy.solucion_greedy(self.lista)
        self.assertEqual(res_s, 357814)
    
    def test_10000_elementos(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte1-tests\\10000.txt'
        self.lista = set_files.set_coins(new_path)    
        res_s, _, _ = greedy.solucion_greedy(self.lista)
        self.assertEqual(res_s, 3550307)
    
    def test_20000_elementos(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte1-tests\\20000.txt'
        self.lista = set_files.set_coins(new_path)      
        res_s, _, _ = greedy.solucion_greedy(self.lista)
        self.assertEqual(res_s, 7139357)

    def test_Bordes_Iguales(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte1-tests\\Bordes-Iguales.txt'
        self.lista = set_files.set_coins(new_path)      
        res_s, _, _ = greedy.solucion_greedy(self.lista)
        self.assertEqual(res_s, 153)

    def test_Cantidad_Impar(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte1-tests\\Cantidad-Impar.txt'
        self.lista = set_files.set_coins(new_path)      
        res_s, _, _ = greedy.solucion_greedy(self.lista)
        self.assertEqual(res_s, 32)
    
    def test_Orden_Creciente(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte1-tests\\Orden-Creciente.txt'
        self.lista = set_files.set_coins(new_path)      
        res_s, _, _ = greedy.solucion_greedy(self.lista)
        self.assertEqual(res_s, 51)
    

    def test_Orden_Decreciente(self):
        new_path = self.cur_path + '\\test-juegoDeHermanos\\parte1-tests\\Orden-Decreciente.txt'
        self.lista = set_files.set_coins(new_path)      
        res_s, _, _ = greedy.solucion_greedy(self.lista)
        self.assertEqual(res_s, 51)

    

if __name__ == '__main__':
    unittest.main()