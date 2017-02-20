from django.test import TestCase
from geocoder.helpers import Calle
from geocoder.models import CallesGeocod
from .popular_database import *


class GeocoderTestCase(TestCase):

    def setUp(self):
        CallesGeocod.objects.raw(existe_calle)
        CallesGeocod.objects.raw(altura_total_calle)
        CallesGeocod.objects.raw(existe_altura)
        CallesGeocod.objects.raw(punto_interseccion)
        CallesGeocod.objects.raw(altura_direccion_calle)

        CallesGeocod.objects.create(**cabildo_2000)
        CallesGeocod.objects.create(**cabildo_2100)
        CallesGeocod.objects.create(**juramento_2350)
        CallesGeocod.objects.create(**juramento_2400)


    def test_crea_calle(self):
        """
        #calle = Calle('cabildo')
        #self.assertEqual(calle.nombre, 'cabildo')
        """
        q = CallesGeocod.objects.raw("select existe_calle('cabildo')")
        self.assertTrue(q)

