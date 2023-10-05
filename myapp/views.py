from django.shortcuts import render,redirect
from .models import User,Artist_profile
from .models import Book_Artist
import requests
import random
import stripe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.


stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://localhost:8000'


def index(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=="artist":
			return render(request,'artist-index.html')
		else:
			return render(request,'index.html')
	except:
		return render(request,'index.html')

def about(request):
	return render(request,'about.html')

def artists(request):
	artist_profile=Artist_profile.objects.all()
	return render(request,'artists.html',{'artist_profile':artist_profile})

def daniel_philips(request):
	return render(request,'daniel-philips.html')

def educations(request):
	return render(request,'educations.html')

def events(request):
	return render(request,'events.html')

def grants(request):
	return render(request,'grants.html')

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					country=request.POST['country'],
					state=request.POST['state'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					address=request.POST['address'],
					password=request.POST['password'],
					usertype=request.POST['usertype'],
					profile_pic=request.FILES['profile_pic']
					)
				msg="User signup successfully"
				return render(request,'login.html',{'msg':msg})
			else:
				msg="password and confirm password does not matched"
				return render(request,'signup.html',{'msg':msg}) 
	else:
		return render(request,'signup.html')
def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])

			if user.password==request.POST['password']:
				if user.usertype=="customer":
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['profile_pic']=user.profile_pic.url
					return render(request,'index.html')
				else:
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['profile_pic']=user.profile_pic.url
					return render(request,'artist-index.html')
			else:
				msg="Incorrect Password"
				return render(request,'login.html',{'msg':msg})
		except Exception as e:
			print("hello..........................................................................................................",e)
			msg="Email Not Registered"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['profile_pic']
		return render(request,'login.html')
	except:
		return render(request,'login.html')
def change_password(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnpassword']:
				user.password=request.POST['new_password']
				user.save()
				return redirect('logout')
			else:
				msg="New Password And Confirm Password Does Not Matched"
				if user.usertype=="customer":
					return render(request,'change-password.html',{'msg':msg})
				else:
					return render(request,'artist-change-password.html',{'msg':msg})


		else:
			msg="Old Password Does Not Matched"
			if user.usertype=="customer":
				return render(request,'change-password.html',{'msg':msg})
			else:
				return render(request,'artist-change-password.html',{'msg':msg})

	else:
		if user.usertype=="customer":
			return render(request,'change-password.html')
		else:
			return render(request,'artist-change-password.html')


def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		request.session['profile_pic']=user.profile_pic.url
		return render(request,'profile.html',{'user':user})
	else:
		return render(request,'profile.html',{'user':user})

def forgot_password(request):
	if request.method=="POST":
		mobile=request.POST['mobile']
		try:
			user=User.objects.get(mobile=mobile)
			otp=random.randint(1000,9999)
			url = "https://www.fast2sms.com/dev/bulkV2"
			querystring = {"authorization":"csMwYan580kxUQXGPl9A2NvZHTCjLDW4hug3KpR6FzIdV7fyoqqlCnrEOpRFMWtdxZ7a96LBXSz034Tf","variables_values":str(otp),"route":"otp","numbers":str(mobile)}
			headers = {'cache-control': "no-cache"}
			response = requests.request("GET", url, headers=headers, params=querystring)
			return render(request,'otp.html',{'otp':otp,'mobile':mobile})
		except:
			msg="mobile Not Registered"
			return render(request,'forgot-password.html',{'msg':msg})

	else:
		return render(request,'forgot-password.html')

def verify_otp(request):
	otp=request.POST['otp']
	uotp=request.POST['uotp']
	mobile=request.POST['mobile']

	if otp==uotp:
		return render(request,'new-password.html',{'mobile':mobile})
	else:
		msg="Invelid OTP"
		return render(request,'otp.html',{'otp':otp,'mobile':mobile,'msg':msg})


def new_password(request):
	mobile=request.POST['mobile']
	np=request.POST['new_password']
	cnp=request.POST['cnpassword']

	if np==cnp:
		user=User.objects.get(mobile=mobile)
		user.password=np
		user.save()
		msg="Password Updated successfully"
		return render(request,'login.html',{'msg':msg})

	else:
		msg="New Password And Confirm New Password Does Not Matched"
		return render(request,'new-password.html',{'mobile':mobile,'msg':msg})

def mybookings(request):
	user=User.objects.get(email=request.session['email'])
	if user.usertype=="customer":
		bookings=Book_Artist.objects.filter(user=user)
		return render(request,'mybookings.html',{'bookings':bookings})
	else:
		artist=Artist_profile.objects.get(artist=user)
		bookings=Book_Artist.objects.filter(artist=artist)
		
		return render(request,'artist_bookings.html',{'bookings':bookings})

def artist_profile(request):
	artist_profile=Artist_profile()
	artist=User.objects.get(email=request.session['email'])	
	if request.method=="POST":
		artist_profile.artist=artist
		#artist_profile.artist_category=request.POST['artist_category']
		artist_profile.artist_fees=request.POST['artist_fees']
		artist_profile.artist_desc=request.POST['artist_desc']
		try:
			artist_profile.picture1=request.FILES['picture1']
		except:
			pass
		try:
			artist_profile.picture2=request.FILES['picture2']
		except:
			pass
		try:
			artist_profile.picture3=request.FILES['picture3']
		except:
			pass
		artist_profile.save()
		return render(request,'artist-profile.html',{'artist':artist,'artist_profile':artist_profile})
	else:

		try:
			artist_profile=Artist_profile.objects.get(artist=artist)
		except:
			pass
		return render(request,'artist-profile.html',{'artist':artist,'artist_profile':artist_profile})


def artist_details(request,pk):
	artist_profile=Artist_profile.objects.get(pk=pk)
	return render(request,'artist-details.html',{'artist_profile':artist_profile})

def book_artist(request,pk):
	artist_profile=Artist_profile.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		Book_Artist.objects.create(
				user=user,
				artist=artist_profile,
				date=request.POST['date'],
				venue=request.POST['venue'],
				time=request.POST['time'],
				event=request.POST['event'],
				crowd_strength=request.POST['crowd_strength']
			)
		msg="Artist Booked Successfully"
		return render(request,'book-artist.html',{'artist_profile':artist_profile,'msg':msg})
	else:
		return render(request,'book-artist.html',{'artist_profile':artist_profile})


def confirm_booking(request,pk):
	booking=Book_Artist.objects.get(pk=pk)
	booking.artist_confirmation=True
	booking.save()
	return redirect("mybookings")


@csrf_exempt
def create_checkout_session(request):
	data = json.load(request)
	amount=int(data['amount'])
	final_amount=amount*100
	bid=int(data['bid'])
	book_artist=Book_Artist.objects.get(pk=bid)
	book_artist.payment_status=True
	book_artist.save()
	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price_data': {
				'currency': 'inr',
				'product_data': {
					'name': 'Checkout Session Data',
					},
				'unit_amount': final_amount,
				},
			'quantity': 1,
			}],
		mode='payment',
		success_url=YOUR_DOMAIN + '/success.html',
		cancel_url=YOUR_DOMAIN + '/cancel.html',)
	return JsonResponse({'id': session.id})


def success(request):
	return render(request,'success.html')

def cancel(request):
	return render(request,'cancel.html')