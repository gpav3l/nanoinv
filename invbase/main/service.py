from .models import *
from django.db import IntegrityError
from dataclasses import dataclass
from django.db.models import Q


@dataclass
class index_item:
    pk: int
    inv_number: str
    name: str
    serial_number: str
    point_man: str
    sub_item_count: int
    missed_sub_item_count: int
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
def index_item_list(point_man=None, finds={}):
    ret_list = []

    if point_man == None:
        filtered_items = Items.objects.all()
    else:
        filtered_items = Items.objects.filter(point_man=point_man)

    try:
        find_arg = finds['arg']
        find_mode = finds['mode']
    except:
        find_arg = None
        find_mode = None

    if find_arg != None:
        if find_mode == 'all':
            filtered_items = Items.objects.filter(Q(inventory_number__contains=find_arg) |
                                                  Q(inventory_number__contains=find_arg) |
                                                  Q(serial_number__contains=find_arg) |
                                                  Q(name__contains=find_arg))
        if find_mode == 'inv':
            filtered_items = Items.objects.filter(inventory_number__contains=find_arg)
        if find_mode == 'ser':
            filtered_items = Items.objects.filter(serial_number__contains=find_arg)
        if find_mode == 'nam':
            filtered_items = Items.objects.filter(name__contains=find_arg)

    for itm in filtered_items:
        ret_list.append(index_item(pk=itm.pk,
                                   inv_number=itm.inventory_number,
                                   name=itm.name,
                                   serial_number=itm.serial_number,
                                   point_man=itm.point_man,
                                   sub_item_count=len(Include_items.objects.filter(parrent_id=itm.pk)),
                                   missed_sub_item_count=len(Include_items.objects.filter(parrent_id=itm.pk, location="")),
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
