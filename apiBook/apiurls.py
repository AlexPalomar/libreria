from django.urls import path
from .views_api import GetBooksView, GetBook, CreateBookView, GetBookExternalView 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from .viewsApi import LoginApi, UserApi, ArtistApi

urlpatterns = [
    # path('api/signin/', LoginApi.as_view(), name='signin'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/books/', GetBooksView.as_view()),
    path('api/book/', GetBook.as_view()),
    path('api/book/create', CreateBookView.as_view(), name='book'),
    path('api/books/external/', GetBookExternalView.as_view()),
    # path('api/book/external/', GetBookExternal.as_view()),
    # Agrega otras URL para diferentes vistas de la API aquí
]