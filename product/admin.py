from django.contrib import admin
from .models import Product ,Category, ReviewRating

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'created_date', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    search_fields = ('product_name', 'price', 'category')
    
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'subject', 'rating')

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
