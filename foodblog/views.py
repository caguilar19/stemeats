from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

import datetime, pytz, random

from .models import *

# Create your views here.
def index(request):
	""" Displays the Home Page """
	posts = Post.objects.all()

	return render(request, "foodblog/index.html", {"posts": posts})

def logout_view(request):
	""" Logs a User Out. """
	logout(request)
	return HttpResponseRedirect(reverse("index"))

def restaurant_post(request, post):
	""" Displays a Restaurant Post """
	post = Post.objects.get(pk=post)

	t = post.time.astimezone(pytz.timezone("America/New_York"))
	time = datetime.datetime.strftime(t, "%d.%m.%y %H:%M")

	comments = Comment.objects.filter(post=post)
	context = {"post": post, "time": time, "comments": comments}
	return render(request, "foodblog/restaurant_post.html", context)

def new_comment(request):
	""" Creates a New Comment """
	comment_text = request.GET.get('comment', None)
	post_id = request.GET.get('post', None)
	char = []
	for c in comment_text:
		if c not in char:
			char.append(c)
	if len(char) == 1:
		if char[0] == " ":
			valid = False
		else:
			valid = True
	elif len(char) == 0:
		valid = False
	else:
		valid = True

	if valid:
		post = Post.objects.get(pk=int(post_id))
		now = datetime.datetime.now().astimezone(
			pytz.timezone("America/New_York"))

		time = datetime.datetime.strftime(now, "%d.%m.%y %H:%M")

		comment = Comment(
			user=request.user, comment=comment_text, time=time, post=post)
		comment.save()

	data = {
		'comment': comment.comment,
		'user': comment.user.username,
		'time': comment.time,
		'valid': valid
		}

	return JsonResponse(data)

def randomize(request):
	""" Returns a Random Restaurant """
	restaurants = Restaurant.objects.all()

	n = len(restaurants)

	r = random.randint(0, n - 1)

	result = restaurants[r]

	data = {"result_name": result.name, "result_location": result.location}

	return JsonResponse(data)

def check_username_login(request):
	""" Checks if a Username is Valid """
	username = request.GET.get('username', None)

	try:
		User.objects.get(username=username)
		valid = True
	except ObjectDoesNotExist:
		valid = False

	data = {"valid": valid}

	return JsonResponse(data)

def check_login(request):
	""" Checks if a Login is Valid """
	username = request.GET.get("username", None)
	password = request.GET.get("password", None)
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)

		data = {"login": True}

		return JsonResponse(data)
	else:
		data = {"login": False}

		return JsonResponse(data)

def check_signup(request):
	""" Checks if a Signup is Valid """
	first = request.GET.get('first', None)
	last = request.GET.get('last', None)
	username = request.GET.get('username', None)
	password = request.GET.get('password', None)
	email = request.GET.get('email', None)

	try:
		User.objects.get(username=username)
		username_valid = False
	except ObjectDoesNotExist:
		username_valid = True

	if len(username) < 5:
		username_length = False
	else:
		username_length = True

	if len(password) < 8:
		password_valid = False
	else:
		password_valid = True

	if "@" not in email or "." not in email:
		email_valid = False
	else:
		email_valid = True

	if username_valid and username_length and password_valid and email_valid:
		user = User.objects.create_user(username, email, password)

		user.first_name = first
		user.last_name = last

		user.save()

		login(request, user)

	data = {
		"username_valid": username_valid,
		"username_length": username_length,
		"password_valid": password_valid,
		"email_valid": email_valid
	}

	return JsonResponse(data)

def get_data(request):
	""" Gets Cuisine Data """
	cuisines = []
	for cuisine in Cuisine.objects.all():
		cuisines.append(cuisine)

	c = []
	for cuisine in cuisines:
		c.append({"cuisine": cuisine.cuisine, "count": len(cuisine.restaurants.all())})

	data = {"c": c}

	return JsonResponse(data)