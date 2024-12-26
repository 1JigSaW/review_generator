from django.contrib import admin

from app.models import Language, Tag, ReviewLink, Review

admin.site.register(Language)
admin.site.register(Tag)
admin.site.register(ReviewLink)
admin.site.register(Review)
