from django.urls import path

from app.views import CreateUniqueLink, LanguageList, TagList, GenerateReview

urlpatterns = [
    path('create-link/', CreateUniqueLink.as_view(), name='create_link'),
    path("languages/", LanguageList.as_view(), name="language_list"),
    path("tags/", TagList.as_view(), name="tag_list"),
    path("generate-review/", GenerateReview.as_view(), name="generate_review"),
]
