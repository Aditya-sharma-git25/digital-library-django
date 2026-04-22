from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Book, Bookmark
import json
from django.db.models import Q 


def home(request):
    return render(request, "library/home.html")



def dashboard(request):
    total_books = Book.objects.count()
    saved_books = 0

    if request.user.is_authenticated:
        saved_books = Bookmark.objects.filter(user=request.user).count()

    return render(request, "library/dashboard.html", {
        "total_books": total_books,
        "saved_books": saved_books
    })


def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "library/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "library/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


from django.db.models import Q

def book_list(request):
    books = Book.objects.all()
    bookmarked_books = []

    query = request.GET.get("q")
    category = request.GET.get("category")
    year = request.GET.get("year")

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )

    if category:
        books = books.filter(category__icontains=category)

    if year:
        books = books.filter(year=year)

    if request.user.is_authenticated:
        bookmarked_books = list(
            Bookmark.objects.filter(user=request.user).values_list("book_id", flat=True)
        )

    return render(request, "library/book_list.html", {
        "books": books,
        "bookmarked_books": bookmarked_books,
        "query": query,
        "category": category,
        "year": year,
    })


@login_required
def add_bookmark(request, book_id):
    if request.method == "POST":
        book = get_object_or_404(Book, id=book_id)
        Bookmark.objects.get_or_create(user=request.user, book=book)
    return redirect("book_list")


@login_required
def remove_bookmark(request, book_id):
    if request.method == "POST":
        book = get_object_or_404(Book, id=book_id)
        Bookmark.objects.filter(user=request.user, book=book).delete()
    return redirect("book_list")


@login_required
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related("book")
    return render(request, "library/bookmarks.html", {
        "bookmarks": bookmarks
    })


@csrf_exempt
def ai_chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", "").lower()

        books = Book.objects.filter(category__icontains=message)

        if books.exists():
            results = []
            for book in books[:5]:
                results.append({
                    "title": book.title,
                    "author": book.author
                })

            return JsonResponse({
                "reply": "Here are some books you may like:",
                "books": results
            })

        return JsonResponse({
            "reply": "Sorry, I couldn't find books for that genre."
        })

    return JsonResponse({
        "reply": "Invalid request method."
    })