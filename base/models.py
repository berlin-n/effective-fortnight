from django.db import models
from django.contrib.auth.models import User, AbstractUser


# interaction_choices = (
#     ('Read', 'Read'),
#     ('Rated', 'Rated'),
#     ('Wishlist', 'Wishlist')
# )

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ManyToManyField(Author, related_name="author", blank=True)
    genre = models.ManyToManyField(Genre, related_name="genre", blank=True)
    publication_year = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)
    average_rating = models.FloatField()
    total_rating = models.IntegerField()
    number_of_pages = models.IntegerField()
    cover_img = models.ImageField(null=True, upload_to="images/")

    def __str__(self):
        return self.title
    
# class Book_User_Interaction(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE) 
#     interaction_type = models.CharField(max_length=10, choices=interaction_choices)
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.interaction_type

class Rating(models.Model):
    rating = models.IntegerField()
    name = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name
    
class My_Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, null= True)
    created = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

# class RecommendedBooks(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
