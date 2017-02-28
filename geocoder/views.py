from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import interseccion


class InterseccionView(APIView):

    def get(self, request):
        calle1 = request.GET.get('calle1', None)
        calle2 = request.GET.get('calle2', None)
        inter = interseccion(calle1, calle2)
        if 'error' in inter.keys():
            response = Response(inter, status=status.HTTP_400_BAD_REQUEST)
        elif not inter:
            response = Response({}, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = Response(inter, status=status.HTTP_200_OK)

        return response
