from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('search', views.search, name="search"),
    path('recipe/<int:id1>', views.recipe, name="recipe"),
    #path('recipe_select', views.recipe_select, name="recipe_select"),
]
