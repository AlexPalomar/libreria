import json
import requests
from ..models import Book
from rest_framework.response import Response
from rest_framework import status
from ..serializers import BookSerializer

class ServicesBook:
    def get_book(self, request):
        try:
            key = request.query_params['key']
            params = request.query_params['value']
            values = {key:params}
            result = Book.objects.filter(**values).values()
            if result.exists():
                data = {'DB interna' : result}
                return data
            data_external = self.get_book_external(values)
            data = {'DB google' : data_external}
            return data
        except requests.exceptions.ConnectionError  as error_connection:
            print("Error de conexión:", error_connection)
            return str(error_connection)
        except requests.exceptions.RequestException as error:  
            print(error)
            return str(error)
        
    def get_book_external(self, values):
        try:
            search_params = {'intitle':'title', 'inauthor': 'author', 'inpublisher': 'date_publication'}
            search_option = ['isbn','intitle','inauthor','inpublisher','subject','']
            urlapi = f"https://www.googleapis.com/books/v1/volumes?q={values}&maxResults=1"
            response = requests.get(urlapi)
            query_result = []
            if response.status_code == 200:
                data = response.json()
                for item in data.get('items', []):
                    volume_info = item.get('volumeInfo', {})
                    id = item.get('id', '')
                    isbn = volume_info.get('industryIdentifiers',[])
                    title = volume_info.get('title', 'Sin título')
                    subtitle = volume_info.get('subtitle', '')
                    authors = volume_info.get('authors', [])
                    categories = volume_info.get('categories', [])
                    description = volume_info.get('description', '')
                    publisher = volume_info.get('publisher', '')
                    publishedDate = volume_info.get('publishedDate', '')
                    query_result.append({
                        'id': id,
                        'isbn' : isbn,
                        'title': title,
                        'subtitle': subtitle,
                        'author': str(authors),
                        'category': str(categories),
                        'description': description,
                        'editor': publisher,
                        'date_publication': publishedDate
                    })
                print(self.create_book(query_result))
                return query_result
            return 'ha ocurrido un problema'
        except requests.exceptions.ConnectionError  as error_connection:
            print("Error de conexión:", error_connection)
            return str(error_connection)
        except requests.exceptions.RequestException as error:  
            print(error)
            return str(error)
    
    def create_book(self, query_result):
        query = query_result[0]
        query.pop('id')
        query.pop('isbn')
        # result = Book.objects.create(**query)
        # datos = {'title':'test','author':'Vicente Blazco Ibañez'}
        result = BookSerializer(data=query)
        if result.is_valid():
            result.save()
            return result.data
        return result.errors
        