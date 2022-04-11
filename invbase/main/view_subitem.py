from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.db import IntegrityError
from simple_auth.service import check_auth, check_auth_inline
from .models import *
from .service import *
from django.core.exceptions import ObjectDoesNotExist
from .forms import *


# Page for create new subitem
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
    return render(request, 'main/card_edit_subitem.html', content)



# Subitem card page
def subitem_view(request, root_id, id):
    content = {}
    try:
       content['item'] = Include_items.objects.get(pk=id)
       content['image_list'] = Include_item_images.objects.filter(parent=id)
    except:
        raise Http404("Item not found")

    if check_auth_inline(request):
        # Check for request to remove item
        if request.method == 'GET':
            if request.GET.get('rm', '') == str(id):
                Include_items.objects.filter(pk=id).delete()
                return redirect('item_view', id=root_id)
            if int(request.GET.get('irm', '-1')) > 0:
                Include_item_images.objects.filter(pk=int(request.GET.get('irm', '-1')), parent=id).delete()
                return redirect('subitem_view', root_id, id)
        # Check for request to update item
        if len(request.FILES) != 0:
            img = Include_item_images(parent_id=id)
            imgform = SubitemImageUploadForm(request.POST, request.FILES, instance=img)
            imgform.save()
        if request.method == 'POST':
            form = SubitemEditForm(request.POST, instance=content['item'])
            if form.is_valid():
                form.save()

        content['item'] = Include_items.objects.get(pk=id)
        content['form'] = SubitemEditForm(instance=content['item'])
        content['imgupform'] = SubitemImageUploadForm()
        return render(request, 'main/card_edit_subitem.html', content)
    else:
        return render(request, 'main/card_view_subitem.html', content)



