import uuid

from django.db import models

class ReviewLink(models.Model):
    unique_link = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.unique_link)

class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    link = models.ForeignKey(ReviewLink, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='reviews')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name='reviews')  # Связь с языком
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50] if self.text else 'Review'
