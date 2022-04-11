from django.urls import path
from .views import index
from .view_simple_manag import manage_stuff, manage_location
from .view_item import item_new, item_view
from .view_subitem import subitem_new, subitem_view

urlpatterns = [
    path('', index, name='index'),
    path('new/', item_new, name='item_new'),
    path('<int:id>/', item_view, name='item_view'),
    path('<int:root_id>/new/', subitem_new, name='subitem_new'),
    path('<int:root_id>/<int:id>/', subitem_view, name='subitem_view'),
    path('stuff/', manage_stuff, name='manage_stuff'),
    path('location/', manage_location, name='manage_location'),
]
