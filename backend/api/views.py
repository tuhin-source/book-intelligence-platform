from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer # You'll need to create this
from engine.rag_pipeline import BookRAGPipeline # Import your working class

class RAGQueryView(APIView):
    """POST API for RAG queries """
    def post(self, request):
        query_text = request.data.get('query')
        if not query_text:
            return Response({"error": "No query provided"}, status=400)
        
        rag = BookRAGPipeline()
        # This returns Answer, Summary, Genre, Recommendations, and Sources [cite: 35, 44]
        result = rag.query(query_text) 
        return Response(result)

class BookListView(APIView):
    """GET API to list all books [cite: 18]"""
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)