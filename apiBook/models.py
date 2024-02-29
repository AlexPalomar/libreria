from django.db import models

# Create your models here.
class Book(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    date_publication = models.DateField()
    editor = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='imagenes/', blank=True, null=True)

    objects = models.Manager()
    # def __str__(self):
    #     return self.title

