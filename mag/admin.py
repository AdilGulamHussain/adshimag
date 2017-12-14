from django.contrib import admin
from .models import Article, Category, Comment


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    exclude = ('date_posted', 'slug', 'view_count', 'likes',)


class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
