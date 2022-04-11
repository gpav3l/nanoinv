from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.db import IntegrityError
from simple_auth.service import check_auth, check_auth_inline
from .models import *
from .service import *
from django.core.exceptions import ObjectDoesNotExist
from .forms import *


# Create new item
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
    return render(request, 'main/card_edit_item.html', content)



# Item card page
def item_view(request, id):
    content = {}
    try:
        content['item'] = Items.objects.get(pk=id)
        content['subitem_list'] = subitem_list(id)
        content['image_list'] = Item_images.objects.filter(parent=id) #item_images(id)
    except:
        raise Http404("Item not found")

    if check_auth_inline(request):
        if request.method == 'GET':
            if request.GET.get('rm', '') == str(id):
                content['item'].delete()
                return redirect('index')
        if len(request.FILES) != 0:
            img = Item_images(parent_id=id)
            imgform = ItemImageUploadForm(request.POST, request.FILES, instance=img)
            imgform.save()
        if request.method == 'POST':
            form = ItemEditForm(request.POST, instance=content['item'])
            if form.is_valid():
                form.save()
                # Check inventory_number is same of root item and it subitems
                suditem_list = Include_items.objects.filter(parrent_id=id)
                for it in suditem_list:
                    if it.inventory_number != content['item'].inventory_number:
                        it.inventory_number = content['item'].inventory_number
                        it.save()
                return redirect('item_view', id)

        content['item'] = Items.objects.get(pk=id)
        content['form'] = ItemEditForm(instance=content['item'])
        content['imgupform'] = ItemImageUploadForm()
        return render(request, 'main/card_edit_item.html', content)
    else:
        return render(request, 'main/card_view_item.html', content)
