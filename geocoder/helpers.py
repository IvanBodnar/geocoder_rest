from django.db import connection
from .models import CallesGeocod
from .exceptions import CalleNoExiste, InterseccionNoExiste


def get_calles():
    """
    Retorna una lista con los nombres de todas las calles de CABA
    :return: list
    """
    query = CallesGeocod.objects.order_by('nombre').distinct('nombre')
    return [calle.nombre for calle in query if calle.nombre is not None]


class Calle:

    def __init__(self, nombre):
        """
        Toma el nombre de una calle y chequea su existencia
        :param nombre: str
        """
        query = "select existe_calle(%s)"
        resultado = self._ejecutar_query(query, nombre)

        if not resultado:
             raise CalleNoExiste('La calle {} no existe'.format(nombre))

        self.nombre = nombre.lower()

    def _ejecutar_query(self, query, *args):
        """
        Executes the passed query
        :param query: query string properly formatted
        with %s as parameter placeholders:
        'select function(%s [...%s])'
        :param args: arguments to be passed to the query
        :return : query result. None if no result was retrieved.
        """
        with connection.cursor() as cursor:
            cursor.execute(query, args)
            resultado = cursor.fetchone()[0]
        return resultado

    def ubicar_altura(self, altura):
        """
        Returns a string representation of the geometry
        in wgs84 crs of the point that marks
        the house number passed.
        :param altura int: house number
        :return str: string representation of geometry
        """
        query = "select st_astext(altura_direccion_calle(%s, %s))"
        return self._ejecutar_query(query, self.nombre, altura)

    def __add__(self, other):
        """
        Overloads + operator to allow the return of the geometry
        of an intersection by adding two Calle instances:
        street1 + street2
        :param other: the other Calle instance
        :return str: string representation of the point marking
        the intersection in wgs84 crs.
        """
        query = "select st_astext(punto_interseccion(%s, %s))"
        resultado = self._ejecutar_query(query, self.nombre, other.nombre)

        if not resultado:
            raise InterseccionNoExiste('No se Encontró la Intersección')

        return resultado

    def __str__(self):
        return '{}'.format(self.nombre)
