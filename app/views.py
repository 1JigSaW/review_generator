import uuid

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import ReviewLink, Language, Tag
from app.serializers import LanguageSerializer, TagSerializer, ReviewLinkSerializer
from review_generator import settings
from services.openai_service import generate_review


class CreateUniqueLink(APIView):
    def post(self, request):
        if settings.DEBUG:
            fake_link = f"https://test.com/test-{uuid.uuid4()}"
            return Response({"link": fake_link}, status=status.HTTP_201_CREATED)
        review_link = ReviewLink.objects.create()
        serializer = ReviewLinkSerializer(review_link)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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