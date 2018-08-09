from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("logout", views.logout_view, name="logout"),
	path("<int:post>", views.restaurant_post, name="restaurant_post"),
	path("new_comment", views.new_comment, name="new_comment"),
	path("randomize", views.randomize, name="randomize"),
	path(
		"check_username_login",
		views.check_username_login,
		name="check_username_login"),
	path("check_login", views.check_login, name="check_login"),
	path("check_signup", views.check_signup, name="check_signup"),
	path("get_data", views.get_data, name="get_data")
]