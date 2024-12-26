from rest_framework import serializers
from app.models import ReviewLink, Language, Tag

class ReviewLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewLink
        fields = ['unique_link', 'created_at']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'code', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
