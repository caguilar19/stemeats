from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Cuisine(models.Model):
	cuisine = models.CharField(max_length=100)

	def __str__(self):
		return f"{self.cuisine}"

class Restaurant(models.Model):
	name = models.CharField(max_length=100)
	cusine = models.ManyToManyField(Cuisine, related_name="restaurants")
	location = models.CharField(max_length=100)
	price = models.DecimalField(
		max_digits=4,
		decimal_places=2,
		validators=[MinValueValidator(0), MaxValueValidator(5)])

	def __str__(self):
		return f"{self.name} - {self.location}"

class Post(models.Model):
	title = models.CharField(max_length=100, blank=False, null=False)
	subtitle = models.CharField(max_length=100, blank=True, null=True)
	html = models.TextField(blank=False, null=False)
	time = models.DateTimeField(auto_now=False, auto_now_add=True)
	category = models.CharField(max_length=100)
	restaurant = models.ManyToManyField(Restaurant, related_name="posts")

	def __str__(self):
		return f"{self.title}"

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	comment = models.TextField()
	time = models.CharField(max_length=100)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.user} {self.post} - {self.comment}"


