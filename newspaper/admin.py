from django.contrib import admin
from newspaper.models import Comment, Contact, Newsletter, Post, Category, Tag

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Contact)
admin.site.register(Newsletter)
admin.site.register(Comment)



