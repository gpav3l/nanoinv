from django.shortcuts import render
from .service import users_fio_lst, index_item_list


# Page with item list
def index(request):
    temp = index_item_list()
    content = {'users_list': users_fio_lst(),
               'item_list': temp}
    return render(request, 'main/index.html', content)