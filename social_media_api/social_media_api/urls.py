from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to the Social Media API Home!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('', include('accounts.urls')),
        path('', include('posts.urls')),
    ])),
    path('api-auth/', include('rest_framework.urls')),
    path('', home_view, name='home'),
]
