from django.db import connection
from django.db.utils import DataError
from .models import CallesGeocod
from .exceptions import CalleNoExiste, InterseccionNoExiste, AlturaNoExiste, TramoNoExiste, AlturaInicialAlturaFinal


def get_calles():
    """
    Retorna una lista con los nombres de todas las calles de CABA.
    :return: list
    """
    query = CallesGeocod.objects.order_by('nombre').distinct('nombre')
    return [calle.nombre for calle in query if calle.nombre is not None]


def interseccion(c1, c2):
    """
    Retorna un diccionario con el nombre de la interseccion y el wkt en wgs_1984
    del punto donde las dos calles se intersectan.
    :param c1 str: nombre de la primera calle.
    :param c2 str: nombre de la segunda calle.
    :return: dict
    """
    try:
        calle1 = Calle(c1)
        calle2 = Calle(c2)
        diccionario = {'interseccion': '{} y {}'.format(calle1.nombre, calle2.nombre),
                       'coordenadas': calle1 + calle2}
    except CalleNoExiste as e:
        return {'error': str(e)}
    except InterseccionNoExiste as e:
        return {'error': str(e)}
    except DataError as e:
        return {'error': str(e)}
    except Exception as e:
        return {'error': str(e)}

    return diccionario


def altura_calle(c, altura):
    """
    Retorna un diccionario con el nombre y altura de la calle especificada
    y el wkt en wgs1984 del punto correspondiente a esa altura.
    :param c str: calle a buscar
    :param altura int: altura de la calle a buscar
    """
    try:
        calle = Calle(c)
        diccionario = {'direccion': '{} {}'.format(calle.nombre, altura),
                       'coordenadas': calle.ubicar_altura(altura)}
    except CalleNoExiste as e:
        return {'error': str(e)}
    except AlturaNoExiste as e:
        return {'error': str(e)}
    except DataError as e:
        return {'error': str(e)}
    except Exception as e:
        return {'error': str(e)}

    return diccionario


def tramo(c, inicial, final):
    """
    Retorna un diccionario con el nombre y altura final e inicial del tramo
    buscado y el wkt en web mercator (3857).
    :param c str: calle a buscar
    :param inicial int: altura inicial del tramo
    :param final int: altura final del tramo
    """
    try:
        calle = Calle(c)
        diccionario = {'tramo': '{} entre {} y {}'.format(calle.nombre, inicial, final),
                       'coordenadas': calle.tramo(inicial, final)}
    except CalleNoExiste as e:
        return {'error': str(e)}
    except AlturaNoExiste as e:
        return {'error': str(e)}
    except TramoNoExiste as e:
        return {'error': str(e)}
    except DataError as e:
        return {'error': str(e)}
    except Exception as e:
        return {'error': str(e)}

    return diccionario


class Calle:

    def __init__(self, nombre):
        """
        Toma el nombre de una calle y chequea su existencia
        :param nombre: str
        """
        query = "select existe_calle(%s)"
        resultado = self._ejecutar_query(query, nombre)

        if not resultado:
             raise CalleNoExiste('la calle {} no existe'.format(nombre))

        self.nombre = nombre.lower()

    @staticmethod
    def _ejecutar_query(query, *args):
        """
        Ejecuta la query que se pasa como argumento
        :param query: string que representa la query apropiadamente formateada
        con %s como placeholders de los parametros:
        'select function(%s [...%s])'
        :param args: argumentos a pasarle a la query
        :return : resultado de la query. Retorna None si no arroja resultado
        """
        with connection.cursor() as cursor:
            cursor.execute(query, args)
            resultado = cursor.fetchone()[0]

        return resultado

    def ubicar_altura(self, altura):
        """
        Retorna un string que representa la geometria en wkt
        en crs wgs84 del punto que marca
        el numero de casa pasado como parametro.
        :param altura int: numero de casa
        :return str: representacion en string de la geometria en wkt
        """
        query = "select st_astext(altura_direccion_calle(%s, %s))"
        resultado = self._ejecutar_query(query, self.nombre, altura)

        if not resultado:
            raise AlturaNoExiste('la altura {} no existe para la calle solicitada'.format(altura))

        return resultado

    def tramo(self, altura_inicial, altura_final):
        """
        Retorna el tramo de la calle comprendido entre la altura
        inicial y la altura final especificada en wkt en
        web mercator (3857).
        :param altura_inicial int: altura inicial del tramo 
        :param altura_final int: altura final del tramo (inclusive) 
        :return str: representacion en string de la geometria en wkt 
        """
        # Comprobar altura inicial y altura final
        self.ubicar_altura(altura_inicial)
        self.ubicar_altura(altura_final)

        # Comprobar que altura inicial es menor que altura final
        # y que tienen 100 mts o mas de diferencia
        altura_inicial_int = int(altura_inicial)
        altura_final_int = int(altura_final)
        if (altura_inicial_int >= altura_final_int) or (altura_final_int - altura_inicial_int) < 100:
            raise AlturaInicialAlturaFinal('la altura inicial debe ser menor que la final'
                                           ' y tener una diferencia de 100 mts o mas')

        query = "select st_astext((select * from union_geom(%s, %s, %s)))"
        resultado = self._ejecutar_query(query, self.nombre, altura_inicial, altura_final)

        return resultado

    def __add__(self, other):
        """
        Sobrecarga el operador + para permitir el retorno de la representacion
        en wkt de la geometria de una interseccion al sumar dos instancias de Calle:
        calle1 + calle2
        :param other: la otra instancia de Calle
        :return str: representacion en wkt del punto que marca
        la interseccion en crs wgs84
        """
        query = "select st_astext(punto_interseccion(%s, %s))"
        resultado = self._ejecutar_query(query, self.nombre, other.nombre)

        if not resultado:
            raise InterseccionNoExiste('no se encontro la interseccion')

        return resultado

    def __str__(self):
        return '{}'.format(self.nombre)
