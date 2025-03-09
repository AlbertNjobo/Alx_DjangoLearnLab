from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Article
from .models import Book
from .forms import ArticleForm

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Display a list of all books in the library.
    Requires 'can_view' permission from the Book model.
    """
    books = Book.objects.all()
    context = {
        'books': books,
        'title': 'Library Book List'
    }
    return render(request, 'bookshelf/book_list.html', context)
@permission_required('bookshelf.can_view', raise_exception=True)
def article_list(request):
    """View to list all articles"""
    articles = Article.objects.all()
    return render(request, 'articles/list.html', {'articles': articles})

@permission_required('bookshelf.can_create', raise_exception=True)
def article_create(request):
    """View to create a new article"""
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'articles/create.html', {'form': form})

@permission_required('bookshelf.can_edit', raise_exception=True)
def article_edit(request, pk):
    """View to edit an existing article"""
    article = get_object_or_404(Article, pk=pk)
    # Additional check to ensure only author or admin can edit
    if article.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to edit this article")
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/edit.html', {'form': form})

@permission_required('bookshelf.can_delete', raise_exception=True)
def article_delete(request, pk):
    """View to delete an article"""
    article = get_object_or_404(Article, pk=pk)
    # Additional check to ensure only author or admin can delete
    if article.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to delete this article")
    
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    return render(request, 'articles/delete.html', {'article': article})
