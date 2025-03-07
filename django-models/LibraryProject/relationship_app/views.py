from django.shortcuts import render
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

@permission_required('relationship_app.can_add_book')
def add_book(request):
    # Add book logic here
    pass

# Create your views here.
def check_admin(user):
    return user.userprofile.role == 'Admin'

@user_passes_test(check_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')

def list_books(request):
    books = Books.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books':books})

from django.views.generic import DetailView
from .models import Library

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
