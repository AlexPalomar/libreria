from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    # author = serializers.ChoiceField(source='author[0]')
    # category = serializers.ChoiceField(source='category[0]')
    class Meta:
        model = Book
        fields = '__all__'
        # fields = ['title','author']
        # exclude = ['source', 'isbn']