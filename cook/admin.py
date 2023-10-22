from django.contrib import admin
from .models import Profile,Recipe,Review,CuisineType,Community,CommunityMembership,UserCuisine,CommunitySuggestion

# Register your models here.
admin.site.register(Profile)
admin.site.register(Recipe)
admin.site.register(Review)
admin.site.register(Community)
admin.site.register(UserCuisine)
admin.site.register(CuisineType)
admin.site.register(CommunitySuggestion)
admin.site.register(CommunityMembership)





