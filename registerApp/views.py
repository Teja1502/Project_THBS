from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .forms import UserProfileForm
from django.shortcuts import get_object_or_404
from .models import Readlist, Favourites, UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction 
import json
import string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile  # Assuming UserProfile is defined in your models
import re
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from registerApp.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.core.mail import send_mail
import uuid
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required




def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('registerApp:login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('registerApp:login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('registerApp:login')
        
        login(request , user)
        return redirect('registerApp:index')

    return render(request , 'registerApp/userLogin.html')





# def register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')

#         try:
#             if User.objects.filter(username=username).first():
#                 messages.success(request, 'Username is taken.')
#                 return redirect('registerApp:register')

#             if User.objects.filter(email=email).first():
#                 messages.success(request, 'Email is taken.')
#                 return redirect('registerApp:register')

#             user_obj = User(username=username, email=email, first_name=first_name, last_name=last_name)
#             user_obj.set_password(password)
#             user_obj.save()

#             auth_token = str(uuid.uuid4())

#             user_profile = UserProfile.objects.create(user=user_obj, username=username, email=email, location=request.POST.get('location'), first_name=first_name, last_name=last_name)
#             user_profile.save()

#             profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
#             profile_obj.save()

#             send_mail_after_registration(email, auth_token)
#             return redirect('registerApp:token')

#         except Exception as e:
#             print(e)

#     return render(request, 'registerApp/userRegister.html')



def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        location = request.POST.get('location')

        # Check if all fields are entered
        missing_fields = []
        if not username:
            missing_fields.append('Username')
        if not email:
            missing_fields.append('Email')
        if not password:
            missing_fields.append('Password')
        if not confirm_password:
            missing_fields.append('Confirm Password')
        if not first_name:
            missing_fields.append('First Name')
        if not last_name:
            missing_fields.append('Last Name')
        if not location:
            missing_fields.append('Location')

        if missing_fields:
            messages.error(request, f'Please fill in all the fields: {", ".join(missing_fields)}.')
            return redirect('registerApp:register')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('registerApp:register')

        # Check username format
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            messages.error(request, 'Username should only contain alphanumeric characters and underscore.')
            return redirect('registerApp:register')

        # Check first name format
        if not first_name.isalpha():
            messages.error(request, 'First name should only contain characters.')
            return redirect('registerApp:register')

        # Check last name format
        if not last_name.isalpha():
            messages.error(request, 'Last name should only contain characters.')
            return redirect('registerApp:register')

        # Check password complexity
        if len(password) < 8:
            messages.error(request, 'Your password must contain at least 8 characters.')
            return redirect('registerApp:register')
        elif not any(char.isdigit() for char in password):
            messages.error(request, 'Your password must contain at least one numeric character.')
            return redirect('registerApp:register')
        elif not any(char in string.punctuation for char in password):
            messages.error(request, 'Your password must contain at least one special character.')
            return redirect('registerApp:register')
        elif any(field.lower() in password.lower() for field in [username]):
            messages.error(request, 'Your password can’t be too similar to your username')
            return redirect('registerApp:register')

        try:
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already in use.')
                return redirect('registerApp:register')

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered.')
                return redirect('registerApp:register')

            user_obj = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            auth_token = str(uuid.uuid4())

            user_profile = UserProfile.objects.create(user=user_obj, username=username, email=email, location=location, first_name=first_name, last_name=last_name)
            user_profile.save()

            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()

            domain = request.build_absolute_uri('/')[:-1]
            send_mail_after_registration(email, auth_token, domain)
            return redirect('registerApp:token')

        except Exception as e:
            print(e)

    return render(request, 'registerApp/userRegister.html')


def success(request):
    return render(request , 'registerApp/success.html')


def token_send(request):
    return render(request , 'registerApp/token_send.html')



def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('registerApp:login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('registerApp:login')
        else:
            return redirect('registerApp:error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'registerApp/error.html')



def send_mail_after_registration(email , token, domain):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account {domain}/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )




def userLogout(request):
    logout(request)
    return redirect('registerApp:landing')



def landing(request):
    return render(request, 'registerApp/landing.html')


def pass_reset(request):
    return render(request, 'registerApp/pass_reset.html')



@login_required
@csrf_exempt  
def add_to_readlist(request, title):
    if request.method == 'POST':
        user = request.user
        try:
            data = json.loads(request.body)
            authors = data.get('authors', '')
            previewLink = data.get('previewLink', '')
            thumbnail = data.get('thumbnail', '')
            book = {
                'title': title,
                'authors': authors,
                'previewLink': previewLink,
                'thumbnail': thumbnail,
            }

            existing_entry = Readlist.objects.filter(user=user, book=book).first()
            if existing_entry:
                return JsonResponse({'message': 'Book is already in the Readlist'})
            
            Readlist.objects.create(user=user, book=book)

            return JsonResponse({'message': 'Book added to Readlist successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
@csrf_exempt  
def add_to_favourites(request, title):
    if request.method == 'POST':
        user = request.user
        try:
            data = json.loads(request.body)
            authors = data.get('authors', '')
            previewLink = data.get('previewLink', '')
            thumbnail = data.get('thumbnail', '')
            book = {
                'title': title,
                'authors': authors,
                'previewLink': previewLink,
                'thumbnail': thumbnail,
            }

            # Check if the book is already in Favourites
            existing_entry = Favourites.objects.filter(user=user, book=book).first()
            if existing_entry:
                return JsonResponse({'message': 'Book is already in Favourites'})
            
            Favourites.objects.create(user=user, book=book)

            return JsonResponse({'message': 'Book added to Favourites successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)




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
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None  # Handle the case where the profile does not exist

    user_readlist_count = Readlist.objects.filter(user=request.user).count()
    user_favourites_count = Favourites.objects.filter(user=request.user).count()

    context = {
        'user_profile': user_profile,
        'user_readlist_count': user_readlist_count,
        'user_favourites_count': user_favourites_count,
    }

    return render(request, 'registerApp/profile.html', context)
    

@login_required
def profile_update(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            with transaction.atomic():
                form.save()

            # Check if the entered username is already in use by another user
            new_username = request.POST.get('username')
            if new_username != request.user.username and User.objects.filter(username=new_username).exists():
                form.add_error('username', 'Username already exists. Please choose a different username.')
                return render(request, 'registerApp/profile_update.html', {'form': form})

            # Check if the entered email is already in use by another user
            new_email = request.POST.get('email')
            if new_email != request.user.email and User.objects.filter(email=new_email).exists():
                form.add_error('email', 'Email already exists. Please choose a different email.')
                return render(request, 'registerApp/profile_update.html', {'form': form})

            # Update user information
            user_profile.user.username = new_username
            user_profile.user.first_name = request.POST['first_name']
            user_profile.user.last_name = request.POST['last_name']
            user_profile.user.email = new_email
            user_profile.user.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('registerApp:profile')
        else:
            print(form.errors)  # Print form errors to the console
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'registerApp/profile_update.html', {'form': form})





@login_required
def index(request):
    return render(request, 'registerApp/index.html')

@login_required
def book_detail(request, isbn):
    return render(request, 'bookstore/book.html', {'isbn': isbn})



