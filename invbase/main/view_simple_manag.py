from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.db import IntegrityError
from simple_auth.service import check_auth, check_auth_inline
from .models import *
from .service import *
from django.core.exceptions import ObjectDoesNotExist
from .forms import *

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