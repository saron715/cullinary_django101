from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import Profile,Recipe,Review
from django.db.models import Q
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
#from background_task import background
#from .tasks import suggest_communities 
from django.shortcuts import get_object_or_404
from .forms import ReviewForm
from .forms import RecipeForm
from django.http import JsonResponse
import calendar
from .models import Community, CommunityMembership,CommunitySuggestion
from django.http import HttpResponseRedirect
from .models import UserCuisine 
from calendar import HTMLCalendar
from datetime import datetime
from datetime import datetime, timedelta
from django.db.models import F
from django.db.models import Count, OuterRef, Subquery
from django_q.tasks import async_task
# Create your views here.


def index(request):
    return render(request,"cook/home.html")


def login_view(request):
     if request.method == "POST":
        # Accessing username and password from form data
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if username and password are correct, returning User object if so
        user = authenticate(request, username=username, password=password)

        # If user object is returned, log in and route to index page:
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("profile"))
        # Otherwise, return login page again with new context
        else:
            return render(request, "cook/login.html", {
                "message": "Invalid Credentials"
            })
        
       
    
     return render(request,"cook/login.html")



from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

def profile(request):
    if not request.user.is_authenticated:
        return render(request, "cook/login.html")

    # Calculate the date one week ago
    one_week_ago = datetime.now() - timedelta(days=7)

    subquery = Recipe.objects.filter(id=OuterRef('id')).annotate(like_count=Count('likes'))
    popular_recipes = Recipe.objects.filter(
    date_posted__gte=one_week_ago,
    likes__isnull=False
    ).annotate(like_count=Subquery(subquery.values('like_count'))).distinct().order_by('-like_count')[:5]

    return render(request, "cook/profile.html", {'popular_recipes': popular_recipes})



def logout_view(request):
    logout(request)
    return render(request, "cook/login.html", {
                "message": "Logged Out"
            })

def signup_view(request):
     if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already taken.')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                # You don't need to call user.save() explicitly; it's done by create_user.
                login(request, user)  # Log the user in after registration
                return redirect("settings")
        else:
            messages.error(request, 'Passwords do not match.')

     return render(request, 'cook/signup.html')
    


