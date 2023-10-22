from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime


# Create your models here.
User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank_profile_picture.png')
    location = models.CharField(max_length=100, blank=True)
    

    def __str__(self):
        return self.user.username
    
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
      
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipe_images')
    cuisine_type = models.ForeignKey('CuisineType',on_delete=models.CASCADE,null=True,blank=True)  # Add cuisine_type field
      # Add preparation_time field
    date_posted = models.DateField(auto_now_add=True) 
    likes = models.ManyToManyField(User,related_name= "liked_recipes",null=True,blank=True)

    
    

    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
         return self.title


class Review(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # You can use choices to limit the rating values (e.g., 1 to 5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Review by {self.user.username} for {self.recipe.title}'
    
class CuisineType(models.Model):
    name = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.name    

class Community(models.Model):
    name = models.CharField(max_length=100,blank=True)
    description = models.TextField()
    cuisine_type = models.ForeignKey('CuisineType', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through='CommunityMembership')
    
    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ('name', 'cuisine_type')

    def get_user_joined_communities(self, user):
        joined_communities = Community.objects.filter(members=user)
        return [community.name for community in joined_communities]    


class CommunityMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey('Community', on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f" {self.user.username} joined {self.community}"


class UserCuisine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuisine_type = models.ForeignKey('CuisineType', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.cuisine_type.name}"
    

class CommunitySuggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suggested_at = models.DateTimeField(auto_now_add=True)
    suggested_communities = models.ManyToManyField(Community)
    joined_communities = models.ManyToManyField(Community, related_name="joined_by", blank=True)

    def __str__(self):
        return f"Suggestions for {self.user.username} at {self.suggested_at}"
