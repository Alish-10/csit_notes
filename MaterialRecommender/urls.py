"""MRS URL Configuration

The `urlpatterns` list routes URLs to function. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function function
    1. Add an import:  from my_app import function
    2. Add a URL to urlpatterns:  path('', function.home, name='home')
Class-based function
    1. Add an import:  from other_app.function import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls.static import static

from MaterialRecommender import views
from . import function
urlpatterns = [
    path('', function.Home, name='home'),
    path('search', function.search, name='search'),
    path('studyportal', function.studyportal, name='studyportal'),
    path("profile/",function.profile,name="profile"),




    path('usefullink', function.usefullink, name='usefullink'),

    path('delete_suggestion/<int:pk>', function.delete_suggestion, name='delete_suggestion'),


    path('notes', function.Notes, name='notes'),
    
    path('delete_note/<int:pk>', function.Delete_Note, name='delete_note'),
    path('note_detail/<int:pk>', function.NoteDetailView.as_view(), name='note_detail_view'),

    path('youtube', function.youtube, name='youtube'),



    path("addmaterial",function.addmaterial,name="addmaterial"),
    path("addmember",function.addmember,name="addmember"),
    path("about",function.about,name="about"),


    path('todo', function.ToDo, name='todo'),
    path('update_todo/<int:pk>', function.update_todo, name='update_todo'),
    path('delete_todo/<int:pk>', function.Delete_Todo, name='delete_todo'),

    path('books', function.Books, name='books'),

    path('material_detail/<int:pk>', function.MaterialDetailView, name='material_detail'),
    path('material_delete/<int:pk>', function.Material_delete, name='material_delete'),

]
