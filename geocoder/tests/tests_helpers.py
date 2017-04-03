from django.test import TestCase
from django.db import connection
from geocoder.helpers import Calle, get_calles, interseccion, altura_calle, tramo
from geocoder.models import CallesGeocod
from geocoder.exceptions import CalleNoExiste, InterseccionNoExiste
from .database_definitions import *


def preparar_datos():
    """
   Incorpora a la base de datos que se crea para el testing
   las funciones del geocodificador y dos tramos de
   calles para prueba.
   Las definiciones vienen de database_definitions.py.
   Se usa cursor.execute() porque CallesGeocod.objects.raw()
   no funciona.
   """
    with connection.cursor() as cursor:
        # Incorporar las funciones
        cursor.execute(union_geom)
        cursor.execute(union_geom_v2)
        cursor.execute(existe_calle)
        cursor.execute(altura_total_calle)
        cursor.execute(existe_altura)
        cursor.execute(punto_interseccion)
        cursor.execute(altura_direccion_calle)

    # Incorporar dos tramos que se intersectan
    CallesGeocod.objects.create(**cabildo_2000)
    CallesGeocod.objects.create(**cabildo_2100)
    CallesGeocod.objects.create(**juramento_2350)
    CallesGeocod.objects.create(**juramento_2400)


class GeocoderCalleTestCase(TestCase):
    """
    Testea la clase Calle, que maneja las funciones de la base
    de datos que conforman el geocodificador
    """
    def setUp(self):
        preparar_datos()

    def test_crea_calle(self):
        """
        Testea si la calle es creada.
        :return:
        """
        calle = Calle('cabildo')
        self.assertEqual(calle.nombre, 'cabildo')

    def test_devuelve_punto_interseccion(self):
        """
        Testea si la suma de las instancias de Calle
        devuelve el punto correcto.
        :return:
        """
        calle1 = Calle('cabildo')
        calle2 = Calle('juramento')
        resultado = calle1 + calle2
        self.assertEqual('POINT(-58.4566933131458 -34.5620356414316)', resultado)

    def test_devuelve_punto_altura(self):
        """
        Testea si Calle.ubicar_altura() devuelve el
        punto correcto.
        :return:
        """
        calle = Calle('cabildo')
        resultado = calle.ubicar_altura(2002)
        self.assertEqual('POINT(-58.4558887506853 -34.5629698844945)', resultado)

    def test_raises_callenoexiste(self):
        """
        Testea si el ingreso de una calle que no existe
        levanta la excepcion CalleNoExiste.
        :return:
        """
        with self.assertRaises(CalleNoExiste) as context:
            Calle('aaabbbb')
        self.assertTrue('la calle aaaabbbb no existe', context.exception)

    def test_raises_interseccionnoexiste(self):
        """
        Testea que la suma de dos calles que no se intersectan
        levante la excepcion InterseccionNoExiste.
        :return:
        """
        with self.assertRaises(InterseccionNoExiste) as context:
            calle1 = Calle('juramento')
            calle2 = Calle('juramento')
            calle1 + calle2
        self.assertTrue('no se encontro la interseccion', context.exception)


class GeocoderFuncionesHelpersTestCase(TestCase):
    """
    Testea que las funciones wrapper devuelvan los
    correspondientes diccionarios.
    """
    def setUp(self):
        preparar_datos()

    def test_get_calles(self):
        calles = get_calles()
        self.assertEqual(['cabildo', 'juramento'], calles)

    def test_interseccion(self):
        calle1 = 'cabildo'
        calle2 = 'juramento'
        self.assertEqual({"interseccion": "cabildo y juramento",
                         "coordenadas": "POINT(-58.4566933131458 -34.5620356414316)"},
                         interseccion(calle1, calle2))

    def test_altura_calle(self):
        calle = 'cabildo'
        altura = 2115
        diccionario = {'direccion': 'cabildo 2115',
                       'coordenadas': 'POINT(-58.456815768952 -34.5618934492396)'}
        self.assertEqual(diccionario, altura_calle(calle, altura))


    def test_tramo(self):
        calle = 'cabildo'
        inicial = 2000
        final = 2199
        diccionario = {'tramo': 'cabildo entre 2000 y 2199',
                       'coordenadas': 'MULTILINESTRING((-6507277.94176834 -4104650.53997124,'
                                      '-6507369.33307795 -4104521.67427025))'}
        self.assertEqual(diccionario, tramo(calle, inicial, final))
