from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=500, null=True, blank=True)
    rating = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    book_url = models.URLField(max_length=1000)
    
    # Required AI Insights (at least 2)
    summary = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=200, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title