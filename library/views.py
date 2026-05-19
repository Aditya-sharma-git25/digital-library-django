from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Book, Bookmark, Download
import json
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def home(request):
    return render(request, "library/home.html")


@login_required(login_url='login')
def dashboard(request):
    total_books = Book.objects.count()
    total_bookmarks = Bookmark.objects.filter(user=request.user).count()
    total_downloads = Download.objects.filter(user=request.user).count()
    recent_books = Book.objects.order_by('-id')[:5]

    return render(request, 'library/dashboard.html', {
        'total_books': total_books,
        'total_bookmarks': total_bookmarks,
        'total_downloads': total_downloads,
        'recent_books': recent_books,
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

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(request, "Invalid username or password")
        return redirect("login")

    return render(request, "library/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required(login_url='login')
def book_list(request):
    books = Book.objects.all().order_by('-id')

    query = request.GET.get("q", "")
    category = request.GET.get("category", "")
    year = request.GET.get("year", "")

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )

    if category:
        books = books.filter(category__icontains=category)

    if year:
        books = books.filter(year=year)

    bookmarked_books = list(
        Bookmark.objects.filter(
            user=request.user
        ).values_list("book_id", flat=True)
    )

    return render(request, "library/book_list.html", {
        "books": books,
        "bookmarked_books": bookmarked_books,
        "query": query,
        "category": category,
        "year": year,
    })


@login_required(login_url='login')
def download_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.pdf:
        Download.objects.create(
            user=request.user,
            book=book
        )

        book.downloads += 1
        book.save()

        return FileResponse(
            book.pdf.open(),
            as_attachment=True,
            filename=book.pdf.name.split('/')[-1]
        )

    messages.error(request, "PDF file is not available for this book.")
    return redirect("book_list")


@login_required(login_url='login')
def add_bookmark(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    Bookmark.objects.get_or_create(
        user=request.user,
        book=book
    )

    return redirect("book_list")


@login_required(login_url='login')
def remove_bookmark(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    Bookmark.objects.filter(
        user=request.user,
        book=book
    ).delete()

    return redirect("book_list")


@login_required(login_url='login')
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(
        user=request.user
    ).select_related("book")

    return render(request, "library/bookmarks.html", {
        "bookmarks": bookmarks
    })


@csrf_exempt
def ai_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"reply": "Invalid request data."})

        message = data.get("message", "").strip().lower()

        if not message:
            if request.user.is_authenticated:
                username = request.user.username
                return JsonResponse({
                    "reply": f"Hello {username} 👋 I’m your AI Library Assistant. Ask me for books by topic, author, category, or subject."
                })
            else:
                return JsonResponse({
                    "reply": "Hello guest 👋 I can suggest books and give details, but login is required to read or download them."
                })

        greetings = ["hi", "hello", "hey", "hii", "good morning", "good evening", "gm"]

        if message in greetings:
            if request.user.is_authenticated:
                return JsonResponse({
                    "reply": f"Welcome back {request.user.username} 👋 Tell me what kind of book you want today."
                })
            else:
                return JsonResponse({
                    "reply": "Hello 👋 Welcome to e-Library Hub AI. I can recommend books, but please login to read or download them."
                })

        books = Book.objects.all()

        if not books.exists():
            return JsonResponse({
                "reply": "No books are available right now in our database."
            })

        book_list = list(books)
        documents = []

        for book in book_list:
            title = book.title or ""
            author = book.author or ""
            category = book.category or ""
            description = book.description or ""
            year = str(book.year) if book.year else ""

            documents.append(
                f"{title} {author} {category} {description} {year}"
            )

        documents.append(message)

        try:
            vectorizer = TfidfVectorizer(stop_words="english")
            tfidf_matrix = vectorizer.fit_transform(documents)

            similarities = cosine_similarity(
                tfidf_matrix[-1],
                tfidf_matrix[:-1]
            ).flatten()

            top_indices = similarities.argsort()[::-1][:5]

        except ValueError:
            return JsonResponse({
                "reply": "Please ask me using a topic, author, category, or book name."
            })

        results = []

        for idx in top_indices:
            if similarities[idx] > 0:
                book = book_list[idx]

                book_data = {
                    "title": book.title,
                    "author": book.author,
                    "category": book.category,
                    "year": book.year,
                    "description": book.description,
                    "can_read": request.user.is_authenticated,
                }

                if request.user.is_authenticated:
                    book_data["pdf"] = book.pdf.url if book.pdf else ""
                else:
                    book_data["pdf"] = ""

                results.append(book_data)

        if results:
            if request.user.is_authenticated:
                reply = f"Here are some books for you, {request.user.username} 📚"
            else:
                reply = "Here are some book suggestions 📚 Login to read or download them."

            return JsonResponse({
                "reply": reply,
                "books": results
            })

        return JsonResponse({
            "reply": "I couldn't find matching books 😔 Try another topic like Python, AI, history, novel, or programming."
        })

    return JsonResponse({
        "reply": "Invalid request method."
    })