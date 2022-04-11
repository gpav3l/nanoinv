from django import forms
from django.forms import ModelChoiceField
from .models import *
from .service import *
from datetime import datetime


# Prepare Tuple from user model
def user_select_choices():
    ret_list = [("", "")]
    for itm in Users.objects.all():
        ret_list.append(tuple([itm.fio, itm.fio]))
    return tuple(ret_list)


# Prepare Tuple from location model
def location_select_choices():
    ret_list = [("", "")]
    for itm in Locations.objects.all():
        ret_list.append(tuple([itm.name, itm.name]))
    return tuple(ret_list)


# Set celandar view to DateInput widget
class DateInput(forms.DateInput):
    input_type = 'date'


# Form for edit item
class ItemEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemEditForm, self).__init__(*args, **kwargs)
        self.fields['date_start_use'].required = False
        self.fields['date_end_use'].required = False

    class Meta:
        model = Items
        fields = ['inventory_number', 'name', 'serial_number', 'amount', 'point_man', 'location', 'comments', 'date_start_use', 'date_end_use']
        widgets = {
            'inventory_number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'point_man': forms.Select(attrs={'class': 'form-select'}, choices=user_select_choices()),
            'location': forms.Select(attrs={'class': 'form-select'}, choices=location_select_choices()),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_start_use': DateInput(attrs={'class': 'form-control'}),
            'date_end_use': DateInput(attrs={'class': 'form-control'}),
        }


# Form for edit subitems
class SubitemEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubitemEditForm, self).__init__(*args, **kwargs)
        self.fields['date_start_use'].required = False
        self.fields['date_end_use'].required = False

    class Meta:
        model = Include_items
        fields = ['name', 'serial_number', 'amount', 'location', 'comments', 'date_start_use', 'date_end_use']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-select'}, choices=location_select_choices()),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_start_use': DateInput(attrs={'class': 'form-control'}),
            'date_end_use': DateInput(attrs={'class': 'form-control'}),
        }


# Form for item image upload
class ItemImageUploadForm(forms.ModelForm):
    class Meta:
        model = Item_images
        fields = ['image']


# Form for subitem image upload
class SubitemImageUploadForm(forms.ModelForm):
    class Meta:
        model = Include_item_images
        fields = ['image']
