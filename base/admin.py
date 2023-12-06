from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book, Author, Genre, Rating, My_Book, Wishlist

# Register your models here.

class My_BookAdmin(admin.ModelAdmin):
    list_display = ('user','book','rating')

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user','book')

class RecommededBookAdmin(admin.ModelAdmin):
    list_display = ('user','book')

admin.site.register(Book)
admin.site.register(Author)
# admin.site.register(Book_User_Interaction)
admin.site.register(Genre)
admin.site.register(Rating)
admin.site.register(My_Book, My_BookAdmin)
admin.site.register(Wishlist, WishlistAdmin)
# admin.site.register(RecommendedBooks, RecommededBookAdmin)