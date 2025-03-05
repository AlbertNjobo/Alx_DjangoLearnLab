from django.contrib import admin
from .models import Book
# Register your models here.

@admin.register(Book)

class BookAdmin(admin.ModelAdmin):

    list_diplay = ('title', 'author', 'publication_year')

    list_filter = ('author', 'publication_year')

    search_fields = ('title', 'author')

    fieldsets = (('Book Details', {'fields':('title', 'author', 'publication_year')}),)
