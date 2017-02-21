from django.test import TestCase
from django.db import connection
from geocoder.helpers import Calle, get_calles
from geocoder.models import CallesGeocod
from geocoder.exceptions import CalleNoExiste, InterseccionNoExiste
from .database_definitions import *


class GeocoderTestCase(TestCase):
    """
    Testea la clase Calle, que maneja las funciones de la base
    de datos que conforman el geocodificador
    """
    def setUp(self):
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
        self.assertTrue('La calle aaaabbbb no existe', context.exception)

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
        self.assertTrue('No se Encontró la Intersección', context.exception)

    def test_get_calles(self):
        """
        Testea que la funcion get_calles() devuelva una lista
        en orden alfabetico con las calles que figuran en la base.
        :return:
        """
        calles = get_calles()
        self.assertEqual(['cabildo', 'juramento'], calles)


