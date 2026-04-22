from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('books/', views.book_list, name='book_list'),

    path('bookmarks/', views.bookmark_list, name='bookmarks'),
    path('bookmark/add/<int:book_id>/', views.add_bookmark, name='add_bookmark'),
    path('bookmark/remove/<int:book_id>/', views.remove_bookmark, name='remove_bookmark'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    path('ai-chat/', views.ai_chat, name='ai_chat'),
]
