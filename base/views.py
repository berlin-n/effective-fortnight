from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Book, My_Book, Wishlist, Rating
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .recommendation import get_recommendations, model, user_item_matrix

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user =  authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect")
    context = {'page': page}
    return render(request, 'base/index3.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('postRegister')
        else:
            messages.error(request, 'An error occured during registration')
    context = {'form': form}
    return render(request, 'base/index3.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    my_books = Book.objects.filter(title__icontains=q)
    context = {'my_books1':my_books}
    return render(request, 'base/index2.html', context)

@login_required(login_url='login')
def user_home(request, pk):
    user = request.user
    user_books = My_Book.objects.filter(user=user)
    context = {'user_books': user_books}
    return render(request, 'base/index4.html',context)

@login_required(login_url='login')
def recommended(request):
    user = request.user.id
    recommendation = get_recommendations(user, model, user_item_matrix, num_recommendations=5)
    # recommended_books = RecommendedBooks.objects.filter(user=user)
    recommended_books = Book.objects.filter(id__in=recommendation)
    context = {'recommended_books':recommended_books}
    # print(recommended_books)
    return render(request, 'base/index5.html', context)

def book(request, pk):
    book = Book.objects.get(id=pk)
    context = {'book': book}
    return render(request, 'base/index.html', context)

@login_required(login_url='login')
def rating(request, pk, rating):
    book = Book.objects.get(id=pk)
    real_rating = Rating.objects.get(rating=rating)
    existing_rating = My_Book.objects.filter(book_id=book.pk, user_id=request.user.id).first()

    if existing_rating:
        if request.method == 'POST':
            existing_rating.rating = real_rating
            existing_rating.save()
            return redirect('user_home', pk=request.user.id)
    else:
        if request.method == 'POST':
            rating = My_Book.objects.create(
                user = request.user,
                rating = real_rating,
                book = book
            )
            return redirect('user_home', pk=request.user.id)
        context = {'book':existing_rating}
    return render(request, 'base/index2.html', context)

@login_required(login_url='login')
def wishlist(request, pk):
    book = Book.objects.get(id=pk)
    if request.method == 'POST':
        wishlist = Wishlist.objects.create(
            user = request.user,
            book = book
        )
        return redirect('wishlist', pk=request.user.id)
    books = Wishlist.objects.filter(user=request.user)
    context = {'books':books}
    return render(request, 'base/index6.html', context)

def postRegister(request):
    return render(request, 'base/inddex9.html')

# index.html = book.html
# index2.html = home.html
# index3.html = login_register.html
# index4.html = myBooks.html
# index5.html = recommended.html
# index6.html = wishlist.html
# index7.html = main.html
# index8.html = navbar.html
# index9.html = postRegister.html