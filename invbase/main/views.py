from django.shortcuts import render
from .service import users_fio_lst, index_item_list


# Page with item list
def index(request):
    point_man = None
    find_lst = {}
    if request.method == 'GET':
        point_man = request.GET.get('pm', None)

    if request.method == 'POST':
        print(f"{request.POST.get('fm')}")
        find_lst['mode'] = request.POST.get('fm', None)
        find_lst['arg'] = request.POST.get('fa', None)

    temp = index_item_list(point_man, find_lst)
    content = {'users_list': users_fio_lst(),
               'item_list': temp}
    return render(request, 'main/index.html', content)