import uuid

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import ReviewLink, Language, Tag, Review
from app.serializers import LanguageSerializer, TagSerializer, ReviewLinkSerializer
from review_generator import settings
from services.openai_service import generate_review


class CreateUniqueLink(APIView):
    def post(self, request):
        review_link = ReviewLink.objects.create()
        if settings.DEBUG:
            fake_link = f"https://test.com/{review_link.unique_link}"
            return Response({"link": fake_link}, status=status.HTTP_201_CREATED)

        return Response({"error": "This endpoint is available only in DEBUG mode"}, status=status.HTTP_403_FORBIDDEN)


class GenerateReview(APIView):
    def post(self, request):
        try:
            tags = request.data.get("tags", [])
            language = request.data.get("language", "EN")

            if not tags:
                return Response({"error": "Tags are required"}, status=status.HTTP_400_BAD_REQUEST)

            generated_text = generate_review(tags, language)

            return Response({"review": generated_text}, status=status.HTTP_200_OK)

        except RuntimeError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LanguageList(APIView):
    def get(self, request):
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagList(APIView):
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SaveReview(APIView):
    def post(self, request):
        try:
            unique_link = request.data.get("unique_link")
            review_text = request.data.get("text", "")
            tags = request.data.get("tags", [])
            language_code = request.data.get("language")

            if not unique_link:
                return Response({"error": "Unique link is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                uuid_obj = uuid.UUID(unique_link.split("/")[-1])
            except ValueError:
                return Response({"error": f"'{unique_link}' is not a valid UUID"}, status=status.HTTP_400_BAD_REQUEST)
            print('uuid_obj', uuid_obj)
            review_link = get_object_or_404(ReviewLink, unique_link=uuid_obj)

            language = Language.objects.filter(code=language_code).first()
            if not language:
                return Response({"error": "Invalid language code"}, status=status.HTTP_400_BAD_REQUEST)

            review = Review.objects.create(
                link=review_link,
                text=review_text,
                language=language
            )

            if tags:
                tag_objects = Tag.objects.filter(name__in=tags)
                review.tags.set(tag_objects)

            return Response({"message": "Review saved successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
