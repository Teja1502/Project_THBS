from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from .forms import UserProfileForm
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Readlist, Favourites, UserProfile
from django.db import transaction 
import json
import re



def userLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        myUser = authenticate(request, username=username, password=pass1)

        if myUser is not None:
            login(request, myUser)
            return redirect('registerApp:index')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return render(request, 'registerApp/userLogin.html')

   
    signup_success_message = request.session.pop('signup_success_message', None)
    if signup_success_message:
        messages.success(request, signup_success_message, extra_tags='successfully')

    return render(request, 'registerApp/userLogin.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return render(request, 'registerApp/userRegister.html')
        else:
            myUser = User.objects.create_user(username=username, password=pass1)
            myUser.first_name = fname
            myUser.last_name = lname
            myUser.email = email
            myUser.save()

            UserProfile.objects.create(user=myUser, username=username, first_name=fname, last_name=lname, email=email)

            signup_success_message = "You have been registered successfully. Please login."
            request.session['signup_success_message'] = signup_success_message

            return redirect('registerApp:login')

    return render(request, 'registerApp/userRegister.html')

def userLogout(request):
    logout(request)
    return redirect('registerApp:login')



# def book_search(request):
#     if request.method == 'POST':
#         search_query = request.POST.get('search_query')

        
#         max_results = 25

        
#         api_key = 'AIzaSyBUBwEh8IFXh26H6Naballr5wEf7ujCckg'
#         url = f'https://www.googleapis.com/books/v1/volumes?q={search_query}&maxResults={max_results}&key={api_key}'
#         response = requests.get(url)
#         data = response.json()

       
#         books = []
#         if 'items' in data:
#             for item in data['items']:
#                 book_info = item['volumeInfo']
#                 title = book_info.get('title', 'N/A')
#                 authors = ', '.join(book_info.get('authors', ['Unknown']))
#                 description = book_info.get('description', 'No description available')
#                 thumbnail = book_info['imageLinks']['thumbnail'] if 'imageLinks' in book_info else None

#                 if re.match("^[a-zA-Z0-9 _-]*$", title):
#                     authors = ', '.join(book_info.get('authors', ['Unknown']))
#                     description = book_info.get('description', 'No description available')
#                     thumbnail = book_info['imageLinks']['thumbnail'] if 'imageLinks' in book_info else None

#                     books.append({
#                         'title': title,
#                         'authors': authors,
#                         'description': description,
#                         'thumbnail': thumbnail,
                        
#                     })

#         return render(request, 'registerApp/book_search.html', {'books': books, 'search_query': search_query})

#     return render(request, 'registerApp/book_search.html')





@login_required
def add_to_readlist(request, title):
    if request.method == 'POST':
        user = request.user
        book = {
            'title': title,
            'authors': request.POST.get('authors'),
            'description': request.POST.get('description'),
            'thumbnail': request.POST.get('thumbnail'),
        }

        Readlist.objects.get_or_create(user=user, book=book)

    return redirect('registerApp:readlist')

@login_required
def add_to_favourites(request, title):
    if request.method == 'POST':
        user = request.user
        book = {
            'title': title,
            'authors': request.POST.get('authors'),
            'description': request.POST.get('description'),
            'thumbnail': request.POST.get('thumbnail'),
        }

        Favourites.objects.get_or_create(user=user, book=book)
    
    return redirect('registerApp:favourites')


@login_required
def readlist(request):
    user = request.user
    readlist_books = Readlist.objects.filter(user=user).values('book')

 
    books = [book['book'] for book in readlist_books]

    return render(request, 'registerApp/readlist.html', {'books': books})

@login_required
def favourites(request):
    user = request.user
    favourites_books = Favourites.objects.filter(user=user).values('book')

   
    books = [book['book'] for book in favourites_books]

    return render(request, 'registerApp/favourites.html', {'books': books})


@login_required
def remove_from_readlist(request, title):
    if request.method == 'POST':
        user = request.user
        Readlist.objects.filter(user=user, book__title=title).delete()

    return redirect('registerApp:readlist')

@login_required
def remove_from_favourites(request, title):
    if request.method == 'POST':
        user = request.user
        Favourites.objects.filter(user=user, book__title=title).delete()

    return redirect('registerApp:favourites')

@login_required
def profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'registerApp/profile.html', {'user_profile': user_profile})

@login_required
def profile_update(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            with transaction.atomic():
                form.save()

            # Assuming you have a UserProfile model with a OneToOneField to User
            # user_profile.user.profile_picture = request.POST['profile_picture']
            user_profile.user.username = request.POST['username']
            user_profile.user.first_name = request.POST['first_name']
            user_profile.user.last_name = request.POST['last_name']
            user_profile.user.email = request.POST['email']
            user_profile.user.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('registerApp:profile')
        else:
            print(form.errors)  # Print form errors to the console
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'registerApp/profile_update.html', {'form': form})

# @login_required
# def profile_update(request):
#     user_profile = get_object_or_404(UserProfile, user=request.user)

#     if request.method == 'POST':
#         try:
#             profile_picture = request.FILES['profile_picture']
#             form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
#         except MultiValueDictKeyError:
#             # Handle the case where 'profile_picture' is not in request.FILES
#             form = UserProfileForm(request.POST, instance=user_profile)
#         if form.is_valid():
#             with transaction.atomic():
#                 form.save()
#             messages.success(request, 'Profile updated successfully.')
#             return redirect('registerApp:profile')
#         else:
#             print(form.errors)  # Print form errors to the console
#     else:
#         form = UserProfileForm(instance=user_profile)

#     return render(request, 'registerApp/profile_update.html', {'form': form})

@login_required
def index(request):
    return render(request, 'registerApp/index.html')










    
