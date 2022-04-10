from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('new/', item_new, name='item_new'),
    path('<int:id>/', item_view, name='item_view'),
    path('<int:root_id>/new/', subitem_new, name='subitem_new'),
    path('<int:root_id>/<int:id>/', subitem_view, name='subitem_view'),
    path('stuff/', manage_stuff, name='manage_stuff'),
    path('location/', manage_location, name='manage_location'),
]
