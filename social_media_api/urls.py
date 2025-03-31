from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
# ...existing imports...

def home_view(request):
    return HttpResponse("Welcome to the Social Media API Home!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # ...existing patterns such as media serving...
    path('', home_view, name='home'),  # Add this for root path
]
