from django.urls import path
from . import views

urlpatterns = [
    path('get-items/', views.get_todo_items, name='get_todo_items'),
    path('make-item/', views.create_todo_item, name='create_todo_item'),
    path('update-completed/', views.update_completed, name='update_completed'),
    path('update-title/', views.update_title, name='update_title'),
    path('delete-item/', views.delete_item, name="delete_item")
]