from django.contrib.auth.models import User
from django import forms
from django.forms import HiddenInput

from saver_app.models import Data


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        if 'user' in kwargs.keys():
            user = kwargs.pop('user')
            self.user = user

        else:
            self.user = None

        if 'obj_id' in kwargs.keys():
            self.object_id = kwargs.pop('obj_id')
        else:
            self.object_id = None

        initial = kwargs.get('initial', {})
        initial['owner'] = self.user.id
        kwargs['initial'] = initial

        super(BaseForm, self).__init__(*args, **kwargs)


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('email', 'password')


class DataForm(BaseForm):
    def __init__(self, *args, **kwargs):

        super(DataForm, self).__init__(*args, **kwargs)
        self.fields['owner'].initial = User.objects.all().first()
        self.fields['owner'].widget = HiddenInput()

    class Meta:
        model = Data
        exclude = []
