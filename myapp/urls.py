from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('artists/',views.artists,name='artists'),
    path('events/',views.events,name='events'),
    path('grants/',views.grants,name='grants'),
    path('login/',views.login,name='login'),
    path('daniel-philips/',views.daniel_philips,name='daniel-philips'),
    path('educations/',views.educations,name='educations'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('change-password/',views.change_password,name='change-password'),
    path('profile/',views.profile,name='profile'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('verify-otp/',views.verify_otp,name='verify-otp'),
    path('new-password/',views.new_password,name='new-password'),
    path('artist-profile/',views.artist_profile,name='artist-profile'),
    path('mybookings/',views.mybookings,name='mybookings'),
    path('artist-details/<int:pk>/',views.artist_details,name='artist-details'),
    path('book-artist/<int:pk>/',views.book_artist,name='book-artist'),
    path('confirm-booking/<int:pk>/',views.confirm_booking,name='confirm-booking'),
    path('create-checkout-session/', views.create_checkout_session, name='payment'),
    path('success.html/',views.success,name='success'),
    path('cancel.html/',views.cancel,name='cancel'),



    
    ]