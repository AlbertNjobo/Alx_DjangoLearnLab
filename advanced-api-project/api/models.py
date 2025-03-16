from django.db import models


class Book(models.Model):
   
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.DateField()
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        """
        Returns the string representation of the Book object.
        """
        return self.title
class Author(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        """
        Returns the string representation of the Author object.
        """
        return self.name


# Create your models here.
