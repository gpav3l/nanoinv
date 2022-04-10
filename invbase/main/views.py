from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.db import IntegrityError
from simple_auth.service import check_auth, check_auth_inline
from .models import *
from .service import *
from django.core.exceptions import ObjectDoesNotExist
from .forms import *


# Page with item list
def index(request):
    temp = index_item_list()
    content = {'users_list': users_fio_lst(),
               'item_list': temp}
    return render(request, 'main/index.html', content)


# Item card page
def item_view(request, id):
    content = {}
    try:
        content['item'] = Items.objects.get(pk=id)
        content['subitem_list'] = subitem_list(id)
    except:
        raise Http404("Item not found")

    if check_auth_inline(request):
        if request.method == 'GET':
            if request.GET.get('rm', '') == str(id):
                content['item'].delete()
                return redirect('index')
        if request.method == 'POST':
            form = ItemEditForm(request.POST, instance=content['item'])
            if form.is_valid():
                form.save()
                return redirect('item_view', id)

        content['item'] = Items.objects.get(pk=id)
        content['form'] = ItemEditForm(instance=content['item'])
        return render(request, 'main/item_edit.html', content)
    else:
        return render(request, 'main/item_card.html', content)


# Location manage
@check_auth
def item_new(request):
    content = {'item': Items()}

    if request.method == 'POST':
        form = ItemEditForm(request.POST, instance=content['item'])
        if form.is_valid():
            form.save()
            return redirect('item_view', id=content['item'].pk)
    else:
        form = ItemEditForm()

    content['form'] = form
    return render(request, 'main/item_edit.html', content)


# Subitem card page
def subitem_view(request, root_id, id):
    '''
    content = {}
    print("Subitem call")
    try:
        content['item'] = Items.objects.get(pk=root_id)
    except:
        raise Http404("Item not found")

    if check_auth_inline(request):
        if request.method == 'GET':
            if request.GET.get('rm', '') == str(id):
                content['item'].delete()
                return redirect('index')
        if request.method == 'POST':
            form = ItemEditForm(request.POST, instance=content['item'])
            if form.is_valid():
                print(f"Update: {form.instance.name}")
                form.save()
                return redirect('item_view', id)

        content['item'] = Items.objects.get(pk=id)
        content['form'] = ItemEditForm(instance=content['item'])
        return render(request, 'main/subitem_edit.html', content)
    else:
        return render(request, 'main/subitem_card.html', content)
'''
    raise Http404("Under construction")


# Location manage
@check_auth
def subitem_new(request, root_id):
    content = {'item': Include_items(),
               'form': SubitemEditForm()}
    try:
        content['item'].parrent_id=Items.objects.get(pk=root_id)
    except:
        raise Http404("Parent item not found!")

    content['item'].parrent_id=Items.objects.get(pk=root_id)
    content['item'].inventory_number = content['item'].parrent_id.inventory_number
    content['item'].location = content['item'].parrent_id.location
    content['item'].point_man = content['item'].parrent_id.point_man
    content['item'].date_start_use = content['item'].parrent_id.date_start_use
    content['item'].date_end_use = content['item'].parrent_id.date_end_use

    if request.method == 'POST':
        form = SubitemEditForm(request.POST, instance=content['item'])
        if form.is_valid():
            form.save()
            return redirect('subitem_view', root_id=content['item'].parrent_id.pk, id=content['item'].pk)
    else:
        form = SubitemEditForm(instance=content['item'])

    content['form'] = form
    return render(request, 'main/subitem_edit.html', content)


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
               'error_msg': "",
               'success_msg': "",}

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
