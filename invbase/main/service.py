from .models import *
from django.db import IntegrityError
from dataclasses import dataclass


@dataclass
class index_item:
    pk: int
    inv_number: str
    name: str
    serial_number: str
    point_man: str
    sub_item_count: int
    is_not_located: bool


@dataclass
class subitem_row:
    pk: int
    name: str
    serial_number: str
    location: str


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
        ret_list.append(index_item(pk=itm.pk,
                                   inv_number=itm.inventory_number,
                                   name=itm.name,
                                   serial_number=itm.serial_number,
                                   point_man=itm.point_man,
                                   sub_item_count=len(Include_items.objects.filter(parrent_id=itm.pk)),
                                   is_not_located=not bool(itm.location)))

    return ret_list


# Prepare item list for index page
def subitem_list(parent_id):
    ret_list = []
    try:
        for itm in Include_items.objects.filter(parrent_id=parent_id):
            ret_list.append(subitem_row(pk=itm.pk,
                                       name=itm.name,
                                       serial_number=itm.serial_number,
                                       location=itm.location,))
    except:
        ret_list = []

    return ret_list
