from django.contrib import admin

from .models import User, Title, Category, Genre, Comment, Review

admin.site.register(User)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Review)
