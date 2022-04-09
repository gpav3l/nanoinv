from django import forms


class LoginForms(forms.Form):
    password = forms.CharField(max_length=255, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForms, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"
            visible.field.widget.attrs['placeholder'] = visible.label
