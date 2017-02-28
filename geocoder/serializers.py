from rest_framework import serializers
from .helpers import Calle
from .exceptions import CalleNoExiste, InterseccionNoExiste


def interseccion(c1, c2):
    try:
        calle1 = Calle(c1)
        calle2 = Calle(c2)
        diccionario = {'nombre_calles': '{} y {}'.format(calle1.nombre, calle2.nombre),
                       'interseccion': calle1 + calle2}
    except CalleNoExiste:
        return {'error': 'la calle no existe'}
    except InterseccionNoExiste:
        return {'error': 'la interseccion no existe'}

    return diccionario