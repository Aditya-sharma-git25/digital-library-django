# 📚 E-Library Hub AI

E-Library Hub AI is a modern Digital Library Archive Web Portal developed using Django and Python.  
The platform provides students, researchers, and educators with centralized access to academic books and digital resources through an intelligent and user-friendly web application.

The system includes secure authentication, PDF viewing/downloading, bookmarks, dashboards, analytics, and an AI-powered recommendation chatbot using Natural Language Processing (NLP) techniques.

---

# 🚀 Features

## 👤 User Authentication
- User Registration
- Secure Login & Logout
- Django Authentication System
- Session Management

## 📖 Book Management
- Browse Available Books
- View Detailed Book Information
- Upload Books (Admin)
- Edit/Delete Books (Admin)
- PDF File Support

## 🔍 Advanced Search & Filtering
- Search by Title
- Search by Author
- Search by Category
- Search by Publication Year

## ⭐ User Features
- Bookmark/Favorite Books
- Personalized Dashboard
- Track Download Activity
- Responsive UI for Mobile/Desktop

## 🤖 AI-Powered Recommendation Chatbot
- NLP-based Recommendation System
- TF-IDF Vectorization
- Cosine Similarity Matching
- Suggests Books Based on User Interests
- Interactive Chatbot Interface

## 📊 Analytics
- Download Counter
- User Activity Tracking
- Dashboard Statistics

---

# 🛠️ Technology Stack

| Technology | Usage |
|------------|------|
| Python 3.x | Core Programming Language |
| Django | Backend Framework |
| HTML5 | Frontend Structure |
| CSS3 | Styling |
| Bootstrap 5 | Responsive Design |
| JavaScript | Frontend Interactivity |
| SQLite | Development Database |
| PostgreSQL | Production Database |
| Git & GitHub | Version Control |
| NLP / TF-IDF | AI Recommendation Engine |

---

# 🧠 AI Recommendation System

The project includes a content-based recommendation chatbot that recommends books based on:
- Genre
- User Interests
- Search Keywords
- Book Categories

The chatbot uses:
- TF-IDF Vectorization
- Cosine Similarity
- NLP-based text matching

---

# 📂 Project Structure

```bash
digital-library-django/
│
├── digital_library/
├── library/
├── templates/
├── static/
├── media/
├── db.sqlite3
├── manage.py
└── requirements.txt
