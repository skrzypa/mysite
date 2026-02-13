from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth.decorators import login_required

from .models import NewBook
from .forms import NewBookForm

from pprint import pprint


@login_required(login_url= "my_apps:users_log_in")
def books(request: WSGIRequest) -> render:

    all_books = take_my_books(request)
    books_template = create_template(request, all_books)

    if 'add_new_book' in request.POST:
        return add_new_book(request, all_books)
    
    if 'del_book' in request.POST:
        return delete_book(request)
    
    if "edit_book" in request.POST:
        return edit_book(request)

    return render(
        request, 
        'books/books.html',
        context= {
            'all_books': books_template,
            'new_book_form': render(
                    request, 
                    "books/new_book_form.html", 
                    context= {'form': NewBookForm()}
                ).content.decode('utf-8'),
            'site_name': "books | PSkrzynski"
        }
    )


def edit_book(request: WSGIRequest) -> JsonResponse:
    book_id = request.POST.get('edit_book')
    get_book = NewBook.objects.get(id= book_id)
    if request.user != get_book.owner:
        return JsonResponse(
            data= {
                "status": "success",
                "redirect": True,
                "redirect_url": reverse("books:books"),
            }
        )
    
    form: NewBookForm = NewBookForm(request.POST, instance= get_book)
    if form.is_valid():
        form.save()
    
    # get_book.title = request.POST['title']
    # get_book.author = request.POST['author']
    # get_book.date = request.POST['date']
    # get_book.link_to_cover = request.POST['link_to_cover']
    # get_book.hide = request.POST.get('hide') == 'on'
    # get_book.save()

    return JsonResponse(
        data= {
            "status": "success",
            "all_books": create_template(request, take_my_books(request)),
        }
    )


def delete_book(request: WSGIRequest) -> JsonResponse:
    try:
        book = NewBook.objects.get(id=request.POST['del_book'])
    except:
        return redirect(reverse("books:books"))

    if request.user != book.owner:
        return redirect(reverse("books:books"))
    
    book_id = book.id
    year = str(book.date.year)
    book.delete()

    all_books = take_my_books(request)
    redirect_needed = year not in all_books

    return JsonResponse(
        data= {
            "status": "success",
            "book_id": str(book_id),
            "edit_year": year,
            "yearhtml": create_year(request, year, all_books[year]),
            "bookshtml": create_books_loop(request, all_books[year], year),
            "redirect": redirect_needed,
            "redirect_url": reverse("books:books"),
        }
    )


def add_new_book(request: WSGIRequest, all_books: dict) -> JsonResponse:
    form = NewBookForm(request.POST)
    if form.is_valid():
        book = form.save(commit=False)
        book.owner = request.user
        book.save()

        year = str(book.date.year)

        redirect_needed = year not in all_books
        if redirect_needed:
            all_books[year] = []
        
        all_books[year].append(book)
        all_books[year] = sorted(all_books[year], key= lambda b: b.date)

        return JsonResponse(
            {
                "status": "success",
                "year": year,
                "yearhtml": create_year(request, year, all_books[year]),
                "bookshtml": create_books_loop(request, all_books[year], year),
                "redirect": redirect_needed,
                "redirect_url": reverse("books:books"),
            }
        )


def create_template(request: WSGIRequest, all_books: dict):
    books_template = []
    for year, books in all_books.items():
        books_template.append(
            create_year(request, year, books),
        )
        books_template.append(
            create_books_loop(request, books, year)
        )
    return "".join(books_template)


def take_my_books(request: WSGIRequest, user: User= None) -> dict:
    if not user:
        user = request.user
    my_books = NewBook.objects.all().filter(owner= user).order_by("date")

    all_books = {}
    for book in my_books:
        if str(book.date.year) not in all_books:
            all_books[str(book.date.year)] = []
        all_books[str(book.date.year)].append(book)

    all_books = dict(sorted(all_books.items(), key= lambda x: x[0], reverse= True))

    return all_books


def create_year(request: WSGIRequest, year: str, books: dict) -> str:
    return render(
        request,
        "books/year.html",
        context= {
            "year": year,
            'books': books,
        }
    ).content.decode('utf-8')


def create_books_loop(request: WSGIRequest, books: list[NewBook], year: str) -> str:
    return render(
        request,
        "books/books_loop.html",
        context= {
            "books": [create_book(request, book) for book in books],
            "year": year,
        }
    ).content.decode('utf-8')


def create_book(request: WSGIRequest, book: NewBook) -> str:
    return render(
        request,
        "books/book.html",
        context= {
            "book": book,
            "edit_form": NewBookForm(instance= book),
        }
    ).content.decode('utf-8')