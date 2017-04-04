from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .helpers import get_calles, interseccion, altura_calle, tramo


class NombresCallesView(APIView):

    def get(self, request):
        response = Response(get_calles(), status=status.HTTP_200_OK)

        return response


class InterseccionView(APIView):

    def get(self, request):
        calle1 = request.GET.get('calle1', None)
        calle2 = request.GET.get('calle2', None)
        inter = interseccion(calle1, calle2)
        if not calle1 or not calle2:
            response = Response({'error': 'deben suministrarse dos calles'},
                                status=status.HTTP_400_BAD_REQUEST)
        elif 'error' in inter.keys():
            response = Response(inter, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = Response(inter, status=status.HTTP_200_OK)

        return response


class AlturaView(APIView):

    def get(self, request):
        calle = request.GET.get('calle', None)
        altura = request.GET.get('altura', None)
        _altura_calle = altura_calle(calle, altura)
        if not calle or not altura:
            response = Response({'error': 'deben suministrarse calle y altura'},
                                status=status.HTTP_400_BAD_REQUEST)
        elif 'error' in _altura_calle.keys():
            response = Response(_altura_calle, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = Response(_altura_calle, status=status.HTTP_200_OK)

        return response


class TramoView(APIView):

    def get(self, request):
        calle = request.GET.get('calle', None)
        altura_inicial = request.GET.get('inicial', None)
        altura_final = request.GET.get('final', None)
        _tramo = tramo(calle, altura_inicial, altura_final)
        if not calle or not altura_inicial or not altura_final:
            response = Response({'error': 'deben suministrarse calle, altura inicial y altura final'},
                                status=status.HTTP_400_BAD_REQUEST)
        elif 'error' in _tramo.keys():
            response = Response(_tramo, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = Response(_tramo, status=status.HTTP_200_OK)

        return response
