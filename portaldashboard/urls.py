from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('notes', views.notes,name="notes"),
    path('deletenote/<int:pk>', views.deletenote,name="deletenote"),
   # path('notes_detail/<int:pk>', views.NoteDetailView.as_view(),name="notedetail"),
    path('detail/<int:pk>', views.detail,name="detail"),
    path('homework', views.homework,name="homework"),
    path('update_homework/<int:pk>', views.update_homework,name="update-homework"),
    path('delete_homework/<int:pk>', views.delete_homework,name="delete-homework"),
    path('youtube', views.youtube,name="youtube"),
    path('todo', views.todo,name="todo"),
    path('update_todo/<int:pk>', views.update_todo,name="update-todo"),
    path('delete_todo/<int:pk>', views.delete_todo,name="delete-todo"),
    path('books', views.books,name="books"),
    path('dictionary', views.dictionary,name="dictionary"),
    path('wiki', views.wiki,name="wiki"),
    path('quiz', views.quiz,name="quiz"),
    path('<id>', views.take_quiz,name="take_quiz"),
    path('api/<id>', views.api_ques,name="api_ques"),
 
]