from django.contrib import admin

from .models import Category, Product


# Ovo je samo alternativan pristup dobivanja podataka u /admin (alternativa: admin.site.register(Customer)), klasa isto nije potrebna, ali putem nje se kastomizira /admin prikaz
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'slug', 'price', 'in_stock', 'created', 'updated']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('title',)}
