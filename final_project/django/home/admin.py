from django.contrib import admin
from .models import Category, Article, Comment, Bookmark, Rating

# Register your models here.

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Bookmark)
admin.site.register(Rating)