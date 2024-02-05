from django.urls import path
from . import views


app_name = 'registerApp'

urlpatterns = [
    path('', views.landing, name="landing"), 
    path('login/', views.userLogin, name="login"),
    path('register/', views.register, name="register"),
    # path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path('logout/', views.userLogout, name="logout"),
    # path('book_search/', views.book_search, name='book_search'),
    path('add_to_readlist/<str:title>/', views.add_to_readlist, name='add_to_readlist'),
    path('add_to_favourites/<str:title>/', views.add_to_favourites, name='add_to_favourites'),
    path('readlist/', views.readlist, name='readlist'),
    path('favourites/', views.favourites, name='favourites'),
    path('remove_from_readlist/<str:title>/', views.remove_from_readlist, name='remove_from_readlist'),
    path('remove_from_favourites/<str:title>/', views.remove_from_favourites, name='remove_from_favourites'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('index/', views.index, name='index'),
    path('book/<str:isbn>/', views.book_detail, name='book_detail'),
    path('token/' , views.token_send , name="token_send"),
    path('success/' , views.success , name='success'),
    path('verify/<auth_token>/' , views.verify , name="verify"),
    path('error/' , views.error_page , name="error")
    
]