@login_required(login_url='login')
def settings_view(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        image = request.FILES.get('image', user_profile.profileimg)
        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect("settings")

    return render(request, "cook/setting.html", {'user_profile': user_profile})

def recipe_post(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)  # Include files in the form data
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            cuisine_type = recipe.cuisine_type  # Change this to how you retrieve the cuisine type

            # Create a UserCuisine entry for the user
            existing_entry = UserCuisine.objects.filter(user=request.user, cuisine_type=cuisine_type).first()

# If the entry doesn't exist, create it
            if not existing_entry:
                user_cuisine = UserCuisine(user=request.user, cuisine_type=cuisine_type)
                user_cuisine.save()
            #suggest_communities(recipe.id, user=request.user)
           
            return redirect("recipe_list")

    else:
        form = RecipeForm()

    return render(request, 'cook/post.html', {'form': form})





def recipe_list_view(request):
    # Check if the 'all_recipes' parameter is in the request's GET parameters
    # If 'all_recipes' is present, fetch all recipes; otherwise, fetch recipes for the logged-in user
    if 'all_recipes' in request.GET:
        # Fetch all recipes
        recipes = Recipe.objects.all()
        is_all_recipes = True
    else:
        # Fetch recipes for the logged-in user
        recipes = Recipe.objects.filter(user=request.user)
        is_all_recipes = False

    context = {
        'recipes': recipes,
        'is_all_recipes': is_all_recipes,
    }

    return render(request, 'cook/recipe_list.html', context)



def user_profile(request):

    return render(request,"cook/user_profile.html")





# In your view that displays suggestions


def community_suggestions(request):
    user = request.user

    # Query for suggestions related to the current user
    suggestions = CommunitySuggestion.objects.filter(user=user)
    joined_communities = Community.objects.filter(members=user)

    

    return render(request, 'cook/community.html', {'suggestions': suggestions, 'joined_communities': joined_communities})






def recipe_search(request):
    # Get the current search criteria from session or use an empty string
    searched = request.session.get('searched', '')

    if request.method == "POST":
        # Check if the like-form was submitted
        if 'like-form' in request.POST:
            # Handle liking a recipe here
            # You can add code to process the like action
            return HttpResponseRedirect('/cook/recipe_search')

        # If the search form was submitted, update the search criteria
        searched = request.POST.get('searched', '')
        request.session['searched'] = searched  # Store the search criteria in session

    # Apply the search criteria to filter the recipes
    recipes = Recipe.objects.filter(Q(title__icontains=searched) | Q(description__icontains=searched))

    return render(request, 'cook/recipe_search.html', {'recipes': recipes, 'searched': searched})

    
   
       

    
    
    

    




"""@login_required
def like_recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id)

    # Check if the user has already liked the recipe
    if Like.objects.filter(user=request.user, recipe=recipe).exists():
        # Unlike the recipe
        recipe.likes -= 1
        Like.objects.filter(user=request.user, recipe=recipe).delete()
        liked = False
    else:
        # Like the recipe
        recipe.likes += 1
        Like.objects.create(user=request.user, recipe=recipe)
        liked = True

    recipe.save()

    return JsonResponse({'likes': recipe.likes, 'liked': liked})
recipe = get_object_or_404(Recipe, pk=id)

    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            review = Review.objects.create(user=request.user, recipe=recipe, content=content)
            review.save( )

    return redirect("recipe_detail", id=id)
"""




def add_review(request, id):
    submitted = False
    recipe = get_object_or_404(Recipe, pk=id)  # Get the corresponding recipe

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.recipe = recipe 
            review.user = request.user # Associate the review with the recipe
            review.save()
            cuisine_type = recipe.cuisine_type
            existing_entry = UserCuisine.objects.filter(user=request.user, cuisine_type=cuisine_type).first()

# If the entry doesn't exist, create it
            if not existing_entry:
                user_cuisine = UserCuisine(user=request.user, cuisine_type=cuisine_type)
                user_cuisine.save()

            return HttpResponseRedirect(f'/cook/add_review/{recipe.id}?submitted=True')
    else:
        form = ReviewForm()

    if 'submitted' in request.GET:
        submitted = True

    return render(request, 'cook/add_review.html', {'form': form, 'recipe': recipe, 'submitted': submitted})


   


def view_reviews(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    reviews = Review.objects.filter(recipe=recipe).order_by('-created_at')

    return render(request, 'cook/view_reviews.html', {'recipe': recipe, 'reviews': reviews})

def recipe_details(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    
    return render(request, 'cook/recipe_details.html', {'recipe': recipe})

def like_recipe(request, pk):
    recipe = get_object_or_404(Recipe, id=request.POST.get('recipe_id'))
    recipe.likes.add(request.user)

    return HttpResponseRedirect(reverse('recipe_search'))

@receiver(post_save, sender=UserCuisine)
def suggest_communities(sender,instance,created, **kwargs):
    user=instance.user
    if created:
        user_id = user.id
        async_task(suggest_c, user_id)





from functools import reduce
from .models import UserCuisine



def suggest_c(user_id):
    user = User.objects.get(id=user_id)

    # Step 1: Retrieve the most recent cuisine preference added by the user
    new_cuisine_preference = UserCuisine.objects.filter(user=user).latest('id')

    # Step 2: Get the cuisine type from the newly added preference
    new_cuisine_type = new_cuisine_preference.cuisine_type

    # Step 3: Retrieve existing communities for this cuisine type
    existing_communities = Community.objects.filter(cuisine_type=new_cuisine_type)

    suggested_communities = []

    for existing_community in existing_communities:
        # Check if the user is already a member of the existing community
        user_already_member = existing_community.members.filter(id=user.id).exists()

        # Check if the user has already received a suggestion for this community
        suggestion_exists = CommunitySuggestion.objects.filter(
            user=user,
            suggested_communities=existing_community,
        ).exists()

        if not user_already_member and not suggestion_exists:
            # Suggest the existing community to the user
            suggested_communities.append(existing_community)

    # Step 4: Store the suggestion with the suggested communities
    suggestion_made_at = datetime.now()
    community_suggestion = CommunitySuggestion.objects.create(
        user=user,
        suggested_at=suggestion_made_at,
    )
    community_suggestion.suggested_communities.set(suggested_communities)




from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Community, CommunitySuggestion

def join_community(request, community_id):
    user = request.user
    community = Community.objects.get(id=community_id)

    # Attempt to retrieve the user's specific suggestion for the community
    try:
        suggestion = CommunitySuggestion.objects.get(user=user, suggested_communities=community)
        suggestion.delete()
    except CommunitySuggestion.DoesNotExist:
        # Handle the case where there is no matching suggestion
        pass

    # User is not a member, so join the community
    community.members.add(user)
    return render(request, 'cook/comm_view.html', {'community': community})

    









from django.http import Http404

def community_view(request,community_id):
    user = request.user
    try:
        community = Community.objects.get(id=community_id)
        
        # Check if the user is a member of the community
        if user not in community.members.all():
            raise Http404("You are not a member of this community.")
    except Community.DoesNotExist:
        raise Http404("Community does not exist.")
    
    return render(request, 'cook/comm_view.html', {'community': community})

def member_list_view(request):
    users = Profile.objects.all()
    return render(request, 'cook/member_list.html', {'users': users})