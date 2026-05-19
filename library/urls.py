from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('books/', views.book_list, name='book_list'),

    # Bookmarks
    path(
        'bookmark/add/<int:book_id>/',
        views.add_bookmark,
        name='add_bookmark'
    ),

    path(
        'bookmark/remove/<int:book_id>/',
        views.remove_bookmark,
        name='remove_bookmark'
    ),

    # Downloads
    path(
        'download/<int:book_id>/',
        views.download_book,
        name='download_book'
    ),

    # AI Chatbot
    path('ai-chat/', views.ai_chat, name='ai_chat'),
]