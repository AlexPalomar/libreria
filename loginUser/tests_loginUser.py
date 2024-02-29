from django.test import TestCase

# Create your tests here.
import json

# Django Rest Framework
from rest_framework.test import APIClient
from rest_framework import status

# Models
# from models import User

class LoginUserTestCase:
    def setUp(self):
        user = User(
            email='testing_login@test.com',
            first_name='Testing',
            last_name='Testing',
            username='testing_login'
        )
        user.set_password('admin123')
        user.save()