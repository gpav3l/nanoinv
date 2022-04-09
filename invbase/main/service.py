from .models import *
from django.db import IntegrityError
from dataclasses import dataclass


@dataclass
class index_item:
    pk: int
    inv_number: str
    name: str
    point_man: str
    sub_item_count: int
    is_not_located: bool

# Get simple list of user based on database
def users_fio_lst():
    ret_list = []
    for itm in Users.objects.all():
        ret_list.append(itm.fio)
    return ret_list

# Get simple list of user based on database
def users_fio_lst():
    ret_list = []
    for itm in Users.objects.all():
        ret_list.append(itm.fio)
    return ret_list

# Get simple list of user based on database
def location_name_lst():
    ret_list = []
    for itm in Locations.objects.all():
        ret_list.append(itm.name)
    return ret_list


# Prepare item list for index page
def index_item_list():
    ret_list = []
    for itm in Items.objects.all():
        ret_list.append(index_item(pk=itm.pk, inv_number=itm.inventory_number, name=itm.name, point_man=itm.point_man,
                             sub_item_count=len(Include_items.objects.filter(parrent_id=itm.pk)), is_not_located=not bool(itm.location)))

    return ret_list