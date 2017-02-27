import json
from rest_framework import serializers


class GeocoderSerializer(serializers.Serializer):

    def interseccion(self, calle1, calle2):
        diccionario = {'nombre_calles': '{} y {}'.format(calle1.nombre, calle2.nombre),
                       'interseccion': calle1 + calle2}
        return json.dumps(diccionario)