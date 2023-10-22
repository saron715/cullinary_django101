from django.urls import path,include
from . import views
urlpatterns = [
    path("",views.index,name="index"),
    path("login",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("profile",views.profile,name="profile"),
    path("signup",views.signup_view,name="signup"),
    path("settings",views.settings_view,name="settings"),
    path("recipe_post",views.recipe_post,name="recipe_post"),
    path("recipe_list",views.recipe_list_view,name="recipe_list"),
    #path("community_view",views.community_view,name="community_view"),
    path("user_profile",views.user_profile,name="user_profile"),
    path("recipe_search",views.recipe_search,name="recipe_search"),
    path('like_recipe/<int:pk>/', views.like_recipe, name='like_recipe'),
    path('add_review/<int:id>/', views.add_review, name='add_review'),
    path('view_reviews/<int:id>/', views.view_reviews, name='view_reviews'),
    path('recipe/<int:id>/', views.recipe_details, name='recipe_detail'),
    path('community_suggestions', views.community_suggestions, name='community_suggestions'),
    path('join_community/<int:community_id>/', views.join_community, name='join_community'),
    path('community_view/<int:community_id>/', views.community_view, name='community_view'),
    path("member_list_view",views.member_list_view,name="member_list_view"),

]
