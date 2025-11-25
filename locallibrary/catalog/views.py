from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book, Author, BookInstance, Genre

# Главная страница (функция)
from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre

def index(request):
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    num_books_with_word = Book.objects.filter(title__icontains='война').count()

    # Получение количества посещений домашней страницы из сессии
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_with_word': num_books_with_word,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

# Список книг
class BookListView(ListView):
    model = Book
    paginate_by = 10

# Детали книги
class BookDetailView(DetailView):
    model = Book

# Список авторов
class AuthorListView(ListView):
    model = Author
    paginate_by = 10

# Детали автора
class AuthorDetailView(DetailView):
    model = Author