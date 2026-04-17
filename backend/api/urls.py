from django.urls import path
from .views import BookListView, RAGQueryView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('query/', RAGQueryView.as_view(), name='rag-query'),
]