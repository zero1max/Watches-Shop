from django.contrib import admin
from .models import Watches, News, Category
from django.utils.html import format_html

# Register your models here.
class WatchesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'get_discount_price', 'quantity','category', 'created_at', 'updated_at', 'is_published', 'photo_tag']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'description']
    list_editable = ['is_published', 'category']
    prepopulated_fields = {"slug": ('title',)}
    list_filter = ['is_published', 'category']

    def photo_tag(self, obj):
        if obj.photo:
            return format_html(f'<img src="{obj.photo.url}" width=80 height=auto>')
        else:
            return format_html('-')
    photo_tag.short_description = 'Photo'

    def get_discount_price(self, obj):
        return obj.get_discount_price()
    get_discount_price.short_description = 'Discount Price'

class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'is_published', 'photo_tag']
    list_editable = ['is_published']
    list_display_links = ['id', 'title']

    def photo_tag(self, obj):
        if obj.photo:
            return format_html(f'<img src="{obj.photo.url}" width=80 height=auto>')
        else:
            return format_html('-')
    photo_tag.short_description = 'Photo'

admin.site.register(Watches, WatchesAdmin)
admin.site.register(Category)
admin.site.register(News, NewsAdmin)