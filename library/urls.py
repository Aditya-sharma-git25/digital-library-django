from django.urls import path
import library.views as views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ai-chat/', views.ai_chat, name='ai_chat'),
    path('bookmark/<int:book_id>/', views.add_bookmark, name='add_bookmark'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
]