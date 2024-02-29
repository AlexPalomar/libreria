from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from .services.service_book import ServicesBook
from django.urls import reverse
import requests

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

# class CustomTokenObtainPairView(TokenObtainPairView):
#     # permission_classes = (permissions.AllowAny,)  # Puedes ajustar esto según tus necesidades.
#     permission_classes = [ IsAuthenticated ] # Puedes ajustar esto según tus necesidades.

# class CustomTokenRefreshView(TokenRefreshView):
#     permission_classes = [ IsAuthenticated ]
#     # permission_classes = (permissions.AllowAny,)  

class GetBooksView(APIView):
    # permission_classes = [ IsAuthenticated ]
    def get(self, request):
        # Lógica para manejar la solicitud GET
        data = Book.objects.filter().values()
        # api = Service.generate_request(self, 'https://randomuser.me/api'+'?results=2')
        # data = {'message': 'This is a GET request'}
        # return Response(api, status=status.HTTP_200_OK)
        return Response(data, status=status.HTTP_200_OK)

class CreateBookView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetBookExternalView(APIView):
    def get(self, request):
        try:
            # isbn = 9783442178582 ##habitos atomicos
            isbn = 9780060919764 ##tus zonas erroneas
            #para consultar libro con isbn
            # url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key=AIzaSyCnVgE5NLsPkDFLS4MG8yR_qrS_xo1COCU"
            
            #para colsultar varios libros sin isbn 
            url = f"https://www.googleapis.com/books/v1/volumes"
            # Parámetros de la consulta
            params = {
                "q": "Python programming",  # Query de búsqueda
                "maxResults": 5  # Número máximo de resultados a devolver
            }
            response = requests.get(url, params)
            datos = []
            if response.status_code == 200:
                data = response.json()
                for item in data.get('items', []):
                    volume_info = item.get('volumeInfo', {})
                    title = volume_info.get('title', 'Sin título')
                    subtitle = volume_info.get('subtitle', '')
                    authors = volume_info.get('authors', [])
                    categories = volume_info.get('categories', [])
                    description = volume_info.get('description', '')
                    publisher = volume_info.get('publisher', '')
                    publishedDate = volume_info.get('publishedDate', '')
                    datos.append({
                        'titulo': title,
                        'subtitulo': subtitle,
                        'autores': authors,
                        'categorias': categories,
                        'descripcion': description,
                        'editor': publisher,
                        'fechaPublicacion': publishedDate
                    })
                return Response(datos, status=status.HTTP_200_OK)
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(str(error))
            Response(str(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetBook(APIView):
    def get(self, request):
        try:
            service_book = ServicesBook()
            response = service_book.get_book(request=request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as error:
            Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
         
