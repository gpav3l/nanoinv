from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('item/<int:id>/', item_view, name='item_view'),
    path('item/new/', item_new, name='item_new'),
    path('manage/stuff/', manage_stuff, name='manage_stuff'),
    path('manage/location/', manage_location, name='manage_location'),
]
