from django import forms
from django.forms import ModelChoiceField
from .models import *
from .service import *
from datetime import datetime


def user_select_choices():
    ret_list = [("", "")]
    for itm in Users.objects.all():
        ret_list.append(tuple([itm.fio, itm.fio]))
    return tuple(ret_list)


def location_select_choices():
    ret_list = [("", "")]
    for itm in Locations.objects.all():
        ret_list.append(tuple([itm.name, itm.name]))
    return tuple(ret_list)


class DateInput(forms.DateInput):
    input_type = 'date'


class ItemEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemEditForm, self).__init__(*args, **kwargs)
        self.fields['date_start_use'].required = False
        self.fields['date_end_use'].required = False

    class Meta:
        _year = datetime.now().year
        _year_delta = 25
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


