from django.shortcuts import render, redirect
from django.http import Http404
from django.db import IntegrityError
from simple_auth.service import check_auth, check_auth_inline
from .models import *
from .service import *
from django.core.exceptions import ObjectDoesNotExist
from .forms import *

# Page with item list
def index(request):
    content = {'users_list': users_fio_lst(),
               'item_list': index_item_list()}
    return render(request, 'main/index.html', content)


# Item card page
def item_view(request, id):
    item = Items.objects.filter(pk=id)
    content = {'item': item,
               'users_list': users_fio_lst()}
    if item == None:
        raise Http404("Item not found")

    if check_auth_inline(request):
        return render(request, 'main/item_edit.html', content)
    else:
        return render(request, 'main/item_card.html', content)


# Item update request
@check_auth
def item_update(request):
    content = {'users_list': users_fio_lst(),
               'location_list': location_name_lst(),}
    if request.method == 'POST':
        try:
            item = Items.objects.get(inventory_number=request.POST.get('inventory_number', ''))
        except ObjectDoesNotExist:
            item = None
        if item == None:
            item = Items(inventory_number=request.POST.get('inventory_number', ''),
                             name=request.POST.get('name', ''),
                             serial_number=request.POST.get('serial_number', ''),
                             amount=request.POST.get('amount', '1'),
                             point_man=request.POST.get('point_man', ''),
                             location=request.POST.get('location', ''))
            try:
                item.save()
                print(f"ID is {item.pk}")
                #return render(request, f'main/item_edit.html', content)
            except IntegrityError as e:
                content["error_msg"] = e
                return redirect('item_new', content)
        else:
            print("Update item in base")

    #return render(request, 'main/item_edit.html', content)
    raise Http404("Item not found")


# Location manage
@check_auth
def item_new(request):
    content = {'item': Items()}

    if request.method == 'POST':
        form = ItemEditForm(request.POST)
        #try:
        form.save()
        #except ValueError:
        #    content['error_msg'] = ValueError
    else:
        form = ItemEditForm()

    content['form'] = form
    return render(request, 'main/item_edit.html', content)


# Stuff manage allow add new person and remove exists
@check_auth
def manage_stuff(request):
    content = {'header': 'Сотрудники',
               'data_list': [],
               'error_msg': "",
               'success_msg': "",}

    # If get, try execute model update
    if request.method == 'GET':
        op = request.GET.get('op', '')
        arg = request.GET.get('arg', '')
        if op != '' and arg != '':
            if op == 'mk':
                try:
                    Users(fio=arg).save()
                    content['success_msg'] = f"Пользователь {arg} успешно сохранен в базе"
                except IntegrityError as e:
                    content["error_msg"] = e.__cause__
            elif op == 'rm':
                try:
                    Users.objects.filter(fio=arg).delete()
                    content['success_msg'] = f"Пользователь {arg} удален из базы"
                except IntegrityError as e:
                    content["error_msg"] = e.__cause__

    # Read all stuff list, and form content
    content['data_list'] = users_fio_lst()

    return render(request, 'main/simple_manage.html', content)


# Location manage allow add new and remove exist
@check_auth
def manage_location(request):
    content = {'header': 'Расположение',
               'data_list': [],
               'error_msg': "", }

    # If get, try execute model update
    if request.method == 'GET':
        op = request.GET.get('op', '')
        arg = request.GET.get('arg', '')
        if op != '' and arg != '':
            if op == 'mk':
                try:
                    Locations(name=arg).save()
                    content['success_msg'] = f"Расположение {arg} успешно сохранено в базе"
                except IntegrityError as e:
                    content["error_msg"] = e.__cause__
            elif op == 'rm':
                try:
                    Locations.objects.filter(fio=arg).delete()
                    content['success_msg'] = f"Расположение {arg} удалено из базы"
                except IntegrityError as e:
                    content["error_msg"] = e.__cause__

    # Read all location list, and form content
    content['data_list'] = location_name_lst()

    return render(request, 'main/simple_manage.html', content)
