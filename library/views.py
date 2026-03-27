from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Book, Bookmark
import json


def home(request):
    return render(request, "library/home.html")


@login_required
def dashboard(request):
    return render(request, "library/dashboard.html")


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


def book_list(request):
    books = Book.objects.all()
    return render(request, "library/book_list.html", {"books": books})


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


@login_required
def add_bookmark(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if not Bookmark.objects.filter(user=request.user, book=book).exists():
        Bookmark.objects.create(user=request.user, book=book)
        messages.success(request, "Book bookmarked successfully.")
    else:
        messages.info(request, "Book already bookmarked.")

    return redirect("book_list")


@login_required
def bookmarks(request):
    user_bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request, "library/bookmarks.html", {"bookmarks": user_bookmarks})