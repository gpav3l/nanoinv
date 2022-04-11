from django.shortcuts import render
from .service import users_fio_lst, index_item_list


# Page with item list
def index(request):
    point_man = None
    if request.method == 'GET':
        point_man = request.GET.get('pm', None)
        find_mode = request.GET.get('fm', None)
        find_arg = request.GET.get('fa', None)

    temp = index_item_list(point_man)
    content = {'users_list': users_fio_lst(),
               'item_list': temp}
    return render(request, 'main/index.html', content)